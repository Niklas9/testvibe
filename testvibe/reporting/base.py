

# TODO(niklas9):
# * add options here if subclass accepts reporting continuously or only at end
#   (like JUnit XML Format)

class ReportingBase(object):

    def add_test_result(self, testsuite, result):
        raise NotImplementedError

    def finish(self):
        pass 
