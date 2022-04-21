from .context import entropy

import typing


class MockNotificationTarget(entropy.NotificationTarget):
    def __init__(self) -> None:
        super().__init__()
        self.send_notification_called = False

    def send_notification(self, item: typing.Any) -> None:
        self.send_notification_called = True


def test_notification_target_constructor() -> None:
    succeeded = False
    try:
        entropy.NotificationTarget()  # type: ignore[abstract]
    except TypeError:
        # Can't instantiate the abstract base class.
        succeeded = True
    assert succeeded


def test_telegram_notification_target_constructor() -> None:
    address = "chat@bot"
    actual = entropy.TelegramNotificationTarget(address)
    assert actual is not None
    assert actual.chat_id == "chat"
    assert actual.bot_id == "bot"


def test_discord_notification_target_constructor() -> None:
    address = "discord-address"
    actual = entropy.DiscordNotificationTarget(address)
    assert actual is not None
    assert actual.address == address


def test_mailjet_notification_target_constructor() -> None:
    encoded_parameters = "user:secret:subject:from%20name:from@address:to%20name%20with%20colon%3A:to@address"
    actual = entropy.MailjetNotificationTarget(encoded_parameters)
    assert actual is not None
    assert actual.api_key == "user"
    assert actual.api_secret == "secret"
    assert actual.subject == "subject"
    assert actual.from_name == "from name"
    assert actual.from_address == "from@address"
    assert actual.to_name == "to name with colon:"
    assert actual.to_address == "to@address"


def test_filtering_notification_target_constructor() -> None:
    mock = MockNotificationTarget()

    def func(_: typing.Any) -> bool:
        return True

    actual = entropy.FilteringNotificationTarget(mock, func)
    assert actual is not None
    assert actual.inner_notifier == mock
    assert actual.filter_func == func


def test_filtering_notification_target() -> None:
    mock = MockNotificationTarget()
    filtering = entropy.FilteringNotificationTarget(mock, lambda x: bool(x == "yes"))
    filtering.send("no")
    assert not mock.send_notification_called
    filtering.send("yes")
    assert mock.send_notification_called


def test_parse_notification_target() -> None:
    telegram_target = entropy.parse_notification_target(
        "telegram:012345678@9876543210:ABCDEFGHijklmnop-qrstuvwxyzABCDEFGH"
    )
    assert telegram_target is not None

    discord_target = entropy.parse_notification_target(
        "discord:https://discord.com/api/webhooks/012345678901234567/ABCDE_fghij-KLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN"
    )
    assert discord_target is not None

    mailjet_target = entropy.parse_notification_target(
        "mailjet:user:secret:subject:from%20name:from@address:to%20name%20with%20colon%3A:to@address"
    )
    assert mailjet_target is not None
