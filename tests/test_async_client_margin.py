import pytest

pytestmark = [pytest.mark.margin, pytest.mark.asyncio]

async def test_margin__get_account_status(asyncClient):
    await asyncClient.get_account_status()

async def test_margin_get_account_api_trading_status(asyncClient):
    await asyncClient.get_account_api_trading_status()

async def test_margin_get_account_api_permissions(asyncClient):
    await asyncClient.get_account_api_permissions()

async def test_margin_get_dust_assets(asyncClient):
    await asyncClient.get_dust_assets()

async def test_margin_get_dust_log(asyncClient):
    await asyncClient.test_get_dust_log()

async def test_margin_transfer_dust(asyncClient):
    await asyncClient.transfer_dust()

async def test_margin_get_asset_dividend_history(asyncClient):
    await asyncClient.get_asset_dividend_history()

async def test_margin_make_universal_transfer(asyncClient):
    await asyncClient.make_universal_transfer()

async def test_margin_query_universal_transfer_history(asyncClient):
    await asyncClient.query_universal_transfer_history()

async def test_margin_get_trade_fee(asyncClient):
    await asyncClient.get_trade_fee()

async def test_margin_get_asset_details(asyncClient):
    await asyncClient.get_asset_details()

async def test_margin_get_spot_delist_schedule(asyncClient):
    await asyncClient.get_spot_delist_schedule()

# Withdraw Endpoints

async def test_margin_withdraw(asyncClient):
    await asyncClient.withdraw()

async def test_margin_get_deposit_history(asyncClient):
    await asyncClient.get_deposit_history()

async def test_margin_get_withdraw_history(asyncClient):
    await asyncClient.get_withdraw_history()

async def test_margin_get_withdraw_history_id(asyncClient):
    await asyncClient.get_withdraw_history_id()

async def test_margin_get_deposit_address(asyncClient):
    await asyncClient.get_deposit_address()

# Margin Trading Endpoints

async def test_margin_get_margin_account(asyncClient):
    await asyncClient.get_margin_account()

async def test_margin_get_isolated_margin_account(asyncClient):
    await asyncClient.get_isolated_margin_account()

async def test_margin_enable_isolated_margin_account(asyncClient):
    await asyncClient.enable_isolated_margin_account()

async def test_margin_disable_isolated_margin_account(asyncClient):
    await asyncClient.disable_isolated_margin_account()

async def test_margin_get_enabled_isolated_margin_account_limit(asyncClient):
    await asyncClient.get_enabled_isolated_margin_account_limit()

async def test_margin_get_margin_dustlog(asyncClient):
    await asyncClient.get_margin_dustlog()

async def test_margin_get_margin_dust_assets(asyncClient):
    await asyncClient.get_margin_dust_assets()

async def test_margin_transfer_margin_dust(asyncClient):
    await asyncClient.transfer_margin_dust()

async def test_margin_get_cross_margin_collateral_ratio(asyncClient):
    await asyncClient.get_cross_margin_collateral_ratio()

async def test_margin_get_small_liability_exchange_assets(asyncClient):
    await asyncClient.get_small_liability_exchange_assets()

async def test_margin_exchange_small_liability_assets(asyncClient):
    await asyncClient.exchange_small_liability_assets()

async def test_margin_get_small_liability_exchange_history(asyncClient):
    await asyncClient.get_small_liability_exchange_history()

async def test_margin_get_future_hourly_interest_rate(asyncClient):
    await asyncClient.get_future_hourly_interest_rate()

async def test_margin_get_margin_capital_flow(asyncClient):
    await asyncClient.get_margin_capital_flow()

async def test_margin_get_margin_asset(asyncClient):
    await asyncClient.get_margin_asset()

async def test_margin_get_margin_symbol(asyncClient):
    await asyncClient.get_margin_symbol()

async def test_margin_get_margin_all_assets(asyncClient):
    await asyncClient.get_margin_all_assets()

async def test_margin_get_margin_all_pairs(asyncClient):
    await asyncClient.get_margin_all_pairs()

async def test_margin_create_isolated_margin_account(asyncClient):
    await asyncClient.create_isolated_margin_account()

async def test_margin_get_isolated_margin_symbol(asyncClient):
    await asyncClient.get_isolated_margin_symbol()

async def test_margin_get_all_isolated_margin_symbols(asyncClient):
    await asyncClient.get_all_isolated_margin_symbols()

async def test_margin_get_isolated_margin_fee_data(asyncClient):
    await asyncClient.get_isolated_margin_fee_data()

async def test_margin_get_isolated_margin_tier_data(asyncClient):
    await asyncClient.get_isolated_margin_tier_data()

async def test_margin_margin_manual_liquidation(asyncClient):
    await asyncClient.margin_manual_liquidation()

async def test_margin_toggle_bnb_burn_spot_margin(asyncClient):
    await asyncClient.toggle_bnb_burn_spot_margin()

async def test_margin_get_bnb_burn_spot_margin(asyncClient):
    await asyncClient.get_bnb_burn_spot_margin()

async def test_margin_get_margin_price_index(asyncClient):
    await asyncClient.get_margin_price_index()

