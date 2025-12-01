"""Tests for verbose mode functionality"""

import pytest
import logging
from binance.client import Client
from binance.async_client import AsyncClient


def test_client_verbose_initialization():
    """Test that Client can be initialized with verbose mode"""
    client = Client(verbose=True, ping=False)
    assert client.verbose is True
    assert client.logger is not None
    assert client.logger.level == logging.DEBUG


def test_client_non_verbose_initialization():
    """Test that Client defaults to non-verbose mode"""
    client = Client(verbose=False, ping=False)
    assert client.verbose is False
    assert client.logger is not None
    # When verbose=False, we don't set the logger level (respects external config)


def test_client_default_verbose():
    """Test that Client defaults to verbose=False"""
    client = Client(ping=False)
    assert client.verbose is False


@pytest.mark.asyncio()
async def test_async_client_verbose_initialization():
    """Test that AsyncClient can be initialized with verbose mode"""
    client = AsyncClient(verbose=True)
    assert client.verbose is True
    assert client.logger is not None
    assert client.logger.level == logging.DEBUG
    await client.close_connection()


@pytest.mark.asyncio()
async def test_async_client_non_verbose_initialization():
    """Test that AsyncClient defaults to non-verbose mode"""
    client = AsyncClient(verbose=False)
    assert client.verbose is False
    assert client.logger is not None
    # When verbose=False, we don't set the logger level (respects external config)
    await client.close_connection()


@pytest.mark.asyncio()
async def test_async_client_default_verbose():
    """Test that AsyncClient defaults to verbose=False"""
    client = AsyncClient()
    assert client.verbose is False
    await client.close_connection()
