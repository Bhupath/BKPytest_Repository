#/usr/bin/python
import os
from datetime import datetime
import logging

def createLogger():
  logger = logging.getLogger(__name__)
  log_file_path = f"output_{datetime.strftime(datetime.now(),'%H_%M_%S')}.log"
  formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s][%(filename)s][%(funcName)s:%(lineno)d]: %(message)s")
  fileHandler = loggin.FileHandler(log_file_path)
  fileHandler.setFormatter(formatter)
  logging.addHandler(fileHandler)
  logging.setLeve(logging.DEBUG)
  return logger
  
