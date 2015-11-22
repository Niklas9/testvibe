
class AssertionException(Exception):  pass
class AssertionExceptionEqual(AssertionException):  pass
class AssertionExceptionNotEqual(AssertionException):  pass
class AssertionExceptionIsNull(AssertionException):  pass
class AssertionExceptionIsNotNull(AssertionException):  pass
class AssertionExceptionGreaterThan(AssertionException):  pass
class AssertionExceptionGreaterThanOrEqual(AssertionException):  pass
class AssertionExceptionLesserThan(AssertionException):  pass
class AssertionExceptionLesserThanOrEqual(AssertionException):  pass

# TODO(niklas9):
# * add the error messages in the AssertionException object instead of logging?
#   the exception object could potentially take care of logging as well..?
# * add "assert_in" for checking if keys are in json

# NOTE(niklas9):
# * this is an abstract class, self.log needs to be set

class Asserts(object):

    LOG_FMT = 'assert %s (%s) %s (%s)'
    LOG_OBJ_FMT = '%r, %s'
    LOG_EQ = 'equal'
    LOG_EQ_OP = '=='
    LOG_NOT_EQ = 'NOT equal'
    LOG_NOT_EQ_OP = '!='
    LOG_IS_NULL = 'is null'
    LOG_IS_NULL_OP = '=='
    LOG_IS_NOT_NULL = 'is NOT null'
    LOG_IS_NOT_NULL_OP = '!='
    LOG_GREATER_THAN = 'greater'
    LOG_GREATER_THAN_OP = '>'
    LOG_GREATER_THAN_OR_EQUAL = 'greater or equal'
    LOG_GREATER_THAN_OR_EQUAL_OP = '>='
    LOG_LESSER_THAN = 'lesser or equal'
    LOG_LESSER_THAN_OP = '<'
    LOG_LESSER_THAN_OR_EQUAL = 'lesser'
    LOG_LESSER_THAN_OR_EQUAL_OP = '<='

    def __init__(self):
        pass

    def assert_equal(self, obj1, obj2):
        if not obj1 == obj2:
            msg = self._log_fmt(self.LOG_EQ, self.LOG_NOT_EQ_OP, obj1, obj2)
            raise AssertionExceptionEqual(msg)
        self._log(self.LOG_EQ, self.LOG_EQ_OP, obj1, obj2)

    def assert_eq(self, *args):  return self.assert_equal(*args)
    def a_eq(self, *args):  return self.assert_equal(*args)

    def assert_not_equal(self, obj1, obj2):
        if obj1 == obj2:
            msg = self._log_fmt(self.LOG_NOT_EQ, self.LOG_EQ_OP, obj1, obj2)
            raise AssertionExceptionNotEqual(msg)
        self._log(self.LOG_NOT_EQ, self.LOG_NOT_EQ_OP, obj1, obj2)

    def assert_neq(self, *args):  return self.assert_not_equal(*args)
    def a_neq(self, *args):  return self.assert_not_equal(*args)

    def assert_null(self, obj):
        if obj is not None:
            msg = self._log_fmt(self.LOG_IS_NULL, self.LOG_IS_NOT_NULL_OP,
                                obj, None)
            raise AssertionExceptionIsNull(msg)
        self._log(self.LOG_IS_NULL, self.LOG_IS_NULL_OP, obj, None)

    def a_null(self, *args):  return self.assert_is_null(*args)

    def assert_not_null(self, obj):
        if obj is None:
            msg = self._log_fmt(self.LOG_IS_NOT_NULL, self.LOG_IS_NULL_OP,
                                obj, None)
            raise AssertionExceptionIsNotNull()
        self._log(self.LOG_IS_NOT_NULL, self.LOG_IS_NOT_NULL_OP, obj, None)

    def a_not_null(self, *args):  return self.assert_is_not_null(*args)

    def assert_greater_than(self, val1, val2):
        if not val1 > val2:
            msg = self._log_fmt(self.LOG_GREATER_THAN,
                                self.LOG_LESSER_THAN_OR_EQUAL_OP, val1, val2)
            raise AssertionExceptionGreaterThan(msg)
        self._log(self.LOG_GREATER_THAN, self.LOG_GREATER_THAN_OP, val1, val2)

    def assert_gt(self, *args):  return self.assert_greater_than(*args)
    def a_gt(self, *args):  return self.assert_greater_than(*args)

    def assert_greater_than_or_equal(self, val1, val2):
        if not val1 >= val2:
            msg = self._log_fmt(self.LOG_GREATER_THAN_OR_EQUAL,
                                self.LOG_LESSER_THAN_OP, val1, val2)
            raise AssertionExceptionGreaterThanOrEqual(msg)
        self._log(self.LOG_GREATER_THAN_OR_EQUAL,
                  self.LOG_GREATER_THAN_OR_EQUAL_OP, val1, val2)

    def assert_gte(self, *args):  return self.assert_greater_than_or_equal(*args)
    def a_gte(self, *args):  return self.assert_greater_than_or_equal(*args)

    def assert_lesser_than(self, val1, val2):
        if not val1 < val2:
            msg = self._log_fmt(self.LOG_LESSER_THAN,
                                self.LOG_GREATER_THAN_OR_EQUAL_OP, val1, val2)
            raise AssertionExceptionLesserThan(msg)
        self._log(self.LOG_LESSER_THAN, self.LOG_LESSER_THAN_OP, val1, val2)

    def assert_lt(self, *args):  return self.assert_lesser_than(*args)
    def a_lt(self, *args):  return self.assert_lesser_than(*args)

    def assert_lesser_than_or_equal(self, val1, val2):
        if not val1 <= val2:
            msg = self._log_fmt(self.LOG_LESSER_THAN_OR_EQUAL,
                                self.LOG_GREATER_THAN_OP, val1, val2)
            raise AssertionExceptionLesserThanOrEqual()
        self._log(self.LOG_LESSER_THAN_OR_EQUAL,
                  self.LOG_LESSER_THAN_OR_EQUAL_OP, val1, val2)

    def assert_lte(self, *args):  return self.assert_lesser_than_or_equal(*args)
    def a_lte(self, *args):  return self.assert_lesser_than_or_equal(*args)

    def _log(self, assert_type, op, obj1, obj2):
        self.log.debug(self._log_fmt(assert_type, op, obj1, obj2))

    def _log_fmt(self, assert_type, op, obj1, obj2):
        return self.LOG_FMT % (assert_type, self._log_obj_fmt(obj1), op,
                               self._log_obj_fmt(obj2))

    def _log_obj_fmt(self, obj):
        return self.LOG_OBJ_FMT % (obj, type(obj))