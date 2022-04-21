from .context import entropy


def test_equality() -> None:
    assert entropy.Version.V1.value == entropy.Version.V1.value


def test_inequality() -> None:
    assert entropy.Version.V1.value != entropy.Version.V2.value
