
import testvibe.core.utils as utils


class TestUtils(object):

    def test_get_path(self):
        m = utils.get_path
        assert m(['1', '2', '3']) == '1/2/3'
        assert m(('tmp', 'test/vibe', 'logs')) == 'tmp/test/vibe/logs'
        assert m(['/tmp', 'testsuite.py']) == '/tmp/testsuite.py'