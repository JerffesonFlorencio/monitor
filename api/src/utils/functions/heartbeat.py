import os
from datetime import datetime
from api.src.utils.logs.index import log

def update_heartbeat():
    path = os.path.join(os.path.dirname(__file__), "heartbeat.txt")
    with open(path, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info(f"💓 Heartbeat atualizado em: {path}")