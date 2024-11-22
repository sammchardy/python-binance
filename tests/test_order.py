def assert_contract_order(client, order):
    assert isinstance(order, dict)

    assert order["clientOrderId"].startswith(client.CONTRACT_ORDER_PREFIX)
    assert order["symbol"]
