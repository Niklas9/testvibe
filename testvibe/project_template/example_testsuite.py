
import testvibe


# Create your test suite and test cases here

class ExampleTestsuite(testvibe.Testsuite):

    def test_example(self):
        json, r = self.api.get('https://api.github.com')
        self.assert_equal(r.status_code, 200)
        self.assert_equal(json['hub_url'], 'https://api.github.com/hub')
        self.assert_in('X-RateLimit-Limit', r.headers)