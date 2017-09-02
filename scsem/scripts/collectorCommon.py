import logging
import sys


LOGFILE_DEV="/tmp/emem.log"
LOGFILE_EXCEPTION="/tmp/ememe.log"

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


