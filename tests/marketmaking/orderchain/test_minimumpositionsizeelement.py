import argparse
import typing

from ...context import entropy
from ...fakes import fake_context, fake_model_state, fake_order

from decimal import Decimal

from entropy.marketmaking.orderchain.minimumquantityelement import (
    MinimumQuantityElement,
)

bids: typing.Sequence[entropy.Order] = [
    fake_order(price=Decimal(78), quantity=Decimal(1), side=entropy.Side.BUY),
    fake_order(price=Decimal(77), quantity=Decimal(2), side=entropy.Side.BUY),
    fake_order(price=Decimal(76), quantity=Decimal(1), side=entropy.Side.BUY),
    fake_order(price=Decimal(75), quantity=Decimal(5), side=entropy.Side.BUY),
    fake_order(price=Decimal(74), quantity=Decimal(3), side=entropy.Side.BUY),
    fake_order(price=Decimal(73), quantity=Decimal(7), side=entropy.Side.BUY),
]
asks: typing.Sequence[entropy.Order] = [
    fake_order(price=Decimal(82), quantity=Decimal(3), side=entropy.Side.SELL),
    fake_order(price=Decimal(83), quantity=Decimal(1), side=entropy.Side.SELL),
    fake_order(price=Decimal(84), quantity=Decimal(1), side=entropy.Side.SELL),
    fake_order(price=Decimal(85), quantity=Decimal(3), side=entropy.Side.SELL),
    fake_order(price=Decimal(86), quantity=Decimal(3), side=entropy.Side.SELL),
    fake_order(price=Decimal(87), quantity=Decimal(7), side=entropy.Side.SELL),
]
orderbook: entropy.OrderBook = entropy.OrderBook(
    "TEST", entropy.NullLotSizeConverter(), bids, asks
)
model_state = fake_model_state(orderbook=orderbook)


def test_from_args() -> None:
    args: argparse.Namespace = argparse.Namespace(
        minimumquantity_size=Decimal(7), minimumquantity_remove=True
    )
    actual: MinimumQuantityElement = (
        MinimumQuantityElement.from_command_line_parameters(args)
    )
    assert actual is not None
    assert actual.minimum_quantity == 7
    assert actual.remove


def test_high_buy_not_updated() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(75), quantity=Decimal(20), side=entropy.Side.BUY
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10))
    result = actual.process(context, model_state, [order])

    assert result[0] == order


def test_low_buy_updated() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(75), quantity=Decimal(7), side=entropy.Side.BUY
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10))
    result = actual.process(context, model_state, [order])

    assert result[0].quantity == 10


def test_low_buy_removed() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(75), quantity=Decimal(7), side=entropy.Side.BUY
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10), True)
    result = actual.process(context, model_state, [order])

    assert len(result) == 0


def test_high_sell_not_updated() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(85), quantity=Decimal(16), side=entropy.Side.SELL
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10))
    result = actual.process(context, model_state, [order])

    assert result[0] == order


def test_low_sell_updated() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(85), quantity=Decimal(6), side=entropy.Side.SELL
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10))
    result = actual.process(context, model_state, [order])

    assert result[0].quantity == 10


def test_low_sell_removed() -> None:
    context = fake_context()
    order: entropy.Order = fake_order(
        price=Decimal(85), quantity=Decimal(6), side=entropy.Side.SELL
    )

    actual: MinimumQuantityElement = MinimumQuantityElement(Decimal(10), True)
    result = actual.process(context, model_state, [order])

    assert len(result) == 0
