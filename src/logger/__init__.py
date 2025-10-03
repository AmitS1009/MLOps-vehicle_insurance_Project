import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime


#constraint for log configuration :
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024 #5mb
BACKUP_COUNT = 3   # number of backup log file to keep


# Construct log file path
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)



def configure_logger():

    """ configures logging with rotating  file handler and console handler"""

    # create custon logger 
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #define formatter 
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    #file handler with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    #console handler 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    #Add handler to logger 
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


#configure the logger 
configure_logger()
