
import atexit
import datetime
import os
try:
    import queue
except ImportError:
    import Queue as queue  # fallback for Python 2.x
import sys
import threading
import time


LOG_LEVEL_PROD = 1
LOG_LEVEL_DEBUG = 2

# TODO(niklas9):
# * add to docs that Log() is a singleton class
# * make logging format customizable
# * add option to make it blocking ?


class InvalidLogLevelException(Exception):  pass

class Log(object):

    TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%S.%f'
    LOG_FMT = '%s|%s|%s|%s\n'  # timestamp, pid, debug level, msg
    LEVEL_INFO = 'INFO'
    LEVEL_DEBUG = 'DEBUG'
    LEVEL_WARNING = 'WARN'
    LEVEL_ERROR = 'ERROR'
    LOG_FLUSH_TIMEOUT_CHECK = 0.1  # seconds
    LOG_FLUSH_TIMEOUT_WARN = 0.5  # seconds
    LOG_FLUSH_TIMEOUT = 5  # seconds

    log_level = None
    queue = None
    _instance = None  # placeholder for singleton instance

    def __init__(self, log_level=None):
        if log_level is None:
            log_level = LOG_LEVEL_DEBUG  # default to debug
        if log_level not in (LOG_LEVEL_PROD, LOG_LEVEL_DEBUG):
            raise InvalidLogLevelException(log_level)
        self.log_level = log_level
        self.queue = queue.Queue()  # FIFO
        t = threading.Thread(target=self._log_worker)
        t.daemon = True
        # NOTE(niklas9):  * make sure log queue is emptied before exit
        atexit.register(self._wait_until_queue_is_empty)
        t.start()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def info(self, msg):
        self._log(self.LEVEL_INFO, msg)

    def debug(self, msg):
        if self.log_level == LOG_LEVEL_DEBUG:
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
            finally:
                # TODO(niklas9):
                # * move time to _log ? then we get the right time of the
                #   actual log entry happening.. not when the worker
                #   thread picks it up..
                ts = datetime.datetime.utcnow().strftime(self.TIMESTAMP_FMT)
                msg = self.LOG_FMT % (ts, os.getpid(), log_level, msg)
                sys.stdout.write(msg)
                # TODO(niklas9):
                # * figure out why task_done() is called too many times at
                #   certain test runs.. and raises ValueError
                try:
                    self.queue.task_done()
                except ValueError:
                    pass

    def _wait_until_queue_is_empty(self):
        # TODO(niklas9):
        # * best practice to exit with some error code 1 if timeout exceeded ?
        total_time_waited = 0
        while not self.queue.empty():
            total_time_waited += self.LOG_FLUSH_TIMEOUT_CHECK
            if total_time_waited == self.LOG_FLUSH_TIMEOUT_WARN:
                sys.stdout.write('log queue size is still %d, waiting %d more '
                                 'secs for log queue to be flushed..\n'
                                 % (self.queue.qsize(), self.LOG_FLUSH_TIMEOUT))
            time.sleep(self.LOG_FLUSH_TIMEOUT_CHECK)
            if total_time_waited >= self.LOG_FLUSH_TIMEOUT:
                sys.stderr.write('log timeout reached (%ds), exiting even though '
                                 'there are still %d log entries left to be '
                                 'synced\n' % (self.LOG_FLUSH_TIMEOUT,
                                 self.queue.qsize()))
                break
