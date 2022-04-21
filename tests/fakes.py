import construct
import entropy
import entropy.marketmaking
import typing

from decimal import Decimal
from pyserum.market.market import Market as PySerumMarket
from pyserum.market.state import MarketState as PySerumMarketState
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from solana.rpc.types import RPCResponse


class MockCompatibleClient(Client):
    def __init__(self) -> None:
        super().__init__("http://localhost", Commitment("processed"))
        self.token_accounts_by_owner: typing.Sequence[typing.Any] = []

    def get_token_accounts_by_owner(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> RPCResponse:
        return RPCResponse(result={"value": self.token_accounts_by_owner})

    def get_minimum_balance_for_rent_exemption(
        size, *args: typing.Any, **kwargs: typing.Any
    ) -> RPCResponse:
        return RPCResponse(result=27)


class MockClient(entropy.BetterClient):
    def __init__(self) -> None:
        rpc = entropy.RPCCaller(
            "fake",
            "http://localhost",
            "ws://localhost",
            -1,
            [],
            entropy.NullSlotHolder(),
            entropy.InstructionReporter(),
        )
        compound = entropy.CompoundRPCCaller("fake", [rpc])
        super().__init__(
            MockCompatibleClient(),
            "test",
            "local",
            Commitment("processed"),
            False,
            -1,
            "base64",
            0,
            compound,
        )


def fake_public_key() -> PublicKey:
    return PublicKey("11111111111111111111111111111112")


def fake_seeded_public_key(seed: str) -> PublicKey:
    return PublicKey.create_with_seed(
        PublicKey("11111111111111111111111111111112"),
        seed,
        PublicKey("11111111111111111111111111111111"),
    )


def fake_context(
    entropy_program_address: typing.Optional[PublicKey] = None,
) -> entropy.Context:
    context = entropy.Context(
        name="Entropy Test",
        cluster_name="test",
        cluster_urls=[
            entropy.ClusterUrlData(rpc="http://localhost"),
            entropy.ClusterUrlData(rpc="http://localhost"),
        ],
        skip_preflight=False,
        tpu_retransmissions=-1,
        commitment="processed",
        encoding="base64",
        blockhash_cache_duration=0,
        http_request_timeout=-1,
        stale_data_pauses_before_retry=[],
        entropy_program_address=entropy_program_address
        or fake_seeded_public_key("Entropy program address"),
        serum_program_address=fake_seeded_public_key("Serum program address"),
        group_name="TEST_GROUP",
        group_address=fake_seeded_public_key("group ID"),
        gma_chunk_size=Decimal(20),
        gma_chunk_pause=Decimal(25),
        reflink=None,
        instrument_lookup=entropy.IdsJsonTokenLookup("devnet", "devnet.2"),
        market_lookup=entropy.NullMarketLookup(),
    )
    context.client = MockClient()
    return context


def fake_account_info(
    address: typing.Optional[PublicKey] = None,
    executable: bool = False,
    lamports: Decimal = Decimal(0),
    owner: PublicKey = fake_public_key(),
    rent_epoch: Decimal = Decimal(0),
    data: bytes = bytes([0]),
) -> entropy.AccountInfo:
    if address is None:
        address = fake_public_key()
    return entropy.AccountInfo(address, executable, lamports, owner, rent_epoch, data)


def fake_instrument(symbol: str = "FAKE", decimals: int = 6) -> entropy.Instrument:
    return entropy.Instrument(symbol, f"Fake Instrument ({symbol})", Decimal(decimals))


def fake_token(symbol: str = "FAKE", decimals: int = 6) -> entropy.Token:
    return entropy.Token(
        symbol,
        f"Fake Token ({symbol})",
        Decimal(decimals),
        fake_seeded_public_key(f"fake token ({symbol})"),
    )


def fake_perp_account() -> entropy.PerpAccount:
    return entropy.PerpAccount(
        Decimal(0),
        Decimal(0),
        Decimal(0),
        Decimal(0),
        Decimal(0),
        Decimal(0),
        Decimal(0),
        Decimal(0),
        fake_instrument_value(),
        entropy.PerpOpenOrders([]),
        entropy.NullLotSizeConverter(),
        fake_instrument_value(),
        Decimal(0),
        Decimal(0),
    )


def fake_token_bank(symbol: str = "FAKE") -> entropy.TokenBank:
    return entropy.TokenBank(fake_token(symbol), fake_seeded_public_key("root bank"))


def fake_market() -> PySerumMarket:
    # Container = NamedTuple("Container", [("own_address", PublicKey), ("vault_signer_nonce", int)])
    container = construct.Container(
        {
            "own_address": fake_seeded_public_key("market address"),
            "vault_signer_nonce": 2,
        }
    )
    # container: Container[typing.Any] = Container(
    #     own_address=fake_seeded_public_key("market address"), vault_signer_nonce=2)
    state = PySerumMarketState(container, fake_seeded_public_key("program ID"), 6, 6)
    state.base_vault = lambda: fake_seeded_public_key("base vault")  # type: ignore[assignment]
    state.quote_vault = lambda: fake_seeded_public_key("quote vault")  # type: ignore[assignment]
    state.event_queue = lambda: fake_seeded_public_key("event queue")  # type: ignore[assignment]
    state.request_queue = lambda: fake_seeded_public_key("request queue")  # type: ignore[assignment]
    state.bids = lambda: fake_seeded_public_key("bids")  # type: ignore[assignment]
    state.asks = lambda: fake_seeded_public_key("asks")  # type: ignore[assignment]
    state.base_lot_size = lambda: 1  # type: ignore[assignment]
    state.quote_lot_size = lambda: 1  # type: ignore[assignment]
    return PySerumMarket(MockCompatibleClient(), state)


def fake_spot_market_stub() -> entropy.SpotMarketStub:
    return entropy.SpotMarketStub(
        fake_seeded_public_key("program ID"),
        fake_seeded_public_key("spot market"),
        fake_token("BASE"),
        fake_token("QUOTE"),
        fake_seeded_public_key("group address"),
    )


def fake_loaded_market(
    base_lot_size: Decimal = Decimal(1), quote_lot_size: Decimal = Decimal(1)
) -> entropy.LoadedMarket:
    class FakeLoadedMarket(entropy.LoadedMarket):
        @property
        def fully_qualified_symbol(self) -> str:
            return "full:MARKET/SYMBOL"

        @property
        def bids_address(self) -> PublicKey:
            return fake_seeded_public_key("bids_address")

        @property
        def asks_address(self) -> PublicKey:
            return fake_seeded_public_key("asks_address")

        @property
        def event_queue_address(self) -> PublicKey:
            return fake_seeded_public_key("event_queue_address")

        def on_fill(
            self,
            context: entropy.Context,
            handler: typing.Callable[[entropy.FillEvent], None],
        ) -> entropy.Disposable:
            return entropy.Disposable()

        def on_event(
            self,
            context: entropy.Context,
            handler: typing.Callable[[entropy.Event], None],
        ) -> entropy.Disposable:
            return entropy.Disposable()

        def parse_account_info_to_orders(
            self, account_info: entropy.AccountInfo
        ) -> typing.Sequence[entropy.Order]:
            return []

    base = fake_token("BASE")
    quote = fake_token("QUOTE")
    return FakeLoadedMarket(
        entropy.MarketType.PERP,
        fake_seeded_public_key("program ID"),
        fake_seeded_public_key("perp market"),
        entropy.InventorySource.ACCOUNT,
        base,
        quote,
        entropy.LotSizeConverter(base, base_lot_size, quote, quote_lot_size),
    )


def fake_token_account() -> entropy.TokenAccount:
    token_account_info = fake_account_info()
    token = fake_token()
    token_value = entropy.InstrumentValue(token, Decimal("100"))
    return entropy.TokenAccount(
        token_account_info,
        entropy.Version.V1,
        fake_seeded_public_key("owner"),
        token_value,
    )


def fake_instrument_value(value: Decimal = Decimal(100)) -> entropy.InstrumentValue:
    return entropy.InstrumentValue(fake_token(), value)


def fake_wallet() -> entropy.Wallet:
    wallet = entropy.Wallet(bytes([1] * 64))
    wallet.keypair = Keypair()
    return wallet


def fake_order(
    price: Decimal = Decimal(1),
    quantity: Decimal = Decimal(1),
    side: entropy.Side = entropy.Side.BUY,
    order_type: entropy.OrderType = entropy.OrderType.LIMIT,
) -> entropy.Order:
    return entropy.Order.from_values(
        side=side, price=price, quantity=quantity, order_type=order_type
    )


# serum ID structure - 16-byte 'int': low 8 bytes is a sequence number, high 8 bytes is price
def fake_order_id(index: int, price: int) -> int:
    # price needs to be max of 64bit/8bytes, considering signed int is not permitted
    if index > (2 ** 64) - 1 or price > (2 ** 64) - 1:
        raise ValueError(
            f"Provided index '{index}' or price '{price}' is bigger than 8 bytes int"
        )
    index_bytes = index.to_bytes(8, byteorder="big", signed=False)
    price_bytes = price.to_bytes(8, byteorder="big", signed=False)
    return int.from_bytes((price_bytes + index_bytes), byteorder="big", signed=False)


def fake_price(
    market: entropy.LoadedMarket = fake_loaded_market(),
    price: Decimal = Decimal(100),
    bid: Decimal = Decimal(99),
    ask: Decimal = Decimal(101),
) -> entropy.Price:
    return entropy.Price(
        entropy.OracleSource(
            "test", "test", entropy.SupportedOracleFeature.TOP_BID_AND_OFFER, market
        ),
        entropy.utc_now(),
        market,
        bid,
        price,
        ask,
        Decimal(0),
    )


def fake_placed_orders_container() -> entropy.PlacedOrdersContainer:
    return entropy.PerpOpenOrders([])


def fake_inventory(
    incentives: Decimal = Decimal(1),
    available: Decimal = Decimal(100),
    base: Decimal = Decimal(10),
    quote: Decimal = Decimal(10),
) -> entropy.Inventory:
    return entropy.Inventory(
        entropy.InventorySource.SPL_TOKENS,
        fake_instrument_value(incentives),
        fake_instrument_value(available),
        fake_instrument_value(base),
        fake_instrument_value(quote),
    )


def fake_bids() -> typing.Sequence[entropy.Order]:
    return []


def fake_asks() -> typing.Sequence[entropy.Order]:
    return []


def fake_account_slot() -> entropy.AccountSlot:
    return entropy.AccountSlot(
        1,
        fake_instrument(),
        fake_token_bank(),
        fake_token_bank(),
        Decimal(1),
        fake_instrument_value(),
        Decimal(0),
        fake_instrument_value(),
        fake_seeded_public_key("open_orders"),
        None,
    )


def fake_account(address: typing.Optional[PublicKey] = None) -> entropy.Account:
    meta_data = entropy.Metadata(
        entropy.layouts.DATA_TYPE.Account, entropy.Version.V1, True
    )
    quote = fake_account_slot()
    return entropy.Account(
        fake_account_info(address=address),
        entropy.Version.V1,
        meta_data,
        "GROUPNAME",
        fake_seeded_public_key("group"),
        fake_seeded_public_key("owner"),
        "INFO",
        quote,
        [],
        [],
        [],
        Decimal(1),
        False,
        False,
        fake_seeded_public_key("advanced_orders"),
        False,
        fake_seeded_public_key("delegate"),
    )


def fake_root_bank() -> entropy.RootBank:
    meta_data = entropy.Metadata(
        entropy.layouts.DATA_TYPE.RootBank, entropy.Version.V1, True
    )
    return entropy.RootBank(
        fake_account_info(),
        entropy.Version.V1,
        meta_data,
        Decimal(0),
        Decimal(0),
        Decimal(0),
        [],
        Decimal(0),
        Decimal(0),
        entropy.utc_now(),
    )


def fake_cache() -> entropy.Cache:
    meta_data = entropy.Metadata(
        entropy.layouts.DATA_TYPE.RootBank, entropy.Version.V1, True
    )
    return entropy.Cache(fake_account_info(), entropy.Version.V1, meta_data, [], [], [])


def fake_root_bank_cache() -> entropy.RootBankCache:
    return entropy.RootBankCache(
        Decimal(1),
        Decimal(2),
        entropy.utc_now(),
    )


def fake_group(address: typing.Optional[PublicKey] = None) -> entropy.Group:
    account_info = fake_account_info(address=address)
    name = "FAKE_GROUP"
    meta_data = entropy.Metadata(
        entropy.layouts.DATA_TYPE.Group, entropy.Version.V1, True
    )
    instrument_lookup = fake_context().instrument_lookup
    usdc = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("usdc"))
    quote_info = entropy.TokenBank(usdc, fake_seeded_public_key("root bank"))
    signer_nonce = Decimal(1)
    signer_key = fake_seeded_public_key("signer key")
    admin_key = fake_seeded_public_key("admin key")
    serum_program_address = fake_seeded_public_key("DEX program ID")
    cache_key = fake_seeded_public_key("cache key")
    valid_interval = Decimal(7)
    insurance_vault = fake_seeded_public_key("insurance vault")
    srm_vault = fake_seeded_public_key("srm vault")
    msrm_vault = fake_seeded_public_key("msrm vault")
    fees_vault = fake_seeded_public_key("fees vault")
    max_entropy_accounts = Decimal(1000000)
    num_entropy_accounts = Decimal(1)
    referral_surcharge_centibps = Decimal(7)
    referral_share_centibps = Decimal(8)
    referral_mngo_required = Decimal(9)

    return entropy.Group(
        account_info,
        entropy.Version.V1,
        name,
        meta_data,
        quote_info,
        [],
        [],
        signer_nonce,
        signer_key,
        admin_key,
        serum_program_address,
        cache_key,
        valid_interval,
        insurance_vault,
        srm_vault,
        msrm_vault,
        fees_vault,
        max_entropy_accounts,
        num_entropy_accounts,
        referral_surcharge_centibps,
        referral_share_centibps,
        referral_mngo_required,
    )


