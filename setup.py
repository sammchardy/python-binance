#!/usr/bin/env python
from setuptools import setup

setup(
    name="python-binance-async",
    version="0.7.2",
    packages=["binance"],
    description="Binance REST API python implementation that using asyncio",
    url="https://github.com/gbozee/python-binance-async",
    author="Sam McHardy / Biola Oyeniyi",
    license="MIT",
    author_email="",
    install_requires=["requests_async", "dateparser","twisted","autobahn"],
    keywords="binance exchange rest api bitcoin ethereum btc eth neo",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
