#/usr/bin/python
import os
from datetime import datetime
import logging

def createLogger():
  logger = logging.getLogger(__name__)
  log_file_path = f"output_{datetime.strftime(datetime.now(),'%H_%M_%S')}.log"
  formatter = logging.Formatter("[%(asctime)s][%(name)s][]")
