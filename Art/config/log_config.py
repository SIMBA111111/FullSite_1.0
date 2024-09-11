import logging
import os
from logging.handlers import RotatingFileHandler

# current_dir = os.path.dirname(__file__)
# parent_dir = os.path.dirname(current_dir)
# info_log_file_path = os.path.join(parent_dir, "info_log.txt")
# error_log_file_path = os.path.join(parent_dir, "error_log.txt")

# logging.basicConfig(level=logging.INFO,
#                     filename=log_file_path,
#                     format="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
#                     )
# logging.shutdown()

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
