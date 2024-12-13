import logging
from typing import Any

import kopf
from pydantic import ValidationError

from app.handlers import *  # noqa: F403
from app.settings import TwingateOperatorSettings, KopfWatchingSettings


class TwingateSmartProgressStorage(kopf.SmartProgressStorage):
    def __init__(self, **kwargs):
        kwargs = kwargs or {}
        kwargs["name"] = "twingate"
        kwargs["prefix"] = "twingate.com"
        super().__init__(**kwargs)


class TwingateAnnotationsDiffBaseStorage(kopf.AnnotationsDiffBaseStorage):
    def __init__(self, **kwargs):
        kwargs = kwargs or {}
        kwargs["prefix"] = "twingate.com"
        super().__init__(**kwargs)


@kopf.on.startup()
def startup(
    settings: kopf.OperatorSettings,
    logger: logging.Logger | logging.LoggerAdapter,
    memo: Any,
    **kwargs,
):
    logger.info("Operator is starting up...")

    KopfWatchingSettings().update_kopf_watching_settings(settings)
    settings.persistence.finalizer = "twingate.com/finalizer"
    settings.persistence.diffbase_storage = TwingateAnnotationsDiffBaseStorage()
    settings.persistence.progress_storage = TwingateSmartProgressStorage()

    try:
        memo.twingate_settings = TwingateOperatorSettings()
    except ValidationError:
        logger.exception("Failed to load settings.")

    # Disable health logging
    logging.getLogger("aiohttp.access").setLevel(level=logging.WARNING)


@kopf.on.cleanup()
def shutdown(logger: logging.Logger | logging.LoggerAdapter, **_):
    logger.info("Shutting down...")
