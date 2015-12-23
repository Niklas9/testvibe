
import time

import requests

import testvibe.core.utils as utils


class APIResponseNotAsExpected(Exception):  pass
class APIResponseCodeNotSuccessException(Exception):  pass

class APIController(object):

    # TODO(niklas9):
    # * how to unit test this? see if requests has some test flag where actual
    #   request is not initiated ?

    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'
    HTTP_METHOD_PUT = 'PUT'
    HTTP_METHOD_DELETE = 'DELETE'
    HTTP_METHOD_PATCH = 'PATCH'  # http://tools.ietf.org/html/rfc5789
    HTTP_CODE_INFORMATION_RANGE = range(100, 199)
    HTTP_CODE_SUCCESSFUL_RANGE = range(200, 299)
    HTTP_CODE_REDIRECTION_RANGE = range(300, 399)
    HTTP_CODE_CLIENT_ERROR_RANGE = range(400, 499)
    HTTP_CODE_SERVER_ERROR_RANGE = range(500, 599)
    HEADER_USER_AGENT_KEY = 'User-Agent'
    # TODO(niklas9):
    # * figure out how to get testvibe version number here from __init_,
    #   can't import it because of circular imports (testvibe.__init__ imports
    #   testsuite which imports this class, api_controller)
    HEADER_USER_AGENT_DEFAULT_VALUE = 'testvibe/0.0.1'

    log = None
    root_domain = None

    def __init__(self, log_handler):
        self.log = log_handler

    def set_root_domain(self, root_domain):
        self.root_domain = root_domain

    def get(self, url, expected=None, headers=None):
        return self._exec_http_method(self.HTTP_METHOD_GET, requests.get, url,
                                      expected, headers=headers)

    def post(self, url, data, expected=None, headers=None):
        return self._exec_http_method(self.HTTP_METHOD_POST, requests.post,
                                      url, expected, data=data,
                                      headers=headers)

    def put(self, url, data, expected=None, headers=None):
        return self._exec_http_method(self.HTTP_METHOD_PUT, requests.put, url,
                                      expected, data=data, headers=headers)

    def delete(self, url, expected=None, headers=None):
        return self._exec_http_method(self.HTTP_METHOD_DELETE, requests.delete,
                                      url, expected, data=data,
                                      headers=headers)

    def patch(self, url, data, expected=None, headers=None):
        return self._exec_http_method(self.HTTP_METHOD_PATCH, requests.patch,
                                      url, expected, data=data,
                                      headers=headers)

    def _exec_http_method(self, method, req_m, url, expected, data=None,
                          headers=None):
        # TODO(niklas9):
        # * do sanity checks here that url is valid, headers is a dict,
        #   expect is an integer between 100-599 etc
        full_url = self._construct_full_url(url)
        headers = self._construct_headers(headers)
        self.log.debug('executing HTTP %s <%s>...' % (method, full_url))
        r = self._do_http_req(req_m, full_url, data, headers)
        if method == self.HTTP_METHOD_DELETE:
            return None, r  # dont expect any response body when DELETE is used
        # TODO(niklas9):
        # * if request fails.. provide in logs exact curl cmd to reproduce
        if expected is not None and not expected == r.status_code:
            msg = ('response code was %d, expected %d'
                   % (r.status_code, expected))
            raise APIResponseNotAsExpected(msg)
        elif (expected is None and
              r.status_code not in self.HTTP_CODE_SUCCESSFUL_RANGE):
            msg = 'response code was %d, expected 2xx' % r.status_code
            raise APIResponseCodeNotSuccessException(msg)
        try:
            json = r.json()
        except ValueError as e:
            json = None
            self.log.warn('problem serializing JSON document - %s' % e)
        finally:
            return json, r

    def _do_http_req(self, req_m, full_url, data, headers):
        start_time = time.time()
        r = req_m(full_url, data=data, headers=headers)
        end_time = time.time()
        time_diff = end_time - start_time
        self.log.debug('response code %d, fetched %db in %fs'
                       % (r.status_code, len(r.text), time_diff))
        return r

    def _construct_full_url(self, url):
        if self.root_domain is not None:
            if not url.startswith(utils.STRING_SLASH):
                url = utils.STRING_SLASH + url
            return self.root_domain + url
        return url

    def _construct_headers(self, headers):
        # TODO(niklas9):
        # * add perhaps authentication middleware here..
        # * make sure we don't override already set User-Agent header here
        if headers is None:  headers = dict()
        headers.update({self.HEADER_USER_AGENT_KEY:
                        self.HEADER_USER_AGENT_DEFAULT_VALUE})
        return headers