import sys, os, pytest
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from purl import Purl
from purl.exceptions import *

class TestParserFunctions(object):

  def test_simple_url(self):
    str_url = 'http://blank'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'https://blank'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'http://blank.com'
    url = Purl(str_url)
    assert str(url) == str_url

  def test_invalid_url(self):

    with pytest.raises(InvalidUrlError):
      Purl('bad')

    with pytest.raises(InvalidUrlError):
      Purl('bad.com/abc/def')

    with pytest.raises(InvalidUrlError):
      Purl('http://bad:xwy/one/2/three')

    with pytest.raises(InvalidUrlError):
      Purl('http://bad://?hello')

  def test_url_mirrors_valid_inputs(self):
    str_url = 'http://blank:1234'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'file://blank/path/to/file'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'https://blank.com/resource/1'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'http://blank.org:1234/resouce/1/other'
    url = Purl(str_url)
    assert str(url) == str_url

    str_url = 'file://blank.org:1234/file.txt'
    url = Purl(str_url)
    assert str(url) == str_url

  def test_fields(self):
    url = Purl('sftp://secure-site:123')
    assert url.protocol() == 'sftp://'
    assert url.hostname() == 'secure-site'
    assert url.port()     == ':123'
    assert url.path()     == None

    url = Purl('http://nada.com')
    assert url.protocol() == 'http://'
    assert url.hostname() == 'nada.com'
    assert url.port()     == None
    assert url.path()     == None

    url = Purl('file://filesys/somefile.png')
    assert url.protocol() == 'file://'
    assert url.hostname() == 'filesys'
    assert url.port()     == None
    assert url.path()     == '/somefile.png'

    expected = 'https://firehouse.com:3333/freedom'
    url = Purl('http://blank')
    assert str(url.protocol('https://')
      .hostname('firehouse.com')
      .path('/freedom')
      .port(':3333')) == expected
    assert str(url) == expected

  def test_invalid_fields(self):
    u = Purl('http://blank')

    with pytest.raises(InvalidUrlError):
      u.protocol('')
    with pytest.raises(InvalidUrlError):
      u.protocol('://')
    with pytest.raises(InvalidUrlError):
      u.protocol('abc')

    with pytest.raises(InvalidUrlError):
      u.hostname('')
    with pytest.raises(InvalidUrlError):
      u.hostname('abcd/123/546')
    with pytest.raises(InvalidUrlError):
      u.hostname('abcd:123')
    with pytest.raises(InvalidUrlError):
      u.hostname('abcd:abcd')

    with pytest.raises(InvalidUrlError):
      u.port('80')
    with pytest.raises(InvalidUrlError):
      u.port(':abcd')

    with pytest.raises(InvalidUrlError):
      u.path('abcd/123')
    with pytest.raises(InvalidUrlError):
      u.path('abcd/123/')


  def test_create_with(self):
    expected = Purl('file://blank')
    url = Purl.create_with({
      'protocol': 'file://',
      'hostname': 'blank'
    })
    assert(str(url) == str(expected))

    expected = Purl('https://blank:321/some/path')
    url = Purl.create_with({
      'protocol': 'https://',
      'hostname': 'blank',
      'port': ':321',
      'path': '/some/path'
    })
    assert(str(url) == str(expected))

    expected = Purl('https://blank:321/some/path?a=1&b=2&c=false')
    url = Purl.create_with({
      'protocol': 'https://',
      'hostname': 'blank',
      'port': ':321',
      'path': '/some/path?a=1&b=2&c=false'
    })
    assert(str(url) == str(expected))

    expected = Purl('http://somehost/some/path?a=1&b=2&c=false')
    url = Purl.create_with({
      'protocol': 'http://',
      'hostname': 'somehost',
      'path': '/some/path?a=1&b=2&c=false'
    })
    assert(str(url) == str(expected))

  def test_create_with_invalid_args(self):
    with pytest.raises(InvalidUrlError):
      Purl.create_with({})

    with pytest.raises(InvalidUrlError):
      Purl.create_with({
        'hostname': 'dne'
      })

    with pytest.raises(InvalidUrlError):
      Purl.create_with({
        'protocol': 'ssh',
        'hostname': 'bad'
      })

    with pytest.raises(InvalidUrlError):
      Purl.create_with({
        'protocol': 'ssh://',
        'hostname': 'bad',
        'port': ':abc'
      })

    with pytest.raises(InvalidUrlError):
      Purl.create_with({
        'protocol': 'ssh://',
        'hostname': 'bad',
        'port': '321'
      })
