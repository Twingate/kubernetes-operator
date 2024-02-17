import binascii
import logging
import os
import tomllib
from base64 import b64decode
from typing import Annotated, ClassVar

from pydantic.functional_validators import AfterValidator
from pydantic_core._pydantic_core import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


def validate_graphql_global_id(value: str) -> str:
    value_decoded: str = ""
    try:
        value_bytes: bytes = value.encode("ascii")
        value_decoded = b64decode(value_bytes).decode("ascii")
    except (binascii.Error, UnicodeDecodeError, UnicodeEncodeError):
        pass

    if ":" not in value_decoded:
        raise ValueError("Invalid global id")

    return value


GlobalID = Annotated[str, AfterValidator(validate_graphql_global_id)]


class TwingateOperatorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TWINGATE_")
    NULL_RN_ID: ClassVar[str] = "ZmFrZTp2YWx1ZQo="  # temp value ("fake:value" encoded)

    api_key: str
    network: str
    remote_network_id: GlobalID = NULL_RN_ID
    remote_network_name: str | None = None
    host: str = "twingate.com"

    @property
    def full_url(self) -> str:
        return f"https://{self.network}.{self.host}"

    def __init__(self, *args, **kwargs):
        from app.api import TwingateAPIClient

        super().__init__(*args, **kwargs)

        if self.remote_network_name:
            client = TwingateAPIClient(self)
            rn = client.get_remote_network_by_name(self.remote_network_name)
            if not rn:
                raise ValueError(f"Remote network {self.remote_network_name} not found")
            self.remote_network_id = rn.id

        if self.remote_network_id == self.NULL_RN_ID:
            raise ValidationError("Remote network id is required")


__settings: TwingateOperatorSettings | None = None
__version: str | None = None


def get_settings() -> TwingateOperatorSettings:  # pragma: no cover
    global __settings
    if not __settings:
        __settings = TwingateOperatorSettings()
    return __settings


def get_version() -> str:  # pragma: no cover
    # ruff: noqa: E722
    global __version
    if not __version:
        try:
            filename = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
            with open(filename, "rb") as f:
                data = tomllib.load(f)
                __version = (
                    data.get("tool", {}).get("poetry", {}).get("version", "0.0.0")
                )
        except:
            logging.exception("Failed to load version from pyproject.toml")
            __version = "0.0.0"

    return __version or "0.0.0"
