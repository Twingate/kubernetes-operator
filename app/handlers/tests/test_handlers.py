from datetime import timedelta

import kopf


def test_timer_handlers_minimum_5h():
    # For safe-keeping - during debug someone might change timer
    exceptions = ["twingate_connector_pod_reconciler"]

    registry = kopf.get_default_registry()
    spawning_handlers = registry._spawning  # noqa: SLF001
    for handler in spawning_handlers._handlers:  # noqa: SLF001
        if (
            isinstance(handler, kopf._core.intents.handlers.TimerHandler)  # noqa: SLF001
            and handler.id not in exceptions
        ):
            assert handler.interval > timedelta(hours=5).seconds