def fake_prices(
    prices: typing.Sequence[str],
) -> typing.Sequence[entropy.InstrumentValue]:
    instrument_lookup = fake_context().instrument_lookup
    ETH = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("ETH"))
    BTC = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("BTC"))
    SOL = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("SOL"))
    SRM = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("SRM"))
    USDC = entropy.Token.ensure(instrument_lookup.find_by_symbol_or_raise("USDC"))
    eth, btc, sol, srm, usdc = prices

    return [
        entropy.InstrumentValue(ETH, Decimal(eth)),
        entropy.InstrumentValue(BTC, Decimal(btc)),
        entropy.InstrumentValue(SOL, Decimal(sol)),
        entropy.InstrumentValue(SRM, Decimal(srm)),
        entropy.InstrumentValue(USDC, Decimal(usdc)),
    ]


def fake_open_orders(
    base_token_free: Decimal = Decimal(0),
    base_token_total: Decimal = Decimal(0),
    quote_token_free: Decimal = Decimal(0),
    quote_token_total: Decimal = Decimal(0),
    referrer_rebate_accrued: Decimal = Decimal(0),
) -> entropy.OpenOrders:
    account_info = fake_account_info()
    program_address = fake_seeded_public_key("program address")
    market = fake_seeded_public_key("market")
    owner = fake_seeded_public_key("owner")

    base = fake_token("FAKEBASE")
    quote = fake_token("FAKEQUOTE")
    flags = entropy.AccountFlags(
        entropy.Version.V1, True, False, True, False, False, False, False, False
    )
    return entropy.OpenOrders(
        account_info,
        entropy.Version.V1,
        program_address,
        flags,
        market,
        owner,
        base,
        quote,
        base_token_free,
        base_token_total,
        quote_token_free,
        quote_token_total,
        [],
        referrer_rebate_accrued,
    )


