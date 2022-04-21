from .context import entropy


def test_decode_binary() -> None:
    data = entropy.decode_binary(["SGVsbG8gV29ybGQ=", "base64"])  # "Hello World"
    assert len(data) == 11
