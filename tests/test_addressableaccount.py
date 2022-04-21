import typing

from .context import entropy
from .fakes import fake_account_info


def test_constructor() -> None:
    class __derived(entropy.AddressableAccount):
        def subscribe(
            self,
            context: entropy.Context,
            websocketmanager: entropy.WebSocketSubscriptionManager,
            callback: typing.Callable[[entropy.AddressableAccount], None],
        ) -> entropy.Disposable:
            raise NotImplementedError(
                "AddressableAccount.subscribe is not implemented on this test class."
            )

    account_info = fake_account_info()
    actual = __derived(account_info)
    assert actual is not None
    assert actual.address == account_info.address
