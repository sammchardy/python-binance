import pytest

pytestmark = [pytest.mark.gift_card, pytest.mark.asyncio]


async def test_gift_card_fetch_token_limit(liveClientAsync):
    await liveClientAsync.gift_card_fetch_token_limit(baseToken="BUSD")


async def test_gift_card_fetch_rsa_public_key(liveClientAsync):
    await liveClientAsync.gift_card_fetch_rsa_public_key()


async def test_gift_card_create_verify_and_redeem(liveClientAsync):
    # create a gift card
    response = await liveClientAsync.gift_card_create(token="USDT", amount=1.0)
    assert response["data"]["referenceNo"] is not None
    assert response["data"]["code"] is not None
    # verify the gift card
    response = await liveClientAsync.gift_card_verify(
        referenceNo=response["data"]["referenceNo"]
    )
    assert response["data"]["valid"] == "SUCCESS"
    # redeem the gift card
    redeem_response = await liveClientAsync.gift_card_redeem(
        code=response["data"]["code"],
    )
    assert response["data"]["referenceNo"] == redeem_response["data"]["referenceNo"]


async def test_gift_card_create_dual_token_and_redeem(liveClientAsync):
    response = await liveClientAsync.gift_card_create_dual_token(
        baseToken="USDT", faceToken="BNB", baseTokenAmount=1.0
    )
    assert response["data"]["referenceNo"] is not None
    assert response["data"]["code"] is not None
    # verify the gift card
    response = await liveClientAsync.gift_card_verify(
        referenceNo=response["data"]["referenceNo"]
    )
    assert response["data"]["valid"] == "SUCCESS"
    # redeem the gift card
    redeem_response = await liveClientAsync.gift_card_redeem(
        code=response["data"]["code"],
    )
    assert response["data"]["referenceNo"] == redeem_response["data"]["referenceNo"]
