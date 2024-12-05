import pytest


pytestmark = pytest.mark.margin


def test_margin__get_account_status(client):
    client.get_account_status()


def test_margin_get_account_api_trading_status(client):
    client.get_account_api_trading_status()


def test_margin_get_account_api_permissions(client):
    client.get_account_api_permissions()


def test_margin_get_dust_assets(client):
    client.get_dust_assets()


def test_margin_get_dust_log(client):
    client.test_get_dust_log()


def test_margin_transfer_dust(client):
    client.transfer_dust()


def test_margin_get_asset_dividend_history(client):
    client.get_asset_dividend_history()


def test_margin_make_universal_transfer(client):
    client.make_universal_transfer()


def test_margin_query_universal_transfer_history(client):
    client.query_universal_transfer_history()


def test_margin_get_trade_fee(client):
    client.get_trade_fee()


def test_margin_get_asset_details(client):
    client.get_asset_details()


def test_margin_get_spot_delist_schedule(client):
    client.get_spot_delist_schedule()


# Withdraw Endpoints


def test_margin_withdraw(client):
    client.withdraw()


def test_margin_get_deposit_history(client):
    client.get_deposit_history()


def test_margin_get_withdraw_history(client):
    client.get_withdraw_history()


def test_margin_get_withdraw_history_id(client):
    client.get_withdraw_history_id()


def test_margin_get_deposit_address(client):
    client.get_deposit_address()


# Margin Trading Endpoints


def test_margin_get_margin_account(client):
    client.get_margin_account()


def test_margin_get_isolated_margin_account(client):
    client.get_isolated_margin_account()


def test_margin_enable_isolated_margin_account(client):
    client.enable_isolated_margin_account()


def test_margin_disable_isolated_margin_account(client):
    client.disable_isolated_margin_account()


def test_margin_get_enabled_isolated_margin_account_limit(client):
    client.get_enabled_isolated_margin_account_limit()


def test_margin_get_margin_dustlog(client):
    client.get_margin_dustlog()


def test_margin_get_margin_dust_assets(client):
    client.get_margin_dust_assets()


def test_margin_transfer_margin_dust(client):
    client.transfer_margin_dust()


def test_margin_get_cross_margin_collateral_ratio(client):
    client.get_cross_margin_collateral_ratio()


def test_margin_get_small_liability_exchange_assets(client):
    client.get_small_liability_exchange_assets()


def test_margin_exchange_small_liability_assets(client):
    client.exchange_small_liability_assets()


def test_margin_get_small_liability_exchange_history(client):
    client.get_small_liability_exchange_history()


def test_margin_get_future_hourly_interest_rate(client):
    client.get_future_hourly_interest_rate()


def test_margin_get_margin_capital_flow(client):
    client.get_margin_capital_flow()


def test_margin_get_margin_asset(client):
    client.get_margin_asset()


def test_margin_get_margin_symbol(client):
    client.get_margin_symbol()


def test_margin_get_margin_all_assets(client):
    client.get_margin_all_assets()


def test_margin_get_margin_all_pairs(client):
    client.get_margin_all_pairs()


def test_margin_create_isolated_margin_account(client):
    client.create_isolated_margin_account()


def test_margin_get_isolated_margin_symbol(client):
    client.get_isolated_margin_symbol()


def test_margin_get_all_isolated_margin_symbols(client):
    client.get_all_isolated_margin_symbols()


def test_margin_get_isolated_margin_fee_data(client):
    client.get_isolated_margin_fee_data()


def test_margin_get_isolated_margin_tier_data(client):
    client.get_isolated_margin_tier_data()


def test_margin_margin_manual_liquidation(client):
    client.margin_manual_liquidation()


def test_margin_toggle_bnb_burn_spot_margin(client):
    client.toggle_bnb_burn_spot_margin()


def test_margin_get_bnb_burn_spot_margin(client):
    client.get_bnb_burn_spot_margin()


def test_margin_get_margin_price_index(client):
    client.get_margin_price_index()


def test_margin_transfer_margin_to_spot(client):
    client.transfer_margin_to_spot()


def test_margin_transfer_spot_to_margin(client):
    client.transfer_spot_to_margin()


def test_margin_transfer_isolated_margin_to_spot(client):
    client.transfer_isolated_margin_to_spot()


def test_margin_transfer_spot_to_isolated_margin(client):
    client.transfer_spot_to_isolated_margin()


def test_margin_get_isolated_margin_tranfer_history(client):
    client.get_isolated_margin_tranfer_history()


def test_margin_create_margin_loan(client):
    client.create_margin_loan()


def test_margin_repay_margin_loan(client):
    client.repay_margin_loan()


