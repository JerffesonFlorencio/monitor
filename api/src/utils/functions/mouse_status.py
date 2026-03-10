import time
import pyautogui

tempo_limite = 30
ultima_posicao = pyautogui.position()
ultimo_movimento = time.time()
status = "ATIVO"

while True:
    posicao_atual = pyautogui.position()

    if posicao_atual != ultima_posicao:
        ultima_posicao = posicao_atual
        ultimo_movimento = time.time()
        status = "ATIVO"

    tempo_parado = time.time() - ultimo_movimento

    if tempo_parado >= tempo_limite:
        status = "PARADO"

    print(f"\rStatus atual: {status} | Posição: {posicao_atual}", end="")

    time.sleep(0.5)
