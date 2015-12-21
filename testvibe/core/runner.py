
import importlib
import os

import tqdm

import testvibe
import testvibe.core.cli_file_mgmt as cli_file_mgmt
import testvibe.core.utils as utils


class Runner(object):
    """ Test runner """

    RUNLIST_COMMENT_PREFIX = '#'

    log = None
    verbosity = None

    def __init__(self, log_handler, verbosity):
        self.log = log_handler
        self.verbosity = verbosity

    def execute(self, cwd):
        runlists = cli_file_mgmt.CLIFileMgmt.get_runlists(cwd)
        if len(runlists) == 0:
            sys.stderr.write('no runlists found...\n')
            sys.exit(1)
        for rl in runlists:
            if '/' in rl:
                tgroup = rl.split('/')[0]
                tsuites = self._parse_runlist(rl)
                self.log.info('starting test run on testgroup <%s>' % tgroup)
                self._run_tsuites(tgroup, tsuites)
            else:
                tgroup = os.getcwd().split('/')[-1]
                tsuites = self._parse_runlist(rl)
                self.log.info('starting test run on all testsuites in current dir')
                self._run_tsuites(tgroup, tsuites)

    def _run_tsuites(self, tgroup, tsuites):
        self.log.debug('found %d test suites' % len(tsuites))
        len_tsuites = len(tsuites)
        if self.verbosity:
            iterable = xrange(len_tsuites)
        else:
            iterable = tqdm.tqdm(range(len_tsuites), leave=True, desc=tgroup)
        for i in iterable:
            tsuite = tsuites[i]
            if '/' in tsuite:
                tsuite = tsuite.split('/')[-1]
            self.log.debug('initating run on testsuite <%s>' % tsuite)
            # TODO(niklas9):
            # * add exception handling for the importing below.. the user can
            #   enter lots of bad stuff in the runlists.. we should give them a
            #   hint
            ts = importlib.import_module('.%s' % tsuite[:-3],
                                         package=tgroup)
            tsuite_classes = self._get_all_tsuite_classes(ts)
            if len(tsuite_classes) == 0:
                # TODO(niklas9):
                # * this is actually too late.. should do some sanity check on
                #   all runlists before initiating a test run..
                #   like "validating runlists".. could be a separate cmd to
                #   tvctl as well
                sys.stderr.write('no subclasses of testvibe.Testsuite found\n')
                sys.exit(1)
            for tsuite_class in tsuite_classes:
                tcs = self._get_all_tcases(tsuite_class)
                tsuite_class_i = tsuite_class()
                for tc in tcs:
                    # TODO(niklas9):
                    # * execute each test case in a separate thread, easier to collect
                    #   results continuously
                    # * I don't get why class instance is second arg below.. should
                    #   replace 'self' so should be the first one?!!
                    tsuite_class_i.test(tc, tsuite_class_i)
                    # TODO(niklas9):
                    # * print results in smth like:
                    # >>> print tabulate.tabulate([['create_product', '5/5', '3.2s']], headers=['Test case', 'Asserts', 'Time'])
                    # Test case       Asserts    Time
                    # --------------  ---------  ------
                    # create_product  5/5        3.2s

    @staticmethod
    def _get_all_tcases(cl):
        tcases = set()
        reserved_names = testvibe.Testsuite.RESERVED_NAMES
        for o in dir(cl):
            if o.startswith('_'):  continue  # no private methods
            if o in reserved_names:  continue  # skip the reserved method names
            if o not in cl.__dict__:  continue  # don't consider inherited
            if not callable(getattr(cl, o)):  continue  # only methods
            tcases.add(getattr(cl, o))
        return tcases

    @staticmethod
    def _get_all_tsuite_classes(module):
        tsuites = set()
        for o in dir(module):
            co = getattr(module, o)  # co == call object
            if isinstance(co, type) and issubclass(co, testvibe.Testsuite):
                tsuites.add(co)
        return tsuites

    @staticmethod
    def _parse_runlist(path):
        tsuites = list()  # dups are fine, if one wants to rerun tsuites
        for line in utils.get_file_content(path).splitlines():
            if not line.startswith(Runner.RUNLIST_COMMENT_PREFIX):
                tsuites.append(line)
        return tuple(tsuites)
