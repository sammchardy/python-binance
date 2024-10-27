

def test_client_initialization(client):
    assert client.API_KEY == 'test_api_key'
    assert client.API_SECRET == 'test_api_secret'
    assert client.testnet == False
