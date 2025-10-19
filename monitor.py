from datetime import datetime, timedelta
import signal
import subprocess
from time import sleep
import os, sys
# from api.src.utils.functions.sendmail import sendmail
from api.src.utils.logs.index import log
from pathlib import Path
from api.src.utils.functions.payload_n8n import moni_active, moni_stop
from api.src.utils.functions.screenshot import capture_screenshot

HEARTBEAT_FILE = "C:/Users/api/src/utils/functions/heartbeat.txt"
INTERVALO = 5 # minutos #esse tempo e pra test
INTERVALO_LOOP = 240 #esse tempo e pra test
SCREEN_ALERTAS_CONSECUTIVOS = 5
MAX_ALERTAS_CONSECUTIVOS = 10

def check_heartbeat():
    sleep(30)  # espera 30 segundos para garantir que o arquivo foi atualizado
    if not os.path.exists(HEARTBEAT_FILE):
        log.warning("⚠️ Arquivo de heartbeat não encontrado.")
        return False

    try:
        with open(HEARTBEAT_FILE, "r") as f:
            ultima_execucao = datetime.fromisoformat(f.read().strip())
    except Exception as e:
        log.error(f"❌ Erro ao ler o heartbeat: {e}")
        return False

    tempo_passado = datetime.now() - ultima_execucao
    if tempo_passado > timedelta(minutes=INTERVALO):
        return False
    return True

if __name__ == "__main__":
    alertas_consecutivos = 0
    log.info("🟡 Iniciando monitoramento do heartbeat...")
    
    BASE_DIR = Path(__file__).resolve().parent

    automacao_proc = subprocess.Popen(
        [sys.executable, str(BASE_DIR / "main.py")],  # usa o python da venv
        cwd=str(BASE_DIR),                            # garante que roda na pasta certa
        env=os.environ.copy()
    )

    try:
        while True:
            if not check_heartbeat():
                log.error("❌ Automação parada por mais de 5 minutos. Enviando alerta por e-mail...")
                # sendmail("Automação parada há mais de 5 minutos Robô_Jerffeson")
                moni_stop()
                
                alertas_consecutivos += 1
                
                if alertas_consecutivos >= MAX_ALERTAS_CONSECUTIVOS:
                    log.critical("🛑 Número máximo de alertas consecutivos atingido. Encerrando monitoramento.")
                    automacao_proc.send_signal(signal.SIGINT)
                    break

                elif alertas_consecutivos >= SCREEN_ALERTAS_CONSECUTIVOS:
                    capture_screenshot(prefix="alert_heartbeat")
                    log.info("📸 Screenshot capturada devido a alertas consecutivos.")
            
            else:
                alertas_consecutivos = 0
                log.info("✅ Automação rodando normalmente.")
                moni_active()
                
                
            sleep(INTERVALO_LOOP)
    except KeyboardInterrupt:
        log.info("🛑 Monitoramento interrompido manualmente.")     
        automacao_proc.terminate()