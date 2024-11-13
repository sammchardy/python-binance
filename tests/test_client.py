def test_client_initialization(client):
    assert client.API_KEY is not None
    assert client.API_SECRET is not None


# TODO: whitelist in proxy to pass test
# def test_get_products(client):
#     client.get_products()


def test_get_exchange_info(client):
    client.get_exchange_info()


def test_get_symbol_info(client):
    client.get_symbol_info("BTCUSDT")


def test_ping(client):
    client.ping()


def test_get_server_time(client):
    client.get_server_time()


def test_get_all_tickers(client):
    client.get_all_tickers()


def test_get_orderbook_tickers(client):
    client.get_orderbook_tickers()


def test_get_order_book(client):
    client.get_order_book(symbol="BTCUSDT")


def test_get_recent_trades(client):
    client.get_recent_trades(symbol="BTCUSDT")


def test_get_historical_trades(client):
    client.get_historical_trades(symbol="BTCUSDT")


def test_get_aggregate_trades(client):
    client.get_aggregate_trades(symbol="BTCUSDT")


def test_get_klines(client):
    client.get_klines(symbol="BTCUSDT", interval="1d")


def test_get_avg_price(client):
    client.get_avg_price(symbol="BTCUSDT")


def test_get_ticker(client):
    client.get_ticker(symbol="BTCUSDT")


def test_get_symbol_ticker(client):
    client.get_symbol_ticker(symbol="BTCUSDT")


def test_get_orderbook_ticker(client):
    client.get_orderbook_ticker(symbol="BTCUSDT")


def test_get_account(client):
    client.get_account()


def test_get_asset_balance(client):
    client.get_asset_balance(asset="BTC")


def test_get_my_trades(client):
    client.get_my_trades(symbol="BTCUSDT")


def test_get_system_status(client):
    client.get_system_status()


# TODO: Tests not working on testnet
# def test_get_account_status(client):
#     client.get_account_status()


# def test_get_account_api_trading_status(client):
#     client.get_account_api_trading_status()


# def test_get_account_api_permissions(client):
#     client.get_account_api_permissions()


# def test_get_dust_assets(client):
#     client.get_dust_assets()


def test_get_dust_log(client):
    client.test_get_dust_log()


def test_transfer_dust(client):
    client.transfer_dust()


def test_get_asset_dividend_history(client):
    client.get_asset_dividend_history()


def test_make_universal_transfer(client):
    client.make_universal_transfer()


def test_query_universal_transfer_history(client):
    client.query_universal_transfer_history()


def test_get_trade_fee(client):
    client.get_trade_fee()


def test_get_asset_details(client):
    client.get_asset_details()


def test_get_spot_delist_schedule(client):
    client.get_spot_delist_schedule()


# Withdraw Endpoints


def test_withdraw(client):
    client.withdraw()


def test_get_deposit_history(client):
    client.get_deposit_history()


def test_get_withdraw_history(client):
    client.get_withdraw_history()


def test_get_withdraw_history_id(client):
    client.get_withdraw_history_id()


def test_get_deposit_address(client):
    client.get_deposit_address()


# User Stream Endpoints


def test_stream_get_listen_key(client):
    client.stream_get_listen_key()


def test_stream_close(client):
    client.stream_close()


# Margin Trading Endpoints


def test_get_margin_account(client):
    client.get_margin_account()


def test_get_isolated_margin_account(client):
    client.get_isolated_margin_account()


def test_enable_isolated_margin_account(client):
    client.enable_isolated_margin_account()


def test_disable_isolated_margin_account(client):
    client.disable_isolated_margin_account()


def test_get_enabled_isolated_margin_account_limit(client):
    client.get_enabled_isolated_margin_account_limit()


def test_get_margin_dustlog(client):
    client.get_margin_dustlog()


def test_get_margin_dust_assets(client):
    client.get_margin_dust_assets()


def test_transfer_margin_dust(client):
    client.transfer_margin_dust()


def test_get_cross_margin_collateral_ratio(client):
    client.get_cross_margin_collateral_ratio()


def test_get_small_liability_exchange_assets(client):
    client.get_small_liability_exchange_assets()


def test_exchange_small_liability_assets(client):
    client.exchange_small_liability_assets()


