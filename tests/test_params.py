import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from purl import Purl

class TestParserFunctions(object):

  def test_simple_param(self):
    expected = 'http://blank/resource/41/nested-item' 
    str_url = 'http://blank/resource/:id/:resource'
    url = Purl(str_url).param({
      'resource': 'nested-item'
    }).param('id', 41)
    assert str(url) == expected

    expected = 'http://blank/resource/hello/nested-item'
    url.param('id', 'hello')
    assert str(url) == expected

  def test_param_empty(self):
    expected = 'https://site.edu/resource/72/five?ok=true'
    str_url  = 'https://site.edu/resource/72/five'
    url = Purl(str_url).param('dne', 0).add_query('ok', True)
    assert str(url) == expected

  def test_param_multi(self):
    expected = 'http://www.site.edu:123/web52/download/new?msg=world'
    str_url  = 'http://www.site.edu:123/:basepath/:action/:misc?msg=hello&there=true'
    url = Purl(str_url).param({
      'basepath': 'web52',
      'action': 'download',
      'misc': 'new'
    }).add_query('msg', 'world').delete_query('there')
    assert str(url) == expected

    expected = 'http://www.site.edu:123/web52/stream/p?msg=false'
    assert str(url.add_query('msg', False)
      .param('action', 'stream')
      .param('misc','p')) == expected
