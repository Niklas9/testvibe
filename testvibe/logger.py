
import datetime
import os
try:
    import queue
except ImportError:
    import Queue as queue  # fallback for Python 2.x
import sys
import threading


class InvalidLogLevelException(Exception):  pass

class Log(object):

    TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%S.%f'
    LOG_FMT = '%s|%s|%s|%s\n'  # timestamp, pid, debug level, msg
    LEVEL_INFO = 'INFO'
    LEVEL_DEBUG = 'DEBUG'
    LEVEL_WARNING = 'WARN'
    LEVEL_ERROR = 'ERROR'
    LOG_LEVEL_PROD = 1
    LOG_LEVEL_DEBUG = 2

    log_level = None
    queue = None
    _instance = None  # singleton instance

    def __init__(self, log_level=None):
        if log_level is None:
            log_level = self.LOG_LEVEL_DEBUG  # default to debug
        if log_level not in (self.LOG_LEVEL_PROD, self.LOG_LEVEL_DEBUG):
            raise InvalidLogLevelException(log_level)
        self.log_level = log_level
        self.queue = queue.Queue()  # FIFO
        t = threading.Thread(target=self._log_worker)
        t.daemon = True  # TODO(niklas9): might exit before queue is emptied
        t.start()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def info(self, msg):
        self._log(self.LEVEL_INFO, msg)

    def debug(self, msg):
        if self.log_level == self.LOG_LEVEL_DEBUG:
            self._log(self.LEVEL_DEBUG, msg)

    def warn(self, msg):
        self._log(self.LEVEL_WARNING, msg)

    def warning(self, msg):  self.warn(msg)

    def error(self, msg):
        self._log(self.LEVEL_ERROR, msg)

    def _log(self, log_level, msg):
        self.queue.put((log_level, msg))

    def _log_worker(self):
        while True:
            try:
                log_level, msg = self.queue.get(block=True)
            except queue.Empty:
                continue
            else:
                ts = datetime.datetime.utcnow().strftime(self.TIMESTAMP_FMT)
                msg = self.LOG_FMT % (ts, os.getpid(), log_level, msg)
                sys.stdout.write(msg)
                self.queue.task_done()