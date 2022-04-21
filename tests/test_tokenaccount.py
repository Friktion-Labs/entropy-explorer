from .context import entropy
from .fakes import fake_account_info, fake_seeded_public_key, fake_token

from decimal import Decimal


def test_constructor() -> None:
    token = fake_token()
    token_value = entropy.InstrumentValue(token, Decimal(6))
    owner = fake_seeded_public_key("token owner")
    actual = entropy.TokenAccount(
        fake_account_info(), entropy.Version.V1, owner, token_value
    )
    assert actual is not None
