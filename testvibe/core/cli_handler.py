
import argparse
import datetime
import os
import sys
import re

import testvibe.logger as logger
import testvibe.core.cli_file_mgmt as cli_file_mgmt
import testvibe.core.runner as runner
import testvibe.core.utils as utils

try:
    import settings
except ImportError:
    # NOTE(niklas9):
    # * this should only happen during testing, otherwise a global settings
    #   be importable for every project
    settings = None


class CLIHandler(object):
    """ CLI validation and initator """

    RE_VALID_NAME = r'^[A-Za-z0-9_]+$'
    CMD_STARTPROJECT = 'startproject'
    CMD_ADDTESTGROUP = 'addtestgroup'
    CMD_RUN = 'run'
    CMDS_WITH_NAME_ARG = (CMD_STARTPROJECT, CMD_ADDTESTGROUP)
    LOG_FILE_FMT = 'runner-%s.log'
    LOG_FILE_TIMESTAMP_FMT = '%Y-%m-%dT%H%M%S.%f'
    DEFAULT_ITERATIONS = 1

    args = None
    verbosity = None
    iterations = None
    cwd = None

    def __init__(self, args):
        self.args = args
        log_level = logger.LOG_LEVEL_DEBUG
        if settings is not None and not settings.LOG_LEVEL_DEBUG:
            log_level = logger.LOG_LEVEL_PROD
        self.verbosity = False
        if self.args.verbosity:
            self.verbosity = True
        if self.args.path is None:
            self.cwd = os.getcwd()
        else:
            cwd = self.args.path
            if cwd.endswith(utils.STRING_SLASH):
                cwd = cwd [:-1]  # remove trailing /
            self.cwd = cwd
        sys.path.append(self.cwd)
        self.iterations = self.DEFAULT_ITERATIONS
        # TODO(niklas9):
        # * should perhaps output smth to the console if given iterations value
        #   is not an integer
        if (utils.is_int(self.args.iterations) and
            not self.args.iterations == self.iterations):
            self.iterations = int(self.args.iterations)
        # TODO(niklas9):
        # * make it a project specific testvibe setting to use log files or
        #   not, however default should be yes
        self.log = logger.Log(log_level=log_level, use_stdout=self.verbosity,
                              log_file=self._setup_log_file(self.cwd))

    def execute(self):
        cmd = self.args.cmd
        if cmd in self.CMDS_WITH_NAME_ARG:
            name = self.args.name
            if not self._is_valid_name(name):
                # NOTE(niklas9):
                # * for example dashes (-) in names will cause unimportable
                #   projects in Python
                sys.stderr.write('error: unsupported characters in name\n')
                sys.exit(1)
            cli_fm = cli_file_mgmt.CLIFileMgmt(self.log)
            if cmd == self.CMD_STARTPROJECT:
                cli_fm.startproject(self.cwd, self.args.name)
            elif cmd == self.CMD_ADDTESTGROUP:
                cli_fm.addtestgroup(self.cwd, self.args.name)
        elif cmd == self.CMD_RUN:
            r = runner.Runner(self.log, self.args.parallel, self.verbosity,
                              self.args.silent, self.iterations)
            r.execute(self.cwd)

    @staticmethod
    def _is_valid_name(s):
        return re.match(CLIHandler.RE_VALID_NAME, s) is not None

    @staticmethod
    def _setup_log_file(cwd):
        time_fmt = CLIHandler.LOG_FILE_TIMESTAMP_FMT
        time = datetime.datetime.utcnow().strftime(time_fmt)
        filename = CLIHandler.LOG_FILE_FMT % time
        paths = [cwd, cli_file_mgmt.CLIFileMgmt.DEFAULT_LOG_DIR]
        if not os.path.exists(utils.get_path(paths)):
            os.makedirs(utils.get_path(paths))
        paths.append(filename)
        return utils.get_path(paths)

class ArgumentParserWithError(argparse.ArgumentParser):

    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(1)