def test_get_small_liability_exchange_history(client):
    client.get_small_liability_exchange_history()


def test_get_future_hourly_interest_rate(client):
    client.get_future_hourly_interest_rate()


def test_get_margin_capital_flow(client):
    client.get_margin_capital_flow()


def test_get_margin_asset(client):
    client.get_margin_asset()


def test_get_margin_symbol(client):
    client.get_margin_symbol()


def test_get_margin_all_assets(client):
    client.get_margin_all_assets()


def test_get_margin_all_pairs(client):
    client.get_margin_all_pairs()


def test_create_isolated_margin_account(client):
    client.create_isolated_margin_account()


def test_get_isolated_margin_symbol(client):
    client.get_isolated_margin_symbol()


def test_get_all_isolated_margin_symbols(client):
    client.get_all_isolated_margin_symbols()


def test_get_isolated_margin_fee_data(client):
    client.get_isolated_margin_fee_data()


def test_get_isolated_margin_tier_data(client):
    client.get_isolated_margin_tier_data()


def test_margin_manual_liquidation(client):
    client.margin_manual_liquidation()


def test_toggle_bnb_burn_spot_margin(client):
    client.toggle_bnb_burn_spot_margin()


def test_get_bnb_burn_spot_margin(client):
    client.get_bnb_burn_spot_margin()


def test_get_margin_price_index(client):
    client.get_margin_price_index()


def test_transfer_margin_to_spot(client):
    client.transfer_margin_to_spot()


def test_transfer_spot_to_margin(client):
    client.transfer_spot_to_margin()


def test_transfer_isolated_margin_to_spot(client):
    client.transfer_isolated_margin_to_spot()


def test_transfer_spot_to_isolated_margin(client):
    client.transfer_spot_to_isolated_margin()


def test_get_isolated_margin_tranfer_history(client):
    client.get_isolated_margin_tranfer_history()


def test_create_margin_loan(client):
    client.create_margin_loan()


def test_repay_margin_loan(client):
    client.repay_margin_loan()


def create_margin_ordertest_(client):
    client.create_margin_order()


def test_cancel_margin_order(client):
    client.cancel_margin_order()


def test_set_margin_max_leverage(client):
    client.set_margin_max_leverage()


def test_get_margin_transfer_history(client):
    client.get_margin_transfer_history()


def test_get_margin_loan_details(client):
    client.get_margin_loan_details()


def test_get_margin_repay_details(client):
    client.get_margin_repay_details()


def test_get_cross_margin_data(client):
    client.get_cross_margin_data()


def test_get_margin_interest_history(client):
    client.get_margin_interest_history()


def test_get_margin_force_liquidation_rec(client):
    client.get_margin_force_liquidation_rec()


def test_get_margin_order(client):
    client.get_margin_order()


def test_get_open_margin_orders(client):
    client.get_open_margin_orders()


def test_get_all_margin_orders(client):
    client.get_all_margin_orders()


def test_get_margin_trades(client):
    client.get_margin_trades()


def test_get_max_margin_loan(client):
    client.get_max_margin_loan()


def test_get_max_margin_transfer(client):
    client.get_max_margin_transfer()


def test_get_margin_delist_schedule(client):
    client.get_margin_delist_schedule()


# Margin OCO


def test_create_margin_oco_order(client):
    client.create_margin_oco_order()


def test_cancel_margin_oco_order(client):
    client.cancel_margin_oco_order()


def test_get_margin_oco_order(client):
    client.get_margin_oco_order()


def test_get_open_margin_oco_orders(client):
    client.get_open_margin_oco_orders()


# Cross-margin


def test_margin_stream_get_listen_key(client):
    client.margin_stream_get_listen_key()


def test_margin_stream_close(client):
    client.margin_stream_close()


# Isolated margin


def test_isolated_margin_stream_get_listen_key(client):
    client.isolated_margin_stream_get_listen_key()


def test_isolated_margin_stream_close(client):
    client.isolated_margin_stream_close()


# Simple Earn Endpoints


def test_get_simple_earn_flexible_product_list(client):
    client.get_simple_earn_flexible_product_list()


def test_get_simple_earn_locked_product_list(client):
    client.get_simple_earn_locked_product_list()


def test_subscribe_simple_earn_flexible_product(client):
    client.subscribe_simple_earn_flexible_product()


