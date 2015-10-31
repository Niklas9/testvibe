
class AssertionException(Exception):  pass


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

    def _log(self, msg, op, obj1, obj2):
        print 'assert %s <%s> %s <%s>' % (msg, self._log_obj_fmt(obj1), op,
                                          self._log_obj_fmt(obj2))

    def _log_obj_fmt(self, obj):
        return '%r, %s, %s' % (obj, obj, type(obj))
