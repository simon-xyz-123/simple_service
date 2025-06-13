import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "server.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=False
    )
    handler.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # 可选：加个控制台输出，方便调试
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
