import re
from builtins import object, range
from . import exceptions

class Purl(object):

  def __init__(self, url):
    super(Purl, self).__init__()

    split_url     = url.split('?')
    baseurl_split = split_url[0].split('://')

    # protocol and host are required
    if len(baseurl_split) != 2:
      raise exceptions.InvalidUrlError

    host_port_split = Purl.__split_hostname_and_port(baseurl_split[1])

    self._protocol = baseurl_split[0] + '://'
    self._hostname = host_port_split[0]
    self._port     = None
    self._path     = None

    self._params = {}
    self.query    = None
    self._path_compiled = None

    # port + (path)
    if len(host_port_split) == 2:
      port_path = Purl.__split_once(host_port_split[1], '/')
      self._port = ':' + port_path[0]
      if len(port_path) == 2:
        self._path = port_path[1]

      # check port format
      if not Purl.__is_valid_port(self._port):
        raise exceptions.InvalidUrlError

    # hostname + (path)
    else:
      hostname_path = Purl.__split_once(host_port_split[0], '/')
      if len(hostname_path) == 2:
        self._hostname = hostname_path[0]
        self._path     = hostname_path[1]

    if len(self._hostname) < 1:
      raise purl_exc.InvalidUrlError

    # (query)
    try:
      self.query = Purl.__parse_querystring(split_url[1])
    except IndexError:
      self.query = {}

  @staticmethod
  def create_with(options):
    url = ''
    try:
      url = options['protocol'] + options['hostname']
    except KeyError:
      raise exceptions.InvalidUrlError

    if 'port' in options:
      if not Purl.__is_valid_port(options['port']):
        raise exceptions.InvalidUrlError
      url += options['port']
    if 'path' in options:
      url += options['path']

    return Purl(url)

  # check port format
  @staticmethod
  def __is_valid_port(port):
    return not not re.match(r':\d+', port)

  ## url splitting helper
  @staticmethod
  def __split_once(s, target):
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

  ## generate list containing hostname (and port if available)
  @staticmethod
  def __split_hostname_and_port(host_port):
    host_port_split = None
    host_port_match = re.search('[a-zA-Z](:)', host_port)
    if host_port_match:
      border = host_port_match.start(1)
      host_port_split = [
        host_port[0:border],
        host_port[border + 1:]
      ]
    else:
      host_port_split = [host_port]
    return host_port_split

  ## update query
  def add_query(self, query, value=None):
    if value is None:
      for k in query:
        self.add_query(k, query[k])
    else:
      self.query[query] = value
    return self

  ## delete keys from query
  def delete_query(self, query):
    if isinstance(query, list):
      for k in query:
        Purl.__del_dict(self.query, k)
    else:
      Purl.__del_dict(self.query, query)
    return self

  ## delete query helper
  @staticmethod
  def __del_dict(d, k):
    try:
      del d[k]
    except KeyError:
      pass

  ## update path params
  def param(self, param, value=None):
    if value is None:
      for k in param:
        self._params[k] = param[k]
    else:
      self._params[param] = value

    self._path_compiled = self.path_with_params()
    return self

  def path_with_params(self):
    split_path = self._path.split('/')

    for param in self._params:
      value = self._params[param]
      param = self.__to_param_key(param)

      for i in range(0, len(split_path)):
        if (param == split_path[i]):
          split_path[i] = Purl.__encode_string(value)

    path = '/'.join(split_path)
    return path

  def __to_param_key(self, param):
    return ':' + str(param)

  ## generate querystring
  def querystring(self):
    qs = ''
    for k in self.query:
      k = Purl.__encode_string(k)
      v = Purl.__encode_string(self.query[k])
      qs += k + '=' + v + '&'
    # remove trailing ampersand
    if self.query:
      qs = qs[:-1]
    return qs

  ## convert querystring into a dict
  @staticmethod
  def __parse_querystring(qs):
    query = {}
    split_qs = qs.split('&')
    for qs_pair in split_qs:
      qs_pair = qs_pair.split('=')
      if len(qs_pair) == 2:
        query[qs_pair[0]] = qs_pair[1]
    return query

  ## encode/decode stubs
  @staticmethod
  def __encode_string(s):
    if isinstance(s, bool):
      if s == True:
        s = 'true'
      elif s == False:
        s = 'false'
    s = str(s)

    return s

  @staticmethod
  def __decode_string(s):
    if s == 'true':
      s = True
    elif s == 'false':
      s = False

    return s

  ## generate url string
  def __str__(self):
    url = self._protocol + self._hostname
    qs  = self.querystring()

    if self._port:
      url += self._port
    if self._path:
      if self._path_compiled:
        url += self._path_compiled
      else:
        url += self._path

    if qs:
      url += '?' + qs
    return url

  def __repr__(self):
    s = '<Purl: url="' + str(self) + '">'
    return s  

  ## attribute getters and chainable setters

  def protocol(self, value=None):
    if value is None:
      return self._protocol
    else:
      self._protocol = value
      return self

  def hostname(self, value=None):
    if value is None:
      return self._hostname
    else:
      self._hostname = value
      return self

  def port(self, value=None):
    if value is None:
      return self._port
    else:
      self._port = value
      return self

  def path(self, value=None):
    if value is None:
      return self._path
    else:
      self._path = value
      return self
