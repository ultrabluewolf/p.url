# P.url

P.url is a simple url parsing library for python. Currently, you can modify querystrings for given urls by adding or deleting. Chaining is supported!

## Usage

### Add/update query

```py
from purl import Purl

url = Purl('https://github.com/search?q=cat)

str(url.add_query('q', 'dog')) # => 'https://github.com/search?q=dog'
```

```py
url = Purl('https://github.com/search)

str(url.add_query({
  'q': 'cat',
  'l': 'JavaScript',
  'type': 'Issues'
}))

url = Purl('https://github.com/search)

str(url.add_query('q', 'cat')
  .add_query('l', 'JavaScript')
  .add_query('type', 'Issues')) # => 'https://github.com/search?l=JavaScript&q=cat&type=Issues'

```

### Delete query

```py
from purl import Purl

url = Purl('https://github.com/search?q=cat)

str(url.delete_query('q')) # => 'https://github.com/search'
```

```py
url = Purl('https://github.com/search?l=JavaScript&q=cat&type=Issues')

str(url.delete_query(['q', 'type'])) # => https://github.com/search?l=JavaScript

url = Purl('https://github.com/search?l=JavaScript&q=cat&type=Issues')
str(url.delete_query('q')
  .delete_query('type')) # => 'https://github.com/search?l=JavaScript'

```