def test_subscribe_simple_earn_locked_product(client):
    client.subscribe_simple_earn_locked_product()


def test_redeem_simple_earn_flexible_product(client):
    client.redeem_simple_earn_flexible_product()


def test_redeem_simple_earn_locked_product(client):
    client.redeem_simple_earn_locked_product()


def test_get_simple_earn_flexible_product_position(client):
    client.get_simple_earn_flexible_product_position()


def test_get_simple_earn_locked_product_position(client):
    client.get_simple_earn_locked_product_position()


def test_get_simple_earn_account(client):
    client.get_simple_earn_account()


# Lending Endpoints


def test_get_fixed_activity_project_list(client):
    client.get_fixed_activity_project_list()


def test_change_fixed_activity_to_daily_position(client):
    client.change_fixed_activity_to_daily_position()


# Staking Endpoints


def test_get_staking_product_list(client):
    client.get_staking_product_list()


def test_purchase_staking_product(client):
    client.purchase_staking_product()


def test_redeem_staking_product(client):
    client.redeem_staking_product()


def test_get_staking_position(client):
    client.get_staking_position()


def test_get_staking_purchase_history(client):
    client.get_staking_purchase_history()


def test_set_auto_staking(client):
    client.set_auto_staking()


def test_get_personal_left_quota(client):
    client.get_personal_left_quota()


# US Staking Endpoints


def test_get_staking_asset_us(client):
    client.get_staking_asset_us()


def test_stake_asset_us(client):
    client.stake_asset_us()


def test_unstake_asset_us(client):
    client.unstake_asset_us()


def test_get_staking_balance_us(client):
    client.get_staking_balance_us()


def test_get_staking_history_us(client):
    client.get_staking_history_us()


def test_get_staking_rewards_history_us(client):
    client.get_staking_rewards_history_us()


# Sub Accounts


def test_get_sub_account_list(client):
    client.get_sub_account_list()


def test_get_sub_account_transfer_history(client):
    client.get_sub_account_transfer_history()


def test_get_sub_account_futures_transfer_history(client):
    client.get_sub_account_futures_transfer_history()


def test_create_sub_account_futures_transfer(client):
    client.create_sub_account_futures_transfer()


def test_get_sub_account_assets(client):
    client.get_sub_account_assets()


def test_query_subaccount_spot_summary(client):
    client.query_subaccount_spot_summary()


def test_get_subaccount_deposit_address(client):
    client.get_subaccount_deposit_address()


def test_get_subaccount_deposit_history(client):
    client.get_subaccount_deposit_history()


def test_get_subaccount_futures_margin_status(client):
    client.get_subaccount_futures_margin_status()


def test_enable_subaccount_margin(client):
    client.enable_subaccount_margin()


def test_get_subaccount_margin_details(client):
    client.get_subaccount_margin_details()


def test_get_subaccount_margin_summary(client):
    client.get_subaccount_margin_summary()


def test_enable_subaccount_futures(client):
    client.enable_subaccount_futures()


def test_get_subaccount_futures_details(client):
    client.get_subaccount_futures_details()


def test_get_subaccount_futures_summary(client):
    client.get_subaccount_futures_summary()


def test_get_subaccount_futures_positionrisk(client):
    client.get_subaccount_futures_positionrisk()


def test_make_subaccount_futures_transfer(client):
    client.make_subaccount_futures_transfer()


def test_make_subaccount_margin_transfer(client):
    client.make_subaccount_margin_transfer()


def test_make_subaccount_to_subaccount_transfer(client):
    client.make_subaccount_to_subaccount_transfer()


def test_make_subaccount_to_master_transfer(client):
    client.make_subaccount_to_master_transfer()


def test_get_subaccount_transfer_history(client):
    client.get_subaccount_transfer_history()


def test_make_subaccount_universal_transfer(client):
    client.make_subaccount_universal_transfer()


def test_get_universal_transfer_history(client):
    client.get_universal_transfer_history()


# Futures API


def test_futures_ping(client):
    client.futures_ping()


def test_futures_time(client):
    client.futures_time()


def test_futures_exchange_info(client):
    client.futures_exchange_info()


def test_futures_order_book(client):
    client.futures_order_book()


