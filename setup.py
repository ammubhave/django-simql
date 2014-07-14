#!/usr/bin/env python

import os
from django_simql import metadata

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-simql',
    version=metadata.__version__,
    license=metadata.__license__,
    maintainer=metadata.__maintainer__,
    maintainer_email=metadata.__maintainer_email__,
    description="SimQL database extensions for Django.",
    url='https://github.com/ammubhave/django-simql',
    packages=[
        'django_simql',
        'django_simql.db',
        'django_simql.auth',
        'simmons_db',
        'simmons_db.models',
    ],
    install_requires=[
        "djangotoolbox==1.6.2",
    ],
)
