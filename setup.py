#!/usr/bin/env python
import codecs
import os
import re

from setuptools import setup

with codecs.open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "binance", "__init__.py"),
    "r",
    "latin1",
) as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[0]
    except IndexError as err:
        raise RuntimeError("Unable to determine version.") from err

with open("README.rst") as fh:
    long_description = fh.read()

setup(
    name="python-binance",
    version=version,
    packages=["binance"],
    description="Binance REST API python implementation",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sammchardy/python-binance",
    author="Sam McHardy",
    license="MIT",
    author_email="",
    install_requires=[
        "requests",
        "six",
        "dateparser",
        "aiohttp",
        "ujson",
        "websockets",
        "pycryptodome",
    ],
    keywords="binance exchange rest api bitcoin ethereum btc eth neo",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
