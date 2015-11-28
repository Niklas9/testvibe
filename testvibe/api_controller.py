
import time

import requests


class APIController(object):

    # TODO(niklas9):
    # * how to do negative tests on http method calls?
    #   new arg saying if test is negative or not..?
    # * add headers
    # * how to unit test this? see if requests has some test flag where actual
    #   request is not initiated ?

    log = None
    root_domain = None
    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'
    HTTP_METHOD_PUT = 'PUT'
    HTTP_METHOD_DELETE = 'DELETE'
    HTTP_METHOD_PATCH = 'PATCH'  # http://tools.ietf.org/html/rfc5789

    def __init__(self, log_handler):
        self.log = log_handler

    def set_root_domain(self, root_domain):
        self.root_domain = root_domain

    def get(self, url):
        return self._exec_http_method(self.HTTP_METHOD_GET, requests.get, url)

    def post(self, url, data):
        return self._exec_http_method(self.HTTP_METHOD_POST, requests.post,
                                      url, data=data)

    def put(self, url, data):
        return self._exec_http_method(self.HTTP_METHOD_PUT, requests.put, url,
                                      data=data)

    def delete(self, url):
        return self._exec_http_method(self.HTTP_METHOD_DELETE, requests.delete,
                                      url, data=data)

    def patch(self, url, data):
        return self._exec_http_method(self.HTTP_METHOD_PATCH, requests.patch,
                                      url, data=data)

    def _exec_http_method(self, method, req_m, url, data=None):
        full_url = '%s/%s' % (self.root_domain, url)
        self.log.debug('executing HTTP %s <%s>...' % (method, full_url))
        start_time = time.time()
        r = req_m(full_url, data=data)
        end_time = time.time()
        time_diff = end_time - start_time
        self.log.debug('response code %d, fetched %db in %fs'
                       % (r.status_code, len(r.text), time_diff))
        if method == self.HTTP_METHOD_DELETE:
            return None, r  # dont expect any response body when DELETE is used
        return r.json(), r