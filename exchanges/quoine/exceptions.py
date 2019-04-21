#!/usr/bin/env python
# coding=utf-8


class QuoineAPIException(Exception):
    """Exception class to handle general API Exceptions

        `code` values

        HTTP 400: Bad Request
            There was an error with the request. The body of the response will have more info

        HTTP 401: Unauthorized
            Token is invalid. If your API key is wrong a 401 will also be served,
            so check the response body, it might be that the API_KEY is invalid.

        HTTP 422: Unprocessable Entity
            There was an error with the request. The body of the response will have more info. Some possible reasons:
            - Missing params
            - The format of data is wrong

        HTTP 429: Too Many Requests
            This status indicates that the user has sent too many requests in a given amount of time

        HTTP 503: Service Unavailable
            Many reasons, body will include details
            - An internal error on Authy.
            - Your application is accessing an API call you don't have access too.
            - API usage limit. If you reach API usage limits a 503 will be returned,
            please wait until you can do the call again.

        `message` format

        .. code-block:: python

            {
                "user": ["not_enough_fund"]
            }

    """
    def __init__(self, response):
        try:
            json_res = response.json()
        except ValueError:
            self.messages = response.content
        else:
            if 'message' in json_res:
                self.messages = json_res
            elif 'errors' in json_res:
                self.messages = json_res['errors']

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'QuoineAPIException: {}'.format(self.messages)


class QuoineRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'QuoineRequestException: {}'.format(self.message)
