
import argparse
import os
import sys
import re

import testvibe


class CLIHandler(object):

    DEFAULT_INSTALL_DIR = 'default_install/'
    FILENAME_SETTINGS = 'settings.py'
    FILENAME_RUNLIST = 'RUNLIST'
    FILENAME_TESTSUITE = 'example_testsuite.py'
    FILEMODE_READ = 'r'
    FILEMODE_WRITE = 'w'
    PLACEHOLDER_NAME = '<Example>'
    RE_VALID_NAME = r'^[A-Za-z0-9_]+$'
    CMD_STARTPROJECT = 'startproject'
    CMD_ADDTESTSUITE = 'addtestsuite'
    CMD_ADDTESTGROUP = 'addtestgroup'
    CMD_RUN = 'run'
    CMDS_WITH_NAME_ARG = (CMD_STARTPROJECT, CMD_ADDTESTSUITE, CMD_ADDTESTGROUP)

    args = None

    def __init__(self, args):
        self.args = args

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
            if cmd == self.CMD_STARTPROJECT:
                self.cmd_startproject(self.args.name)
            elif cmd == self.ADD_TESTSUITE:
                self.cmd_addtestsuite(self.args.name)
            elif cmd == self.CMD_ADDTESTGROUP:
                self.cmd_addtestgroup(self.args.name)
        elif cmd == self.CMD_RUN:
            self.cmd_run()

    def cmd_run(self):
        raise NotImplementedError()

    def cmd_startproject(self, name):
        self._exit_if_dir_exists(name)
        os.makedirs(name)
        self._copy_file(name, CLIHandler.FILENAME_SETTINGS,
                       search=CLIHandler.PLACEHOLDER_NAME, replace=name)

    def cmd_addtestsuite(self, name):
        raise NotImplementedError()

    def cmd_addtestgroup(self, name):
        self._exit_if_dir_exists(name)
        os.makedirs(name)
        self._copy_file(name, self.FILENAME_RUNLIST)
        self._copy_file(name, self.FILENAME_TESTSUITE)

    @staticmethod
    def _copy_file(dir_name, filename, search=None, replace=None):
        with open(CLIHandler._get_src(filename), CLIHandler.FILEMODE_READ) as f:
            src_content = f.read()
        if search is not None and replace is not None:
            src_content = src_content.replace(search, replace)
        with open('%s/%s' % (dir_name, filename), CLIHandler.FILEMODE_WRITE) as f:
            f.write(src_content)

    @staticmethod
    def _get_src(filename):
        return ('%s/%s%s' % (os.path.dirname(testvibe.__file__),
                             CLIHandler.DEFAULT_INSTALL_DIR, filename))

    @staticmethod
    def _exit_if_dir_exists(dir_name):
         if os.path.exists(dir_name):
            sys.stderr.write('command error: \'%s\' already exists\n'
                             % os.path.abspath(dir_name))
            sys.exit(1)

    @staticmethod
    def _is_valid_name(s):
        return re.match(CLIHandler.RE_VALID_NAME, s) is not None


class ArgumentParserWithError(argparse.ArgumentParser):

    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(2)
