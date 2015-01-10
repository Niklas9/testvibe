
import os
import sys

import testvibe
import testvibe.core.utils as utils


class CLIFileMgmt(object):
    """ CLI file management commands, such as startproject and addtestgroup """

    PROJECT_TEMPLATE_DIR = 'project_template'
    FILENAME_SETTINGS = 'settings.py'
    FILENAME_RUNLIST = 'RUNLIST'
    FILENAME_TESTSUITE = 'example_testsuite.py'
    FILENAME_INIT = '__init__.py'
    FILEMODE_READ = 'r'
    FILEMODE_WRITE = 'w'
    PLACEHOLDER_NAME = '<Example>'
    DEFAULT_LOG_DIR = 'logs'
    RUNLIST_COMMENT_PREFIX = '#'
    PYTHON_SUFFIX = '.py'

    log = None

    def __init__(self, log_handler):
        self.log = log_handler

    def startproject(self, cwd, name):
        path = utils.get_path((cwd, name))
        self._exit_if_dir_exists(path)
        self.log.debug('creating project dir <%s>' % path)
        os.makedirs(utils.get_path((path, self.DEFAULT_LOG_DIR)))
        utils.copy_file(self._get_src_path(CLIFileMgmt.FILENAME_SETTINGS),
                        utils.get_path((cwd, name,
                                       CLIFileMgmt.FILENAME_SETTINGS)))
        self._add_init_file(path)

    def addtestgroup(self, cwd, name):
        path = utils.get_path((cwd, name))
        self._exit_if_dir_exists(path)
        self.log.debug('creating test group dir <%s>' % path)
        os.makedirs(path)
        self._add_init_file(path)
        utils.copy_file(self._get_src_path(self.FILENAME_RUNLIST),
                        utils.get_path((cwd, name, self.FILENAME_RUNLIST)))
        utils.copy_file(self._get_src_path(self.FILENAME_TESTSUITE),
                        utils.get_path((cwd, name, self.FILENAME_TESTSUITE)))

    @staticmethod
    def _add_init_file(path):
        p = utils.get_path((path, CLIFileMgmt.FILENAME_INIT))
        utils.create_empty_file(p)

    @staticmethod
    def _get_src_path(filename):
        return utils.get_path((os.path.dirname(testvibe.__file__),
                               CLIFileMgmt.PROJECT_TEMPLATE_DIR,
                               filename))

    @staticmethod
    def _exit_if_dir_exists(dir_name):
         if os.path.exists(dir_name):
            sys.stderr.write('command error: \'%s\' already exists\n'
                             % os.path.abspath(dir_name))
            sys.exit(1)

    @staticmethod
    def get_runlists(cwd):
        runlists = set()
        if os.path.exists(CLIFileMgmt.FILENAME_RUNLIST):
            runlists.add(CLIFileMgmt.FILENAME_RUNLIST)
        else:
            dirs = utils.get_all_dirs(cwd)
            for d in dirs:
                for f in os.listdir(d):
                    if f == CLIFileMgmt.FILENAME_RUNLIST:
                        runlists.add(utils.get_path((d, f)))
        return runlists

    @staticmethod
    def parse_runlist(path):
        tsuites = list()  # dups are fine, if one wants to rerun tsuites
        for line in utils.get_file_content(path).splitlines():
            if not line.startswith(CLIFileMgmt.RUNLIST_COMMENT_PREFIX):
                # TODO(niklas9):
                # * what if trailing spaces in the end of runlists? add regexp
                #   for this instead?
                if line.endswith(CLIFileMgmt.PYTHON_SUFFIX):
                    line = line[:-len(CLIFileMgmt.PYTHON_SUFFIX)]
                if utils.STRING_SLASH in line:
                    line = line.split(utils.STRING_SLASH)[-1]
                tsuites.append(line)
        return tuple(tsuites)
