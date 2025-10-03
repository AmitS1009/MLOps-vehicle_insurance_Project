# # below code is to check the logging config


# from src.logger import logging

# logging.debug('This is a debug msg')
# logging.info('This is an info msg')
# logging.warning('This is a warning msg')
# logging.error('This is an error msg')
# logging.critical('This is a critical msg')





# -------------------------------------------------------

#below code is to check the exception config 

from src.logger import logging
from src.exception import MyException
import sys

try:
    a = 1+'z'
except Exception as e:
    logging.info(e)
    raise MyException(e, sys) from e