def test_futures_recent_trades(client):
    client.futures_recent_trades()


def test_futures_historical_trades(client):
    client.futures_historical_trades()


def test_futures_aggregate_trades(client):
    client.futures_aggregate_trades()


def test_futures_klines(client):
    client.futures_klines()


def test_futures_continous_klines(client):
    client.futures_continous_klines()


def test_futures_historical_klines(client):
    client.futures_historical_klines()


def test_futures_historical_klines_generator(client):
    client.futures_historical_klines_generator()


def test_futures_mark_price(client):
    client.futures_mark_price()


def test_futures_funding_rate(client):
    client.futures_funding_rate()


def test_futures_top_longshort_account_ratio(client):
    client.futures_top_longshort_account_ratio()


def test_futures_top_longshort_position_ratio(client):
    client.futures_top_longshort_position_ratio()


def test_futures_global_longshort_ratio(client):
    client.futures_global_longshort_ratio()


def test_futures_ticker(client):
    client.futures_ticker()


def test_futures_symbol_ticker(client):
    client.futures_symbol_ticker()


def test_futures_orderbook_ticker(client):
    client.futures_orderbook_ticker()


def test_futures_liquidation_orders(client):
    client.futures_liquidation_orders()


def test_futures_api_trading_status(client):
    client.futures_api_trading_status()


def test_futures_commission_rate(client):
    client.futures_commission_rate()


def test_futures_adl_quantile_estimate(client):
    client.futures_adl_quantile_estimate()


def test_futures_open_interest(client):
    client.futures_open_interest()


def test_futures_index_info(client):
    client.futures_index_info()


def test_futures_open_interest_hist(client):
    client.futures_open_interest_hist()


def test_futures_leverage_bracket(client):
    client.futures_leverage_bracket()


def test_futures_account_transfer(client):
    client.futures_account_transfer()


def test_transfer_history(client):
    client.transfer_history()


def test_futures_loan_borrow_history(client):
    client.futures_loan_borrow_history()


def test_futures_loan_repay_history(client):
    client.futures_loan_repay_history()


def test_futures_loan_wallet(client):
    client.futures_loan_wallet()


def test_futures_cross_collateral_adjust_history(client):
    client.futures_cross_collateral_adjust_history()


def test_futures_cross_collateral_liquidation_history(client):
    client.futures_cross_collateral_liquidation_history()


def test_futures_loan_interest_history(client):
    client.futures_loan_interest_history()


def test_futures_create_order(client):
    client.futures_create_order()


def test_futures_modify_order(client):
    client.futures_modify_order()


def test_futures_create_test_order(client):
    client.futures_create_test_order()


def test_futures_place_batch_order(client):
    client.futures_place_batch_order()


def test_futures_get_order(client):
    client.futures_get_order()


def test_futures_get_open_orders(client):
    client.futures_get_open_orders()


def test_futures_get_all_orders(client):
    client.futures_get_all_orders()


def test_futures_cancel_order(client):
    client.futures_cancel_order()


def test_futures_cancel_all_open_orders(client):
    client.futures_cancel_all_open_orders()


def test_futures_cancel_orders(client):
    client.futures_cancel_orders()


def test_futures_countdown_cancel_all(client):
    client.futures_countdown_cancel_all()


def test_futures_account_balance(client):
    client.futures_account_balance()


def test_futures_account(client):
    client.futures_account()


def test_futures_change_leverage(client):
    client.futures_change_leverage()


def test_futures_change_margin_type(client):
    client.futures_change_margin_type()


def test_futures_change_position_margin(client):
    client.futures_change_position_margin()


def test_futures_position_margin_history(client):
    client.futures_position_margin_history()


def test_futures_position_information(client):
    client.futures_position_information()


def test_futures_account_trades(client):
    client.futures_account_trades()


def test_futures_income_history(client):
    client.futures_income_history()


def test_futures_change_position_mode(client):
    client.futures_change_position_mode()


def test_futures_get_position_mode(client):
    client.futures_get_position_mode()


def test_futures_change_multi_assets_mode(client):
    client.futures_change_multi_assets_mode()


def test_futures_get_multi_assets_mode(client):
    client.futures_get_multi_assets_mode()


def test_futures_stream_get_listen_key(client):
    client.futures_stream_get_listen_key()


