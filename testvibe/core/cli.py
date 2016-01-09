
import testvibe
import testvibe.core.cli_handler as cli_handler


class CLI(object):
    """ CLI configuration class """

    parser = None
    subparsers = None

    def __init__(self):
        self.parser = cli_handler.ArgumentParserWithError(
                                        description='Testvibe control')
        self.subparsers = self.parser.add_subparsers()

    def run(self):
        self.add_cmd_startproject()
        self.add_cmd_testgroup()
        self.add_cmd_run()
        self.parser.add_argument('-P', '--path',
                                 help='project path, if not set, tries to work '
                                      'out of current directory')
        self.parser.add_argument('-v', '--verbosity', action='store_true',
                                 help='verbosity level')
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

    def add_cmd_run(self):
        cmd = self.add_cmd('run', 'initiate test run')
        cmd.add_argument('-s', '--silent', action='store_true',
                             help='run in silent mode')
        cmd.add_argument('-r', '--report', action='store_true',
                         help='report results, configure in detail in settings')
        # TODO(niklas9):
        # * add silent option to run, only outputs something if errors
        # * add support for running complete testsuites in parallel? or part of
        #   runlist config?
        cmd.add_argument('-p', '--parallel', default=1,
                             help='number of testcases to run in parallel')

    def add_cmd(self, name, help, args=None):
        if args is None:  args = []
        cmd = self.subparsers.add_parser(name, help=help)
        for arg in args:
            cmd.add_argument(arg)
        cmd.set_defaults(cmd=name)
        return cmd
