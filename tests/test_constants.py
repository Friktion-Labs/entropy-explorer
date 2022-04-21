from .context import entropy


# There isn't really a lot to test here that isn't just duplication so instead there are just
# a couple of checks to make sure things have loaded properly.


def test_system_program_address() -> None:
    assert str(entropy.SYSTEM_PROGRAM_ADDRESS) == "11111111111111111111111111111111"


def test_entropy_constants() -> None:
    entropy_groups = entropy.EntropyConstants["groups"]
    assert entropy_groups is not None
    assert len(entropy_groups) > 0
