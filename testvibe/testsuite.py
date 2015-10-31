
import testvibe.logger as logger
import testvibe.asserts as asserts


class TestSuite(asserts.Asserts):

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

    def __init__(self):
        self.results = []
        asserts.Asserts.__init__(self) #, self.results)
        self.log = logger.Log()

    def setup(self):
        # TODO(niklas9):
        # * add logging here..
        pass

    def teardown(self):
        # TODO(niklas9):
        # * add logging
        pass

