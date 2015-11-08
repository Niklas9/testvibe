
import nose

import testvibe.core.cli as cli


class TestTVCtl(object):

	def test_valid_dir_name(self):
		m = cli.CLI._is_valid_dir_name
		assert m('asdf')
		assert m('as-df')

	def test_neg_valid_dir_name(self):
		m = cli.CLI._is_valid_dir_name
		assert not m('asdf$')
		assert not m('fdsa asdf')