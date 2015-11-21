
import requests


class APIController(object):

	root_domain = None

	def set_root_domain(self, root_domain):
		self.root_domain = root_domain

	def get(self, url):
		r = requests.get('%s/%s' % (self.root_domain, url))
		return r.json(), r