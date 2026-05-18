try:
    import picows.websockets as websockets
    from picows.websockets import (
        ConnectionClosed, ConnectionClosedError, ConnectionClosedOK, State, WebSocketClientProtocol, protocol as ws_protocol
    )
    websockets_package_name = "picows.websockets"
except ImportError:
    import websockets
    from websockets import protocol as ws_protocol, WebSocketClientProtocol
    State = ws_protocol.State
    try:
        from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK  # type: ignore
    except ImportError:
        from websockets import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK  # type: ignore

    websockets_package_name = "websockets"