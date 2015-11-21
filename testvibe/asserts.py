
class AssertionException(Exception):  pass

# TODO(niklas9):
# * add the error messages in the AssertionException object instead of logging?
#   the exception object could potentially take care of logging as well..?
# * add "assert_in" for checking if keys are in json

# NOTE(niklas9):
# * this is an abstract class, self.log needs to be set

class Asserts(object):

    def __init__(self):
        pass

    def assert_equal(self, obj1, obj2):
        # TODO(niklas9):
        # * this should be self.log.debug
        self._log('equal', '==', obj1, obj2)
        if not obj1 == obj2:
            raise AssertionException()

    def assert_eq(self, *args):  return self.assert_equal(*args)
    def a_eq(self, *args):  return self.assert_equal(*args)

    def assert_not_equal(self, obj1, obj2):
        self._log('NOT equal', '!=', obj1, obj2)
        if not obj1 == obj2:
            raise AssertionException()

    def assert_null(self, obj):
        self._log('is null', '==', obj, None)
        if obj is not None:
            raise AssertionException()

    def a_null(self, *args):  return self.assert_is_null(*args)

    def assert_not_null(self, obj):
        self._log('is NOT null', '!=', obj, None)
        if obj is None:
            raise AssertionException()

    def a_not_null(self, *args):  return self.assert_is_not_null(*args)

    def assert_greater_than(self, val1, val2):
        self._log('greater', '>', val1, val2)
        if not val1 > val2:
            raise AssertionException()

    def assert_gt(self, *args):  return self.assert_greater_than(*args)
    def a_gt(self, *args):  return self.assert_greater_than(*args)

    def assert_greater_than_or_equal(self, val1, val2):
        self._log('greater or equal', '>=', val1, val2)
        if not val1 >= val2:
            raise AssertionException()

    def assert_gte(self, *args):  return self.assert_greater_than_or_equal(*args)
    def a_gte(self, *args):  return self.assert_greater_than_or_equal(*args)

    def assert_lesser_than(self, val1, val2):
        self._log('lesser', '<', val1, val2)
        if not val1 < val2:
            raise AssertionException()

    def assert_lt(self, *args):  return self.assert_lesser_than(*args)
    def a_lt(self, *args):  return self.assert_lesser_than(*args)

    def assert_lesser_than_or_equal(self, val1, val2):
        self._log('lesser or equal', '<=', val1, val2)
        if not val1 <= val2:
            raise AssertionException()

    def assert_lte(self, *args):  return self.assert_lesser_than_or_equal(*args)
    def a_lte(self, *args):  return self.assert_lesser_than_or_equal(*args)

    def _log(self, assert_type, op, obj1, obj2):
        msg = ('assert %s (%s) %s (%s)' % (assert_type, self._log_fmt(obj1),
                                           op, self._log_fmt(obj2)))
        self.log.debug(msg)

    def _log_fmt(self, obj):
        return '%r, %s' % (obj, type(obj))