def fake_model_state(
    order_owner: typing.Optional[PublicKey] = None,
    market: typing.Optional[entropy.Market] = None,
    group: typing.Optional[entropy.Group] = None,
    account: typing.Optional[entropy.Account] = None,
    price: typing.Optional[entropy.Price] = None,
    placed_orders_container: typing.Optional[entropy.PlacedOrdersContainer] = None,
    inventory: typing.Optional[entropy.Inventory] = None,
    orderbook: typing.Optional[entropy.OrderBook] = None,
    event_queue: typing.Optional[entropy.EventQueue] = None,
) -> entropy.ModelState:
    order_owner = order_owner or fake_seeded_public_key("order owner")
    market = market or fake_loaded_market()
    group = group or fake_group()
    account = account or fake_account()
    price = price or fake_price()
    placed_orders_container = placed_orders_container or fake_placed_orders_container()
    inventory = inventory or fake_inventory()
    orderbook = orderbook or entropy.OrderBook(
        "FAKE", entropy.NullLotSizeConverter(), fake_bids(), fake_asks()
    )
    event_queue = event_queue or entropy.NullEventQueue()
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

    return entropy.ModelState(
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


def fake_entropy_instruction() -> entropy.EntropyInstruction:
    return entropy.EntropyInstruction(
        fake_seeded_public_key("program id"),
        entropy.InstructionType.PlacePerpOrder,
        bytes(),
        "",
        [fake_seeded_public_key("account")],
    )
