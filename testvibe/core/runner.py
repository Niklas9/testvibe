
import importlib
import os
try:
    import queue
except ImportError:
    import Queue as queue  # fallback for Python 2.x
import threading
import sys

import tabulate
import tqdm

import testvibe
import testvibe.core.cli_file_mgmt as cli_file_mgmt
import testvibe.core.utils as utils


class Runner(object):
    """ Test runner """

    RELATIVE_IMPORT_FMT = '.%s'
    UNIX_EXIT_CODE_OK = 0
    UNIX_EXIT_CODE_ERROR = 1

    log = None
    is_verbose = None
    is_silent = None
    parallel_level = None
    tcase_queue = None
    exit_code = UNIX_EXIT_CODE_OK

    def __init__(self, log_handler, parallel_level, is_verbose, is_silent):
        self.log = log_handler
        self.parallel_level = parallel_level  # no of threads
        self.is_verbose = is_verbose
        self.is_silent = is_silent
        self.tcase_queue = queue.Queue()  # FIFO

    def execute(self, cwd):
        runlists = cli_file_mgmt.CLIFileMgmt.get_runlists(cwd)
        if len(runlists) == 0:
            sys.stderr.write('no runlists found...\n')
            sys.exit(1)
        for rl_path in runlists:
            self.log.info('starting test run on from runlist <%s>' % rl_path)
            tsuites = cli_file_mgmt.CLIFileMgmt.parse_runlist(rl_path)
            self._run_tsuites(self._get_import_tgroup(rl_path), tsuites)

    def _run_tsuites(self, import_pkg, tsuites):
        len_tsuites = len(tsuites)
        self.log.debug('found %d test suites' % len_tsuites)
        for tsuite in tsuites:
            self.log.debug('initating run on testsuite <%s>' % tsuite)
            # TODO(niklas9):
            # * add exception handling for the importing below.. the user can
            #   enter lots of bad stuff in the runlists.. we should give them a
            #   hint
            ts = importlib.import_module(self.RELATIVE_IMPORT_FMT % tsuite,
                                         package=import_pkg)
            tsuite_classes = self._get_all_tsuite_classes(ts)
            if len(tsuite_classes) == 0:
                # TODO(niklas9):
                # * this is actually too late.. should do some sanity check on
                #   all runlists before initiating a test run..
                #   like "validating runlists".. could be a separate cmd to
                #   tvctl as well
                sys.stderr.write('no subclasses of testvibe.Testsuite found\n')
                sys.exit(1)
            self._run_tcases(tsuite_classes)
        sys.exit(self.exit_code)

    def _run_tcases(self, tsuite_classes):
        for tsuite_class in tsuite_classes:
            if not self.is_verbose and not self.is_silent:
                sys.stdout.write('%s\n========================\n'
                                 % tsuite_class.__name__)
            results = []
            tcs = self._get_all_tcases(tsuite_class)
            tsuite_class_i = tsuite_class()
            progressb = None
            if not self.is_verbose and not self.is_silent:
                progressb = tqdm.trange(len(tcs), leave=False,
                                        desc='Executing test cases')
            for tc in tcs:
                self.tcase_queue.put((tc, tsuite_class_i))
            # TODO(niklas9):
            # * honor parallelization level arg here, more threads if needed!
            t = threading.Thread(target=self._tc_worker, args=[progressb])
            t.deamon = True  # if someone does Ctrl-C, just die
            t.start()
            while t.is_alive():
                self._report_tcase_results(tsuite_class_i, results)
            t.join()
            # NOTE(niklas9):
            # * make sure results are emptied here before we move on..
            self._report_tcase_results(tsuite_class_i, results)
            if not self.is_verbose and not self.is_silent:
                if progressb is not None:  progressb.close()
                self._output_tsuite_results(results)

    def _tc_worker(self, progressb):
        while not self.tcase_queue.empty():
            try:
                tcase, tsuite = self.tcase_queue.get(block=False)
            except queue.Empty:
                continue
            finally:
                # TODO(niklas9):
                # * I don't get why class instance is second arg below.. should
                #   replace 'self' so should be the first one?!!
                tsuite.test(tcase, tsuite)
                if progressb is not None:  progressb.update()
                self.tcase_queue.task_done()

    def _report_tcase_results(self, tsuite, results):
        while not tsuite.results.empty():
            r = tsuite.results.get(block=False)
            results.append(r)
            if not r.passed:
                self.exit_code = self.UNIX_EXIT_CODE_ERROR

    @staticmethod
    def _get_import_tgroup(rl_path):
        if utils.STRING_SLASH in rl_path:
            return rl_path.split(utils.STRING_SLASH)[0]
        return os.getcwd().split(utils.STRING_SLASH)[-1]

    @staticmethod
    def _get_all_tcases(cl):
        tcases = set()
        reserved_names = testvibe.Testsuite.RESERVED_NAMES
        for o in dir(cl):
            if o.startswith(utils.STRING_UNDERSCORE):  continue  # no private m
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
    def _output_tsuite_results(results):
        sys.stdout.write('\n')
        table = []
        for r in results:
            asserts = '%d/%d' % (r.passed_asserts, r.total_asserts)
            time_elapsed = '%.4fs' % r.time_elapsed
            table.append([r.name, r.result, asserts, time_elapsed])
        headers = ['Test case', 'Result', 'Asserts', 'Time elapsed']
        sys.stdout.write('%s\n\n' % tabulate.tabulate(table, headers=headers))
