import logging
import ssl

import pytest
import urllib3.connection
import urllib3.util
import urllib3.util.ssl_
from kopf import ConnectionInfo

from app.ssl_compat import (
    STRICT_ENV_VAR,
    apply_x509_strict_workaround,
    is_strict_x509_verification_enabled,
    relax_x509_strict,
)

URLLIB3_MODULES = (urllib3.util.ssl_, urllib3.util, urllib3.connection)


@pytest.fixture
def unpatched(monkeypatch):
    """Restore the stock kopf/urllib3 bindings after each test."""
    monkeypatch.delenv(STRICT_ENV_VAR, raising=False)
    monkeypatch.setattr(
        ConnectionInfo, "as_ssl_context", ConnectionInfo.as_ssl_context, raising=True
    )
    for module in URLLIB3_MODULES:
        monkeypatch.setattr(
            module,
            "create_urllib3_context",
            module.create_urllib3_context,
            raising=True,
        )


class TestRelaxX509Strict:
    def test_clears_strict_flag(self):
        """Fails if VERIFY_X509_STRICT survives."""
        context = ssl.create_default_context()
        assert context.verify_flags & ssl.VERIFY_X509_STRICT

        relax_x509_strict(context)

        assert not context.verify_flags & ssl.VERIFY_X509_STRICT

    def test_keeps_the_rest_of_verification(self):
        """Fails if anything other than the strict flag is weakened."""
        context = ssl.create_default_context()
        flags_before = context.verify_flags

        relax_x509_strict(context)

        assert context.verify_mode == ssl.CERT_REQUIRED
        assert context.check_hostname is True
        # Only the strict bit was touched; partial-chain etc. are untouched.
        assert context.verify_flags == flags_before & ~ssl.VERIFY_X509_STRICT


class TestIsStrictX509VerificationEnabled:
    def test_unset(self, monkeypatch):
        """Fails if the workaround is not the default."""
        monkeypatch.delenv(STRICT_ENV_VAR, raising=False)
        assert not is_strict_x509_verification_enabled()

    @pytest.mark.parametrize("value", ["true", "True", "1", "yes", "on", " true "])
    def test_truthy(self, monkeypatch, value):
        """Fails if truthy opt-ins are not honored."""
        monkeypatch.setenv(STRICT_ENV_VAR, value)
        assert is_strict_x509_verification_enabled()

    @pytest.mark.parametrize("value", ["false", "0", "no", "off", ""])
    def test_falsy(self, monkeypatch, value):
        """Fails if falsy values enable strict verification."""
        monkeypatch.setenv(STRICT_ENV_VAR, value)
        assert not is_strict_x509_verification_enabled()

    def test_unparseable_does_not_raise(self, monkeypatch):
        """Fails if a typo'd value crashes startup instead of falling back."""
        monkeypatch.setenv(STRICT_ENV_VAR, "maybe")
        assert not is_strict_x509_verification_enabled()


class TestApplyX509StrictWorkaround:
    def test_opted_out(self, unpatched, monkeypatch):
        """Fails if the opt-out still patches anything."""
        monkeypatch.setenv(STRICT_ENV_VAR, "true")
        originals = {m: m.create_urllib3_context for m in URLLIB3_MODULES}
        original_kopf = ConnectionInfo.as_ssl_context

        assert apply_x509_strict_workaround(logging.getLogger(__name__)) is False

        assert ConnectionInfo.as_ssl_context is original_kopf
        for module, original in originals.items():
            assert module.create_urllib3_context is original

    def test_patches_kopf(self, unpatched):
        """Fails if kopf's API-server context keeps the strict flag."""
        assert apply_x509_strict_workaround() is True

        context = ConnectionInfo(
            server="https://kubernetes.default.svc"
        ).as_ssl_context()

        assert not context.verify_flags & ssl.VERIFY_X509_STRICT
        assert context.verify_mode == ssl.CERT_REQUIRED
        assert context.check_hostname is True

    def test_patches_every_urllib3_binding(self, unpatched):
        """Fails if a module-level re-export still points at the stock function.

        ``urllib3.connection`` binds ``create_urllib3_context`` by name at import
        time, so patching only ``urllib3.util.ssl_`` would leave the
        ``kubernetes`` client on the strict default.
        """
        apply_x509_strict_workaround()

        for module in URLLIB3_MODULES:
            context = module.create_urllib3_context()
            assert not context.verify_flags & ssl.VERIFY_X509_STRICT, module.__name__

    def test_explicit_verify_flags_are_respected(self, unpatched):
        """Fails if an explicit caller request is silently overridden."""
        apply_x509_strict_workaround()

        context = urllib3.connection.create_urllib3_context(
            verify_flags=ssl.VERIFY_X509_STRICT
        )

        assert context.verify_flags & ssl.VERIFY_X509_STRICT

    def test_is_idempotent(self, unpatched):
        """Fails if repeated calls double-wrap the patched functions."""
        assert apply_x509_strict_workaround() is True
        patched_kopf = ConnectionInfo.as_ssl_context
        patched_urllib3 = urllib3.connection.create_urllib3_context

        assert apply_x509_strict_workaround() is False

        assert ConnectionInfo.as_ssl_context is patched_kopf
        assert urllib3.connection.create_urllib3_context is patched_urllib3
