import pytest

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
    assert url.protocol == 'sftp://'
    assert url.hostname == 'secure-site'
    assert url.port     == ':123'
    assert url.path     == None

    url = Purl('http://nada.com')
    assert url.protocol == 'http://'
    assert url.hostname == 'nada.com'
    assert url.port     == None
    assert url.path     == None

    url = Purl('file://filesys/somefile.png')
    assert url.protocol == 'file://'
    assert url.hostname == 'filesys'
    assert url.port     == None
    assert url.path     == '/somefile.png'
