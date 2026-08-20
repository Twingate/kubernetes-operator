import dataclasses
import datetime
import ssl
from unittest.mock import MagicMock, patch

import kopf
import pytest

from app.auth import (
    STRICT_X509_VERIFICATION_ENV,
    NonStrictX509ConnectionInfo,
    is_strict_x509_verification_disabled,
    login_without_strict_x509,
)


def test_non_strict_connection_info_clears_only_the_strict_flag():
    info = NonStrictX509ConnectionInfo(server="https://localhost")

    context = info.as_ssl_context()

    assert not context.verify_flags & ssl.VERIFY_X509_STRICT
    assert context.verify_flags & ssl.VERIFY_X509_PARTIAL_CHAIN
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, False), ("true", False), ("false", True), ("not-a-bool", False)],
)
def test_is_strict_x509_verification_disabled(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv(STRICT_X509_VERIFICATION_ENV, raising=False)
    else:
        monkeypatch.setenv(STRICT_X509_VERIFICATION_ENV, value)

    assert is_strict_x509_verification_disabled() == expected


def test_login_without_strict_x509_wraps_the_default_login():
    original = kopf.ConnectionInfo(
        server="https://172.20.0.1:443",
        ca_path="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt",
        scheme="Bearer",
        token="token",  # nosec
        default_namespace="default",
        priority=10,
        expiration=datetime.datetime(2036, 1, 1, tzinfo=datetime.UTC),
    )
    logger = MagicMock()
    with patch("kopf.login_via_client", return_value=original) as login_mock:
        info = login_without_strict_x509(logger=logger, retry=0)

    login_mock.assert_called_once_with(logger=logger, retry=0)
    assert isinstance(info, NonStrictX509ConnectionInfo)
    for field in dataclasses.fields(original):
        assert getattr(info, field.name) == getattr(original, field.name)


def test_login_without_strict_x509_passes_through_missing_credentials():
    with patch("kopf.login_via_client", return_value=None):
        assert login_without_strict_x509(logger=MagicMock()) is None
