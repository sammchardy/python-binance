from binance import (
    AsyncClient,
    Client,
    DepthCacheManager,
    OptionsDepthCacheManager,
    ThreadedDepthCacheManager,
    FuturesDepthCacheManager,
    BinanceSocketManager,
    ThreadedWebsocketManager,
    BinanceSocketType,
    KeepAliveWebsocket,
    ReconnectingWebsocket
)

def test_version():
    """Test that __version__ is defined"""
    from binance import __version__
    assert isinstance(__version__, str)
    assert __version__ is not None

def test_client_import():
    """Test Client class import"""
    assert Client is not None
    assert isinstance(Client, type)

def test_async_client_import():
    """Test AsyncClient class import"""
    assert AsyncClient is not None
    assert isinstance(AsyncClient, type)

def test_depth_cache_imports():
    """Test depth cache related imports"""
    assert DepthCacheManager is not None
    assert OptionsDepthCacheManager is not None
    assert ThreadedDepthCacheManager is not None
    assert FuturesDepthCacheManager is not None
    assert isinstance(DepthCacheManager, type)
    assert isinstance(OptionsDepthCacheManager, type)
    assert isinstance(ThreadedDepthCacheManager, type)
    assert isinstance(FuturesDepthCacheManager, type)

def test_websocket_imports():
    """Test websocket related imports"""
    assert BinanceSocketManager is not None
    assert ThreadedWebsocketManager is not None
    assert BinanceSocketType is not None
    assert isinstance(BinanceSocketManager, type)
    assert isinstance(ThreadedWebsocketManager, type)

def test_websocket_utility_imports():
    """Test websocket utility imports"""
    assert KeepAliveWebsocket is not None
    assert ReconnectingWebsocket is not None
    assert isinstance(KeepAliveWebsocket, type)
    assert isinstance(ReconnectingWebsocket, type)
