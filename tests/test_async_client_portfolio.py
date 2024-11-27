import pytest

# Apply the 'portfolio' mark to all tests in this file
pytestmark = [pytest.mark.portfolio, pytest.mark.asyncio]


async def test_papi_get_balance(client):
    await client.papi_get_balance()


async def test_papi_get_account(client):
    await client.papi_get_account()


async def test_papi_get_margin_max_borrowable(client):
    await client.papi_get_margin_max_borrowable()


async def test_papi_get_margin_max_withdraw(client):
    await client.papi_get_margin_max_withdraw()


async def test_papi_get_um_position_risk(client):
    await client.papi_get_um_position_risk()


async def test_papi_get_cm_position_risk(client):
    await client.papi_get_cm_position_risk()


async def test_papi_set_um_leverage(client):
    await client.papi_set_um_leverage()


async def test_papi_set_cm_leverage(client):
    await client.papi_set_cm_leverage()


async def test_papi_change_um_position_side_dual(client):
    await client.papi_change_um_position_side_dual()


async def test_papi_get_um_position_side_dual(client):
    await client.papi_get_um_position_side_dual()


async def test_papi_get_cm_position_side_dual(client):
    await client.papi_get_cm_position_side_dual()


async def test_papi_get_um_leverage_bracket(client):
    await client.papi_get_um_leverage_bracket()


async def test_papi_get_cm_leverage_bracket(client):
    await client.papi_get_cm_leverage_bracket()


async def test_papi_get_um_api_trading_status(client):
    await client.papi_get_um_api_trading_status()


async def test_papi_get_um_comission_rate(client):
    await client.papi_get_um_comission_rate()


async def test_papi_get_cm_comission_rate(client):
    await client.papi_get_cm_comission_rate()


async def test_papi_get_margin_margin_loan(client):
    await client.papi_get_margin_margin_loan()


async def test_papi_get_margin_repay_loan(client):
    await client.papi_get_margin_repay_loan()


async def test_papi_get_repay_futures_switch(client):
    await client.papi_get_repay_futures_switch()


async def test_papi_repay_futures_switch(client):
    await client.papi_repay_futures_switch()


async def test_papi_get_margin_interest_history(client):
    await client.papi_get_margin_interest_history()


async def test_papi_repay_futures_negative_balance(client):
    await client.papi_repay_futures_negative_balance()


async def test_papi_get_portfolio_interest_history(client):
    await client.papi_get_portfolio_interest_history()


async def test_papi_fund_auto_collection(client):
    await client.papi_fund_auto_collection()


async def test_papi_fund_asset_collection(client):
    await client.papi_fund_asset_collection()


async def test_papi_bnb_transfer(client):
    await client.papi_bnb_transfer()


async def test_papi_get_um_income_history(client):
    await client.papi_get_um_income_history()


async def test_papi_get_cm_income_history(client):
    await client.papi_get_cm_income_history()


async def test_papi_get_um_account(client):
    await client.papi_get_um_account()


async def test_papi_get_um_account_v2(client):
    await client.papi_get_um_account_v2()


async def test_papi_get_cm_account(client):
    await client.papi_get_cm_account()


async def test_papi_get_um_account_config(client):
    await client.papi_get_um_account_config()


async def test_papi_get_um_symbol_config(client):
    await client.papi_get_um_symbol_config()


async def test_papi_get_um_trade_asyn(client):
    await client.papi_get_um_trade_asyn()


async def test_papi_get_um_trade_asyn_id(client):
    await client.papi_get_um_trade_asyn_id()


async def test_papi_get_um_order_asyn(client):
    await client.papi_get_um_order_asyn()


async def test_papi_get_um_order_asyn_id(client):
    await client.papi_get_um_order_asyn_id()


async def test_papi_get_um_income_asyn(client):
    await client.papi_get_um_income_asyn()


async def test_papi_get_um_income_asyn_id(client):
    await client.papi_get_um_income_asyn_id()


# Public papi endpoints


async def test_papi_ping(client):
    await client.papi_ping()


# Trade papi endpoints


async def test_papi_create_um_order(client):
    await client.papi_create_um_order()


async def test_papi_create_um_conditional_order(client):
    await client.papi_create_um_conditional_order()


async def test_papi_create_cm_order(client):
    await client.papi_create_cm_order()


async def test_papi_create_cm_conditional_order(client):
    await client.papi_create_cm_conditional_order()


async def test_papi_create_margin_order(client):
    await client.papi_create_margin_order()


async def test_papi_margin_loan(client):
    await client.papi_margin_loan()


async def test_papi_repay_loan(client):
    await client.papi_repay_loan()


async def test_papi_margin_order_oco(client):
    await client.papi_margin_order_oco()


async def test_papi_cancel_um_order(client):
    await client.papi_cancel_um_order()


