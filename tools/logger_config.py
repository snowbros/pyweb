import logging
from config import config_options

levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

log_level = levels.get(config_options.log_level, logging.DEBUG)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def coloredType(logType):
    if logType == 'INFO' or logType == 'LOG' or logType == 'TIP':
        return bcolors.OKGREEN + bcolors.BOLD + "<<" + logType + ">>" + bcolors.ENDC
    if logType == 'ERROR':
        return bcolors.FAIL + bcolors.BOLD + "<<" + logType + ">>" + bcolors.ENDC
    if logType == 'WARNING':
        return bcolors.WARNING + bcolors.BOLD + "<<" + logType + ">>" + bcolors.ENDC
    if logType == 'DEBUG':
        return bcolors.HEADER + bcolors.BOLD + "<<" + logType + ">>" + bcolors.ENDC
    return bcolors.OKGREEN + bcolors.BOLD + "<<" + logType + ">>" + bcolors.ENDC

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)


class LogFormatter(logging.Formatter):

    def format(self, record):
        self._fmt = "%(asctime)s "+coloredType(record.levelname)+' %(filename)s (%(lineno)d) %(message)s'
        return logging.Formatter.format(self, record)

# create console handler and set level to debug
hdlr = logging.StreamHandler()
hdlr.setLevel(log_level)
formatter_obj = LogFormatter(datefmt="%Y-%m-%d %H:%m:%S")

logging.root.addHandler(hdlr)
logging.root.setLevel(log_level)

# add formatter to handler
hdlr.setFormatter(formatter_obj)

# add handler to logger
logger.addHandler(hdlr)
