import logging
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    LoggerAdapter = logging.LoggerAdapter[Any]
else:
    LoggerAdapter = logging.LoggerAdapter

Logger = Union[logging.Logger, LoggerAdapter]
