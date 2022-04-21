import entropy

from decimal import Decimal

from entropy.marketmaking.orderreconciler import (
    NullOrderReconciler,
    AlwaysReplaceOrderReconciler,
)

from ..fakes import fake_model_state


def test_nulloperation() -> None:
    existing = [
        entropy.Order.from_values(
            entropy.Side.BUY, price=Decimal(1), quantity=Decimal(10)
        ),
        entropy.Order.from_values(
            entropy.Side.SELL, price=Decimal(2), quantity=Decimal(20)
        ),
    ]
    desired = [
        entropy.Order.from_values(
            entropy.Side.BUY, price=Decimal(3), quantity=Decimal(30)
        ),
        entropy.Order.from_values(
            entropy.Side.SELL, price=Decimal(4), quantity=Decimal(40)
        ),
    ]

    model_state = fake_model_state()
    actual = NullOrderReconciler()
    result = actual.reconcile(model_state, existing, desired)

    assert result.to_keep == existing
    assert result.to_ignore == desired
    assert result.to_cancel == []
    assert result.to_place == []

    assert not result.cancelling_all


def test_alwaysreplace() -> None:
    existing = [
        entropy.Order.from_values(
            entropy.Side.BUY, price=Decimal(1), quantity=Decimal(10)
        ),
        entropy.Order.from_values(
            entropy.Side.SELL, price=Decimal(2), quantity=Decimal(20)
        ),
    ]
    desired = [
        entropy.Order.from_values(
            entropy.Side.BUY, price=Decimal(3), quantity=Decimal(30)
        ),
        entropy.Order.from_values(
            entropy.Side.SELL, price=Decimal(4), quantity=Decimal(40)
        ),
    ]

    model_state = fake_model_state()
    actual = AlwaysReplaceOrderReconciler()
    result = actual.reconcile(model_state, existing, desired)

    assert result.to_keep == []
    assert result.to_ignore == []
    assert result.to_cancel == existing
    assert result.to_place == desired

    assert result.cancelling_all