def test_futures_stream_close(client):
    client.futures_stream_close()


# new methods
def test_futures_account_config(client):
    client.futures_account_config()


def test_futures_symbol_config(client):
    client.futures_symbol_config()


# COIN Futures API
def test_futures_coin_ping(client):
    client.futures_coin_ping()


def test_futures_coin_time(client):
    client.futures_coin_time()


def test_futures_coin_exchange_info(client):
    client.futures_coin_exchange_info()


def test_futures_coin_order_book(client):
    client.futures_coin_order_book()


def test_futures_coin_recent_trades(client):
    client.futures_coin_recent_trades()


def test_futures_coin_historical_trades(client):
    client.futures_coin_historical_trades()


def test_futures_coin_aggregate_trades(client):
    client.futures_coin_aggregate_trades()


def test_futures_coin_klines(client):
    client.futures_coin_klines()


def test_futures_coin_continous_klines(client):
    client.futures_coin_continous_klines()


def test_futures_coin_index_price_klines(client):
    client.futures_coin_index_price_klines()


def test_futures_coin_mark_price_klines(client):
    client.futures_coin_mark_price_klines()


def test_futures_coin_mark_price(client):
    client.futures_coin_mark_price()


def test_futures_coin_funding_rate(client):
    client.futures_coin_funding_rate()


def test_futures_coin_ticker(client):
    client.futures_coin_ticker()


def test_futures_coin_symbol_ticker(client):
    client.futures_coin_symbol_ticker()


def test_futures_coin_orderbook_ticker(client):
    client.futures_coin_orderbook_ticker()


def test_futures_coin_liquidation_orders(client):
    client.futures_coin_liquidation_orders()


def test_futures_coin_open_interest(client):
    client.futures_coin_open_interest()


def test_futures_coin_open_interest_hist(client):
    client.futures_coin_open_interest_hist()


def test_futures_coin_leverage_bracket(client):
    client.futures_coin_leverage_bracket()


def test_new_transfer_history(client):
    client.new_transfer_history()


def test_funding_wallet(client):
    client.funding_wallet()


def test_get_user_asset(client):
    client.get_user_asset()


def test_universal_transfer(client):
    client.universal_transfer()


def test_futures_coin_create_order(client):
    client.futures_coin_create_order()


def test_futures_coin_place_batch_order(client):
    client.futures_coin_place_batch_order()


def test_futures_coin_get_order(client):
    client.futures_coin_get_order()


def test_futures_coin_get_open_orders(client):
    client.futures_coin_get_open_orders()


def test_futures_coin_get_all_orders(client):
    client.futures_coin_get_all_orders()


def test_futures_coin_cancel_order(client):
    client.futures_coin_cancel_order()


def test_futures_coin_cancel_all_open_orders(client):
    client.futures_coin_cancel_all_open_orders()


def test_futures_coin_cancel_orders(client):
    client.futures_coin_cancel_orders()


def test_futures_coin_account_balance(client):
    client.futures_coin_account_balance()


def test_futures_coin_account(client):
    client.futures_coin_account()


def test_futures_coin_change_leverage(client):
    client.futures_coin_change_leverage()


def test_futures_coin_change_margin_type(client):
    client.futures_coin_change_margin_type()


def test_futures_coin_change_position_margin(client):
    client.futures_coin_change_position_margin()


def test_futures_coin_position_margin_history(client):
    client.futures_coin_position_margin_history()


def test_futures_coin_position_information(client):
    client.futures_coin_position_information()


def test_futures_coin_account_trades(client):
    client.futures_coin_account_trades()


def test_futures_coin_income_history(client):
    client.futures_coin_income_history()


def test_futures_coin_change_position_mode(client):
    client.futures_coin_change_position_mode()


def test_futures_coin_get_position_mode(client):
    client.futures_coin_get_position_mode()


def test_futures_coin_stream_get_listen_key(client):
    client.futures_coin_stream_get_listen_key()


def test_futures_coin_stream_close(client):
    client.futures_coin_stream_close()


def test_get_all_coins_info(client):
    client.get_all_coins_info()


def test_get_account_snapshot(client):
    client.get_account_snapshot()


def test_disable_fast_withdraw_switch(client):
    client.disable_fast_withdraw_switch()


