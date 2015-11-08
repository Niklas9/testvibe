
import os
import sys
import re

import argparse


class CLI(object):

    DEFAULT_INSTALL_DIR = 'default_install/'
    FILENAME_SETTINGS = 'settings.py'
    FILENAME_RUNLIST = 'RUNLIST'
    FILENAME_TESTSUITE = 'test_suite.py'
    PLACEHOLDER_NAME = '<Example>'
    RE_VALID_DIR_NAME = '^[A-Za-z0-9-]+$'

    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        if self.args.cmd == 'startproject':
            self.cmd_startproject(self.args.name)
        elif self.args.cmd == 'addtestgroup':
            self.cmd_addtestgroup(self.args.name)
        elif self.args.cmd == 'run':
            self.cmd_run()

    def cmd_run(self):
        raise NotImplementedError()

    def cmd_startproject(self, name):
        if not self._is_valid_dir_name(name):
            sys.stderr.write('error: unsupported characters in project name\n')
            sys.exit(2)
        self._exit_if_dir_exists(name)
        os.makedirs(name)
        self._copy_file(name, CLI.FILENAME_SETTINGS,
                       search=CLI.PLACEHOLDER_NAME, replace=name)

    def cmd_addtestgroup(self, name):
        if not self._is_valid_dir_name(name):
            sys.stderr.write('error: unsupported characters in test group '
                             'name\n')
            sys.exit(2)
        self._exit_if_dir_exists(name)
        os.makedirs(name)
        self._copy_file(name, self.FILENAME_RUNLIST)
        self._copy_file(name, self.FILENAME_TESTSUITE)

    @staticmethod
    def _copy_file(dir_name, filename, search=None, replace=None):
        with open(CLI._get_src(filename), 'r') as f:
            src_content = f.read()
        if search is not None and replace is not None:
            src_content = src_content.replace(search, replace)
        with open('%s/%s' % (dir_name, filename), 'w') as f:
            f.write(src_content)

    @staticmethod
    def _get_src(filename):
        return ('%s/%s%s' % (os.path.dirname(testvibe.__file__),
                             CLI.DEFAULT_INSTALL_DIR, filename))

    @staticmethod
    def _exit_if_dir_exists(dir_name):
         if os.path.exists(dir_name):
            sys.stderr.write('command error: \'%s\' already exists\n'
                             % os.path.abspath(dir_name))
            sys.exit(2)

    @staticmethod
    def _is_valid_dir_name(s):
        return re.match(CLI.RE_VALID_DIR_NAME, s) is not None


class ArgumentParserWithError(argparse.ArgumentParser):

    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(2)
