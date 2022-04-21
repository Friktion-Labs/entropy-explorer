# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Entropy Markets](https://entropy.markets/) support is available at:
#   [Docs](https://docs.entropy.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/entropymarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import abc
import logging
import entropy
import time
import typing

from decimal import Decimal
from solana.publickey import PublicKey

from ..instrumentvalue import InstrumentValue
from ..modelstate import ModelState
from ..tokens import Token


# # 🥭 ModelStateBuilder class
#
# Base class for building a `ModelState` through polling or websockets.
#
class ModelStateBuilder(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def build(self, context: entropy.Context) -> ModelState:
        raise NotImplementedError(
            "ModelStateBuilder.build() is not implemented on the base type."
        )

    def __str__(self) -> str:
        return "« ModelStateBuilder »"

    def __repr__(self) -> str:
        return f"{self}"


# # 🥭 WebsocketModelStateBuilder class
#
# Base class for building a `ModelState` through polling.
#
class WebsocketModelStateBuilder(ModelStateBuilder):
    def __init__(self, model_state: ModelState) -> None:
        super().__init__()
        self.model_state: ModelState = model_state

    def build(self, context: entropy.Context) -> ModelState:
        return self.model_state

    def __str__(self) -> str:
        return f"« WebsocketModelStateBuilder for market '{self.model_state.market.fully_qualified_symbol}' »"


# # 🥭 PollingModelStateBuilder class
#
# Base class for building a `ModelState` through polling.
#
class PollingModelStateBuilder(ModelStateBuilder):
    def __init__(self) -> None:
        super().__init__()

    def build(self, context: entropy.Context) -> ModelState:
        started_at = time.time()
        built: ModelState = self.poll(context)
        time_taken = time.time() - started_at
        self._logger.debug(
            f"Poll for model state complete. Time taken: {time_taken:.2f} seconds."
        )
        return built

    @abc.abstractmethod
    def poll(self, context: entropy.Context) -> ModelState:
        raise NotImplementedError(
            "PollingModelStateBuilder.poll() is not implemented on the base type."
        )

    def from_values(
        self,
        order_owner: PublicKey,
        market: entropy.Market,
        group: entropy.Group,
        account: entropy.Account,
        price: entropy.Price,
        placed_orders_container: entropy.PlacedOrdersContainer,
        inventory: entropy.Inventory,
        orderbook: entropy.OrderBook,
        event_queue: entropy.EventQueue,
    ) -> ModelState:
        group_watcher: entropy.ManualUpdateWatcher[
            entropy.Group
        ] = entropy.ManualUpdateWatcher(group)
        account_watcher: entropy.ManualUpdateWatcher[
            entropy.Account
        ] = entropy.ManualUpdateWatcher(account)
        price_watcher: entropy.ManualUpdateWatcher[
            entropy.Price
        ] = entropy.ManualUpdateWatcher(price)
        placed_orders_container_watcher: entropy.ManualUpdateWatcher[
            entropy.PlacedOrdersContainer
        ] = entropy.ManualUpdateWatcher(placed_orders_container)
        inventory_watcher: entropy.ManualUpdateWatcher[
            entropy.Inventory
        ] = entropy.ManualUpdateWatcher(inventory)
        orderbook_watcher: entropy.ManualUpdateWatcher[
            entropy.OrderBook
        ] = entropy.ManualUpdateWatcher(orderbook)
        event_queue_watcher: entropy.ManualUpdateWatcher[
            entropy.EventQueue
        ] = entropy.ManualUpdateWatcher(event_queue)

        return ModelState(
            order_owner,
            market,
            group_watcher,
            account_watcher,
            price_watcher,
            placed_orders_container_watcher,
            inventory_watcher,
            orderbook_watcher,
            event_queue_watcher,
        )

    def __str__(self) -> str:
        return "« PollingModelStateBuilder »"


# # 🥭 SerumPollingModelStateBuilder class
#
# Polls Solana and builds a `ModelState` for a `SerumMarket`
#
class SerumPollingModelStateBuilder(PollingModelStateBuilder):
    def __init__(
        self,
        order_owner: PublicKey,
        market: entropy.SerumMarket,
        oracle: entropy.Oracle,
        group_address: PublicKey,
        cache_address: PublicKey,
        account_address: PublicKey,
        open_orders_address: PublicKey,
        base_inventory_token_account: entropy.TokenAccount,
        quote_inventory_token_account: entropy.TokenAccount,
    ) -> None:
        super().__init__()
        self.order_owner: PublicKey = order_owner
        self.market: entropy.SerumMarket = market
        self.oracle: entropy.Oracle = oracle

        self.group_address: PublicKey = group_address
        self.cache_address: PublicKey = cache_address
        self.account_address: PublicKey = account_address
        self.open_orders_address: PublicKey = open_orders_address
        self.base_inventory_token_account: entropy.TokenAccount = (
            base_inventory_token_account
        )
        self.quote_inventory_token_account: entropy.TokenAccount = (
            quote_inventory_token_account
        )

        # Serum always uses Tokens
        self.base_token: Token = Token.ensure(
            self.base_inventory_token_account.value.token
        )
        self.quote_token: Token = Token.ensure(
            self.quote_inventory_token_account.value.token
        )

    def poll(self, context: entropy.Context) -> ModelState:
        addresses: typing.List[PublicKey] = [
            self.group_address,
            self.cache_address,
            self.account_address,
            self.open_orders_address,
            self.base_inventory_token_account.address,
            self.quote_inventory_token_account.address,
            self.market.bids_address,
            self.market.asks_address,
            self.market.event_queue_address,
        ]
        account_infos: typing.Sequence[
            entropy.AccountInfo
        ] = entropy.AccountInfo.load_multiple(context, addresses)
        group: entropy.Group = entropy.Group.parse_with_context(
            context, account_infos[0]
        )
        cache: entropy.Cache = entropy.Cache.parse(account_infos[1])
        account: entropy.Account = entropy.Account.parse(account_infos[2], group, cache)
        placed_orders_container: entropy.PlacedOrdersContainer = (
            entropy.OpenOrders.parse(
                account_infos[3], self.market.base, self.market.quote
            )
        )

        # Serum markets don't accrue MNGO liquidity incentives
        mngo_accrued: InstrumentValue = InstrumentValue(
            group.liquidity_incentive_token, Decimal(0)
        )

        base_inventory_token_account = entropy.TokenAccount.parse(
            account_infos[4], self.base_token
        )
        quote_inventory_token_account = entropy.TokenAccount.parse(
            account_infos[5], self.quote_token
        )

        orderbook: entropy.OrderBook = self.market.parse_account_infos_to_orderbook(
            account_infos[6], account_infos[7]
        )

        event_queue: entropy.EventQueue = entropy.SerumEventQueue.parse(
            account_infos[8], self.base_token, self.quote_token
        )

        price: entropy.Price = self.oracle.fetch_price(context)

        available: Decimal = (
            base_inventory_token_account.value.value * price.mid_price
        ) + quote_inventory_token_account.value.value
        available_collateral: InstrumentValue = InstrumentValue(
            quote_inventory_token_account.value.token, available
        )
        inventory: entropy.Inventory = entropy.Inventory(
            entropy.InventorySource.SPL_TOKENS,
            mngo_accrued,
            available_collateral,
            base_inventory_token_account.value,
            quote_inventory_token_account.value,
        )

        return self.from_values(
            self.order_owner,
            self.market,
            group,
            account,
            price,
            placed_orders_container,
            inventory,
            orderbook,
            event_queue,
        )

    def __str__(self) -> str:
        return f"""« SerumPollingModelStateBuilder for market '{self.market.fully_qualified_symbol}' »"""


# # 🥭 SpotPollingModelStateBuilder class
#
# Polls Solana and builds a `ModelState` for a `SpotMarket`
#
class SpotPollingModelStateBuilder(PollingModelStateBuilder):
    def __init__(
        self,
        order_owner: PublicKey,
        market: entropy.SpotMarket,
        oracle: entropy.Oracle,
        group_address: PublicKey,
        cache_address: PublicKey,
        account_address: PublicKey,
        open_orders_address: PublicKey,
        all_open_orders_addresses: typing.Sequence[PublicKey],
    ) -> None:
        super().__init__()
        self.order_owner: PublicKey = order_owner
        self.market: entropy.SpotMarket = market
        self.oracle: entropy.Oracle = oracle

        self.group_address: PublicKey = group_address
        self.cache_address: PublicKey = cache_address
        self.account_address: PublicKey = account_address
        self.open_orders_address: PublicKey = open_orders_address
        self.all_open_orders_addresses: typing.Sequence[
            PublicKey
        ] = all_open_orders_addresses

    def poll(self, context: entropy.Context) -> ModelState:
        addresses: typing.List[PublicKey] = [
            self.group_address,
            self.cache_address,
            self.account_address,
            self.market.bids_address,
            self.market.asks_address,
            self.market.event_queue_address,
            *self.all_open_orders_addresses,
        ]
        account_infos: typing.Sequence[
            entropy.AccountInfo
        ] = entropy.AccountInfo.load_multiple(context, addresses)
        group: entropy.Group = entropy.Group.parse_with_context(
            context, account_infos[0]
        )
        cache: entropy.Cache = entropy.Cache.parse(account_infos[1])
        account: entropy.Account = entropy.Account.parse(account_infos[2], group, cache)

        # Update our stash of OpenOrders addresses for next time, in case new OpenOrders accounts were added
        self.all_open_orders_addresses = account.spot_open_orders

        spot_open_orders_account_infos_by_address = {
            str(account_info.address): account_info
            for account_info in account_infos[6:]
        }

        all_open_orders: typing.Dict[str, entropy.OpenOrders] = {}
        for basket_token in account.slots:
            if (
                basket_token.spot_open_orders is not None
                and str(basket_token.spot_open_orders)
                in spot_open_orders_account_infos_by_address
            ):
                account_info: entropy.AccountInfo = (
                    spot_open_orders_account_infos_by_address[
                        str(basket_token.spot_open_orders)
                    ]
                )
                open_orders: entropy.OpenOrders = entropy.OpenOrders.parse(
                    account_info,
                    Token.ensure(basket_token.base_instrument),
                    account.shared_quote_token,
                )
                all_open_orders[str(basket_token.spot_open_orders)] = open_orders

        placed_orders_container: entropy.PlacedOrdersContainer = all_open_orders[
            str(self.open_orders_address)
        ]

        # Spot markets don't accrue MNGO liquidity incentives
        mngo_accrued: InstrumentValue = InstrumentValue(
            group.liquidity_incentive_token, Decimal(0)
        )

        base_value = entropy.InstrumentValue.find_by_symbol(
            account.net_values, self.market.base.symbol
        )
        quote_value = entropy.InstrumentValue.find_by_symbol(
            account.net_values, self.market.quote.symbol
        )

        frame = account.to_dataframe(group, all_open_orders, cache)
        available_collateral: InstrumentValue = account.init_health(frame)
        inventory: entropy.Inventory = entropy.Inventory(
            entropy.InventorySource.ACCOUNT,
            mngo_accrued,
            available_collateral,
            base_value,
            quote_value,
        )

        orderbook: entropy.OrderBook = self.market.parse_account_infos_to_orderbook(
            account_infos[3], account_infos[4]
        )

        event_queue: entropy.EventQueue = entropy.SerumEventQueue.parse(
            account_infos[5], self.market.base, self.market.quote
        )

        price: entropy.Price = self.oracle.fetch_price(context)

        return self.from_values(
            self.order_owner,
            self.market,
            group,
            account,
            price,
            placed_orders_container,
            inventory,
            orderbook,
            event_queue,
        )

    def __str__(self) -> str:
        return f"""« SpotPollingModelStateBuilder for market '{self.market.fully_qualified_symbol}' »"""


# # 🥭 PerpPollingModelStateBuilder class
#
# Polls Solana and builds a `ModelState` for a `PerpMarket`
#
class PerpPollingModelStateBuilder(PollingModelStateBuilder):
    def __init__(
        self,
        order_owner: PublicKey,
        market: entropy.PerpMarket,
        oracle: entropy.Oracle,
        group_address: PublicKey,
        cache_address: PublicKey,
        all_open_orders_addresses: typing.Sequence[PublicKey],
    ) -> None:
        super().__init__()
        self.order_owner: PublicKey = order_owner
        self.market: entropy.PerpMarket = market
        self.oracle: entropy.Oracle = oracle

        self.group_address: PublicKey = group_address
        self.cache_address: PublicKey = cache_address

        self.all_open_orders_addresses: typing.Sequence[
            PublicKey
        ] = all_open_orders_addresses

    def poll(self, context: entropy.Context) -> ModelState:
        addresses: typing.List[PublicKey] = [
            self.group_address,
            self.cache_address,
            self.order_owner,
            self.market.underlying_perp_market.bids,
            self.market.underlying_perp_market.asks,
            self.market.event_queue_address,
            *self.all_open_orders_addresses,
        ]
        account_infos: typing.Sequence[
            entropy.AccountInfo
        ] = entropy.AccountInfo.load_multiple(context, addresses)
        group: entropy.Group = entropy.Group.parse_with_context(
            context, account_infos[0]
        )
        cache: entropy.Cache = entropy.Cache.parse(account_infos[1])
        account: entropy.Account = entropy.Account.parse(account_infos[2], group, cache)

        # Update our stash of OpenOrders addresses for next time, in case new OpenOrders accounts were added
        self.all_open_orders_addresses = account.spot_open_orders

        spot_open_orders_account_infos_by_address = {
            str(account_info.address): account_info
            for account_info in account_infos[6:]
        }

        all_open_orders: typing.Dict[str, entropy.OpenOrders] = {}
        for basket_token in account.slots:
            if (
                basket_token.spot_open_orders is not None
                and str(basket_token.spot_open_orders)
                in spot_open_orders_account_infos_by_address
            ):
                account_info: entropy.AccountInfo = (
                    spot_open_orders_account_infos_by_address[
                        str(basket_token.spot_open_orders)
                    ]
                )
                open_orders: entropy.OpenOrders = entropy.OpenOrders.parse(
                    account_info,
                    Token.ensure(basket_token.base_instrument),
                    account.shared_quote_token,
                )
                all_open_orders[str(basket_token.spot_open_orders)] = open_orders

        slot = group.slot_by_perp_market_address(self.market.address)
        perp_account = account.perp_accounts_by_index[slot.index]
        if perp_account is None:
            raise Exception(
                f"Could not find perp account at index {slot.index} of account {account.address}."
            )
        placed_orders_container: entropy.PlacedOrdersContainer = (
            perp_account.open_orders
        )

        base_lots = perp_account.base_position
        base_value = self.market.lot_size_converter.base_size_lots_to_number(base_lots)
        base_token_value = entropy.InstrumentValue(self.market.base, base_value)
        quote_token_value = account.shared_quote.net_value
        frame = account.to_dataframe(group, all_open_orders, cache)
        available_collateral: InstrumentValue = account.init_health(frame)
        inventory: entropy.Inventory = entropy.Inventory(
            entropy.InventorySource.ACCOUNT,
            perp_account.mngo_accrued,
            available_collateral,
            base_token_value,
            quote_token_value,
        )

        orderbook: entropy.OrderBook = self.market.parse_account_infos_to_orderbook(
            account_infos[3], account_infos[4]
        )

        event_queue: entropy.EventQueue = entropy.PerpEventQueue.parse(
            account_infos[5], self.market.lot_size_converter
        )

        price: entropy.Price = self.oracle.fetch_price(context)

        return self.from_values(
            self.order_owner,
            self.market,
            group,
            account,
            price,
            placed_orders_container,
            inventory,
            orderbook,
            event_queue,
        )

    def __str__(self) -> str:
        return f"""« PerpPollingModelStateBuilder for market '{self.market.fully_qualified_symbol}' »"""
