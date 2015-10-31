
import nose

import testvibe


class BasicTestSuite(testvibe.TestSuite):

    def test_equal(self, v1, v2):
        self.assert_equal(v1, v2)

    def test_equal_alias_1(self, v1, v2):
        self.assert_eq(v1, v2)  # just a link to assert_equal

    def test_equal_alias_2(self, v1, v2):
        self.a_eq(v1, v2)  # just link to assert_equal

    def test_null(self, v):
        self.assert_null(v)

    def test_not_null(self, v):
        self.assert_not_null(v)


class TestAsserts(object):

    t = None

    def setUp(self):
        self.t = BasicTestSuite()

    def tearDown(self):
        self.t = None

    def test_equal(self):
        self.t.test_equal(9, 9)
        self.t.test_equal_alias_1(9, 9)
        self.t.test_equal_alias_2(9, 9)

    @nose.tools.raises(testvibe.asserts.AssertionException) 
    def test_neg_equal(self):
        self.t.test_equal(1, 3)

    # NOTE(niklas9):
    # * need a second test case for the alias since after the raise
    #   in the first line of test_neg_assert_equal any other statement
    #   won't be executed
    @nose.tools.raises(testvibe.asserts.AssertionException) 
    def test_neg_equal_alias_1(self):
        self.t.test_equal_alias_1(1, 3)

    @nose.tools.raises(testvibe.asserts.AssertionException) 
    def test_neg_equal_alias_2(self):
        self.t.test_equal_alias_2(6, 7)

    def test_null(self):
        self.t.test_null(None)

    @nose.tools.raises(testvibe.asserts.AssertionException)
    def test_neg_null(self):
        self.t.test_null('None')

    def test_not_null(self):
        self.t.test_not_null('None')

    @nose.tools.raises(testvibe.asserts.AssertionException)
    def test_neg_not_null(self):
        self.t.test_not_null(None)