def test_enable_fast_withdraw_switch(client):
    client.enable_fast_withdraw_switch()


# Quoting interface endpoints


def test_options_ping(client):
    client.options_ping()


def test_options_time(client):
    client.options_time()


def test_options_info(client):
    client.options_info()


def test_options_exchange_info(client):
    client.options_exchange_info()


def test_options_index_price(client):
    client.options_index_price()


def test_options_price(client):
    client.options_price()


def test_options_mark_price(client):
    client.options_mark_price()


def test_options_order_book(client):
    client.options_order_book()


def test_options_klines(client):
    client.options_klines()


def test_options_recent_trades(client):
    client.options_recent_trades()


def test_options_historical_trades(client):
    client.options_historical_trades()


# Account and trading interface endpoints


def test_options_account_info(client):
    client.options_account_info()


def test_options_funds_transfer(client):
    client.options_funds_transfer()


def test_options_positions(client):
    client.options_positions()


def test_options_bill(client):
    client.options_bill()


def test_options_place_order(client):
    client.options_place_order()


def test_test_options_place_batch_order(client):
    client.test_options_place_batch_order()


def test_options_cancel_order(client):
    client.options_cancel_order()


def test_options_cancel_batch_order(client):
    client.options_cancel_batch_order()


def test_options_cancel_all_orders(client):
    client.options_cancel_all_orders()


def test_options_query_order(client):
    client.options_query_order()


def test_options_query_pending_orders(client):
    client.options_query_pending_orders()


def test_options_query_order_history(client):
    client.options_query_order_history()


def test_options_user_trades(client):
    client.options_user_trades()


# Fiat Endpoints


def test_get_fiat_deposit_withdraw_history(client):
    client.get_fiat_deposit_withdraw_history()


def test_get_fiat_payments_history(client):
    client.get_fiat_payments_history()


# C2C Endpoints


def test_get_c2c_trade_history(client):
    client.get_c2c_trade_history()


# Pay Endpoints


def test_get_pay_trade_history(client):
    client.get_pay_trade_history()


# Convert Endpoints


def test_get_convert_trade_history(client):
    client.get_convert_trade_history()


def test_convert_request_quote(client):
    client.convert_request_quote()


def test_convert_accept_quote(client):
    client.convert_accept_quote()


def test_papi_get_balance(client):
    client.papi_get_balance()


def test_papi_get_account(client):
    client.papi_get_account()


def test_papi_get_margin_max_borrowable(client):
    client.papi_get_margin_max_borrowable()


def test_papi_get_margin_max_withdraw(client):
    client.papi_get_margin_max_withdraw()


def test_papi_get_um_position_risk(client):
    client.papi_get_um_position_risk()


def test_papi_get_cm_position_risk(client):
    client.papi_get_cm_position_risk()


def test_papi_set_um_leverage(client):
    client.papi_set_um_leverage()


def test_papi_set_cm_leverage(client):
    client.papi_set_cm_leverage()


def test_papi_change_um_position_side_dual(client):
    client.papi_change_um_position_side_dual()


def test_papi_get_um_position_side_dual(client):
    client.papi_get_um_position_side_dual()


def test_papi_get_cm_position_side_dual(client):
    client.papi_get_cm_position_side_dual()


def test_papi_get_um_leverage_bracket(client):
    client.papi_get_um_leverage_bracket()


def test_papi_get_cm_leverage_bracket(client):
    client.papi_get_cm_leverage_bracket()


def test_papi_get_um_api_trading_status(client):
    client.papi_get_um_api_trading_status()


def test_papi_get_um_comission_rate(client):
    client.papi_get_um_comission_rate()


def test_papi_get_cm_comission_rate(client):
    client.papi_get_cm_comission_rate()


def test_papi_get_margin_margin_loan(client):
    client.papi_get_margin_margin_loan()


def test_papi_get_margin_repay_loan(client):
    client.papi_get_margin_repay_loan()


def test_papi_get_repay_futures_switch(client):
    client.papi_get_repay_futures_switch()


def test_papi_repay_futures_switch(client):
    client.papi_repay_futures_switch()


def test_papi_get_margin_interest_history(client):
    client.papi_get_margin_interest_history()


