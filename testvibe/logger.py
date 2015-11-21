
import datetime
import os

# TODO(niklas9):
# * put each new log item in a queue, and have a separate thread working
#   on that queue.. so time is not spent I/O
# * how can I enforce this to be a singleton class in Python?

class Log(object):

    TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%S.%f'
    LOG_FMT = '%s|%s|%s|%s'  # timestamp, pid, debug level, msg
    LEVEL_INFO = 'INFO'
    LEVEL_DEBUG = 'DEBUG'
    LEVEL_WARNING = 'WARN'
    LEVEL_ERROR = 'ERROR'

    log_level = None

    def __init__(self, log_level=None):
        # TODO(niklas9):
        # * add at least 2 log levels here, one with debug and one without
        self.log_level = log_level

    def info(self, msg):
        self._log(self.LEVEL_INFO, msg)

    def debug(self, msg):
        # TODO(niklas9):
        # * take care of log level here
        self._log(self.LEVEL_DEBUG, msg)

    def warn(self, msg):
        self._log(self.LEVEL_WARNING, msg)

    def warning(self, msg):  self.warn(msg)

    def error(self, msg):
        self._log(self.LEVEL_ERROR, msg)

    def _log(self, level, msg):
        # TODO(niklas9):
        # * write to stdout?
        timestamp = datetime.datetime.utcnow().strftime(self.TIMESTAMP_FMT)
        print(self.LOG_FMT % (timestamp, os.getpid(), level, msg))