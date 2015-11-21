
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
    results = None
    log = None
    api = None

    def __init__(self):
        self.results = []
        asserts.Asserts.__init__(self) #, self.results)
        self.log = logger.Log()
        self.api = api_controller.APIController()

    def run(self):
        raise NotImplementedError()

    def test(self, test_id, test_method, *args, **kwargs):
        # TODO(niklas9):
        # * timers etc here, to measure, for timeout etc
        self.setup()
        try:
            test_method(*args, **kwargs)
        except asserts.AssertionException, e:
            print('assertion error')
        self.teardown()

    def setup(self):
        # TODO(niklas9):
        # * add logging here..
        pass

    def teardown(self):
        # TODO(niklas9):
        # * add logging
        pass