def create_margin_ordertest_(client):
    client.create_margin_order()


def test_margin_cancel_margin_order(client):
    client.cancel_margin_order()


def test_margin_set_margin_max_leverage(client):
    client.set_margin_max_leverage()


def test_margin_get_margin_transfer_history(client):
    client.get_margin_transfer_history()


def test_margin_get_margin_loan_details(client):
    client.get_margin_loan_details()


def test_margin_get_margin_repay_details(client):
    client.get_margin_repay_details()


def test_margin_get_cross_margin_data(client):
    client.get_cross_margin_data()


def test_margin_get_margin_interest_history(client):
    client.get_margin_interest_history()


def test_margin_get_margin_force_liquidation_rec(client):
    client.get_margin_force_liquidation_rec()


def test_margin_get_margin_order(client):
    client.get_margin_order()


def test_margin_get_open_margin_orders(client):
    client.get_open_margin_orders()


def test_margin_get_all_margin_orders(client):
    client.get_all_margin_orders()


def test_margin_get_margin_trades(client):
    client.get_margin_trades()


def test_margin_get_max_margin_loan(client):
    client.get_max_margin_loan()


def test_margin_get_max_margin_transfer(client):
    client.get_max_margin_transfer()


def test_margin_get_margin_delist_schedule(client):
    client.get_margin_delist_schedule()


# Margin OCO


def test_margin_create_margin_oco_order(client):
    client.create_margin_oco_order()


def test_margin_cancel_margin_oco_order(client):
    client.cancel_margin_oco_order()


def test_margin_get_margin_oco_order(client):
    client.get_margin_oco_order()


def test_margin_get_open_margin_oco_orders(client):
    client.get_open_margin_oco_orders()


# Cross-margin


def test_margin_margin_stream_get_listen_key(client):
    client.margin_stream_get_listen_key()


def test_margin_margin_stream_close(client):
    client.margin_stream_close()


# Isolated margin


def test_margin_isolated_margin_stream_get_listen_key(client):
    client.isolated_margin_stream_get_listen_key()


def test_margin_isolated_margin_stream_close(client):
    client.isolated_margin_stream_close()


# Simple Earn Endpoints


def test_margin_get_simple_earn_flexible_product_list(client):
    client.get_simple_earn_flexible_product_list()


def test_margin_get_simple_earn_locked_product_list(client):
    client.get_simple_earn_locked_product_list()


def test_margin_subscribe_simple_earn_flexible_product(client):
    client.subscribe_simple_earn_flexible_product()


def test_margin_subscribe_simple_earn_locked_product(client):
    client.subscribe_simple_earn_locked_product()


def test_margin_redeem_simple_earn_flexible_product(client):
    client.redeem_simple_earn_flexible_product()


def test_margin_redeem_simple_earn_locked_product(client):
    client.redeem_simple_earn_locked_product()


def test_margin_get_simple_earn_flexible_product_position(client):
    client.get_simple_earn_flexible_product_position()


def test_margin_get_simple_earn_locked_product_position(client):
    client.get_simple_earn_locked_product_position()


def test_margin_get_simple_earn_account(client):
    client.get_simple_earn_account()


# Lending Endpoints


def test_margin_get_fixed_activity_project_list(client):
    client.get_fixed_activity_project_list()


def test_margin_change_fixed_activity_to_daily_position(client):
    client.change_fixed_activity_to_daily_position()


# Staking Endpoints


def test_margin_get_staking_product_list(client):
    client.get_staking_product_list()


def test_margin_purchase_staking_product(client):
    client.purchase_staking_product()


def test_margin_redeem_staking_product(client):
    client.redeem_staking_product()


def test_margin_get_staking_position(client):
    client.get_staking_position()


def test_margin_get_staking_purchase_history(client):
    client.get_staking_purchase_history()


def test_margin_set_auto_staking(client):
    client.set_auto_staking()


def test_margin_get_personal_left_quota(client):
    client.get_personal_left_quota()


# US Staking Endpoints


def test_margin_get_staking_asset_us(client):
    client.get_staking_asset_us()


def test_margin_stake_asset_us(client):
    client.stake_asset_us()


def test_margin_unstake_asset_us(client):
    client.unstake_asset_us()


def test_margin_get_staking_balance_us(client):
    client.get_staking_balance_us()


def test_margin_get_staking_history_us(client):
    client.get_staking_history_us()


def test_margin_get_staking_rewards_history_us(client):
    client.get_staking_rewards_history_us()


# Sub Accounts


def test_margin_get_sub_account_list(client):
    client.get_sub_account_list()


