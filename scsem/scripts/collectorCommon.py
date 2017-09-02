import logging
import sys
import os

LOGFILE_DEV="/tmp/scsem.log"
LOGFILE_EXCEPTION="/tmp/scseme.log"
EMEM_DEPLOY_DIR="/home/pi/emem"

# Logging
internalLogger = logging.getLogger('simple_logger')
hdlr_1 = logging.FileHandler(LOGFILE_DEV)
formatter_1 = logging.Formatter('%(asctime)s %(levelname)-8s %(threadName)-10s %(funcName)12s() %(message)s')
hdlr_1.setFormatter(formatter_1)
internalLogger.addHandler(hdlr_1)
internalLogger.setLevel(logging.DEBUG)

# Logging with exceptions 
einternalLogger = logging.getLogger('exception_logger')
hdlr_1 = logging.FileHandler(LOGFILE_EXCEPTION)
formatter_1 = logging.Formatter('%(asctime)s %(levelname)-8s %(threadName)-10s %(funcName)12s() %(message)s')
hdlr_1.setFormatter(formatter_1)
einternalLogger.addHandler(hdlr_1)
einternalLogger.setLevel(logging.DEBUG)

def amIaPi():
  rt=False
  if "arm" in os.uname()[4]:
    rt=True
  return rt