def test_papi_repay_futures_negative_balance(client):
    client.papi_repay_futures_negative_balance()


def test_papi_get_portfolio_interest_history(client):
    client.papi_get_portfolio_interest_history()


def test_papi_fund_auto_collection(client):
    client.papi_fund_auto_collection()


def test_papi_fund_asset_collection(client):
    client.papi_fund_asset_collection()


def test_papi_bnb_transfer(client):
    client.papi_bnb_transfer()


def test_papi_get_um_income_history(client):
    client.papi_get_um_income_history()


def test_papi_get_cm_income_history(client):
    client.papi_get_cm_income_history()


def test_papi_get_um_account(client):
    client.papi_get_um_account()


def test_papi_get_um_account_v2(client):
    client.papi_get_um_account_v2()


def test_papi_get_cm_account(client):
    client.papi_get_cm_account()


def test_papi_get_um_account_config(client):
    client.papi_get_um_account_config()


def test_papi_get_um_symbol_config(client):
    client.papi_get_um_symbol_config()


def test_papi_get_um_trade_asyn(client):
    client.papi_get_um_trade_asyn()


def test_papi_get_um_trade_asyn_id(client):
    client.papi_get_um_trade_asyn_id()


def test_papi_get_um_order_asyn(client):
    client.papi_get_um_order_asyn()


def test_papi_get_um_order_asyn_id(client):
    client.papi_get_um_order_asyn_id()


def test_papi_get_um_income_asyn(client):
    client.papi_get_um_income_asyn()


def test_papi_get_um_income_asyn_id(client):
    client.papi_get_um_income_asyn_id()


# Public papi endpoints


def test_papi_ping(client):
    client.papi_ping()


# Trade papi endpoints


def test_papi_create_um_order(client):
    client.papi_create_um_order()


def test_papi_create_um_conditional_order(client):
    client.papi_create_um_conditional_order()


def test_papi_create_cm_order(client):
    client.papi_create_cm_order()


def test_papi_create_cm_conditional_order(client):
    client.papi_create_cm_conditional_order()


def test_papi_create_margin_order(client):
    client.papi_create_margin_order()


def test_papi_margin_loan(client):
    client.papi_margin_loan()


def test_papi_repay_loan(client):
    client.papi_repay_loan()


def test_papi_margin_order_oco(client):
    client.papi_margin_order_oco()


def test_papi_cancel_um_order(client):
    client.papi_cancel_um_order()


def test_papi_cancel_um_all_open_orders(client):
    client.papi_cancel_um_all_open_orders()


def test_papi_cancel_um_conditional_order(client):
    client.papi_cancel_um_conditional_order()


def test_papi_cancel_um_conditional_all_open_orders(client):
    client.papi_cancel_um_conditional_all_open_orders()


def test_papi_cancel_cm_order(client):
    client.papi_cancel_cm_order()


def test_papi_cancel_cm_all_open_orders(client):
    client.papi_cancel_cm_all_open_orders()


def test_papi_cancel_cm_conditional_order(client):
    client.papi_cancel_cm_conditional_order()


def test_papi_cancel_cm_conditional_all_open_orders(client):
    client.papi_cancel_cm_conditional_all_open_orders()


def test_papi_cancel_margin_order(client):
    client.papi_cancel_margin_order()


def test_papi_cancel_margin_order_list(client):
    client.papi_cancel_margin_order_list()


def test_papi_cancel_margin_all_open_orders(client):
    client.papi_cancel_margin_all_open_orders()


def test_papi_modify_um_order(client):
    client.papi_modify_um_order()


def test_papi_modify_cm_order(client):
    client.papi_modify_cm_order()


def test_papi_get_um_order(client):
    client.papi_get_um_order()


def test_papi_get_um_all_orders(client):
    client.papi_get_um_all_orders()


def test_papi_get_um_open_order(client):
    client.papi_get_um_open_order()


def test_papi_get_um_open_orders(client):
    client.papi_get_um_open_orders()


def test_papi_get_um_conditional_all_orders(client):
    client.papi_get_um_conditional_all_orders()


def test_papi_get_um_conditional_open_orders(client):
    client.papi_get_um_conditional_open_orders()


def test_papi_get_um_conditional_open_order(client):
    client.papi_get_um_conditional_open_order()


