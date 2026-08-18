"""Compatibility shim for Python 3.13+ strict X.509 verification.

Python 3.13 added :data:`ssl.VERIFY_X509_STRICT` to the default verification
flags of :func:`ssl.create_default_context`, and urllib3 2.x mirrors that
default in ``create_urllib3_context``. The flag enforces RFC 5280 structural
requirements, one of which is an Authority Key Identifier extension on the CA
certificates in the chain.

Amazon EKS cluster CAs are issued without an AKID, so every TLS connection to
the API server fails with
``SSLCertVerificationError: Missing Authority Key Identifier`` and the operator
crashloops before it can reconcile anything. Both API server clients the
operator uses are affected: kopf (aiohttp, via
:meth:`kopf.ConnectionInfo.as_ssl_context`) and the ``kubernetes`` client
(urllib3, used by :mod:`app.utils_k8s`).

Clearing the flag restores the behavior of Python <= 3.12, which every operator
release up to 1.1.2 shipped with. Chain validation, expiry checks,
``CERT_REQUIRED`` and hostname verification all stay in force - only the RFC
5280 structural strictness is dropped.

Set ``TWINGATE_STRICT_X509_VERIFICATION=true`` to keep the Python 3.13+ default
on clusters whose CA is RFC 5280 compliant.

See https://github.com/Twingate/kubernetes-operator/issues/1128
"""

import functools
import logging
import os
import ssl
from typing import Any

from app.utils import to_bool

STRICT_ENV_VAR = "TWINGATE_STRICT_X509_VERIFICATION"

_PATCHED_MARKER = "__twingate_x509_strict_relaxed__"


def is_strict_x509_verification_enabled() -> bool:
    """Whether the user opted back into the Python 3.13+ strict defaults."""
    value = os.environ.get(STRICT_ENV_VAR, "").strip()
    if not value:
        return False

    try:
        return to_bool(value)
    except ValueError:
        logging.getLogger(__name__).warning(
            "Ignoring unparseable %s=%r; assuming false.", STRICT_ENV_VAR, value
        )
        return False


def relax_x509_strict(context: ssl.SSLContext) -> ssl.SSLContext:
    """Clear ``VERIFY_X509_STRICT`` on ``context``, leaving all else intact."""
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context


def _patch_kopf() -> bool:
    """Relax the SSL context kopf builds for the Kubernetes API server."""
    from kopf import ConnectionInfo

    original = ConnectionInfo.as_ssl_context
    if getattr(original, _PATCHED_MARKER, False):
        return False

    @functools.wraps(original)
    def as_ssl_context(self: ConnectionInfo) -> ssl.SSLContext:
        return relax_x509_strict(original(self))

    setattr(as_ssl_context, _PATCHED_MARKER, True)
    ConnectionInfo.as_ssl_context = as_ssl_context  # type: ignore[method-assign]
    return True


def _patch_urllib3() -> bool:
    """Relax the SSL contexts urllib3 builds, used by the ``kubernetes`` client.

    ``create_urllib3_context`` is re-exported and bound by name in several
    urllib3 modules, so every binding still pointing at the original has to be
    replaced. Contexts the caller passed explicit ``verify_flags`` for are left
    alone - that is a deliberate choice, not the implicit 3.13+ default.
    """
    import urllib3.connection
    import urllib3.util
    import urllib3.util.ssl_

    original = urllib3.util.ssl_.create_urllib3_context
    if getattr(original, _PATCHED_MARKER, False):
        return False

    @functools.wraps(original)
    def create_urllib3_context(*args: Any, **kwargs: Any) -> ssl.SSLContext:
        context = original(*args, **kwargs)
        if kwargs.get("verify_flags") is None:
            relax_x509_strict(context)
        return context

    setattr(create_urllib3_context, _PATCHED_MARKER, True)
    for module in (urllib3.util.ssl_, urllib3.util, urllib3.connection):
        if getattr(module, "create_urllib3_context", None) is original:
            module.create_urllib3_context = create_urllib3_context  # type: ignore[attr-defined]

    return True


def apply_x509_strict_workaround(
    logger: logging.Logger | logging.LoggerAdapter | None = None,
) -> bool:
    """Clear ``VERIFY_X509_STRICT`` from the SSL contexts the operator builds.

    Returns ``True`` when the workaround was applied, ``False`` when it was
    skipped - either opted out via :data:`STRICT_ENV_VAR` or already in place.
    """
    logger = logger or logging.getLogger(__name__)

    if is_strict_x509_verification_enabled():
        logger.info(
            "%s is set - keeping strict RFC 5280 certificate verification. "
            "Note that Amazon EKS cluster CAs carry no Authority Key Identifier "
            "and will be rejected.",
            STRICT_ENV_VAR,
        )
        return False

    patched = _patch_kopf()
    patched = _patch_urllib3() or patched

    if patched:
        logger.debug(
            "Relaxed ssl.VERIFY_X509_STRICT for Kubernetes API connections; "
            "certificate chain, expiry and hostname verification are unchanged. "
            "Set %s=true to disable.",
            STRICT_ENV_VAR,
        )

    return patched
