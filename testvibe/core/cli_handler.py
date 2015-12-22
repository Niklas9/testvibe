
import argparse
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

    args = None
    verbosity = None
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
        self.log = logger.Log(log_level=log_level, use_stdout=self.verbosity)

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
                              self.args.silent)
            r.execute(self.cwd)
            # TODO(niklas9):
            # * provide runlists to runner.. that should be all it takes

    @staticmethod
    def _is_valid_name(s):
        return re.match(CLIHandler.RE_VALID_NAME, s) is not None


class ArgumentParserWithError(argparse.ArgumentParser):

    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(1)
