
import testvibe.core.utils as utils


class TestUtils(object):

    def test_is_int(self):
        m = utils.is_int
        assert m(9)
        assert not m('asdf')
        assert not m(None)
