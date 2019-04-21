import asyncio
import time
from functools import partial

import liquidtap


class LiquidSocketManager(object):
    DEFAULT_USER_REFRESH = 30 * 60  # 30 minutes

    def __init__(self, client, refresh_interval=DEFAULT_USER_REFRESH):
        self._client = client
        self.tap = liquidtap.Client(self._client.API_TOKEN_ID, self._client.API_SECRET)
        self._subscriptions = {}
        self._events = {}
        self._user = None
        self._user_refresh = refresh_interval
        self._counter = 0

    def get_user_info(self):
        self._user = asyncio.run(self._client.get_user_info())

    def controlled_callback(self, callback, *args, **kwargs):
        if self._counter == self._user_refresh:
            self.get_user_info()
            self._counter = 0
        callback(*args, **kwargs)

    async def start_trade_socket(self, currency_pair_code, callback):
        currencies = {"BTCUSD": "product_cash_btcusd_1"}
        if not self._user:
            self._user = await self._client.get_user_info()
        subscriptions = {
            f"price_ladders_cash_{currency_pair_code.lower()}_buy": partial(
                self.controlled_callback, callback, "price_ladders_buy"
            ),
            f"price_ladders_cash_{currency_pair_code.lower()}_sell": partial(
                self.controlled_callback, callback, "price_ladders_sell"
            ),
            f"executions_cash_{currency_pair_code.lower()}": partial(
                self.controlled_callback, callback, "executions_cash"
            ),
        }
        events = {
            f"price_ladders_cash_{currency_pair_code.lower()}_buy": "updated",
            f"price_ladders_cash_{currency_pair_code.lower()}_sell": "updated",
            f"executions_cash_{currency_pair_code.lower()}": "created",
        }
        for key, value in subscriptions.items():
            self._subscriptions[key] = value
            self._events[key] = events[key]

    async def start_user_socket(self, currency, callback):
        if not self._user:
            self._user = await self._client.get_user_info()
        channels = [
            {"pusher": x["pusher_channel"], "currency": x["currency"]}
            for x in self._user["fiat_accounts"]
        ]
        order_subscriptions = {
            f"{x['pusher']}_orders": partial(
                self.controlled_callback, callback, "orders", x["currency"]
            )
            for x in channels
        }
        # executions_subscriptions = {
        #     f"executions_{self._user['id']}_{x['currency_pair_code'].lower()}_{x['id']}": partial(
        #         self.controlled_callback,
        #         callback,
        #         "executions",
        #         x["currency_pair_code"],
        #     )
        #     for x in self._user["products"]
        # }
        # execution_events = {
        #     f"executions_{self._user['id']}_{x['currency_pair_code'].lower()}_{x['id']}": "created"
        #     for x in self._user["products"]
        # }
        order_events = {f"{x['pusher']}_orders": "updated" for x in channels}
        trade_subscriptions = {
            f"{x['pusher']}_trades": partial(
                self.controlled_callback, callback, "trades", x["currency"]
            )
            for x in channels
        }
        trade_events = {f"{x['pusher']}_trades": "updated" for x in channels}
        self._subscriptions.update(order_subscriptions)
        self._subscriptions.update(trade_subscriptions)
        # self._subscriptions.update(executions_subscriptions)
        self._events.update(order_events)
        self._events.update(trade_events)
        # self._events.update(execution_events)

    def on_connect(self, data):
        print(data)
        for key, value in self._subscriptions.items():
            self.tap.pusher.subscribe(key).bind(self._events[key], value)

    def start(self):
        self.tap.pusher.connection.bind(
            "pusher:connection_established", self.on_connect
        )

        self.tap.pusher.connect()
        while True:
            time.sleep(1)
            self._counter += 1
