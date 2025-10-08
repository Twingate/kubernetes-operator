import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    LoggerAdapter = logging.LoggerAdapter[Any]
else:
    LoggerAdapter = logging.LoggerAdapter

Logger = logging.Logger | LoggerAdapter
