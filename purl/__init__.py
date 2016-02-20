import re
from builtins import object
from . import exceptions

class Purl(object):

  def __init__(self, url):
    super(Purl, self).__init__()

    split_url     = url.split('?')
    baseurl_split = split_url[0].split('://')

    # protocol and host are required
    if len(baseurl_split) != 2:
      raise exceptions.InvalidUrlError

    host_port_split = baseurl_split[1].split(':')

    self.protocol = baseurl_split[0] + '://'
    self.hostname = host_port_split[0]
    self.port     = None
    self.path     = None

    # port + (path)
    if len(host_port_split) == 2:
      port_path = self.__split_once(host_port_split[1], '/')
      self.port = ':' + port_path[0]
      if len(port_path) == 2:
        self.path = port_path[1]

      # check port format
      if not re.match(r':\d+', self.port):
        raise exceptions.InvalidUrlError

    # hostname + (path)
    else:
      hostname_path = self.__split_once(host_port_split[0], '/')
      if len(hostname_path) == 2:
        self.hostname = hostname_path[0]
        self.path     = hostname_path[1]

    if len(self.hostname) < 1:
      raise purl_exc.InvalidUrlError

    # (query)
    try:
      self.query = self.__parse_querystring(split_url[1])
    except IndexError:
      self.query = {}

  ## url splitting helper
  def __split_once(self, s, target):
    idx = s.find(target)
    if idx >= 0:
      result = []
      result.append(s[:idx])
      result.append(s[idx:])
      return result
    else:
      return [s]

    if len(result) < 1:
      result = None
    elif len(result) == 1:
      result = result[0]
    return result

  ## update query
  def add_query(self, query, value=None):
    if value is None:
      for k in query:
        self.query[k] = query[k]
    else:
      self.query[query] = value
    return self

  ## delete keys from query
  def delete_query(self, query):
    if isinstance(query, list):
      for k in query:
        self.__del_dict(self.query, k)
    else:
      self.__del_dict(self.query, query)
    return self

  ## delete query helper
  def __del_dict(self, d, k):
    try:
      del d[k]
    except KeyError:
      pass

  ## generate querystring
  def querystring(self):
    qs = ''
    for k in self.query:
      k = self.__encode_string(k)
      v = self.__encode_string(self.query[k])
      qs += k + '=' + v + '&'
    # remove trailing ampersand
    if self.query:
      qs = qs[:-1]
    return qs

  ## convert querystring into a dict
  def __parse_querystring(self, qs):
    query = {}
    split_qs = qs.split('&')
    for qs_pair in split_qs:
      qs_pair = qs_pair.split('=')
      if len(qs_pair) == 2:
        query[qs_pair[0]] = qs_pair[1]
    return query

  ## encode/decode stubs
  def __encode_string(self, s):
    if isinstance(s, bool):
      if s == True:
        s = 'true'
      elif s == False:
        s = 'false'
    s = str(s)

    return s

  def __decode_string(self, s):
    if s == 'true':
      s = True
    elif s == 'false':
      s = False

    return s

  ## generate url string
  def __str__(self):
    url = self.protocol + self.hostname
    qs  = self.querystring()

    if self.port:
      url += self.port
    if self.path:
      url += self.path

    if qs:
      url += '?' + qs
    return url

  def __repr__(self):
    s = '<Purl: url="' + str(self) + '">'
    return s  
