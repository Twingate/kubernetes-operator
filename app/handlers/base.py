from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class _HandlerResult(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    ts: datetime = Field(default_factory=datetime.now)
    success: bool


class _HandlerSuccess(_HandlerResult):
    def __init__(self, **data: Any) -> None:
        super().__init__(success=True, **data)


class _HandlerFailure(_HandlerResult):
    def __init__(self, **data: Any) -> None:
        super().__init__(success=False, **data)


def fail(**data: Any) -> dict:
    return _HandlerFailure(**data).model_dump(mode="json")


def success(**data: Any) -> dict:
    return _HandlerSuccess(**data).model_dump(mode="json")