async def test_margin_transfer_margin_to_spot(asyncClient):
    await asyncClient.transfer_margin_to_spot()

async def test_margin_transfer_spot_to_margin(asyncClient):
    await asyncClient.transfer_spot_to_margin()

async def test_margin_transfer_isolated_margin_to_spot(asyncClient):
    await asyncClient.transfer_isolated_margin_to_spot()

async def test_margin_transfer_spot_to_isolated_margin(asyncClient):
    await asyncClient.transfer_spot_to_isolated_margin()

async def test_margin_get_isolated_margin_tranfer_history(asyncClient):
    await asyncClient.get_isolated_margin_tranfer_history()

async def test_margin_create_margin_loan(asyncClient):
    await asyncClient.create_margin_loan()

async def test_margin_repay_margin_loan(asyncClient):
    await asyncClient.repay_margin_loan()

async def create_margin_ordertest_(asyncClient):
    await asyncClient.create_margin_order()

async def test_margin_cancel_margin_order(asyncClient):
    await asyncClient.cancel_margin_order()

async def test_margin_set_margin_max_leverage(asyncClient):
    await asyncClient.set_margin_max_leverage()

async def test_margin_get_margin_transfer_history(asyncClient):
    await asyncClient.get_margin_transfer_history()

async def test_margin_get_margin_loan_details(asyncClient):
    await asyncClient.get_margin_loan_details()

async def test_margin_get_margin_repay_details(asyncClient):
    await asyncClient.get_margin_repay_details()

async def test_margin_get_cross_margin_data(asyncClient):
    await asyncClient.get_cross_margin_data()

async def test_margin_get_margin_interest_history(asyncClient):
    await asyncClient.get_margin_interest_history()

async def test_margin_get_margin_force_liquidation_rec(asyncClient):
    await asyncClient.get_margin_force_liquidation_rec()

async def test_margin_get_margin_order(asyncClient):
    await asyncClient.get_margin_order()

async def test_margin_get_open_margin_orders(asyncClient):
    await asyncClient.get_open_margin_orders()

async def test_margin_get_all_margin_orders(asyncClient):
    await asyncClient.get_all_margin_orders()

async def test_margin_get_margin_trades(asyncClient):
    await asyncClient.get_margin_trades()

async def test_margin_get_max_margin_loan(asyncClient):
    await asyncClient.get_max_margin_loan()

async def test_margin_get_max_margin_transfer(asyncClient):
    await asyncClient.get_max_margin_transfer()

async def test_margin_get_margin_delist_schedule(asyncClient):
    await asyncClient.get_margin_delist_schedule()

# Margin OCO

async def test_margin_create_margin_oco_order(asyncClient):
    await asyncClient.create_margin_oco_order()

async def test_margin_cancel_margin_oco_order(asyncClient):
    await asyncClient.cancel_margin_oco_order()

async def test_margin_get_margin_oco_order(asyncClient):
    await asyncClient.get_margin_oco_order()

async def test_margin_get_open_margin_oco_orders(asyncClient):
    await asyncClient.get_open_margin_oco_orders()

# Cross-margin

async def test_margin_margin_stream_get_listen_key(asyncClient):
    await asyncClient.margin_stream_get_listen_key()

async def test_margin_margin_stream_close(asyncClient):
    await asyncClient.margin_stream_close()

# Isolated margin

async def test_margin_isolated_margin_stream_get_listen_key(asyncClient):
    await asyncClient.isolated_margin_stream_get_listen_key()

async def test_margin_isolated_margin_stream_close(asyncClient):
    await asyncClient.isolated_margin_stream_close()

# Simple Earn Endpoints

async def test_margin_get_simple_earn_flexible_product_list(asyncClient):
    await asyncClient.get_simple_earn_flexible_product_list()

async def test_margin_get_simple_earn_locked_product_list(asyncClient):
    await asyncClient.get_simple_earn_locked_product_list()

async def test_margin_subscribe_simple_earn_flexible_product(asyncClient):
    await asyncClient.subscribe_simple_earn_flexible_product()

async def test_margin_subscribe_simple_earn_locked_product(asyncClient):
    await asyncClient.subscribe_simple_earn_locked_product()

async def test_margin_redeem_simple_earn_flexible_product(asyncClient):
    await asyncClient.redeem_simple_earn_flexible_product()

async def test_margin_redeem_simple_earn_locked_product(asyncClient):
    await asyncClient.redeem_simple_earn_locked_product()

async def test_margin_get_simple_earn_flexible_product_position(asyncClient):
    await asyncClient.get_simple_earn_flexible_product_position()

async def test_margin_get_simple_earn_locked_product_position(asyncClient):
    await asyncClient.get_simple_earn_locked_product_position()

async def test_margin_get_simple_earn_account(asyncClient):
    await asyncClient.get_simple_earn_account()

# Lending Endpoints

async def test_margin_get_fixed_activity_project_list(asyncClient):
    await asyncClient.get_fixed_activity_project_list()

async def test_margin_change_fixed_activity_to_daily_position(asyncClient):
    await asyncClient.change_fixed_activity_to_daily_position()

# Staking Endpoints

