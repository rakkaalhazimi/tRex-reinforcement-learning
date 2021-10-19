import os
import logging
from datetime import datetime

base_dir = "logs"
base_log = "logs/training.log"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

logging.basicConfig(filename=base_log,
                    filemode="w",
                    format="[%(levelname)s] %(asctime)s: %(message)s",
                    level=logging.INFO)


def log_info(message: str):
    logging.info(message)

def finish_log():
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d %H-%M-%S") + ".log"
    filepath = os.path.join(base_dir, filename)

    with open(filepath, "w") as f:
        
        with open(base_log) as b:
            f.write(b.read())

    