
import logging
from pathlib import Path

from config.settings import LOG_DIR


def get_logger():

    log_directory = Path(LOG_DIR)

    log_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = log_directory / "automation.log"

    logger = logging.getLogger("web_automation")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
