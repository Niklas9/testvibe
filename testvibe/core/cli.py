
import testvibe
import testvibe.core.cli_handler as cli_handler


class CLI(object):

    parser = None
    subparsers = None

    def __init__(self):
        self.parser = cli_handler.ArgumentParserWithError(
                                        description='Testvibe control')
        self.subparsers = self.parser.add_subparsers()

    def run(self):
        self.add_cmd_startproject()
        self.add_cmd_testgroup()
        self.add_cmd_testsuite()
        self.add_cmd_run()
        # TODO(niklas9):  * respect set path here
        self.parser.add_argument('-P', '--path',
                                 help='project path, if not set, tries to work '
                                      'out of current directory')
        self.parser.add_argument('-V', '--version', action='version',
                        version=testvibe.VERSION,
                        help='show program\'s version number and exit')
        ch = cli_handler.CLIHandler(self.parser.parse_args())
        ch.execute()

    def add_cmd_startproject(self):
        self.add_cmd('startproject', 'start a new project', args=['name'])

    def add_cmd_testgroup(self):
        self.add_cmd('addtestgroup', 'add a new test group within a project',
                     args=['name'])

    def add_cmd_testsuite(self):
        self.add_cmd('addtestsuite', 'add a new test suite within a group',
                     args=['name'])

    def add_cmd_run(self):
        cmd = self.add_cmd('run', 'initiate test run')
        cmd.add_argument('-p', '--parallel', default=1,
                             help='number of testsuites to run in parallel')
        cmd.add_argument('-v', '--verbosity', action='store_true',
                            help='verbosity level')

    def add_cmd(self, name, help, args=None):
        if args is None:  args = []
        cmd = self.subparsers.add_parser(name, help=help)
        for arg in args:
            cmd.add_argument(arg)
        cmd.set_defaults(cmd=name)
        return cmd
