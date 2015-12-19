
import testvibe

import settings


# Create your test suite and test cases here

class ExampleTestsuite(testvibe.Testsuite):

    def test_example(self):
        self.api.set_root_domain(settings.API_ROOT_DOMAIN)
        url = ('yql?q=select%20*%20from%20weather.forecast%20where%20w'
               'oeid%20in%20(select%20woeid%20from%20geo.places(1)%20w'
               'here%20text%3D%22nome%2C%20ak%22)&format=json&env=store'
               '%3A%2F%2Fdatatables.org%2Falltableswithkeys')
        json, r = self.api.get(url)
        self.assert_equal(r.status_code, 200)
        country = json['query']['results']['channel']['location']['country']
        self.assert_equal(country, 'United States')
        self.assert_not_equal(country, 'Sweden')