import argparse

from ...context import entropy
from ...fakes import fake_context, fake_model_state, fake_loaded_market, fake_order

from decimal import Decimal

from entropy.marketmaking.orderchain.preventpostonlycrossingbookelement import (
    PreventPostOnlyCrossingBookElement,
)


# The top bid is the highest price someone is willing to pay to BUY
top_bid: entropy.Order = fake_order(
    price=Decimal(90), side=entropy.Side.BUY, order_type=entropy.OrderType.POST_ONLY
)
# The top ask is the lowest price someone is willing to pay to SELL
top_ask: entropy.Order = fake_order(
    price=Decimal(110), side=entropy.Side.SELL, order_type=entropy.OrderType.POST_ONLY
)

orderbook: entropy.OrderBook = entropy.OrderBook(
    "TEST", entropy.NullLotSizeConverter(), [top_bid], [top_ask]
)

model_state = fake_model_state(market=fake_loaded_market(), orderbook=orderbook)


def test_from_args() -> None:
    args: argparse.Namespace = argparse.Namespace()
    actual: PreventPostOnlyCrossingBookElement = (
        PreventPostOnlyCrossingBookElement.from_command_line_parameters(args)
    )
    assert actual is not None


def test_not_crossing_results_in_no_change() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(100), order_type=entropy.OrderType.POST_ONLY
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    result = actual.process(context, model_state, [order])

    assert result == [order]


def test_bid_too_high_results_in_new_bid() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(120),
        side=entropy.Side.BUY,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    result = actual.process(context, model_state, [order])

    assert result[0].price == 109


def test_bid_too_low_results_in_no_change() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(80), side=entropy.Side.BUY, order_type=entropy.OrderType.POST_ONLY
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    result = actual.process(context, model_state, [order])

    assert result == [order]


def test_ask_too_low_results_in_new_ask() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(80),
        side=entropy.Side.SELL,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    result = actual.process(context, model_state, [order])

    assert result[0].price == 91


def test_ask_too_high_results_in_no_change() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(120),
        side=entropy.Side.SELL,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    result = actual.process(context, model_state, [order])

    assert result == [order]


def test_bid_too_high_no_bid_results_in_new_bid() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(120),
        side=entropy.Side.BUY,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    orderbook: entropy.OrderBook = entropy.OrderBook(
        "TEST", entropy.NullLotSizeConverter(), [], [top_ask]
    )
    model_state = fake_model_state(market=fake_loaded_market(), orderbook=orderbook)

    result = actual.process(context, model_state, [order])

    assert result[0].price == 109


def test_ask_too_low_no_ask_results_in_new_ask() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(80),
        side=entropy.Side.SELL,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    orderbook: entropy.OrderBook = entropy.OrderBook(
        "TEST", entropy.NullLotSizeConverter(), [top_bid], []
    )
    model_state = fake_model_state(market=fake_loaded_market(), orderbook=orderbook)
    result = actual.process(context, model_state, [order])

    assert result[0].price == 91


def test_ask_no_orderbook_results_in_no_change() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(120),
        side=entropy.Side.SELL,
        order_type=entropy.OrderType.POST_ONLY,
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    orderbook: entropy.OrderBook = entropy.OrderBook(
        "TEST", entropy.NullLotSizeConverter(), [], []
    )
    model_state = fake_model_state(market=fake_loaded_market(), orderbook=orderbook)
    result = actual.process(context, model_state, [order])

    assert result == [order]


def test_bid_no_orderbook_results_in_no_change() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(80), side=entropy.Side.BUY, order_type=entropy.OrderType.POST_ONLY
    )

    actual: PreventPostOnlyCrossingBookElement = PreventPostOnlyCrossingBookElement()
    orderbook: entropy.OrderBook = entropy.OrderBook(
        "TEST", entropy.NullLotSizeConverter(), [], []
    )
    model_state = fake_model_state(market=fake_loaded_market(), orderbook=orderbook)
    result = actual.process(context, model_state, [order])

    assert result == [order]
