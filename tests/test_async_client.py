import pytest


def test_clientAsync_initialization(clientAsync):
    assert clientAsync.API_KEY is not None
    assert clientAsync.API_SECRET is not None
    assert clientAsync.testnet is False


@pytest.mark.asyncio()
async def test_get_products(clientAsync):
    await clientAsync.get_products()


@pytest.mark.asyncio()
async def test_get_exchange_info(clientAsync):
    await clientAsync.get_exchange_info()


@pytest.mark.asyncio()
async def test_get_symbol_info(clientAsync):
    await clientAsync.get_symbol_info("BTCUSDT")


@pytest.mark.asyncio()
async def test_ping(clientAsync):
    await clientAsync.ping()


@pytest.mark.asyncio()
async def test_get_server_time(clientAsync):
    await clientAsync.get_server_time()


@pytest.mark.asyncio()
async def test_get_all_tickers(clientAsync):
    await clientAsync.get_all_tickers()


@pytest.mark.asyncio()
async def test_get_orderbook_tickers(clientAsync):
    await clientAsync.get_orderbook_tickers()


@pytest.mark.asyncio()
async def test_get_order_book(clientAsync):
    await clientAsync.get_order_book(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_recent_trades(clientAsync):
    await clientAsync.get_recent_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_historical_trades(clientAsync):
    await clientAsync.get_historical_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_aggregate_trades(clientAsync):
    await clientAsync.get_aggregate_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_klines(clientAsync):
    await clientAsync.get_klines(symbol="BTCUSDT", interval="1d")


@pytest.mark.asyncio()
async def test_get_avg_price(clientAsync):
    await clientAsync.get_avg_price(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_ticker(clientAsync):
    await clientAsync.get_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_symbol_ticker(clientAsync):
    await clientAsync.get_symbol_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_orderbook_ticker(clientAsync):
    await clientAsync.get_orderbook_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_account(clientAsync):
    await clientAsync.get_account()


@pytest.mark.asyncio()
async def test_get_asset_balance(clientAsync):
    await clientAsync.get_asset_balance(asset="BTC")


@pytest.mark.asyncio()
async def test_get_my_trades(clientAsync):
    await clientAsync.get_my_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_get_system_status(clientAsync):
    await clientAsync.get_system_status()


@pytest.mark.asyncio()
async def test_get_account_status(clientAsync):
    await clientAsync.get_account_status()


@pytest.mark.asyncio()
async def test_get_account_api_trading_status(clientAsync):
    await clientAsync.get_account_api_trading_status()


@pytest.mark.asyncio()
async def test_get_account_api_permissions(clientAsync):
    await clientAsync.get_account_api_permissions()


@pytest.mark.asyncio()
async def test_get_dust_assets(clientAsync):
    await clientAsync.get_dust_assets()


@pytest.mark.asyncio()
async def test_get_dust_log(clientAsync):
    await clientAsync.test_get_dust_log()


@pytest.mark.asyncio()
async def test_transfer_dust(clientAsync):
    await clientAsync.transfer_dust()


@pytest.mark.asyncio()
async def test_get_asset_dividend_history(clientAsync):
    await clientAsync.get_asset_dividend_history()


@pytest.mark.asyncio()
async def test_make_universal_transfer(clientAsync):
    await clientAsync.make_universal_transfer()


@pytest.mark.asyncio()
async def test_query_universal_transfer_history(clientAsync):
    await clientAsync.query_universal_transfer_history()


@pytest.mark.asyncio()
async def test_get_trade_fee(clientAsync):
    await clientAsync.get_trade_fee()


@pytest.mark.asyncio()
async def test_get_asset_details(clientAsync):
    await clientAsync.get_asset_details()


@pytest.mark.asyncio()
async def test_get_spot_delist_schedule(clientAsync):
    await clientAsync.get_spot_delist_schedule()


# Withdraw Endpoints


@pytest.mark.asyncio()
async def test_withdraw(clientAsync):
    await clientAsync.withdraw()


@pytest.mark.asyncio()
async def test_get_deposit_history(clientAsync):
    await clientAsync.get_deposit_history()


@pytest.mark.asyncio()
async def test_get_withdraw_history(clientAsync):
    await clientAsync.get_withdraw_history()


@pytest.mark.asyncio()
async def test_get_withdraw_history_id(clientAsync):
    await clientAsync.get_withdraw_history_id()


@pytest.mark.asyncio()
async def test_get_deposit_address(clientAsync):
    await clientAsync.get_deposit_address()


# User Stream Endpoints


@pytest.mark.asyncio()
async def test_stream_get_listen_key(clientAsync):
    await clientAsync.stream_get_listen_key()


@pytest.mark.asyncio()
async def test_stream_close(clientAsync):
    await clientAsync.stream_close()


# Margin Trading Endpoints


@pytest.mark.asyncio()
async def test_get_margin_account(clientAsync):
    await clientAsync.get_margin_account()


@pytest.mark.asyncio()
async def test_get_isolated_margin_account(clientAsync):
    await clientAsync.get_isolated_margin_account()


@pytest.mark.asyncio()
async def test_enable_isolated_margin_account(clientAsync):
    await clientAsync.enable_isolated_margin_account()


@pytest.mark.asyncio()
async def test_disable_isolated_margin_account(clientAsync):
    await clientAsync.disable_isolated_margin_account()


@pytest.mark.asyncio()
async def test_get_enabled_isolated_margin_account_limit(clientAsync):
    await clientAsync.get_enabled_isolated_margin_account_limit()


@pytest.mark.asyncio()
async def test_get_margin_dustlog(clientAsync):
    await clientAsync.get_margin_dustlog()


@pytest.mark.asyncio()
async def test_get_margin_dust_assets(clientAsync):
    await clientAsync.get_margin_dust_assets()


@pytest.mark.asyncio()
async def test_transfer_margin_dust(clientAsync):
    await clientAsync.transfer_margin_dust()


@pytest.mark.asyncio()
async def test_get_cross_margin_collateral_ratio(clientAsync):
    await clientAsync.get_cross_margin_collateral_ratio()


@pytest.mark.asyncio()
async def test_get_small_liability_exchange_assets(clientAsync):
    await clientAsync.get_small_liability_exchange_assets()


@pytest.mark.asyncio()
async def test_exchange_small_liability_assets(clientAsync):
    await clientAsync.exchange_small_liability_assets()


@pytest.mark.asyncio()
async def test_get_small_liability_exchange_history(clientAsync):
    await clientAsync.get_small_liability_exchange_history()


@pytest.mark.asyncio()
async def test_get_future_hourly_interest_rate(clientAsync):
    await clientAsync.get_future_hourly_interest_rate()


@pytest.mark.asyncio()
async def test_get_margin_capital_flow(clientAsync):
    await clientAsync.get_margin_capital_flow()


@pytest.mark.asyncio()
async def test_get_margin_asset(clientAsync):
    await clientAsync.get_margin_asset()


@pytest.mark.asyncio()
async def test_get_margin_symbol(clientAsync):
    await clientAsync.get_margin_symbol()


@pytest.mark.asyncio()
async def test_get_margin_all_assets(clientAsync):
    await clientAsync.get_margin_all_assets()


@pytest.mark.asyncio()
async def test_get_margin_all_pairs(clientAsync):
    await clientAsync.get_margin_all_pairs()


@pytest.mark.asyncio()
async def test_create_isolated_margin_account(clientAsync):
    await clientAsync.create_isolated_margin_account()


@pytest.mark.asyncio()
async def test_get_isolated_margin_symbol(clientAsync):
    await clientAsync.get_isolated_margin_symbol()


@pytest.mark.asyncio()
async def test_get_all_isolated_margin_symbols(clientAsync):
    await clientAsync.get_all_isolated_margin_symbols()


@pytest.mark.asyncio()
async def test_get_isolated_margin_fee_data(clientAsync):
    await clientAsync.get_isolated_margin_fee_data()


@pytest.mark.asyncio()
async def test_get_isolated_margin_tier_data(clientAsync):
    await clientAsync.get_isolated_margin_tier_data()


@pytest.mark.asyncio()
async def test_margin_manual_liquidation(clientAsync):
    await clientAsync.margin_manual_liquidation()


@pytest.mark.asyncio()
async def test_toggle_bnb_burn_spot_margin(clientAsync):
    await clientAsync.toggle_bnb_burn_spot_margin()


@pytest.mark.asyncio()
async def test_get_bnb_burn_spot_margin(clientAsync):
    await clientAsync.get_bnb_burn_spot_margin()


@pytest.mark.asyncio()
async def test_get_margin_price_index(clientAsync):
    await clientAsync.get_margin_price_index()


@pytest.mark.asyncio()
async def test_transfer_margin_to_spot(clientAsync):
    await clientAsync.transfer_margin_to_spot()


@pytest.mark.asyncio()
async def test_transfer_spot_to_margin(clientAsync):
    await clientAsync.transfer_spot_to_margin()


@pytest.mark.asyncio()
async def test_transfer_isolated_margin_to_spot(clientAsync):
    await clientAsync.transfer_isolated_margin_to_spot()


@pytest.mark.asyncio()
async def test_transfer_spot_to_isolated_margin(clientAsync):
    await clientAsync.transfer_spot_to_isolated_margin()


@pytest.mark.asyncio()
async def test_get_isolated_margin_tranfer_history(clientAsync):
    await clientAsync.get_isolated_margin_tranfer_history()


@pytest.mark.asyncio()
async def test_create_margin_loan(clientAsync):
    await clientAsync.create_margin_loan()


@pytest.mark.asyncio()
async def test_repay_margin_loan(clientAsync):
    await clientAsync.repay_margin_loan()


@pytest.mark.asyncio()
async def create_margin_ordertest_(clientAsync):
    await clientAsync.create_margin_order()


@pytest.mark.asyncio()
async def test_cancel_margin_order(clientAsync):
    await clientAsync.cancel_margin_order()


@pytest.mark.asyncio()
async def test_set_margin_max_leverage(clientAsync):
    await clientAsync.set_margin_max_leverage()


@pytest.mark.asyncio()
async def test_get_margin_transfer_history(clientAsync):
    await clientAsync.get_margin_transfer_history()


@pytest.mark.asyncio()
async def test_get_margin_loan_details(clientAsync):
    await clientAsync.get_margin_loan_details()


@pytest.mark.asyncio()
async def test_get_margin_repay_details(clientAsync):
    await clientAsync.get_margin_repay_details()


@pytest.mark.asyncio()
async def test_get_cross_margin_data(clientAsync):
    await clientAsync.get_cross_margin_data()


@pytest.mark.asyncio()
async def test_get_margin_interest_history(clientAsync):
    await clientAsync.get_margin_interest_history()


@pytest.mark.asyncio()
async def test_get_margin_force_liquidation_rec(clientAsync):
    await clientAsync.get_margin_force_liquidation_rec()


@pytest.mark.asyncio()
async def test_get_margin_order(clientAsync):
    await clientAsync.get_margin_order()


@pytest.mark.asyncio()
async def test_get_open_margin_orders(clientAsync):
    await clientAsync.get_open_margin_orders()


@pytest.mark.asyncio()
async def test_get_all_margin_orders(clientAsync):
    await clientAsync.get_all_margin_orders()


@pytest.mark.asyncio()
async def test_get_margin_trades(clientAsync):
    await clientAsync.get_margin_trades()


@pytest.mark.asyncio()
async def test_get_max_margin_loan(clientAsync):
    await clientAsync.get_max_margin_loan()


@pytest.mark.asyncio()
async def test_get_max_margin_transfer(clientAsync):
    await clientAsync.get_max_margin_transfer()


@pytest.mark.asyncio()
async def test_get_margin_delist_schedule(clientAsync):
    await clientAsync.get_margin_delist_schedule()


# Margin OCO


@pytest.mark.asyncio()
async def test_create_margin_oco_order(clientAsync):
    await clientAsync.create_margin_oco_order()


@pytest.mark.asyncio()
async def test_cancel_margin_oco_order(clientAsync):
    await clientAsync.cancel_margin_oco_order()


@pytest.mark.asyncio()
async def test_get_margin_oco_order(clientAsync):
    await clientAsync.get_margin_oco_order()


@pytest.mark.asyncio()
async def test_get_open_margin_oco_orders(clientAsync):
    await clientAsync.get_open_margin_oco_orders()


# Cross-margin


@pytest.mark.asyncio()
async def test_margin_stream_get_listen_key(clientAsync):
    await clientAsync.margin_stream_get_listen_key()


@pytest.mark.asyncio()
async def test_margin_stream_close(clientAsync):
    await clientAsync.margin_stream_close()


# Isolated margin


@pytest.mark.asyncio()
async def test_isolated_margin_stream_get_listen_key(clientAsync):
    await clientAsync.isolated_margin_stream_get_listen_key()


@pytest.mark.asyncio()
async def test_isolated_margin_stream_close(clientAsync):
    await clientAsync.isolated_margin_stream_close()


# Simple Earn Endpoints


@pytest.mark.asyncio()
async def test_get_simple_earn_flexible_product_list(clientAsync):
    await clientAsync.get_simple_earn_flexible_product_list()


@pytest.mark.asyncio()
async def test_get_simple_earn_locked_product_list(clientAsync):
    await clientAsync.get_simple_earn_locked_product_list()


@pytest.mark.asyncio()
async def test_subscribe_simple_earn_flexible_product(clientAsync):
    await clientAsync.subscribe_simple_earn_flexible_product()


@pytest.mark.asyncio()
async def test_subscribe_simple_earn_locked_product(clientAsync):
    await clientAsync.subscribe_simple_earn_locked_product()


@pytest.mark.asyncio()
async def test_redeem_simple_earn_flexible_product(clientAsync):
    await clientAsync.redeem_simple_earn_flexible_product()


@pytest.mark.asyncio()
async def test_redeem_simple_earn_locked_product(clientAsync):
    await clientAsync.redeem_simple_earn_locked_product()


@pytest.mark.asyncio()
async def test_get_simple_earn_flexible_product_position(clientAsync):
    await clientAsync.get_simple_earn_flexible_product_position()


@pytest.mark.asyncio()
async def test_get_simple_earn_locked_product_position(clientAsync):
    await clientAsync.get_simple_earn_locked_product_position()


@pytest.mark.asyncio()
async def test_get_simple_earn_account(clientAsync):
    await clientAsync.get_simple_earn_account()


# Lending Endpoints


@pytest.mark.asyncio()
async def test_get_fixed_activity_project_list(clientAsync):
    await clientAsync.get_fixed_activity_project_list()


@pytest.mark.asyncio()
async def test_change_fixed_activity_to_daily_position(clientAsync):
    await clientAsync.change_fixed_activity_to_daily_position()


# Staking Endpoints


@pytest.mark.asyncio()
async def test_get_staking_product_list(clientAsync):
    await clientAsync.get_staking_product_list()


@pytest.mark.asyncio()
async def test_purchase_staking_product(clientAsync):
    await clientAsync.purchase_staking_product()


@pytest.mark.asyncio()
async def test_redeem_staking_product(clientAsync):
    await clientAsync.redeem_staking_product()


@pytest.mark.asyncio()
async def test_get_staking_position(clientAsync):
    await clientAsync.get_staking_position()


@pytest.mark.asyncio()
async def test_get_staking_purchase_history(clientAsync):
    await clientAsync.get_staking_purchase_history()


@pytest.mark.asyncio()
async def test_set_auto_staking(clientAsync):
    await clientAsync.set_auto_staking()


@pytest.mark.asyncio()
async def test_get_personal_left_quota(clientAsync):
    await clientAsync.get_personal_left_quota()


# US Staking Endpoints


@pytest.mark.asyncio()
async def test_get_staking_asset_us(clientAsync):
    await clientAsync.get_staking_asset_us()


@pytest.mark.asyncio()
async def test_stake_asset_us(clientAsync):
    await clientAsync.stake_asset_us()


@pytest.mark.asyncio()
async def test_unstake_asset_us(clientAsync):
    await clientAsync.unstake_asset_us()


@pytest.mark.asyncio()
async def test_get_staking_balance_us(clientAsync):
    await clientAsync.get_staking_balance_us()


@pytest.mark.asyncio()
async def test_get_staking_history_us(clientAsync):
    await clientAsync.get_staking_history_us()


@pytest.mark.asyncio()
async def test_get_staking_rewards_history_us(clientAsync):
    await clientAsync.get_staking_rewards_history_us()


# Sub Accounts


@pytest.mark.asyncio()
async def test_get_sub_account_list(clientAsync):
    await clientAsync.get_sub_account_list()


@pytest.mark.asyncio()
async def test_get_sub_account_transfer_history(clientAsync):
    await clientAsync.get_sub_account_transfer_history()


@pytest.mark.asyncio()
async def test_get_sub_account_futures_transfer_history(clientAsync):
    await clientAsync.get_sub_account_futures_transfer_history()


@pytest.mark.asyncio()
async def test_create_sub_account_futures_transfer(clientAsync):
    await clientAsync.create_sub_account_futures_transfer()


@pytest.mark.asyncio()
async def test_get_sub_account_assets(clientAsync):
    await clientAsync.get_sub_account_assets()


@pytest.mark.asyncio()
async def test_query_subaccount_spot_summary(clientAsync):
    await clientAsync.query_subaccount_spot_summary()


@pytest.mark.asyncio()
async def test_get_subaccount_deposit_address(clientAsync):
    await clientAsync.get_subaccount_deposit_address()


@pytest.mark.asyncio()
async def test_get_subaccount_deposit_history(clientAsync):
    await clientAsync.get_subaccount_deposit_history()


@pytest.mark.asyncio()
async def test_get_subaccount_futures_margin_status(clientAsync):
    await clientAsync.get_subaccount_futures_margin_status()


@pytest.mark.asyncio()
async def test_enable_subaccount_margin(clientAsync):
    await clientAsync.enable_subaccount_margin()


@pytest.mark.asyncio()
async def test_get_subaccount_margin_details(clientAsync):
    await clientAsync.get_subaccount_margin_details()


@pytest.mark.asyncio()
async def test_get_subaccount_margin_summary(clientAsync):
    await clientAsync.get_subaccount_margin_summary()


@pytest.mark.asyncio()
async def test_enable_subaccount_futures(clientAsync):
    await clientAsync.enable_subaccount_futures()


@pytest.mark.asyncio()
async def test_get_subaccount_futures_details(clientAsync):
    await clientAsync.get_subaccount_futures_details()


@pytest.mark.asyncio()
async def test_get_subaccount_futures_summary(clientAsync):
    await clientAsync.get_subaccount_futures_summary()


@pytest.mark.asyncio()
async def test_get_subaccount_futures_positionrisk(clientAsync):
    await clientAsync.get_subaccount_futures_positionrisk()


@pytest.mark.asyncio()
async def test_make_subaccount_futures_transfer(clientAsync):
    await clientAsync.make_subaccount_futures_transfer()


@pytest.mark.asyncio()
async def test_make_subaccount_margin_transfer(clientAsync):
    await clientAsync.make_subaccount_margin_transfer()


@pytest.mark.asyncio()
async def test_make_subaccount_to_subaccount_transfer(clientAsync):
    await clientAsync.make_subaccount_to_subaccount_transfer()


@pytest.mark.asyncio()
async def test_make_subaccount_to_master_transfer(clientAsync):
    await clientAsync.make_subaccount_to_master_transfer()


@pytest.mark.asyncio()
async def test_get_subaccount_transfer_history(clientAsync):
    await clientAsync.get_subaccount_transfer_history()


@pytest.mark.asyncio()
async def test_make_subaccount_universal_transfer(clientAsync):
    await clientAsync.make_subaccount_universal_transfer()


@pytest.mark.asyncio()
async def test_get_universal_transfer_history(clientAsync):
    await clientAsync.get_universal_transfer_history()


# Futures API


@pytest.mark.asyncio()
async def test_futures_ping(clientAsync):
    await clientAsync.futures_ping()


@pytest.mark.asyncio()
async def test_futures_time(clientAsync):
    await clientAsync.futures_time()


@pytest.mark.asyncio()
async def test_futures_exchange_info(clientAsync):
    await clientAsync.futures_exchange_info()


@pytest.mark.asyncio()
async def test_futures_order_book(clientAsync):
    await clientAsync.futures_order_book()


@pytest.mark.asyncio()
async def test_futures_recent_trades(clientAsync):
    await clientAsync.futures_recent_trades()


@pytest.mark.asyncio()
async def test_futures_historical_trades(clientAsync):
    await clientAsync.futures_historical_trades()


@pytest.mark.asyncio()
async def test_futures_aggregate_trades(clientAsync):
    await clientAsync.futures_aggregate_trades()


@pytest.mark.asyncio()
async def test_futures_klines(clientAsync):
    await clientAsync.futures_klines()


@pytest.mark.asyncio()
async def test_futures_continous_klines(clientAsync):
    await clientAsync.futures_continous_klines()


@pytest.mark.asyncio()
async def test_futures_historical_klines(clientAsync):
    await clientAsync.futures_historical_klines()


@pytest.mark.asyncio()
async def test_futures_historical_klines_generator(clientAsync):
    await clientAsync.futures_historical_klines_generator()


@pytest.mark.asyncio()
async def test_futures_mark_price(clientAsync):
    await clientAsync.futures_mark_price()


@pytest.mark.asyncio()
async def test_futures_funding_rate(clientAsync):
    await clientAsync.futures_funding_rate()


@pytest.mark.asyncio()
async def test_futures_top_longshort_account_ratio(clientAsync):
    await clientAsync.futures_top_longshort_account_ratio()


@pytest.mark.asyncio()
async def test_futures_top_longshort_position_ratio(clientAsync):
    await clientAsync.futures_top_longshort_position_ratio()


@pytest.mark.asyncio()
async def test_futures_global_longshort_ratio(clientAsync):
    await clientAsync.futures_global_longshort_ratio()


@pytest.mark.asyncio()
async def test_futures_ticker(clientAsync):
    await clientAsync.futures_ticker()


@pytest.mark.asyncio()
async def test_futures_symbol_ticker(clientAsync):
    await clientAsync.futures_symbol_ticker()


@pytest.mark.asyncio()
async def test_futures_orderbook_ticker(clientAsync):
    await clientAsync.futures_orderbook_ticker()


@pytest.mark.asyncio()
async def test_futures_liquidation_orders(clientAsync):
    await clientAsync.futures_liquidation_orders()


@pytest.mark.asyncio()
async def test_futures_api_trading_status(clientAsync):
    await clientAsync.futures_api_trading_status()


@pytest.mark.asyncio()
async def test_futures_commission_rate(clientAsync):
    await clientAsync.futures_commission_rate()


@pytest.mark.asyncio()
async def test_futures_adl_quantile_estimate(clientAsync):
    await clientAsync.futures_adl_quantile_estimate()


@pytest.mark.asyncio()
async def test_futures_open_interest(clientAsync):
    await clientAsync.futures_open_interest()


@pytest.mark.asyncio()
async def test_futures_index_info(clientAsync):
    await clientAsync.futures_index_info()


@pytest.mark.asyncio()
async def test_futures_open_interest_hist(clientAsync):
    await clientAsync.futures_open_interest_hist()


@pytest.mark.asyncio()
async def test_futures_leverage_bracket(clientAsync):
    await clientAsync.futures_leverage_bracket()


@pytest.mark.asyncio()
async def test_futures_account_transfer(clientAsync):
    await clientAsync.futures_account_transfer()


@pytest.mark.asyncio()
async def test_transfer_history(clientAsync):
    await clientAsync.transfer_history()


@pytest.mark.asyncio()
async def test_futures_loan_borrow_history(clientAsync):
    await clientAsync.futures_loan_borrow_history()


@pytest.mark.asyncio()
async def test_futures_loan_repay_history(clientAsync):
    await clientAsync.futures_loan_repay_history()


@pytest.mark.asyncio()
async def test_futures_loan_wallet(clientAsync):
    await clientAsync.futures_loan_wallet()


@pytest.mark.asyncio()
async def test_futures_cross_collateral_adjust_history(clientAsync):
    await clientAsync.futures_cross_collateral_adjust_history()


@pytest.mark.asyncio()
async def test_futures_cross_collateral_liquidation_history(clientAsync):
    await clientAsync.futures_cross_collateral_liquidation_history()


@pytest.mark.asyncio()
async def test_futures_loan_interest_history(clientAsync):
    await clientAsync.futures_loan_interest_history()


@pytest.mark.asyncio()
async def test_futures_create_order(clientAsync):
    await clientAsync.futures_create_order()


@pytest.mark.asyncio()
async def test_futures_modify_order(clientAsync):
    await clientAsync.futures_modify_order()


@pytest.mark.asyncio()
async def test_futures_create_test_order(clientAsync):
    await clientAsync.futures_create_test_order()


@pytest.mark.asyncio()
async def test_futures_place_batch_order(clientAsync):
    await clientAsync.futures_place_batch_order()


@pytest.mark.asyncio()
async def test_futures_get_order(clientAsync):
    await clientAsync.futures_get_order()


@pytest.mark.asyncio()
async def test_futures_get_open_orders(clientAsync):
    await clientAsync.futures_get_open_orders()


@pytest.mark.asyncio()
async def test_futures_get_all_orders(clientAsync):
    await clientAsync.futures_get_all_orders()


@pytest.mark.asyncio()
async def test_futures_cancel_order(clientAsync):
    await clientAsync.futures_cancel_order()


@pytest.mark.asyncio()
async def test_futures_cancel_all_open_orders(clientAsync):
    await clientAsync.futures_cancel_all_open_orders()


@pytest.mark.asyncio()
async def test_futures_cancel_orders(clientAsync):
    await clientAsync.futures_cancel_orders()


@pytest.mark.asyncio()
async def test_futures_countdown_cancel_all(clientAsync):
    await clientAsync.futures_countdown_cancel_all()


@pytest.mark.asyncio()
async def test_futures_account_balance(clientAsync):
    await clientAsync.futures_account_balance()


@pytest.mark.asyncio()
async def test_futures_account(clientAsync):
    await clientAsync.futures_account()


@pytest.mark.asyncio()
async def test_futures_change_leverage(clientAsync):
    await clientAsync.futures_change_leverage()


@pytest.mark.asyncio()
async def test_futures_change_margin_type(clientAsync):
    await clientAsync.futures_change_margin_type()


@pytest.mark.asyncio()
async def test_futures_change_position_margin(clientAsync):
    await clientAsync.futures_change_position_margin()


@pytest.mark.asyncio()
async def test_futures_position_margin_history(clientAsync):
    await clientAsync.futures_position_margin_history()


@pytest.mark.asyncio()
async def test_futures_position_information(clientAsync):
    await clientAsync.futures_position_information()


@pytest.mark.asyncio()
async def test_futures_account_trades(clientAsync):
    await clientAsync.futures_account_trades()


@pytest.mark.asyncio()
async def test_futures_income_history(clientAsync):
    await clientAsync.futures_income_history()


@pytest.mark.asyncio()
async def test_futures_change_position_mode(clientAsync):
    await clientAsync.futures_change_position_mode()


@pytest.mark.asyncio()
async def test_futures_get_position_mode(clientAsync):
    await clientAsync.futures_get_position_mode()


@pytest.mark.asyncio()
async def test_futures_change_multi_assets_mode(clientAsync):
    await clientAsync.futures_change_multi_assets_mode()


@pytest.mark.asyncio()
async def test_futures_get_multi_assets_mode(clientAsync):
    await clientAsync.futures_get_multi_assets_mode()


@pytest.mark.asyncio()
async def test_futures_stream_get_listen_key(clientAsync):
    await clientAsync.futures_stream_get_listen_key()


@pytest.mark.asyncio()
async def test_futures_stream_close(clientAsync):
    await clientAsync.futures_stream_close()


# new methods
@pytest.mark.asyncio()
async def test_futures_account_config(clientAsync):
    await clientAsync.futures_account_config()


@pytest.mark.asyncio()
async def test_futures_symbol_config(clientAsync):
    await clientAsync.futures_symbol_config()


# COIN Futures API
@pytest.mark.asyncio()
async def test_futures_coin_ping(clientAsync):
    await clientAsync.futures_coin_ping()


@pytest.mark.asyncio()
async def test_futures_coin_time(clientAsync):
    await clientAsync.futures_coin_time()


@pytest.mark.asyncio()
async def test_futures_coin_exchange_info(clientAsync):
    await clientAsync.futures_coin_exchange_info()


@pytest.mark.asyncio()
async def test_futures_coin_order_book(clientAsync):
    await clientAsync.futures_coin_order_book()


@pytest.mark.asyncio()
async def test_futures_coin_recent_trades(clientAsync):
    await clientAsync.futures_coin_recent_trades()


@pytest.mark.asyncio()
async def test_futures_coin_historical_trades(clientAsync):
    await clientAsync.futures_coin_historical_trades()


@pytest.mark.asyncio()
async def test_futures_coin_aggregate_trades(clientAsync):
    await clientAsync.futures_coin_aggregate_trades()


@pytest.mark.asyncio()
async def test_futures_coin_klines(clientAsync):
    await clientAsync.futures_coin_klines()


@pytest.mark.asyncio()
async def test_futures_coin_continous_klines(clientAsync):
    await clientAsync.futures_coin_continous_klines()


@pytest.mark.asyncio()
async def test_futures_coin_index_price_klines(clientAsync):
    await clientAsync.futures_coin_index_price_klines()


@pytest.mark.asyncio()
async def test_futures_coin_mark_price_klines(clientAsync):
    await clientAsync.futures_coin_mark_price_klines()


@pytest.mark.asyncio()
async def test_futures_coin_mark_price(clientAsync):
    await clientAsync.futures_coin_mark_price()


@pytest.mark.asyncio()
async def test_futures_coin_funding_rate(clientAsync):
    await clientAsync.futures_coin_funding_rate()


@pytest.mark.asyncio()
async def test_futures_coin_ticker(clientAsync):
    await clientAsync.futures_coin_ticker()


@pytest.mark.asyncio()
async def test_futures_coin_symbol_ticker(clientAsync):
    await clientAsync.futures_coin_symbol_ticker()


@pytest.mark.asyncio()
async def test_futures_coin_orderbook_ticker(clientAsync):
    await clientAsync.futures_coin_orderbook_ticker()


@pytest.mark.asyncio()
async def test_futures_coin_liquidation_orders(clientAsync):
    await clientAsync.futures_coin_liquidation_orders()


@pytest.mark.asyncio()
async def test_futures_coin_open_interest(clientAsync):
    await clientAsync.futures_coin_open_interest()


@pytest.mark.asyncio()
async def test_futures_coin_open_interest_hist(clientAsync):
    await clientAsync.futures_coin_open_interest_hist()


@pytest.mark.asyncio()
async def test_futures_coin_leverage_bracket(clientAsync):
    await clientAsync.futures_coin_leverage_bracket()


@pytest.mark.asyncio()
async def test_new_transfer_history(clientAsync):
    await clientAsync.new_transfer_history()


@pytest.mark.asyncio()
async def test_funding_wallet(clientAsync):
    await clientAsync.funding_wallet()


@pytest.mark.asyncio()
async def test_get_user_asset(clientAsync):
    await clientAsync.get_user_asset()


@pytest.mark.asyncio()
async def test_universal_transfer(clientAsync):
    await clientAsync.universal_transfer()


@pytest.mark.asyncio()
async def test_futures_coin_create_order(clientAsync):
    await clientAsync.futures_coin_create_order()


@pytest.mark.asyncio()
async def test_futures_coin_place_batch_order(clientAsync):
    await clientAsync.futures_coin_place_batch_order()


@pytest.mark.asyncio()
async def test_futures_coin_get_order(clientAsync):
    await clientAsync.futures_coin_get_order()


@pytest.mark.asyncio()
async def test_futures_coin_get_open_orders(clientAsync):
    await clientAsync.futures_coin_get_open_orders()


@pytest.mark.asyncio()
async def test_futures_coin_get_all_orders(clientAsync):
    await clientAsync.futures_coin_get_all_orders()


@pytest.mark.asyncio()
async def test_futures_coin_cancel_order(clientAsync):
    await clientAsync.futures_coin_cancel_order()


@pytest.mark.asyncio()
async def test_futures_coin_cancel_all_open_orders(clientAsync):
    await clientAsync.futures_coin_cancel_all_open_orders()


@pytest.mark.asyncio()
async def test_futures_coin_cancel_orders(clientAsync):
    await clientAsync.futures_coin_cancel_orders()


@pytest.mark.asyncio()
async def test_futures_coin_account_balance(clientAsync):
    await clientAsync.futures_coin_account_balance()


@pytest.mark.asyncio()
async def test_futures_coin_account(clientAsync):
    await clientAsync.futures_coin_account()


@pytest.mark.asyncio()
async def test_futures_coin_change_leverage(clientAsync):
    await clientAsync.futures_coin_change_leverage()


@pytest.mark.asyncio()
async def test_futures_coin_change_margin_type(clientAsync):
    await clientAsync.futures_coin_change_margin_type()


@pytest.mark.asyncio()
async def test_futures_coin_change_position_margin(clientAsync):
    await clientAsync.futures_coin_change_position_margin()


@pytest.mark.asyncio()
async def test_futures_coin_position_margin_history(clientAsync):
    await clientAsync.futures_coin_position_margin_history()


@pytest.mark.asyncio()
async def test_futures_coin_position_information(clientAsync):
    await clientAsync.futures_coin_position_information()


@pytest.mark.asyncio()
async def test_futures_coin_account_trades(clientAsync):
    await clientAsync.futures_coin_account_trades()


@pytest.mark.asyncio()
async def test_futures_coin_income_history(clientAsync):
    await clientAsync.futures_coin_income_history()


@pytest.mark.asyncio()
async def test_futures_coin_change_position_mode(clientAsync):
    await clientAsync.futures_coin_change_position_mode()


@pytest.mark.asyncio()
async def test_futures_coin_get_position_mode(clientAsync):
    await clientAsync.futures_coin_get_position_mode()


@pytest.mark.asyncio()
async def test_futures_coin_stream_get_listen_key(clientAsync):
    await clientAsync.futures_coin_stream_get_listen_key()


@pytest.mark.asyncio()
async def test_futures_coin_stream_close(clientAsync):
    await clientAsync.futures_coin_stream_close()


@pytest.mark.asyncio()
async def test_get_all_coins_info(clientAsync):
    await clientAsync.get_all_coins_info()


@pytest.mark.asyncio()
async def test_get_account_snapshot(clientAsync):
    await clientAsync.get_account_snapshot()


@pytest.mark.asyncio()
async def test_disable_fast_withdraw_switch(clientAsync):
    await clientAsync.disable_fast_withdraw_switch()


@pytest.mark.asyncio()
async def test_enable_fast_withdraw_switch(clientAsync):
    await clientAsync.enable_fast_withdraw_switch()


# Quoting interface endpoints


@pytest.mark.asyncio()
async def test_options_ping(clientAsync):
    await clientAsync.options_ping()


@pytest.mark.asyncio()
async def test_options_time(clientAsync):
    await clientAsync.options_time()


@pytest.mark.asyncio()
async def test_options_info(clientAsync):
    await clientAsync.options_info()


@pytest.mark.asyncio()
async def test_options_exchange_info(clientAsync):
    await clientAsync.options_exchange_info()


@pytest.mark.asyncio()
async def test_options_index_price(clientAsync):
    await clientAsync.options_index_price()


@pytest.mark.asyncio()
async def test_options_price(clientAsync):
    await clientAsync.options_price()


@pytest.mark.asyncio()
async def test_options_mark_price(clientAsync):
    await clientAsync.options_mark_price()


@pytest.mark.asyncio()
async def test_options_order_book(clientAsync):
    await clientAsync.options_order_book()


@pytest.mark.asyncio()
async def test_options_klines(clientAsync):
    await clientAsync.options_klines()


@pytest.mark.asyncio()
async def test_options_recent_trades(clientAsync):
    await clientAsync.options_recent_trades()


@pytest.mark.asyncio()
async def test_options_historical_trades(clientAsync):
    await clientAsync.options_historical_trades()


# Account and trading interface endpoints


@pytest.mark.asyncio()
async def test_options_account_info(clientAsync):
    await clientAsync.options_account_info()


@pytest.mark.asyncio()
async def test_options_funds_transfer(clientAsync):
    await clientAsync.options_funds_transfer()


@pytest.mark.asyncio()
async def test_options_positions(clientAsync):
    await clientAsync.options_positions()


@pytest.mark.asyncio()
async def test_options_bill(clientAsync):
    await clientAsync.options_bill()


@pytest.mark.asyncio()
async def test_options_place_order(clientAsync):
    await clientAsync.options_place_order()


@pytest.mark.asyncio()
async def test_test_options_place_batch_order(clientAsync):
    await clientAsync.test_options_place_batch_order()


@pytest.mark.asyncio()
async def test_options_cancel_order(clientAsync):
    await clientAsync.options_cancel_order()


@pytest.mark.asyncio()
async def test_options_cancel_batch_order(clientAsync):
    await clientAsync.options_cancel_batch_order()


@pytest.mark.asyncio()
async def test_options_cancel_all_orders(clientAsync):
    await clientAsync.options_cancel_all_orders()


@pytest.mark.asyncio()
async def test_options_query_order(clientAsync):
    await clientAsync.options_query_order()


@pytest.mark.asyncio()
async def test_options_query_pending_orders(clientAsync):
    await clientAsync.options_query_pending_orders()


@pytest.mark.asyncio()
async def test_options_query_order_history(clientAsync):
    await clientAsync.options_query_order_history()


@pytest.mark.asyncio()
async def test_options_user_trades(clientAsync):
    await clientAsync.options_user_trades()


# Fiat Endpoints


@pytest.mark.asyncio()
async def test_get_fiat_deposit_withdraw_history(clientAsync):
    await clientAsync.get_fiat_deposit_withdraw_history()


@pytest.mark.asyncio()
async def test_get_fiat_payments_history(clientAsync):
    await clientAsync.get_fiat_payments_history()


# C2C Endpoints


@pytest.mark.asyncio()
async def test_get_c2c_trade_history(clientAsync):
    await clientAsync.get_c2c_trade_history()


# Pay Endpoints


@pytest.mark.asyncio()
async def test_get_pay_trade_history(clientAsync):
    await clientAsync.get_pay_trade_history()


# Convert Endpoints


@pytest.mark.asyncio()
async def test_get_convert_trade_history(clientAsync):
    await clientAsync.get_convert_trade_history()


@pytest.mark.asyncio()
async def test_convert_request_quote(clientAsync):
    await clientAsync.convert_request_quote()


@pytest.mark.asyncio()
async def test_convert_accept_quote(clientAsync):
    await clientAsync.convert_accept_quote()


@pytest.mark.asyncio()
async def test_papi_get_balance(clientAsync):
    await clientAsync.papi_get_balance()


@pytest.mark.asyncio()
async def test_papi_get_account(clientAsync):
    await clientAsync.papi_get_account()


@pytest.mark.asyncio()
async def test_papi_get_margin_max_borrowable(clientAsync):
    await clientAsync.papi_get_margin_max_borrowable()


@pytest.mark.asyncio()
async def test_papi_get_margin_max_withdraw(clientAsync):
    await clientAsync.papi_get_margin_max_withdraw()


@pytest.mark.asyncio()
async def test_papi_get_um_position_risk(clientAsync):
    await clientAsync.papi_get_um_position_risk()


@pytest.mark.asyncio()
async def test_papi_get_cm_position_risk(clientAsync):
    await clientAsync.papi_get_cm_position_risk()


@pytest.mark.asyncio()
async def test_papi_set_um_leverage(clientAsync):
    await clientAsync.papi_set_um_leverage()


@pytest.mark.asyncio()
async def test_papi_set_cm_leverage(clientAsync):
    await clientAsync.papi_set_cm_leverage()


@pytest.mark.asyncio()
async def test_papi_change_um_position_side_dual(clientAsync):
    await clientAsync.papi_change_um_position_side_dual()


@pytest.mark.asyncio()
async def test_papi_get_um_position_side_dual(clientAsync):
    await clientAsync.papi_get_um_position_side_dual()


@pytest.mark.asyncio()
async def test_papi_get_cm_position_side_dual(clientAsync):
    await clientAsync.papi_get_cm_position_side_dual()


@pytest.mark.asyncio()
async def test_papi_get_um_leverage_bracket(clientAsync):
    await clientAsync.papi_get_um_leverage_bracket()


@pytest.mark.asyncio()
async def test_papi_get_cm_leverage_bracket(clientAsync):
    await clientAsync.papi_get_cm_leverage_bracket()


@pytest.mark.asyncio()
async def test_papi_get_um_api_trading_status(clientAsync):
    await clientAsync.papi_get_um_api_trading_status()


@pytest.mark.asyncio()
async def test_papi_get_um_comission_rate(clientAsync):
    await clientAsync.papi_get_um_comission_rate()


@pytest.mark.asyncio()
async def test_papi_get_cm_comission_rate(clientAsync):
    await clientAsync.papi_get_cm_comission_rate()


@pytest.mark.asyncio()
async def test_papi_get_margin_margin_loan(clientAsync):
    await clientAsync.papi_get_margin_margin_loan()


@pytest.mark.asyncio()
async def test_papi_get_margin_repay_loan(clientAsync):
    await clientAsync.papi_get_margin_repay_loan()


@pytest.mark.asyncio()
async def test_papi_get_repay_futures_switch(clientAsync):
    await clientAsync.papi_get_repay_futures_switch()


@pytest.mark.asyncio()
async def test_papi_repay_futures_switch(clientAsync):
    await clientAsync.papi_repay_futures_switch()


@pytest.mark.asyncio()
async def test_papi_get_margin_interest_history(clientAsync):
    await clientAsync.papi_get_margin_interest_history()


@pytest.mark.asyncio()
async def test_papi_repay_futures_negative_balance(clientAsync):
    await clientAsync.papi_repay_futures_negative_balance()


@pytest.mark.asyncio()
async def test_papi_get_portfolio_interest_history(clientAsync):
    await clientAsync.papi_get_portfolio_interest_history()


@pytest.mark.asyncio()
async def test_papi_fund_auto_collection(clientAsync):
    await clientAsync.papi_fund_auto_collection()


@pytest.mark.asyncio()
async def test_papi_fund_asset_collection(clientAsync):
    await clientAsync.papi_fund_asset_collection()


@pytest.mark.asyncio()
async def test_papi_bnb_transfer(clientAsync):
    await clientAsync.papi_bnb_transfer()


@pytest.mark.asyncio()
async def test_papi_get_um_income_history(clientAsync):
    await clientAsync.papi_get_um_income_history()


@pytest.mark.asyncio()
async def test_papi_get_cm_income_history(clientAsync):
    await clientAsync.papi_get_cm_income_history()


@pytest.mark.asyncio()
async def test_papi_get_um_account(clientAsync):
    await clientAsync.papi_get_um_account()


@pytest.mark.asyncio()
async def test_papi_get_um_account_v2(clientAsync):
    await clientAsync.papi_get_um_account_v2()


@pytest.mark.asyncio()
async def test_papi_get_cm_account(clientAsync):
    await clientAsync.papi_get_cm_account()


@pytest.mark.asyncio()
async def test_papi_get_um_account_config(clientAsync):
    await clientAsync.papi_get_um_account_config()


@pytest.mark.asyncio()
async def test_papi_get_um_symbol_config(clientAsync):
    await clientAsync.papi_get_um_symbol_config()


@pytest.mark.asyncio()
async def test_papi_get_um_trade_asyn(clientAsync):
    await clientAsync.papi_get_um_trade_asyn()


@pytest.mark.asyncio()
async def test_papi_get_um_trade_asyn_id(clientAsync):
    await clientAsync.papi_get_um_trade_asyn_id()


@pytest.mark.asyncio()
async def test_papi_get_um_order_asyn(clientAsync):
    await clientAsync.papi_get_um_order_asyn()


@pytest.mark.asyncio()
async def test_papi_get_um_order_asyn_id(clientAsync):
    await clientAsync.papi_get_um_order_asyn_id()


@pytest.mark.asyncio()
async def test_papi_get_um_income_asyn(clientAsync):
    await clientAsync.papi_get_um_income_asyn()


@pytest.mark.asyncio()
async def test_papi_get_um_income_asyn_id(clientAsync):
    await clientAsync.papi_get_um_income_asyn_id()


# Public papi endpoints


@pytest.mark.asyncio()
async def test_papi_ping(clientAsync):
    await clientAsync.papi_ping()


# Trade papi endpoints


@pytest.mark.asyncio()
async def test_papi_create_um_order(clientAsync):
    await clientAsync.papi_create_um_order()


@pytest.mark.asyncio()
async def test_papi_create_um_conditional_order(clientAsync):
    await clientAsync.papi_create_um_conditional_order()


@pytest.mark.asyncio()
async def test_papi_create_cm_order(clientAsync):
    await clientAsync.papi_create_cm_order()


@pytest.mark.asyncio()
async def test_papi_create_cm_conditional_order(clientAsync):
    await clientAsync.papi_create_cm_conditional_order()


@pytest.mark.asyncio()
async def test_papi_create_margin_order(clientAsync):
    await clientAsync.papi_create_margin_order()


@pytest.mark.asyncio()
async def test_papi_margin_loan(clientAsync):
    await clientAsync.papi_margin_loan()


@pytest.mark.asyncio()
async def test_papi_repay_loan(clientAsync):
    await clientAsync.papi_repay_loan()


@pytest.mark.asyncio()
async def test_papi_margin_order_oco(clientAsync):
    await clientAsync.papi_margin_order_oco()


@pytest.mark.asyncio()
async def test_papi_cancel_um_order(clientAsync):
    await clientAsync.papi_cancel_um_order()


@pytest.mark.asyncio()
async def test_papi_cancel_um_all_open_orders(clientAsync):
    await clientAsync.papi_cancel_um_all_open_orders()


@pytest.mark.asyncio()
async def test_papi_cancel_um_conditional_order(clientAsync):
    await clientAsync.papi_cancel_um_conditional_order()


@pytest.mark.asyncio()
async def test_papi_cancel_um_conditional_all_open_orders(clientAsync):
    await clientAsync.papi_cancel_um_conditional_all_open_orders()


@pytest.mark.asyncio()
async def test_papi_cancel_cm_order(clientAsync):
    await clientAsync.papi_cancel_cm_order()


@pytest.mark.asyncio()
async def test_papi_cancel_cm_all_open_orders(clientAsync):
    await clientAsync.papi_cancel_cm_all_open_orders()


@pytest.mark.asyncio()
async def test_papi_cancel_cm_conditional_order(clientAsync):
    await clientAsync.papi_cancel_cm_conditional_order()


@pytest.mark.asyncio()
async def test_papi_cancel_cm_conditional_all_open_orders(clientAsync):
    await clientAsync.papi_cancel_cm_conditional_all_open_orders()


@pytest.mark.asyncio()
async def test_papi_cancel_margin_order(clientAsync):
    await clientAsync.papi_cancel_margin_order()


@pytest.mark.asyncio()
async def test_papi_cancel_margin_order_list(clientAsync):
    await clientAsync.papi_cancel_margin_order_list()


@pytest.mark.asyncio()
async def test_papi_cancel_margin_all_open_orders(clientAsync):
    await clientAsync.papi_cancel_margin_all_open_orders()


@pytest.mark.asyncio()
async def test_papi_modify_um_order(clientAsync):
    await clientAsync.papi_modify_um_order()


@pytest.mark.asyncio()
async def test_papi_modify_cm_order(clientAsync):
    await clientAsync.papi_modify_cm_order()


@pytest.mark.asyncio()
async def test_papi_get_um_order(clientAsync):
    await clientAsync.papi_get_um_order()


@pytest.mark.asyncio()
async def test_papi_get_um_all_orders(clientAsync):
    await clientAsync.papi_get_um_all_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_open_order(clientAsync):
    await clientAsync.papi_get_um_open_order()


@pytest.mark.asyncio()
async def test_papi_get_um_open_orders(clientAsync):
    await clientAsync.papi_get_um_open_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_conditional_all_orders(clientAsync):
    await clientAsync.papi_get_um_conditional_all_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_conditional_open_orders(clientAsync):
    await clientAsync.papi_get_um_conditional_open_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_conditional_open_order(clientAsync):
    await clientAsync.papi_get_um_conditional_open_order()


@pytest.mark.asyncio()
async def test_papi_get_um_conditional_order_history(clientAsync):
    await clientAsync.papi_get_um_conditional_order_history()


@pytest.mark.asyncio()
async def test_papi_get_cm_order(clientAsync):
    await clientAsync.papi_get_cm_order()


@pytest.mark.asyncio()
async def test_papi_get_cm_all_orders(clientAsync):
    await clientAsync.papi_get_cm_all_orders()


@pytest.mark.asyncio()
async def test_papi_get_cm_open_order(clientAsync):
    await clientAsync.papi_get_cm_open_order()


@pytest.mark.asyncio()
async def test_papi_get_cm_open_orders(clientAsync):
    await clientAsync.papi_get_cm_open_orders()


@pytest.mark.asyncio()
async def test_papi_get_cm_conditional_all_orders(clientAsync):
    await clientAsync.papi_get_cm_conditional_all_orders()


@pytest.mark.asyncio()
async def test_papi_get_cm_conditional_open_orders(clientAsync):
    await clientAsync.papi_get_cm_conditional_open_orders()


@pytest.mark.asyncio()
async def test_papi_get_cm_conditional_open_order(clientAsync):
    await clientAsync.papi_get_cm_conditional_open_order()


@pytest.mark.asyncio()
async def test_papi_get_cm_conditional_order_history(clientAsync):
    await clientAsync.papi_get_cm_conditional_order_history()


@pytest.mark.asyncio()
async def test_papi_get_um_force_orders(clientAsync):
    await clientAsync.papi_get_um_force_orders()


@pytest.mark.asyncio()
async def test_papi_get_cm_force_orders(clientAsync):
    await clientAsync.papi_get_cm_force_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_order_amendment(clientAsync):
    await clientAsync.papi_get_um_order_amendment()


@pytest.mark.asyncio()
async def test_papi_get_cm_order_amendment(clientAsync):
    await clientAsync.papi_get_cm_order_amendment()


@pytest.mark.asyncio()
async def test_papi_get_margin_force_orders(clientAsync):
    await clientAsync.papi_get_margin_force_orders()


@pytest.mark.asyncio()
async def test_papi_get_um_user_trades(clientAsync):
    await clientAsync.papi_get_um_user_trades()


@pytest.mark.asyncio()
async def test_papi_get_cm_user_trades(clientAsync):
    await clientAsync.papi_get_cm_user_trades()


@pytest.mark.asyncio()
async def test_papi_get_um_adl_quantile(clientAsync):
    await clientAsync.papi_get_um_adl_quantile()


@pytest.mark.asyncio()
async def test_papi_get_cm_adl_quantile(clientAsync):
    await clientAsync.papi_get_cm_adl_quantile()


@pytest.mark.asyncio()
async def test_papi_set_um_fee_burn(clientAsync):
    await clientAsync.papi_set_um_fee_burn()


@pytest.mark.asyncio()
async def test_papi_get_um_fee_burn(clientAsync):
    await clientAsync.papi_get_um_fee_burn()


@pytest.mark.asyncio()
async def test_papi_get_margin_order(clientAsync):
    await clientAsync.papi_get_margin_order()


@pytest.mark.asyncio()
async def test_papi_get_margin_open_orders(clientAsync):
    await clientAsync.papi_get_margin_open_orders()


@pytest.mark.asyncio()
async def test_papi_get_margin_all_orders(clientAsync):
    await clientAsync.papi_get_margin_all_orders()


@pytest.mark.asyncio()
async def test_papi_get_margin_order_list(clientAsync):
    await clientAsync.papi_get_margin_order_list()


@pytest.mark.asyncio()
async def test_papi_get_margin_all_order_list(clientAsync):
    await clientAsync.papi_get_margin_all_order_list()


@pytest.mark.asyncio()
async def test_papi_get_margin_open_order_list(clientAsync):
    await clientAsync.papi_get_margin_open_order_list()


@pytest.mark.asyncio()
async def test_papi_get_margin_my_trades(clientAsync):
    await clientAsync.papi_get_margin_my_trades()


@pytest.mark.asyncio()
async def test_papi_get_margin_repay_debt(clientAsync):
    await clientAsync.papi_get_margin_repay_debt()


@pytest.mark.asyncio()
async def test_close_connection(clientAsync):
    await clientAsync.close_connection()


#########################
# Websocket API Requests #
#########################


@pytest.mark.asyncio()
async def test_ws_get_order_book(clientAsync):
    await clientAsync.ws_get_order_book(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_recent_trades(clientAsync):
    await clientAsync.ws_get_recent_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_historical_trades(clientAsync):
    await clientAsync.ws_get_historical_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_aggregate_trades(clientAsync):
    await clientAsync.ws_get_aggregate_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_klines(clientAsync):
    await clientAsync.ws_get_klines(symbol="BTCUSDT", interval="1m")


@pytest.mark.asyncio()
async def test_ws_get_uiKlines(clientAsync):
    await clientAsync.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")


@pytest.mark.asyncio()
async def test_ws_get_avg_price(clientAsync):
    await clientAsync.ws_get_avg_price(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_ticker(clientAsync):
    ticker = await clientAsync.ws_get_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_trading_day_ticker(clientAsync):
    await clientAsync.ws_get_trading_day_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_symbol_ticker_window(clientAsync):
    await clientAsync.ws_get_symbol_ticker_window(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_symbol_ticker(clientAsync):
    await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_orderbook_ticker(clientAsync):
    await clientAsync.ws_get_orderbook_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_ping(clientAsync):
    await clientAsync.ws_ping()


@pytest.mark.asyncio()
async def test_ws_get_time(clientAsync):
    await clientAsync.ws_get_time()


@pytest.mark.asyncio()
async def test_ws_get_exchange_info(clientAsync):
    await clientAsync.ws_get_exchange_info(symbol="BTCUSDT")
