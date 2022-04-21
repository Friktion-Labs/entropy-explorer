from .context import entropy


def test_compare_from_timestamp_to_utc_now() -> None:
    timestamp = entropy.datetime_from_timestamp(1645793955)
    now = entropy.utc_now()
    assert now > timestamp


def test_compare_from_timestamp_to_chain() -> None:
    timestamp = entropy.datetime_from_timestamp(1645793955)
    chain = entropy.datetime_from_chain(1645793955)
    assert chain == timestamp


def test_compare_from_chain_to_utc_now() -> None:
    chain = entropy.datetime_from_chain(1645793955)
    now = entropy.utc_now()
    assert now > chain


def test_compare_from_chain_to_local_now() -> None:
    chain = entropy.datetime_from_chain(1645793955)
    now = entropy.local_now()
    assert now > chain
