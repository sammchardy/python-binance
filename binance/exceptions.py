# coding=utf-8
import json

ERROR_MESSAGES = {
    "invalid_json": "Invalid JSON error message from Binance: {}",
    "unknown_symbol": "Unknown symbol {}",
    "inactive_symbol": "Attempting to trade an inactive symbol {}",
    "min_amount": "Amount must be a multiple of {}",
    "min_price": "Price must be at least {}",
    "min_total": "Total must be at least {}",
    "not_implemented": "Not implemented: {}"
}

class BinanceAPIException(Exception):
    def __init__(self, response, status_code, text):
        self.code = 0
        try:
            json_res = json.loads(text)
        except ValueError:
            self.message = ERROR_MESSAGES["invalid_json"].format(response.text)
        else:
            self.code = json_res.get('code')
            self.message = json_res.get('msg')
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return f'APIError(code={self.code}): {self.message}'

class BinanceRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'BinanceRequestException: {self.message}'

class BinanceOrderException(Exception):
    def __init__(self, code, message_key, value=None):
        self.code = code
        self.message = ERROR_MESSAGES[message_key].format(value)

    def __str__(self):
        return f'BinanceOrderException(code={self.code}): {self.message}'

class BinanceOrderMinAmountException(BinanceOrderException):
    def __init__(self, value):
        super().__init__(-1013, "min_amount", value)

class BinanceOrderMinPriceException(BinanceOrderException):
    def __init__(self, value):
        super().__init__(-1013, "min_price", value)

class BinanceOrderMinTotalException(BinanceOrderException):
    def __init__(self, value):
        super().__init__(-1013, "min_total", value)

class BinanceOrderUnknownSymbolException(BinanceOrderException):
    def __init__(self, value):
        super().__init__(-1013, "unknown_symbol", value)

class BinanceOrderInactiveSymbolException(BinanceOrderException):
    def __init__(self, value):
        super().__init__(-1013, "inactive_symbol", value)

class BinanceWebsocketUnableToConnect(Exception):
    pass

class NotImplementedException(Exception):
    def __init__(self, value):
        super().__init__(ERROR_MESSAGES["not_implemented"].format(value))

class UnknownDateFormat(Exception):
    pass
