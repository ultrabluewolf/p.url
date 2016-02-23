# P.url

P.url is a simple url parsing library for python. Currently, you can modify querystrings for given urls by adding or deleting. Chaining is supported!

## Usage

### Add/update query

```py
from purl import Purl

url = Purl('https://github.com/search?q=cat')

str(url.add_query('q', 'dog')) # => 'https://github.com/search?q=dog'
```

```py
url = Purl('https://github.com/search')

str(url.add_query({
  'q': 'cat',
  'l': 'JavaScript',
  'type': 'Issues'
}))

# or

url = Purl('https://github.com/search')

str(url.add_query('q', 'cat')
  .add_query('l', 'JavaScript')
  .add_query('type', 'Issues')) # => 'https://github.com/search?l=JavaScript&q=cat&type=Issues'

```

### Delete query

```py
from purl import Purl

url = Purl('https://github.com/search?q=cat')

str(url.delete_query('q')) # => 'https://github.com/search'
```

```py
url = Purl('https://github.com/search?l=JavaScript&q=cat&type=Issues')

str(url.delete_query(['q', 'type'])) # => https://github.com/search?l=JavaScript

# or

url = Purl('https://github.com/search?l=JavaScript&q=cat&type=Issues')
str(url.delete_query('q')
  .delete_query('type')) # => 'https://github.com/search?l=JavaScript'

```

### Params

```py
url = ( Purl('https://some.public.api.com')
  .path('/:resource/:id/:action')
  .param('resource', 'user').param('id', 12).param('action', 'favorites')
)
str(url)

# or

url = ( Purl('https://some.public.api.com')
  .path('/:resource/:id/:action')
  .param({
    'resource': 'user',
    'id': 12,
    'action': 'favorites'
  })
)
str(url) # => 'https://some.public.api.com/user/12/favorites'
```

## Running the tests

make sure you have py test installed

`pip install pytest`

Then run:

`py.test`
