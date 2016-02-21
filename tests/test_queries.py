import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from purl import Purl

class TestQueryFunctions(object):

  def test_simple_query(self):
    url = Purl('http://blank')
    url.add_query('c', 1)
    assert str(url) == 'http://blank?c=1'
    assert str(url.add_query('a', 'one')) == 'http://blank?a=one&c=1'
    assert str(url) == 'http://blank?a=one&c=1'

  def test_query_multiple(self):
    url = Purl('https://hello.org')
    url.add_query({'c': 1})
    assert str(url) == 'https://hello.org?c=1'

    url = Purl('https://hello.org')
    url.add_query({'a': 'one', 'c': 45})
    assert str(url) == 'https://hello.org?a=one&c=45'

    url = Purl('https://hello.org?')
    url.add_query({'a': 'one', 'c': 45})
    assert str(url) == 'https://hello.org?a=one&c=45'

    url = Purl('https://hello.org?d=dee')
    url.add_query({'a': 'one', 'c': 45})
    assert str(url) == 'https://hello.org?a=one&c=45&d=dee'

    url = Purl('https://hello.org?a=aye&d=dee')
    url.add_query({'a': 'one', 'c': 45})
    assert str(url) == 'https://hello.org?a=one&c=45&d=dee'

    url = Purl('https://hello.org?g=gamma&d=dee')
    url.add_query({'a': 'one', 'c': 45})
    assert str(url) == 'https://hello.org?a=one&c=45&d=dee&g=gamma'

    url = Purl('https://hello.org?g=gamma&d=dee')
    url.add_query({'a': False, 'c': True})
    assert str(url) == 'https://hello.org?a=false&c=true&d=dee&g=gamma'

  def test_delete_query(self):
    url = Purl('http://blank.com')
    url.delete_query('bat');
    assert str(url) == 'http://blank.com'

    url = Purl('http://blank.com?')
    url.delete_query('bat');
    assert str(url) == 'http://blank.com'

    url = Purl('http://blank.com?')
    url.add_query('bat', 'man').delete_query('bat');
    assert str(url) == 'http://blank.com'

    url = Purl('http://blank.com?bat=man')
    url.delete_query('bat');
    assert str(url) == 'http://blank.com'

    url = Purl('http://blank.com?man=nam&bat=man')
    assert str(url.delete_query('man')) == 'http://blank.com?bat=man';
    assert str(url) == 'http://blank.com?bat=man'

    url = Purl('http://blank.com?man=nam&bat=man')
    assert str(
      url.delete_query('man')
        .delete_query('man')
        .delete_query('bat')
      ) == 'http://blank.com';
    assert str(url) == 'http://blank.com'

    url = Purl('http://blank.com?man=nam&bat=man')
    assert str(url.delete_query(['man', 'bat'])) == 'http://blank.com';
    assert str(url) == 'http://blank.com'
