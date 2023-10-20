import kopf
from pydantic import ValidationError

from app.api import TwingateAPIClient
from app.handlers import *  # noqa: F403
from app.settings import TwingateOperatorSettings


@kopf.on.startup()
def startup(logger, memo, **kwargs):
    logger.info("Operator is starting up...")
    try:
        memo.twingate_settings = TwingateOperatorSettings()
        memo.twingate_client = TwingateAPIClient(memo.twingate_settings)
    except ValidationError:
        logger.exception("Failed to load settings.")


@kopf.on.cleanup()
def shutdown(logger, **_):
    logger.info("Shutting down...")
