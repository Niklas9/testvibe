
try:
    import queue
except ImportError:
    import Queue as queue  # fallback for Python 2.x
import time
import traceback

import testvibe.api_controller as api_controller
import testvibe.asserts as asserts
import testvibe.logger as logger

try:
    import settings
except ImportError:
    # NOTE(niklas9):
    # * this should only happen during testing, otherwise a global settings
    #   be importable for every project
    settings = None


class Testsuite(asserts.Asserts):

    # TODO(niklas9):
    # * add wrappers for performance tests, time limits how long a test is
    #   running before it fails.. add decorator options for this?
    RESERVED_NAMES = ('test', 'setup', 'teardown')
    RESULT_PASSED = 'PASSED'
    RESULT_FAILED = 'FAILED'
    RESULT_ERROR = 'ERROR'  # Python errors, setup errors (?)

    results = None
    log = None
    api = None

    def __init__(self):
        asserts.Asserts.__init__(self)
        log_level = logger.LOG_LEVEL_DEBUG
        if settings is not None and not settings.LOG_LEVEL_DEBUG:
            log_level = logger.LOG_LEVEL_PROD
        self.log = logger.Log(log_level=log_level)
        self.api = api_controller.APIController(self.log)
        self.results = queue.Queue()  # FIFO

    def test(self, test_method, *args, **kwargs):
        # NOTE(niklas9):
        # * this method needs to be thread safe! depending on the
        #   parallelization level set by the user, this might be
        #   executed in parallel by several threads
        # TODO(niklas9):
        # * add timers for setup, teardown and test separately..
        # * add timeout option
        # * how to handle test ids ?
        start_time = time.time()
        self.setup()
        self.log.info('running testcase %s...' % test_method.__name__)
        try:
            r = test_method(*args, **kwargs)
        # TODO(niklas9):
        # * should catch more specific exceptions here in the future
        #except asserts.AssertionException as e:
        except Exception as e:
            self.log.error(e)
            self.log.debug(traceback.format_exc())
        finally:
            success_counter, total_counter = self.get_assert_counters()
            if success_counter == total_counter:
                result = self.RESULT_PASSED
                self.log.debug('%d/%d asserts successful in %s'
                               % (success_counter, total_counter,
                                  test_method.__name__))
                self.log.info('testcase %s PASSED' % test_method.__name__)
            else:
                result = self.RESULT_FAILED
                self.log.warn('%d/%d asserts FAILED in %s'
                              % ((total_counter-success_counter),
                                  total_counter, test_method.__name__))
                self.log.error('testcase %s FAILED' % test_method.__name__)
            self.teardown()
            self.reset_assert_counter()
        time_elapsed = time.time() - start_time
        self.log.debug('time elapsed during test case: %.4fs' % time_elapsed)
        tcr = TestCaseResult(test_method.__name__, result, success_counter,
                             total_counter, time_elapsed)
        self.results.put(tcr)
        return r

    def setup(self):
        pass  # to be overriden by subclass

    def teardown(self):
        pass  # to be overriden by subclass


class TestCaseResult(object):

    def __init__(self, name, result, passed_asserts, total_asserts,
                 time_elapsed):
        self.name = name
        self.result = result
        self.passed_asserts = passed_asserts
        self.total_asserts = total_asserts
        self.time_elapsed = time_elapsed

    def __str__(self):
        return ('<name: %s, result: %s, asserts %d/%d, time elapsed: %.4fs>'
                % (self.name, self.result, self.passed_asserts,
                   self.total_asserts, self.time_elapsed))