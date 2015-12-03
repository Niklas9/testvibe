

import testvibe.core.cli_handler as cli_handler


class TestTVCtl(object):

    def test_valid_dir_name(self):
        m = cli_handler.CLIHandler._is_valid_name
        assert m('asdf')
        assert m('asdf324')
        assert m('asdf_fdsa')

    def test_neg_valid_dir_name(self):
        m = cli_handler.CLIHandler._is_valid_name
        assert not m('asdf$')
        assert not m('fdsa asdf')
        assert not m('as-df')
