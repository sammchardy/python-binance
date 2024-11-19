import pytest
import requests_mock

pytestmark = pytest.mark.gift_card


def test_mock_gift_card_fetch_token_limit(liveClient):
    """Test gift card token limit endpoint with mocked response"""
    expected_response = {
        "code": "000000",
        "message": "success",
        "data": [{"coin": "BNB", "fromMin": "0.01", "fromMax": "1"}],
        "success": True,
    }

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/sapi/v1/giftcard/buyCode/token-limit",
            json=expected_response,
        )

        response = liveClient.gift_card_fetch_token_limit(baseToken="BUSD")
        assert response == expected_response


def test_gift_card_fetch_token_limit(liveClient):
    liveClient.gift_card_fetch_token_limit(baseToken="BUSD")


def test_gift_card_fetch_rsa_public_key(liveClient):
    liveClient.gift_card_fetch_rsa_public_key()


def test_gift_card_create_verify_and_redeem(liveClient):
    # create a gift card
    response = liveClient.gift_card_create(token="USDT", amount=1.0)
    assert response["data"]["referenceNo"] is not None
    assert response["data"]["code"] is not None
    # verify the gift card
    response = liveClient.gift_card_verify(referenceNo=response["data"]["referenceNo"])
    assert response["data"]["valid"] == "SUCCESS"
    # redeem the gift card
    redeem_response = liveClient.gift_card_redeem(
        code=response["data"]["code"],
    )
    assert response["data"]["referenceNo"] == redeem_response["data"]["referenceNo"]


def test_gift_card_create_dual_token_and_redeem(liveClient):
    response = liveClient.gift_card_create_dual_token(
        baseToken="USDT", faceToken="BNB", baseTokenAmount=1.0
    )
    assert response["data"]["referenceNo"] is not None
    assert response["data"]["code"] is not None
    # verify the gift card
    response = liveClient.gift_card_verify(referenceNo=response["data"]["referenceNo"])
    assert response["data"]["valid"] == "SUCCESS"
    # redeem the gift card
    redeem_response = liveClient.gift_card_redeem(
        code=response["data"]["code"],
    )
    assert response["data"]["referenceNo"] == redeem_response["data"]["referenceNo"]
