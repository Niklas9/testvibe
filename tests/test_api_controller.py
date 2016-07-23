
import testvibe.api_controller as api_controller 
import testvibe.logger as logger


class TestAPIController(object):

    log = None

    def __init__(self):
        # TODO(niklas9):
        # * use fake logger here instead, no real need to send unit test outputs
        #   to stdout
        self.log = logger.Log()

    def test_construct_full_url(self):
        api_c = api_controller.APIController(None)
        m = api_c._construct_full_url
        assert m('/asdf') == '/asdf'
        api_c.set_root_domain('http://testvibe.org/')
        assert m('/asdf') == 'http://testvibe.org/asdf'
        assert m('asdf') == 'http://testvibe.org/asdf'

    def test_construct_headers(self):
        api_c = api_controller.APIController(None)
        m = api_c._construct_headers
        assert isinstance(m(None), dict)
        assert len(m(None).keys()) == 1
        assert api_c.HEADER_USER_AGENT_KEY in m(None)
        assert len(m({'asdf': 'fdsa'}).keys()) == 2
        r = m({'asdf': 'fdsa'})
        assert 'asdf' in r and r['asdf'] == 'fdsa'

    def test_do_http_req(self):
        api_c = api_controller.APIController(self.log)
        r = api_c._do_http_req(self._fake_req_m, 'asdf', None, None)
        assert r.status_code == 200

    @staticmethod
    def _fake_req_m(full_url, data=None, headers=None):
        return TestAPIController.FakeResponse()

    class FakeResponse(object):

        status_code = 200
        text = 'asdf'
