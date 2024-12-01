from enum import Enum

KEEPALIVE_TIMEOUT = 5 * 60  # 5 minutes


class WSListenerState(Enum):
    INITIALISING = "Initialising"
    STREAMING = "Streaming"
    RECONNECTING = "Reconnecting"
    EXITING = "Exiting"
