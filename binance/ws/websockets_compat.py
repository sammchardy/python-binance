import re


def _check_picows_version():
    import picows

    match = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", picows.__version__)
    if not match:
        raise ImportError("picows>=2.1.0 is required")

    version = tuple(int(part or 0) for part in match.groups())

    MIN_PICOWS_VERSION = (2, 1, 0)
    if not version >= MIN_PICOWS_VERSION:
        raise ImportError("picows>=2.1.0 is required")


try:
    _check_picows_version()

    import picows.websockets as websockets
    from picows.websockets import (
        ConnectionClosed,
        ConnectionClosedError,
        ConnectionClosedOK,
        State,
        WebSocketClientProtocol,
        protocol as ws_protocol,
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
