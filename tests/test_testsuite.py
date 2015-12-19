
import nose

import testvibe


class BasicTestSuite(testvibe.Testsuite):  pass


class TestSetupTeardown(object):

    t = None

    def setUp(self):
        self.t = BasicTestSuite()

    def tearDown(self):
        self.t = None

    def test_class_type(self):
        assert isinstance(self.t, testvibe.Testsuite)

    def test_run_test(self):
        m = lambda:  9
        x = self.t.test(m)
        assert x == 9