async def test_papi_cancel_um_all_open_orders(client):
    await client.papi_cancel_um_all_open_orders()


async def test_papi_cancel_um_conditional_order(client):
    await client.papi_cancel_um_conditional_order()


async def test_papi_cancel_um_conditional_all_open_orders(client):
    await client.papi_cancel_um_conditional_all_open_orders()


async def test_papi_cancel_cm_order(client):
    await client.papi_cancel_cm_order()


async def test_papi_cancel_cm_all_open_orders(client):
    await client.papi_cancel_cm_all_open_orders()


async def test_papi_cancel_cm_conditional_order(client):
    await client.papi_cancel_cm_conditional_order()


async def test_papi_cancel_cm_conditional_all_open_orders(client):
    await client.papi_cancel_cm_conditional_all_open_orders()


async def test_papi_cancel_margin_order(client):
    await client.papi_cancel_margin_order()


async def test_papi_cancel_margin_order_list(client):
    await client.papi_cancel_margin_order_list()


async def test_papi_cancel_margin_all_open_orders(client):
    await client.papi_cancel_margin_all_open_orders()


async def test_papi_modify_um_order(client):
    await client.papi_modify_um_order()


async def test_papi_modify_cm_order(client):
    await client.papi_modify_cm_order()


async def test_papi_get_um_order(client):
    await client.papi_get_um_order()


async def test_papi_get_um_all_orders(client):
    await client.papi_get_um_all_orders()


async def test_papi_get_um_open_order(client):
    await client.papi_get_um_open_order()


async def test_papi_get_um_open_orders(client):
    await client.papi_get_um_open_orders()


async def test_papi_get_um_conditional_all_orders(client):
    await client.papi_get_um_conditional_all_orders()


async def test_papi_get_um_conditional_open_orders(client):
    await client.papi_get_um_conditional_open_orders()


async def test_papi_get_um_conditional_open_order(client):
    await client.papi_get_um_conditional_open_order()


async def test_papi_get_um_conditional_order_history(client):
    await client.papi_get_um_conditional_order_history()


async def test_papi_get_cm_order(client):
    await client.papi_get_cm_order()


async def test_papi_get_cm_all_orders(client):
    await client.papi_get_cm_all_orders()


async def test_papi_get_cm_open_order(client):
    await client.papi_get_cm_open_order()


async def test_papi_get_cm_open_orders(client):
    await client.papi_get_cm_open_orders()


async def test_papi_get_cm_conditional_all_orders(client):
    await client.papi_get_cm_conditional_all_orders()


async def test_papi_get_cm_conditional_open_orders(client):
    await client.papi_get_cm_conditional_open_orders()


async def test_papi_get_cm_conditional_open_order(client):
    await client.papi_get_cm_conditional_open_order()


async def test_papi_get_cm_conditional_order_history(client):
    await client.papi_get_cm_conditional_order_history()


async def test_papi_get_um_force_orders(client):
    await client.papi_get_um_force_orders()


async def test_papi_get_cm_force_orders(client):
    await client.papi_get_cm_force_orders()


async def test_papi_get_um_order_amendment(client):
    await client.papi_get_um_order_amendment()


async def test_papi_get_cm_order_amendment(client):
    await client.papi_get_cm_order_amendment()


async def test_papi_get_margin_force_orders(client):
    await client.papi_get_margin_force_orders()


async def test_papi_get_um_user_trades(client):
    await client.papi_get_um_user_trades()


async def test_papi_get_cm_user_trades(client):
    await client.papi_get_cm_user_trades()


async def test_papi_get_um_adl_quantile(client):
    await client.papi_get_um_adl_quantile()


async def test_papi_get_cm_adl_quantile(client):
    await client.papi_get_cm_adl_quantile()


async def test_papi_set_um_fee_burn(client):
    await client.papi_set_um_fee_burn()


async def test_papi_get_um_fee_burn(client):
    await client.papi_get_um_fee_burn()


async def test_papi_get_margin_order(client):
    await client.papi_get_margin_order()


async def test_papi_get_margin_open_orders(client):
    await client.papi_get_margin_open_orders()


async def test_papi_get_margin_all_orders(client):
    await client.papi_get_margin_all_orders()


async def test_papi_get_margin_order_list(client):
    await client.papi_get_margin_order_list()


async def test_papi_get_margin_all_order_list(client):
    await client.papi_get_margin_all_order_list()


async def test_papi_get_margin_open_order_list(client):
    await client.papi_get_margin_open_order_list()


async def test_papi_get_margin_my_trades(client):
    await client.papi_get_margin_my_trades()


async def test_papi_get_margin_repay_debt(client):
    await client.papi_get_margin_repay_debt()


async def test_close_connection(client):
    await client.close_connection()
