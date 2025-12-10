FAQ
=======

*Q: Why do I get "Timestamp for this request is not valid"*

*A*: This occurs in 2 different cases.

The timestamp sent is outside of the serverTime - recvWindow value
The timestamp sent is more than 1000ms ahead of the server time

Check that your system time is in sync. See `this issue <https://github.com/sammchardy/python-binance/issues/2#issuecomment-324878152>`_ for some sample code to check the difference between your local
time and the Binance server time.

*Q: Why do I get "Signature for this request is not valid"*

*A1*: One of your parameters may not be in the correct format.

Check recvWindow is an integer and not a string.

*A2*: You may need to regenerate your API Key and Secret

*A3*: You may be attempting to access the API from a Chinese IP address, these are now restricted by Binance.

*Q: How can I debug API issues?*

*A*: Enable verbose mode to see detailed request and response information:

.. code:: python

    client = Client(api_key, api_secret, verbose=True)

This will log all HTTP requests and responses, including headers, body, and status codes. This is particularly helpful for debugging authentication issues, understanding API behavior, and troubleshooting network problems.

See the Logging section in the `Getting Started guide <overview.html#verbose-mode>`_ for more details.
