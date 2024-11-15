import pytest

# Apply the 'portfolio' mark to all tests in this file
pytestmark = pytest.mark.portfolio


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
