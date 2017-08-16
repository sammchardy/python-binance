#!/usr/bin/env python

from setuptools import setup

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
    keywords='binance exchange bitcoin ethereum btc eth neo'
)
