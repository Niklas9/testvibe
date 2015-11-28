
import traceback

import testvibe.api_controller as api_controller
import testvibe.asserts as asserts
import testvibe.logger as logger


class Testsuite(asserts.Asserts):

    # TODO(niklas9):
    # * make 
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
        asserts.Asserts.__init__(self)
        self.log = logger.Log()
        self.api = api_controller.APIController(self.log)

    def run(self):
        raise NotImplementedError()

    def test(self, test_id, test_method, *args, **kwargs):
        # TODO(niklas9):
        # * timers etc here, to measure, for timeout etc
        self.setup()
        test_id_method = '%s (%s)' % (test_method.__name__, test_id)
        self.log.info('executing %s...' % test_id_method)
        try:
            test_method(*args, **kwargs)
        # TODO(niklas9):
        # * should catch more specific exceptions here in the future
        #except asserts.AssertionException as e:
        except Exception as e:
            self.log.error(e)
            self.log.debug(traceback.format_exc())
        finally:
            success_counter, total_counter = self.get_assert_counters()
            if success_counter == total_counter:
                self.log.debug('%d/%d asserts successful in %s'
                               % (success_counter, total_counter,
                                  test_id_method))
            else:
                self.log.warn('%d/%d asserts FAILED in %s'
                              % ((total_counter-success_counter),
                                  total_counter, test_id_method))
            self.teardown()
            self.reset_assert_counter()

    def setup(self):
        pass  # to be overriden by subclass

    def teardown(self):
        pass  # to be overriden by subclass
