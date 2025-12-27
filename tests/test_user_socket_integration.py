"""
Integration tests for user socket with ws_api subscription routing.

These tests verify that the user socket correctly:
1. Uses ws_api for subscription (not creating its own connection)
2. Has its own queue for receiving events (not sharing ws_api's queue)
3. Does not start its own read loop (ws_api handles reading)
4. Properly cleans up subscriptions on exit

Requirements:
- Binance testnet API credentials (configured in conftest.py)
- Network connectivity to testnet

Run with: pytest tests/test_user_socket_integration.py -v
"""
import asyncio
import pytest
import pytest_asyncio

from binance import BinanceSocketManager


@pytest_asyncio.fixture
async def socket_manager(clientAsync):
    """Create a BinanceSocketManager using the clientAsync fixture from conftest."""
    return BinanceSocketManager(clientAsync)


class TestUserSocketArchitecture:
    """Tests verifying the user socket architecture is correct."""

    @pytest.mark.asyncio
    async def test_user_socket_has_separate_queue(self, clientAsync, socket_manager):
        """User socket should have its own queue, not share ws_api's queue."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            # Queues should be different objects
            assert user_socket._queue is not clientAsync.ws_api._queue, \
                "user_socket should have its own queue, not share ws_api's queue"

    @pytest.mark.asyncio
    async def test_user_socket_uses_ws_api_subscription(self, clientAsync, socket_manager):
        """User socket should use ws_api subscription mechanism."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            # Should be marked as using ws_api subscription
            assert user_socket._uses_ws_api_subscription is True, \
                "user_socket should be marked as using ws_api subscription"

            # Should have a subscription ID
            assert user_socket._subscription_id is not None, \
                "user_socket should have a subscription ID"

    @pytest.mark.asyncio
    async def test_user_socket_no_read_loop(self, clientAsync, socket_manager):
        """User socket should NOT have its own read loop (ws_api handles reading)."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            # user_socket should not have started its own read loop
            assert user_socket._handle_read_loop is None, \
                "user_socket should not have its own read loop"

            # ws_api should have a read loop
            assert clientAsync.ws_api._handle_read_loop is not None, \
                "ws_api should have a read loop"

    @pytest.mark.asyncio
    async def test_user_socket_queue_registered_with_ws_api(self, clientAsync, socket_manager):
        """User socket's queue should be registered with ws_api for event routing."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            sub_id = user_socket._subscription_id

            # Subscription should be registered in ws_api
            assert sub_id in clientAsync.ws_api._subscription_queues, \
                "Subscription should be registered with ws_api"

            # Registered queue should be user_socket's queue
            registered_queue = clientAsync.ws_api._subscription_queues[sub_id]
            assert registered_queue is user_socket._queue, \
                "Registered queue should be user_socket's queue"

    @pytest.mark.asyncio
    async def test_user_socket_cleanup_on_exit(self, clientAsync, socket_manager):
        """User socket should unregister from ws_api on exit."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            sub_id = user_socket._subscription_id
            # Verify it's registered while connected
            assert sub_id in clientAsync.ws_api._subscription_queues

        # After exit, subscription should be unregistered
        assert sub_id not in clientAsync.ws_api._subscription_queues, \
            "Subscription should be unregistered after exit"


class TestUserSocketFunctionality:
    """Tests verifying user socket functionality works correctly."""

    @pytest.mark.asyncio
    async def test_user_socket_recv_timeout(self, clientAsync, socket_manager):
        """User socket recv() should timeout gracefully when no events."""
        user_socket = socket_manager.user_socket()

        async with user_socket:
            # recv() should timeout without errors (no events on quiet account)
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(user_socket.recv(), timeout=2)

    @pytest.mark.asyncio
    async def test_user_socket_context_manager(self, clientAsync, socket_manager):
        """User socket should work as async context manager."""
        user_socket = socket_manager.user_socket()

        # Should not be connected initially
        assert user_socket._subscription_id is None

        async with user_socket:
            # Should be connected inside context
            assert user_socket._subscription_id is not None
            assert user_socket._uses_ws_api_subscription is True

        # Subscription ID is cleared after unsubscribe
        assert user_socket._subscription_id is None


class TestNonUserSockets:
    """Tests verifying other socket types still work normally."""

    @pytest.mark.asyncio
    async def test_margin_socket_not_using_ws_api_subscription(self, clientAsync, socket_manager):
        """Non-user KeepAliveWebsockets (like margin socket) should not use ws_api subscription."""
        # margin_socket is a KeepAliveWebsocket with keepalive_type="margin"
        # Create it but don't connect - just check the flag
        margin_socket = socket_manager.margin_socket()

        # Before connecting, the flag should be False (default)
        assert margin_socket._uses_ws_api_subscription is False, \
            "Margin socket should not use ws_api subscription"

        # The _keepalive_type should be "margin", not "user"
        assert margin_socket._keepalive_type == "margin"


class TestWsApiSubscriptionRouting:
    """Tests verifying ws_api correctly routes subscription events."""

    @pytest.mark.asyncio
    async def test_ws_api_has_subscription_queues(self, clientAsync):
        """ws_api should have subscription queues dict."""
        # Ensure ws_api is initialized
        await clientAsync.ws_api._ensure_ws_connection()

        assert hasattr(clientAsync.ws_api, '_subscription_queues'), \
            "ws_api should have _subscription_queues attribute"
        assert isinstance(clientAsync.ws_api._subscription_queues, dict), \
            "_subscription_queues should be a dict"

    @pytest.mark.asyncio
    async def test_ws_api_register_unregister_queue(self, clientAsync):
        """ws_api should be able to register and unregister queues."""
        await clientAsync.ws_api._ensure_ws_connection()

        test_queue = asyncio.Queue()
        test_sub_id = "test_subscription_123"

        # Register
        clientAsync.ws_api.register_subscription_queue(test_sub_id, test_queue)
        assert test_sub_id in clientAsync.ws_api._subscription_queues
        assert clientAsync.ws_api._subscription_queues[test_sub_id] is test_queue

        # Unregister
        clientAsync.ws_api.unregister_subscription_queue(test_sub_id)
        assert test_sub_id not in clientAsync.ws_api._subscription_queues

    @pytest.mark.asyncio
    async def test_ws_api_unregister_nonexistent_is_safe(self, clientAsync):
        """Unregistering a non-existent subscription should not raise."""
        await clientAsync.ws_api._ensure_ws_connection()

        # Should not raise
        clientAsync.ws_api.unregister_subscription_queue("nonexistent_sub_id")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
