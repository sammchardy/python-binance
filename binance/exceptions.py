# coding=utf-8
import json


class BinanceAPIException(Exception):
    def __init__(self, response, status_code, text):
        self.code = 0
        try:
            json_res = json.loads(text)
        except ValueError:
            self.message = "Invalid JSON error message from Binance: {}".format(
                response.text
            )
        else:
            self.code = json_res.get("code")
            self.message = json_res.get("msg")
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):  # pragma: no cover
        return "APIError(code=%s): %s" % (self.code, self.message)


class BinanceRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "BinanceRequestException: %s" % self.message


class BinanceOrderException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "BinanceOrderException(code=%s): %s" % (self.code, self.message)


class BinanceOrderMinAmountException(BinanceOrderException):
    def __init__(self, value):
        message = "Amount must be a multiple of %s" % value
        super().__init__(-1013, message)


class BinanceOrderMinPriceException(BinanceOrderException):
    def __init__(self, value):
        message = "Price must be at least %s" % value
        super().__init__(-1013, message)


class BinanceOrderMinTotalException(BinanceOrderException):
    def __init__(self, value):
        message = "Total must be at least %s" % value
        super().__init__(-1013, message)


class BinanceOrderUnknownSymbolException(BinanceOrderException):
    def __init__(self, value):
        message = "Unknown symbol %s" % value
        super().__init__(-1013, message)


class BinanceOrderInactiveSymbolException(BinanceOrderException):
    def __init__(self, value):
        message = "Attempting to trade an inactive symbol %s" % value
        super().__init__(-1013, message)


class BinanceWebsocketUnableToConnect(Exception):
    pass


class BinanceWebsocketQueueOverflow(Exception):
    """Raised when the websocket message queue exceeds its maximum size."""
    pass

class BinanceWebsocketClosed(Exception):
    """Raised when websocket connection is closed."""
    pass

class ReadLoopClosed(Exception):
    """Raised when trying to read from read loop but already closed"""
    pass

class NotImplementedException(Exception):
    def __init__(self, value):
        message = f"Not implemented: {value}"
        super().__init__(message)


class UnknownDateFormat(Exception):
    ...


class BinanceRegionException(Exception):
    """Raised when using a region-specific endpoint with incompatible client."""

    def __init__(
        self, required_tld: str, actual_tld: str, endpoint_name: str = "endpoint"
    ):
        self.required_tld = required_tld
        self.actual_tld = actual_tld
        self.endpoint_name = endpoint_name
        self.message = (
            f"{endpoint_name} is only available on binance.{required_tld}, "
            f"but client is configured for binance.{actual_tld}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"BinanceRegionException: {self.message}"
