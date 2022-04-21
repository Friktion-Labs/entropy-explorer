from .context import entropy

from solana.publickey import PublicKey


def test_scout_report_constructor() -> None:
    address: PublicKey = PublicKey("11111111111111111111111111111112")
    actual = entropy.ScoutReport(address)
    assert actual is not None
    assert actual.address == address
    assert actual.errors == []
    assert actual.warnings == []
    assert actual.details == []


def test_account_scout_constructor() -> None:
    actual = entropy.AccountScout()
    assert actual is not None
