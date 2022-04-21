import glob
import entropy
import os.path
import typing


def instrument_lookup_mainnet() -> entropy.InstrumentLookup:
    mainnet_token_lookup: entropy.InstrumentLookup = entropy.IdsJsonTokenLookup(
        "mainnet", "mainnet.2"
    )

    mainnet_overrides_filename = os.path.join(
        entropy.DATA_PATH, "overrides.tokenlist.json"
    )
    mainnet_overrides_token_lookup: entropy.InstrumentLookup = (
        entropy.SPLTokenLookup.load(mainnet_overrides_filename)
    )
    mainnet_non_spl_instrument_lookup: entropy.InstrumentLookup = (
        entropy.NonSPLInstrumentLookup.load(
            entropy.NonSPLInstrumentLookup.DefaultMainnetDataFilepath
        )
    )

    return entropy.CompoundInstrumentLookup(
        [
            mainnet_overrides_token_lookup,
            mainnet_token_lookup,
            mainnet_non_spl_instrument_lookup,
        ]
    )


def instrument_lookup_devnet() -> entropy.InstrumentLookup:
    devnet_token_lookup: entropy.InstrumentLookup = entropy.IdsJsonTokenLookup(
        "devnet", "devnet.2"
    )

    devnet_overrides_filename = os.path.join(
        entropy.DATA_PATH, "overrides.tokenlist.devnet.json"
    )
    devnet_overrides_token_lookup: entropy.InstrumentLookup = (
        entropy.SPLTokenLookup.load(devnet_overrides_filename)
    )
    devnet_non_spl_instrument_lookup: entropy.InstrumentLookup = (
        entropy.NonSPLInstrumentLookup.load(
            entropy.NonSPLInstrumentLookup.DefaultDevnetDataFilepath
        )
    )

    return entropy.CompoundInstrumentLookup(
        [
            devnet_overrides_token_lookup,
            devnet_token_lookup,
            devnet_non_spl_instrument_lookup,
        ]
    )


def instrument_lookup() -> entropy.InstrumentLookup:
    return entropy.CompoundInstrumentLookup(
        [instrument_lookup_mainnet(), instrument_lookup_devnet()]
    )


def market_lookup_mainnet() -> entropy.MarketLookup:
    return entropy.IdsJsonMarketLookup("mainnet", instrument_lookup_mainnet())


def market_lookup_devnet() -> entropy.MarketLookup:
    return entropy.IdsJsonMarketLookup("devnet", instrument_lookup_devnet())


def market_lookup() -> entropy.MarketLookup:
    return entropy.CompoundMarketLookup(
        [market_lookup_mainnet(), market_lookup_devnet()]
    )


def load_group(filename: str) -> entropy.Group:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    instruments: entropy.InstrumentLookup = instrument_lookup()
    markets: entropy.MarketLookup = market_lookup()
    return entropy.Group.parse(account_info, "devnet.2", instruments, markets)


def load_account(
    filename: str, group: entropy.Group, cache: entropy.Cache
) -> entropy.Account:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    return entropy.Account.parse(account_info, group, cache)


def load_openorders(filename: str) -> entropy.OpenOrders:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    parsed = entropy.layouts.OPEN_ORDERS.parse(account_info.data)
    markets: entropy.MarketLookup = market_lookup()
    market = markets.find_by_address(parsed.market)
    if market is None:
        raise Exception(f"Could not find market metadata for {parsed.market}")

    return entropy.OpenOrders.parse(
        account_info, entropy.Token.ensure(market.base), market.quote
    )


def load_cache(filename: str) -> entropy.Cache:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    return entropy.Cache.parse(account_info)


def load_root_bank(filename: str) -> entropy.RootBank:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    return entropy.RootBank.parse(account_info)


def load_node_bank(filename: str) -> entropy.NodeBank:
    account_info: entropy.AccountInfo = entropy.AccountInfo.load_json(filename)
    return entropy.NodeBank.parse(account_info)


def load_data_from_directory(
    directory_path: str,
) -> typing.Tuple[
    entropy.Group, entropy.Cache, entropy.Account, typing.Dict[str, entropy.OpenOrders]
]:
    all_openorders = {}
    for filepath in glob.iglob(f"{directory_path}/openorders*.json"):
        openorders = load_openorders(filepath)
        all_openorders[str(openorders.address)] = openorders
    cache = load_cache(f"{directory_path}/cache.json")
    group = load_group(f"{directory_path}/group.json")
    account = load_account(f"{directory_path}/account.json", group, cache)

    return group, cache, account, all_openorders
