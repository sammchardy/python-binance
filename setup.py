#!/usr/bin/env python

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'PYPIREADME.rst')).read()

setup(
    name='python-binance',
    version='0.1.0',
    packages=['binance'],
    description='Binance API python implementation',
    url='https://github.com/sammchardy/python-binance',
    author='Sam McHardy',
    license='MIT',
    author_email='',
    install_requires=['requests', 'six', 'Twisted', 'pyOpenSSL', 'autobahn', 'service-identity'],
    keywords='binance exchange bitcoin ethereum btc eth neo',
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
