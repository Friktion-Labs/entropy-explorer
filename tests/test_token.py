from .context import entropy

from decimal import Decimal
from solana.publickey import PublicKey


def test_instrument_constructor() -> None:
    symbol = "TEST"
    name = "Test Instrument"
    decimals = Decimal(18)
    actual = entropy.Instrument(symbol, name, decimals)
    assert actual is not None
    assert actual.symbol == symbol
    assert actual.name == name
    assert actual.decimals == decimals


def test_instrument_constructor_uppercases_symbol() -> None:
    symbol = "test1"
    name = "Test Instrument"
    decimals = Decimal(18)
    actual = entropy.Instrument(symbol, name, decimals)
    assert actual.symbol == "TEST1"


def test_token_constructor() -> None:
    symbol = "TEST"
    name = "Test Token"
    mint = PublicKey("11111111111111111111111111111113")
    decimals = Decimal(18)
    actual = entropy.Token(symbol, name, decimals, mint)
    assert actual is not None
    assert actual.symbol == symbol
    assert actual.name == name
    assert actual.mint == mint
    assert actual.decimals == decimals


def test_token_constructor_uppercases_symbol() -> None:
    symbol = "test2"
    name = "Test Token"
    mint = PublicKey("11111111111111111111111111111113")
    decimals = Decimal(18)
    actual = entropy.Token(symbol, name, decimals, mint)
    assert actual.symbol == "TEST2"


def test_instrument_symbol_matching() -> None:
    assert entropy.Instrument.symbols_match("BTC", "BTC")
    assert entropy.Instrument.symbols_match("eth", "eth")
    assert entropy.Instrument.symbols_match("btc", "BTC")
    assert entropy.Instrument.symbols_match("ETH", "eth")
    assert not entropy.Instrument.symbols_match("ETH", "BTC")
