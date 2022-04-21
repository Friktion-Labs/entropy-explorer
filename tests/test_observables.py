from .context import entropy

import rx


def test_collecting_observer_subscriber() -> None:
    items = ["a", "b", "c"]
    actual = entropy.CollectingObserverSubscriber()
    rx.from_(items).subscribe(actual)
    assert actual.collected == items
