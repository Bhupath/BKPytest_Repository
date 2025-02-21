import logging.handlers
import os
import sys
import time
import logging
import input

def createLogger()->logging.Logger:
    if not os.path.exists(input.sanity_logs):
        os.makedirs(input.sanity_logs)
    logfile=(input.sanity_logs + '/SanityExecution.log')
    print(logfile)
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers = []
    formatter=logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s][%(filename)s][%(funcName)s:%(lineno)d]: %(message)s')
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    #logger.propagate = False
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    return logger
