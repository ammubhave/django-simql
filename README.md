django-simql
============

django-simql is a Django SimQL DB Backend. It communicates over the network and executes remote queries with it. It also takes care of token generation and processing for the queries.

SimQL is a SQL derivative but with more restricted features. Namely it does not support schema modification statements like CREATE, ALTER or DROP.

Settings
--------

You need to add the following to your settings.py:

```
INSTALLED_APPS = (
    '...',
    'django_simql.auth',
    '...',
)

DATABASES = {
    'default': {
        'ENGINE': 'django_simql.db',
        'URL': '<SimQL DB server hostname>',
        'QUERY_ENDPOINT': '/query',
        'TOKEN_ENDPOINT': '/auth',
        'APP_KEY': '<App Key>',
        'APP_SECRET': '<App Secret>',
    }
}

AUTH_USER_MODEL = 'django_simql.auth.models.User'

AUTHENTICATION_BACKENDS = ('django_simql.auth.backends.SimqlAuthBackend',)

MIDDLEWARE_CLASSES = (
    '...',
    'django_simql.auth.middleware.SimqlAuthMiddleware',
    '...',
)
```