def test_margin_get_sub_account_transfer_history(client):
    client.get_sub_account_transfer_history()


def test_margin_get_sub_account_futures_transfer_history(client):
    client.get_sub_account_futures_transfer_history()


def test_margin_create_sub_account_futures_transfer(client):
    client.create_sub_account_futures_transfer()


def test_margin_get_sub_account_assets(client):
    client.get_sub_account_assets()


def test_margin_query_subaccount_spot_summary(client):
    client.query_subaccount_spot_summary()


def test_margin_get_subaccount_deposit_address(client):
    client.get_subaccount_deposit_address()


def test_margin_get_subaccount_deposit_history(client):
    client.get_subaccount_deposit_history()


def test_margin_get_subaccount_futures_margin_status(client):
    client.get_subaccount_futures_margin_status()


def test_margin_enable_subaccount_margin(client):
    client.enable_subaccount_margin()


def test_margin_get_subaccount_margin_details(client):
    client.get_subaccount_margin_details()


def test_margin_get_subaccount_margin_summary(client):
    client.get_subaccount_margin_summary()


def test_margin_enable_subaccount_futures(client):
    client.enable_subaccount_futures()


def test_margin_get_subaccount_futures_details(client):
    client.get_subaccount_futures_details()


def test_margin_get_subaccount_futures_summary(client):
    client.get_subaccount_futures_summary()


def test_margin_get_subaccount_futures_positionrisk(client):
    client.get_subaccount_futures_positionrisk()


def test_margin_make_subaccount_futures_transfer(client):
    client.make_subaccount_futures_transfer()


def test_margin_make_subaccount_margin_transfer(client):
    client.make_subaccount_margin_transfer()


def test_margin_make_subaccount_to_subaccount_transfer(client):
    client.make_subaccount_to_subaccount_transfer()


def test_margin_make_subaccount_to_master_transfer(client):
    client.make_subaccount_to_master_transfer()


def test_margin_get_subaccount_transfer_history(client):
    client.get_subaccount_transfer_history()


def test_margin_make_subaccount_universal_transfer(client):
    client.make_subaccount_universal_transfer()


def test_margin_get_universal_transfer_history(client):
    client.get_universal_transfer_history()


# Fiat Endpoints


def test_margin_get_fiat_deposit_withdraw_history(client):
    client.get_fiat_deposit_withdraw_history()


def test_margin_get_fiat_payments_history(client):
    client.get_fiat_payments_history()


# C2C Endpoints


def test_margin_get_c2c_trade_history(client):
    client.get_c2c_trade_history()


# Pay Endpoints


def test_margin_get_pay_trade_history(client):
    client.get_pay_trade_history()


# Convert Endpoints


def test_margin_get_convert_trade_history(client):
    client.get_convert_trade_history()


def test_margin_convert_request_quote(client):
    client.convert_request_quote()


def test_margin_convert_accept_quote(client):
    client.convert_accept_quote()


def test_margin_new_transfer_history(futuresClient):
    futuresClient.new_transfer_history()


def test_margin_funding_wallet(futuresClient):
    futuresClient.funding_wallet()


def test_margin_get_user_asset(futuresClient):
    futuresClient.get_user_asset()


def test_margin_universal_transfer(futuresClient):
    futuresClient.universal_transfer()


def test_margin_get_all_coins_info(client):
    client.get_all_coins_info()


def test_margin_get_account_snapshot(client):
    client.get_account_snapshot()


def test_margin_disable_fast_withdraw_switch(client):
    client.disable_fast_withdraw_switch()


def test_margin_enable_fast_withdraw_switch(client):
    client.enable_fast_withdraw_switch()


@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_next_hourly_interest_rate(client):
    client.margin_next_hourly_interest_rate(
        assets="BTC",
        isIsolated="FALSE"
    )


@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_interest_history(client):
    client.margin_interest_history(
        asset="BTC",
    )


@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_borrow_repay(client):
    client.margin_borrow_repay(
        asset="BTC",
        amount=0.1,
        isIsolated="FALSE",
        symbol="BTCUSDT",
        type="BORROW"
    )


@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_get_borrow_repay_records(client):
    client.margin_get_borrow_repay_records(
        asset="BTC",
        isolatedSymbol="BTCUSDT",
        txId=2970933056,
        startTime=1563438204000,
        endTime=1563438204000,
        current=1,
        size=10
    )

@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_interest_rate_history(client):
    client.margin_interest_rate_history(
        asset="BTC",
    )

@pytest.mark.skip(reason="can't test margin endpoints")
def test_margin_max_borrowable(client):
    client.margin_max_borrowable(
        asset="BTC",
    )
