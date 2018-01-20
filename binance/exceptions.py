# coding=utf-8


class APIException(Exception):

    LISTENKEY_NOT_EXIST = '-1125'

    def __init__(self, response):
        self.status_code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Binance: {}'.format(response.text)
        else:
            self.code = json_res['code']
            self.message = json_res['msg']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIError(code=%s): %s' % (self.code, self.message)


class RequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'RequestException: %s' % self.message


class OrderException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'OrderException(code=%s): %s' % (self.code, self.message)


class OrderMinAmountException(OrderException):

    def __init__(self, value):
        message = "Amount must be a multiple of %s" % value
        super(OrderMinAmountException, self).__init__(-1013, message)


class OrderMinPriceException(OrderException):

    def __init__(self, value):
        message = "Price must be at least %s" % value
        super(OrderMinPriceException, self).__init__(-1013, message)


class OrderMinTotalException(OrderException):

    def __init__(self, value):
        message = "Total must be at least %s" % value
        super(OrderMinTotalException, self).__init__(-1013, message)


class OrderUnknownSymbolException(OrderException):

    def __init__(self, value):
        message = "Unknown symbol %s" % value
        super(OrderUnknownSymbolException, self).__init__(-1013, message)


class OrderInactiveSymbolException(OrderException):

    def __init__(self, value):
        message = "Attempting to trade an inactive symbol %s" % value
        super(OrderInactiveSymbolException, self).__init__(-1013, message)


class WithdrawException(Exception):
    def __init__(self, message):
        if message == u'参数异常':
            message = 'Withdraw to this address through the website first'
        self.message = message

    def __str__(self):
        return 'WithdrawException: %s' % self.message
