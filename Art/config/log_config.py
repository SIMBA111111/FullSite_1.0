import logging
import os
from logging.handlers import RotatingFileHandler


formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s"
)

info_logger = logging.getLogger(__name__)
error_logger = logging.getLogger(__name__)

error_logger.setLevel(logging.ERROR)
info_logger.setLevel(logging.INFO)

error_handler = RotatingFileHandler(
    'logs/error.log'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

info_handler = RotatingFileHandler(
    'logs/info.log'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)


error_logger.addHandler(error_handler)
info_logger.addHandler(info_handler)
