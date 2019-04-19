#!/usr/bin/env python
# coding=utf-8

from binance.client import Client


def test_get_sub_account_list(mocker):
    """Test get_sub_account_list."""

    # Arrange
    client = Client('fake_api_key', 'fake_api_secret')
    client._request_withdraw_api = mocker.MagicMock()
    # Action
    client.get_sub_account_list()
    # Assert
    client._request_withdraw_api.assert_called_with('get', 'sub-account/list.html', True, data={})


def test_get_sub_account_transfer_history():
    """Test get_sub_account_transfer_history."""

    def mock_func(method, path, flag, data):
        assert data['email'] == fake_email
        assert method == 'get'
        assert path == 'sub-account/transfer/history.html'
        assert flag

    # Arrange
    client = Client('fake_api_key', 'fake_api_secret')
    client._request_withdraw_api = mock_func
    fake_email = 'fake@fake.com'

    # Action
    client.get_sub_account_transfer_history(email=fake_email)
