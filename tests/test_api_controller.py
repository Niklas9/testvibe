
import testvibe.api_controller as api_controller 


class TestAPIController(object):

    def test_construct_full_url(self):
        api_c = api_controller.APIController(None)
        m = api_c._construct_full_url
        assert m('/asdf') == '/asdf'
        api_c.set_root_domain('http://testvibe.org/')
        assert m('/asdf') == 'http://testvibe.org/asdf'

    def test_construct_headers(self):
        api_c = api_controller.APIController(None)
        m = api_c._construct_headers
        assert isinstance(m(None), dict)
        assert len(m(None).keys()) == 1
        assert api_c.HEADER_USER_AGENT_KEY in m(None)
        assert len(m({'asdf': 'fdsa'}).keys()) == 2
        r = m({'asdf': 'fdsa'})
        assert 'asdf' in r and r['asdf'] == 'fdsa'
