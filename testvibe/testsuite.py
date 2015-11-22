
import traceback

import testvibe.api_controller as api_controller
import testvibe.asserts as asserts
import testvibe.logger as logger


class Testsuite(asserts.Asserts):

    # TODO(niklas9):
    # * make 
    # * add logging..
    # * add wrappers for performance tests, time limits how long a test is
    #   running before it fails.. add decorator options for this?
    # * add assertions
    # * add result metrics.. report continuously or in the end? should be an
    #   arg flag perhaps..
    # * return bad unix exit code when any of the testcases in the
    #   testsuite fails
    results = None
    log = None
    api = None

    def __init__(self):
        self.results = []
        asserts.Asserts.__init__(self) #, self.results)
        self.log = logger.Log()
        self.api = api_controller.APIController(self.log)

    def run(self):
        raise NotImplementedError()

    def test(self, test_id, test_method, *args, **kwargs):
        # TODO(niklas9):
        # * timers etc here, to measure, for timeout etc
        self.setup()
        self.log.info('exectuing %s, %s...' % (test_id, test_method.func_name))
        try:
            test_method(*args, **kwargs)
        except asserts.AssertionException as e:
            self.log.error(e)
            self.log.debug(traceback.format_exc())
        else:
            self.teardown()

    def setup(self):
        # NOTE(niklas9):  to be overriden by inherting class
        pass

    def teardown(self):
        # NOTE(niklas9):  to be overriden by inherting class
        pass