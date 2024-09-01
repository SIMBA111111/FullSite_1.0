import logging
import os


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
log_file_path = os.path.join(parent_dir, "log.txt")

logging.basicConfig(level=logging.INFO,
                    filename=log_file_path,
                    format="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
                    )
logging.shutdown()
logger = logging.getLogger(__name__)