async def test_margin_get_staking_product_list(asyncClient):
    await asyncClient.get_staking_product_list()

async def test_margin_purchase_staking_product(asyncClient):
    await asyncClient.purchase_staking_product()

async def test_margin_redeem_staking_product(asyncClient):
    await asyncClient.redeem_staking_product()

async def test_margin_get_staking_position(asyncClient):
    await asyncClient.get_staking_position()

async def test_margin_get_staking_purchase_history(asyncClient):
    await asyncClient.get_staking_purchase_history()

async def test_margin_set_auto_staking(asyncClient):
    await asyncClient.set_auto_staking()

async def test_margin_get_personal_left_quota(asyncClient):
    await asyncClient.get_personal_left_quota()

# US Staking Endpoints

async def test_margin_get_staking_asset_us(asyncClient):
    await asyncClient.get_staking_asset_us()

async def test_margin_stake_asset_us(asyncClient):
    await asyncClient.stake_asset_us()

async def test_margin_unstake_asset_us(asyncClient):
    await asyncClient.unstake_asset_us()

async def test_margin_get_staking_balance_us(asyncClient):
    await asyncClient.get_staking_balance_us()

async def test_margin_get_staking_history_us(asyncClient):
    await asyncClient.get_staking_history_us()

async def test_margin_get_staking_rewards_history_us(asyncClient):
    await asyncClient.get_staking_rewards_history_us()

# Sub Accounts

async def test_margin_get_sub_account_list(asyncClient):
    await asyncClient.get_sub_account_list()

async def test_margin_get_sub_account_transfer_history(asyncClient):
    await asyncClient.get_sub_account_transfer_history()

async def test_margin_get_sub_account_futures_transfer_history(asyncClient):
    await asyncClient.get_sub_account_futures_transfer_history()

async def test_margin_create_sub_account_futures_transfer(asyncClient):
    await asyncClient.create_sub_account_futures_transfer()

async def test_margin_get_sub_account_assets(asyncClient):
    await asyncClient.get_sub_account_assets()

async def test_margin_query_subaccount_spot_summary(asyncClient):
    await asyncClient.query_subaccount_spot_summary()

async def test_margin_get_subaccount_deposit_address(asyncClient):
    await asyncClient.get_subaccount_deposit_address()

async def test_margin_get_subaccount_deposit_history(asyncClient):
    await asyncClient.get_subaccount_deposit_history()

async def test_margin_get_subaccount_futures_margin_status(asyncClient):
    await asyncClient.get_subaccount_futures_margin_status()

async def test_margin_enable_subaccount_margin(asyncClient):
    await asyncClient.enable_subaccount_margin()

async def test_margin_get_subaccount_margin_details(asyncClient):
    await asyncClient.get_subaccount_margin_details()

async def test_margin_get_subaccount_margin_summary(asyncClient):
    await asyncClient.get_subaccount_margin_summary()

async def test_margin_enable_subaccount_futures(asyncClient):
    await asyncClient.enable_subaccount_futures()

async def test_margin_get_subaccount_futures_details(asyncClient):
    await asyncClient.get_subaccount_futures_details()

async def test_margin_get_subaccount_futures_summary(asyncClient):
    await asyncClient.get_subaccount_futures_summary()

async def test_margin_get_subaccount_futures_positionrisk(asyncClient):
    await asyncClient.get_subaccount_futures_positionrisk()

async def test_margin_make_subaccount_futures_transfer(asyncClient):
    await asyncClient.make_subaccount_futures_transfer()

async def test_margin_make_subaccount_margin_transfer(asyncClient):
    await asyncClient.make_subaccount_margin_transfer()

async def test_margin_make_subaccount_to_subaccount_transfer(asyncClient):
    await asyncClient.make_subaccount_to_subaccount_transfer()

async def test_margin_make_subaccount_to_master_transfer(asyncClient):
    await asyncClient.make_subaccount_to_master_transfer()

async def test_margin_get_subaccount_transfer_history(asyncClient):
    await asyncClient.get_subaccount_transfer_history()

async def test_margin_make_subaccount_universal_transfer(asyncClient):
    await asyncClient.make_subaccount_universal_transfer()

async def test_margin_get_universal_transfer_history(asyncClient):
    await asyncClient.get_universal_transfer_history()

# Fiat Endpoints

async def test_margin_get_fiat_deposit_withdraw_history(asyncClient):
    await asyncClient.get_fiat_deposit_withdraw_history()

async def test_margin_get_fiat_payments_history(asyncClient):
    await asyncClient.get_fiat_payments_history()

# C2C Endpoints

async def test_margin_get_c2c_trade_history(asyncClient):
    await asyncClient.get_c2c_trade_history()

# Pay Endpoints

async def test_margin_get_pay_trade_history(asyncClient):
    await asyncClient.get_pay_trade_history()

# Convert Endpoints

async def test_margin_get_convert_trade_history(asyncClient):
    await asyncClient.get_convert_trade_history()

async def test_margin_convert_request_quote(asyncClient):
    await asyncClient.convert_request_quote()

async def test_margin_convert_accept_quote(asyncClient):
    await asyncClient.convert_accept_quote()
