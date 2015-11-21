
import time

import requests


class APIController(object):

	log = None
	root_domain = None

	def __init__(self, log_handler):
		self.log = log_handler

	def set_root_domain(self, root_domain):
		self.root_domain = root_domain

	def get(self, url):
		full_url = '%s/%s' % (self.root_domain, url)
		self.log.debug('fetching <%s>...' % full_url)
		start_time = time.time()
		r = requests.get(full_url)
		end_time = time.time()
		time_diff = end_time - start_time
		self.log.debug('fetched %db in %fs' % (len(r.text), time_diff))
		return r.json(), r