def test_papi_get_um_conditional_order_history(client):
    client.papi_get_um_conditional_order_history()


def test_papi_get_cm_order(client):
    client.papi_get_cm_order()


def test_papi_get_cm_all_orders(client):
    client.papi_get_cm_all_orders()


def test_papi_get_cm_open_order(client):
    client.papi_get_cm_open_order()


def test_papi_get_cm_open_orders(client):
    client.papi_get_cm_open_orders()


def test_papi_get_cm_conditional_all_orders(client):
    client.papi_get_cm_conditional_all_orders()


def test_papi_get_cm_conditional_open_orders(client):
    client.papi_get_cm_conditional_open_orders()


def test_papi_get_cm_conditional_open_order(client):
    client.papi_get_cm_conditional_open_order()


def test_papi_get_cm_conditional_order_history(client):
    client.papi_get_cm_conditional_order_history()


def test_papi_get_um_force_orders(client):
    client.papi_get_um_force_orders()


def test_papi_get_cm_force_orders(client):
    client.papi_get_cm_force_orders()


def test_papi_get_um_order_amendment(client):
    client.papi_get_um_order_amendment()


def test_papi_get_cm_order_amendment(client):
    client.papi_get_cm_order_amendment()


def test_papi_get_margin_force_orders(client):
    client.papi_get_margin_force_orders()


def test_papi_get_um_user_trades(client):
    client.papi_get_um_user_trades()


def test_papi_get_cm_user_trades(client):
    client.papi_get_cm_user_trades()


def test_papi_get_um_adl_quantile(client):
    client.papi_get_um_adl_quantile()


def test_papi_get_cm_adl_quantile(client):
    client.papi_get_cm_adl_quantile()


def test_papi_set_um_fee_burn(client):
    client.papi_set_um_fee_burn()


def test_papi_get_um_fee_burn(client):
    client.papi_get_um_fee_burn()


def test_papi_get_margin_order(client):
    client.papi_get_margin_order()


def test_papi_get_margin_open_orders(client):
    client.papi_get_margin_open_orders()


def test_papi_get_margin_all_orders(client):
    client.papi_get_margin_all_orders()


def test_papi_get_margin_order_list(client):
    client.papi_get_margin_order_list()


def test_papi_get_margin_all_order_list(client):
    client.papi_get_margin_all_order_list()


def test_papi_get_margin_open_order_list(client):
    client.papi_get_margin_open_order_list()


def test_papi_get_margin_my_trades(client):
    client.papi_get_margin_my_trades()


def test_papi_get_margin_repay_debt(client):
    client.papi_get_margin_repay_debt()


def test_close_connection(client):
    client.close_connection()


#########################
# Websocket API Requests #
#########################


def test_ws_get_order_book(client):
    client.ws_get_order_book(symbol="BTCUSDT")


def test_ws_get_recent_trades(client):
    client.ws_get_recent_trades(symbol="BTCUSDT")


def test_ws_get_historical_trades(client):
    client.ws_get_historical_trades(symbol="BTCUSDT")


def test_ws_get_aggregate_trades(client):
    client.ws_get_aggregate_trades(symbol="BTCUSDT")


def test_ws_get_klines(client):
    client.ws_get_klines(symbol="BTCUSDT", interval="1m")


def test_ws_get_uiKlines(client):
    client.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")


def test_ws_get_avg_price(client):
    client.ws_get_avg_price(symbol="BTCUSDT")


def test_ws_get_ticker(client):
    ticker = client.ws_get_ticker(symbol="BTCUSDT")


def test_ws_get_trading_day_ticker(client):
    client.ws_get_trading_day_ticker(symbol="BTCUSDT")


def test_ws_get_symbol_ticker_window(client):
    client.ws_get_symbol_ticker_window(symbol="BTCUSDT")


def test_ws_get_symbol_ticker(client):
    client.ws_get_symbol_ticker(symbol="BTCUSDT")


def test_ws_get_orderbook_ticker(client):
    client.ws_get_orderbook_ticker(symbol="BTCUSDT")


def test_ws_ping(client):
    client.ws_ping()


def test_ws_get_time(client):
    client.ws_get_time()


def test_ws_get_exchange_info(client):
    client.ws_get_exchange_info(symbol="BTCUSDT")
