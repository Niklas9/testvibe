
import codecs

import testvibe.reporting.base as rbase


# NOTE(niklas9):
# * I'm by intention not using libxml or any other xml parser here.. don't want
#   to add such a heavy dependency for two main reasons:
#     1) not everyone is using this
#     2) we're just writing xml, not parsing.. writing is at least said to be
#        easier :)

class JUnitXMLMiddleware(rbase.ReportingBase):

    OUTPUT_FILENAME_FMT = 'junit-%s.xml'
    OUTPUT_FILE_ENCODING_UTF8 = 'utf-8'
    FILEMODE_WRITE = 'w'

    output_filename = None
    results = None

    def __init__(self, build_no):
        # TODO(niklas9):
        # * should be able to set output filename from CLI
        self.output_filename = self.OUTPUT_FILENAME_FMT  % build_no
        self.results = {}

    def add_test_result(self, testsuite, result):
        if testsuite not in self.results:
            self.results[testsuite] = list()
        self.results[testsuite].append(result)

    def finish(self):
        with codecs.open(self.output_filename, mode=self.FILEMODE_WRITE,
                         encoding=self.OUTPUT_FILE_ENCODING_UTF8) as f:
            f.write(self._xml_header())
            # TODO(niklas9):  * add support for disabled, errors etc args
            f.write(self._xml_testsuites_start())
            for tsuite, tcases in self.results.iteritems():
                f.write(self._xml_testsuite_start(tsuite))
                for tc in tcases:
                    # TODO(niklas9):  * support for err_msg, fail_msg, sys_*
                    f.write(self._xml_testcase(tc.name, tc.total_asserts,
                                               tsuite, tc.result,
                                               tc.time_elapsed))
                f.write(self._xml_testsuite_end())
                f.flush()
            f.write(self._xml_testsuites_end())

    @staticmethod
    def _xml_header():
        return ('<?xml version="1.0" encoding="%s"?>\n'
                % JUnitXMLMiddleware.OUTPUT_FILE_ENCODING_UTF8.upper())

    @staticmethod
    def _xml_testsuites_start(disabled='', errors='', failures='', tests='',
                              time=''):
        return ('<testsuites disabled="%s" errors="%s" failures="%s" tests="%s"'
                ' time="%s">\n' % (disabled, errors, failures, tests, time))

    @staticmethod
    def _xml_testsuites_end():
        return '</testsuites>\n'

    @staticmethod
    def _xml_testsuite_start(name, disabled='', errors='', failures='',
                             tests='', time=''):
         return ('\t<testsuite name="%s" disabled="%s" errors="%s" '
                 'failures="%s" tests="%s" time="%s">\n'
                 % (name, disabled, errors, failures, tests, time))

    @staticmethod
    def _xml_testsuite_end():
        return '\t</testsuite>\n'

    @staticmethod
    def _xml_testcase(name, assertions, classname, status, time, err_msg=None,
                      fail_msg=None, sys_out=None, sys_err=None):
        s = ('\t\t<testcase name="%s" assertions="%s" classname="%s" '
             'status="%s" time="%s">\n' % (name, assertions, classname, status,
                                           time))
        if err_msg is not None:
            s += '\t\t\t<error message="%s" type="" />\n' % err_msg
        if fail_msg is not None:
            s += '\t\t\t<failure message="%s" type="%s" />\n' % fail_msg
        if sys_out is not None:
            s += '\t\t\t<system-out>%s</system-out>\n' % sys_out
        if sys_err is not None:
            s += '\t\t\t<system-err>%s</system-err>\n' % sys_err
        s += '\t\t</testcase>\n'
        return s
