# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Entropy Markets](https://entropy.trade/) support is available at:
#   [Docs](https://docs.entropy.trade/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/entropymarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import enum
import entropy
import typing

from solana.publickey import PublicKey

from ..constants import SYSTEM_PROGRAM_ADDRESS
from ..modelstate import ModelState
from .modelstatebuilder import (
    ModelStateBuilder,
    WebsocketModelStateBuilder,
    SerumPollingModelStateBuilder,
    SpotPollingModelStateBuilder,
    PerpPollingModelStateBuilder,
)


class ModelUpdateMode(enum.Enum):
    # We use strings here so that argparse can work with these as parameters.
    WEBSOCKET = "WEBSOCKET"
    POLL = "POLL"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self}"


# # 🥭 ModelStateBuilder class
#
# Base class for building a `ModelState` through polling or websockets.
#
def model_state_builder_factory(
    mode: ModelUpdateMode,
    context: entropy.Context,
    disposer: entropy.Disposable,
    websocket_manager: entropy.WebSocketSubscriptionManager,
    health_check: entropy.HealthCheck,
    wallet: entropy.Wallet,
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.LoadedMarket,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    if mode == ModelUpdateMode.WEBSOCKET:
        return _websocket_model_state_builder_factory(
            context,
            disposer,
            websocket_manager,
            health_check,
            wallet,
            group,
            account,
            market,
            oracle,
        )
    else:
        return _polling_model_state_builder_factory(
            context, wallet, group, account, market, oracle
        )


def _polling_model_state_builder_factory(
    context: entropy.Context,
    wallet: entropy.Wallet,
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.Market,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    if entropy.SerumMarket.isa(market):
        return _polling_serum_model_state_builder_factory(
            context, wallet, group, account, entropy.SerumMarket.ensure(market), oracle
        )
    elif entropy.SpotMarket.isa(market):
        return _polling_spot_model_state_builder_factory(
            group, account, entropy.SpotMarket.ensure(market), oracle
        )
    elif entropy.PerpMarket.isa(market):
        return _polling_perp_model_state_builder_factory(
            group, account, entropy.PerpMarket.ensure(market), oracle
        )
    else:
        raise Exception(
            f"Could not determine type of market {market.fully_qualified_symbol}: {market}"
        )


def _polling_serum_model_state_builder_factory(
    context: entropy.Context,
    wallet: entropy.Wallet,
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.SerumMarket,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    base_account = entropy.TokenAccount.fetch_largest_for_owner_and_token(
        context, wallet.address, market.base
    )
    if base_account is None:
        raise Exception(
            f"Could not find token account owned by {wallet.address} for base token {market.base}."
        )
    quote_account = entropy.TokenAccount.fetch_largest_for_owner_and_token(
        context, wallet.address, market.quote
    )
    if quote_account is None:
        raise Exception(
            f"Could not find token account owned by {wallet.address} for quote token {market.quote}."
        )
    all_open_orders = entropy.OpenOrders.load_for_market_and_owner(
        context,
        market.address,
        wallet.address,
        context.serum_program_address,
        market.base,
        market.quote,
    )
    if len(all_open_orders) == 0:
        raise Exception(
            f"Could not find serum openorders account owned by {wallet.address} for market {market.fully_qualified_symbol}."
        )
    return SerumPollingModelStateBuilder(
        all_open_orders[0].address,
        market,
        oracle,
        group.address,
        group.cache,
        account.address,
        all_open_orders[0].address,
        base_account,
        quote_account,
    )


def _polling_spot_model_state_builder_factory(
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.SpotMarket,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    market_index: int = group.slot_by_spot_market_address(market.address).index
    open_orders_address: typing.Optional[PublicKey] = account.spot_open_orders_by_index[
        market_index
    ]
    all_open_orders_addresses: typing.Sequence[PublicKey] = account.spot_open_orders
    if open_orders_address is None:
        raise Exception(
            f"Could not find spot openorders in account {account.address} for market {market.fully_qualified_symbol}."
        )
    return SpotPollingModelStateBuilder(
        open_orders_address,
        market,
        oracle,
        group.address,
        group.cache,
        account.address,
        open_orders_address,
        all_open_orders_addresses,
    )


def _polling_perp_model_state_builder_factory(
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.PerpMarket,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    all_open_orders_addresses: typing.Sequence[PublicKey] = account.spot_open_orders
    return PerpPollingModelStateBuilder(
        account.address,
        market,
        oracle,
        group.address,
        group.cache,
        all_open_orders_addresses,
    )


def __load_all_openorders_watchers(
    context: entropy.Context,
    wallet: entropy.Wallet,
    account: entropy.Account,
    group: entropy.Group,
    websocket_manager: entropy.WebSocketSubscriptionManager,
    health_check: entropy.HealthCheck,
) -> typing.Sequence[entropy.Watcher[entropy.OpenOrders]]:
    all_open_orders_watchers: typing.List[entropy.Watcher[entropy.OpenOrders]] = []
    for basket_token in account.base_slots:
        if basket_token.spot_open_orders is not None:
            spot_market_symbol: str = f"spot:{basket_token.base_instrument.symbol}/{account.shared_quote_token.symbol}"
            spot_market = entropy.SpotMarket.ensure(
                entropy.market(context, spot_market_symbol)
            )
            oo_watcher = entropy.build_spot_open_orders_watcher(
                context,
                websocket_manager,
                health_check,
                wallet,
                account,
                group,
                spot_market,
            )
            all_open_orders_watchers += [oo_watcher]

    return all_open_orders_watchers


def _websocket_model_state_builder_factory(
    context: entropy.Context,
    disposer: entropy.Disposable,
    websocket_manager: entropy.WebSocketSubscriptionManager,
    health_check: entropy.HealthCheck,
    wallet: entropy.Wallet,
    group: entropy.Group,
    account: entropy.Account,
    market: entropy.LoadedMarket,
    oracle: entropy.Oracle,
) -> ModelStateBuilder:
    group_watcher = entropy.build_group_watcher(
        context, websocket_manager, health_check, group
    )
    cache = entropy.Cache.load(context, group.cache)
    cache_watcher = entropy.build_cache_watcher(
        context, websocket_manager, health_check, cache, group
    )
    account_subscription, latest_account_observer = entropy.build_account_watcher(
        context, websocket_manager, health_check, account, group_watcher, cache_watcher
    )

    initial_price = oracle.fetch_price(context)
    price_feed = oracle.to_streaming_observable(context)
    latest_price_observer = entropy.LatestItemObserverSubscriber(initial_price)
    price_disposable = price_feed.subscribe(latest_price_observer)
    disposer.add_disposable(price_disposable)
    health_check.add("price_subscription", price_feed)

    if entropy.SerumMarket.isa(market):
        serum_market = entropy.SerumMarket.ensure(market)
        order_owner: PublicKey = (
            serum_market.find_openorders_address_for_owner(context, wallet.address)
            or SYSTEM_PROGRAM_ADDRESS
        )
        price_watcher: entropy.Watcher[entropy.Price] = entropy.build_price_watcher(
            context, websocket_manager, health_check, disposer, "market", serum_market
        )
        inventory_watcher: entropy.Watcher[
            entropy.Inventory
        ] = entropy.build_serum_inventory_watcher(
            context,
            websocket_manager,
            health_check,
            disposer,
            wallet,
            serum_market,
            price_watcher,
        )
        latest_open_orders_observer: entropy.Watcher[
            entropy.PlacedOrdersContainer
        ] = entropy.build_serum_open_orders_watcher(
            context, websocket_manager, health_check, serum_market, wallet
        )
        latest_orderbook_watcher: entropy.Watcher[
            entropy.OrderBook
        ] = entropy.build_orderbook_watcher(
            context, websocket_manager, health_check, serum_market
        )
        latest_event_queue_watcher: entropy.Watcher[
            entropy.EventQueue
        ] = entropy.build_serum_event_queue_watcher(
            context, websocket_manager, health_check, serum_market
        )
    elif entropy.SpotMarket.isa(market):
        spot_market = entropy.SpotMarket.ensure(market)
        market_index: int = group.slot_by_spot_market_address(spot_market.address).index
        order_owner = (
            account.spot_open_orders_by_index[market_index] or SYSTEM_PROGRAM_ADDRESS
        )

        all_open_orders_watchers = __load_all_openorders_watchers(
            context, wallet, account, group, websocket_manager, health_check
        )
        latest_open_orders_observer = list(
            [
                oo_watcher
                for oo_watcher in all_open_orders_watchers
                if (
                    spot_market.base == spot_market.base
                    and spot_market.quote == spot_market.quote
                )
            ]
        )[0]

        inventory_watcher = entropy.InventoryAccountWatcher(
            spot_market,
            latest_account_observer,
            group_watcher,
            all_open_orders_watchers,
            cache_watcher,
        )
        latest_orderbook_watcher = entropy.build_orderbook_watcher(
            context, websocket_manager, health_check, spot_market
        )
        latest_event_queue_watcher = entropy.build_spot_event_queue_watcher(
            context, websocket_manager, health_check, spot_market
        )
    elif entropy.PerpMarket.isa(market):
        perp_market = entropy.PerpMarket.ensure(market)
        order_owner = account.address

        all_open_orders_watchers = __load_all_openorders_watchers(
            context, wallet, account, group, websocket_manager, health_check
        )

        inventory_watcher = entropy.InventoryAccountWatcher(
            perp_market,
            latest_account_observer,
            group_watcher,
            all_open_orders_watchers,
            cache_watcher,
        )

        latest_open_orders_observer = entropy.build_perp_open_orders_watcher(
            context,
            websocket_manager,
            health_check,
            perp_market,
            account,
            group,
            account_subscription,
        )
        latest_orderbook_watcher = entropy.build_orderbook_watcher(
            context, websocket_manager, health_check, perp_market
        )
        latest_event_queue_watcher = entropy.build_perp_event_queue_watcher(
            context, websocket_manager, health_check, perp_market
        )
    else:
        raise Exception(
            f"Could not determine type of market {market.fully_qualified_symbol} - {market}"
        )

    model_state = ModelState(
        order_owner,
        market,
        group_watcher,
        latest_account_observer,
        latest_price_observer,
        latest_open_orders_observer,
        inventory_watcher,
        latest_orderbook_watcher,
        latest_event_queue_watcher,
    )
    return WebsocketModelStateBuilder(model_state)
