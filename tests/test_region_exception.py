"""Tests for BinanceRegionException and region validation."""

import pytest
from binance.client import Client
from binance.async_client import AsyncClient
from binance.exceptions import BinanceRegionException


class TestBinanceRegionException:
    """Tests for the BinanceRegionException class itself."""

    def test_exception_attributes(self):
        """Test that exception has correct attributes."""
        exc = BinanceRegionException("us", "com", "test_endpoint")
        assert exc.required_tld == "us"
        assert exc.actual_tld == "com"
        assert exc.endpoint_name == "test_endpoint"

    def test_exception_message_format(self):
        """Test that exception message is properly formatted."""
        exc = BinanceRegionException("us", "com", "get_staking_asset_us")
        assert "binance.us" in str(exc)
        assert "binance.com" in str(exc)
        assert "get_staking_asset_us" in str(exc)

    def test_exception_default_endpoint_name(self):
        """Test that endpoint_name defaults to 'endpoint'."""
        exc = BinanceRegionException("us", "com")
        assert exc.endpoint_name == "endpoint"
        assert "endpoint is only available" in str(exc)


class TestSyncClientRegionValidation:
    """Tests for region validation in synchronous Client."""

    def test_get_staking_asset_us_wrong_tld(self):
        """Test that get_staking_asset_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.get_staking_asset_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.actual_tld == "com"
        assert exc_info.value.endpoint_name == "get_staking_asset_us"

    def test_stake_asset_us_wrong_tld(self):
        """Test that stake_asset_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.stake_asset_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.endpoint_name == "stake_asset_us"

    def test_unstake_asset_us_wrong_tld(self):
        """Test that unstake_asset_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.unstake_asset_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.endpoint_name == "unstake_asset_us"

    def test_get_staking_balance_us_wrong_tld(self):
        """Test that get_staking_balance_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.get_staking_balance_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.endpoint_name == "get_staking_balance_us"

    def test_get_staking_history_us_wrong_tld(self):
        """Test that get_staking_history_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.get_staking_history_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.endpoint_name == "get_staking_history_us"

    def test_get_staking_rewards_history_us_wrong_tld(self):
        """Test that get_staking_rewards_history_us raises exception for non-US client."""
        client = Client("test_key", "test_secret", tld="com", ping=False)
        with pytest.raises(BinanceRegionException) as exc_info:
            client.get_staking_rewards_history_us()
        assert exc_info.value.required_tld == "us"
        assert exc_info.value.endpoint_name == "get_staking_rewards_history_us"


@pytest.mark.asyncio
class TestAsyncClientRegionValidation:
    """Tests for region validation in asynchronous AsyncClient."""

    async def test_get_staking_asset_us_wrong_tld_async(self):
        """Test that async get_staking_asset_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.get_staking_asset_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.actual_tld == "com"
            assert exc_info.value.endpoint_name == "get_staking_asset_us"
        finally:
            await client.close_connection()

    async def test_stake_asset_us_wrong_tld_async(self):
        """Test that async stake_asset_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.stake_asset_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.endpoint_name == "stake_asset_us"
        finally:
            await client.close_connection()

    async def test_unstake_asset_us_wrong_tld_async(self):
        """Test that async unstake_asset_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.unstake_asset_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.endpoint_name == "unstake_asset_us"
        finally:
            await client.close_connection()

    async def test_get_staking_balance_us_wrong_tld_async(self):
        """Test that async get_staking_balance_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.get_staking_balance_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.endpoint_name == "get_staking_balance_us"
        finally:
            await client.close_connection()

    async def test_get_staking_history_us_wrong_tld_async(self):
        """Test that async get_staking_history_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.get_staking_history_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.endpoint_name == "get_staking_history_us"
        finally:
            await client.close_connection()

    async def test_get_staking_rewards_history_us_wrong_tld_async(self):
        """Test that async get_staking_rewards_history_us raises exception for non-US client."""
        client = AsyncClient("test_key", "test_secret", tld="com")
        try:
            with pytest.raises(BinanceRegionException) as exc_info:
                await client.get_staking_rewards_history_us()
            assert exc_info.value.required_tld == "us"
            assert exc_info.value.endpoint_name == "get_staking_rewards_history_us"
        finally:
            await client.close_connection()
