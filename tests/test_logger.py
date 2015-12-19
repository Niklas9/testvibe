
import nose

import testvibe.logger as logger


class TestLogger(object):

    @nose.tools.raises(logger.InvalidLogLevelException)
    def test_invalid_log_level(self):
        logger.Log(log_level=3, re_init=True)

    def test_singleton_of_log_class(self):
        l1 = logger.Log()
        l2 = logger.Log()
        assert id(l1) == id(l2)