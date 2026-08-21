import dataclasses
import logging
import os
import ssl

import kopf

from app.utils import to_bool

logger = logging.getLogger(__name__)

K8S_API_SERVER_STRICT_X509_VERIFICATION_ENV = (
    "TWINGATE_K8S_API_SERVER_STRICT_X509_VERIFICATION_DISABLED"
)


def is_strict_x509_verification_disabled() -> bool:
    value = os.environ.get(K8S_API_SERVER_STRICT_X509_VERIFICATION_ENV, False)
    try:
        return to_bool(value)
    except ValueError:
        logger.warning(
            "Invalid %s value %r; keeping strict X.509 verification enabled.",
            K8S_API_SERVER_STRICT_X509_VERIFICATION_ENV,
            value,
        )
        return False


@dataclasses.dataclass(frozen=True, kw_only=True)
class NonStrictX509ConnectionInfo(kopf.ConnectionInfo):
    """A ``kopf.ConnectionInfo`` whose SSL context skips RFC 5280 strict checks."""

    def as_ssl_context(self) -> ssl.SSLContext:
        context = super().as_ssl_context()
        context.verify_flags &= ~ssl.VERIFY_X509_STRICT
        return context


def login_without_strict_x509(
    *, logger: logging.Logger | logging.LoggerAdapter, **kwargs
) -> kopf.ConnectionInfo | None:
    """Authenticate like kopf's default login, minus ``VERIFY_X509_STRICT``.

    ``kopf.login_via_client`` is the only login handler kopf registers by
    default here (the official ``kubernetes`` client is installed), so
    wrapping it keeps the authentication behavior identical.
    """
    info = kopf.login_via_client(logger=logger, **kwargs)
    if info is None:
        return None

    logger.warning(
        "%s=false: strict X.509 verification (RFC 5280) is disabled for the "
        "Kubernetes API connection.",
        K8S_API_SERVER_STRICT_X509_VERIFICATION_ENV,
    )
    return NonStrictX509ConnectionInfo(
        **{f.name: getattr(info, f.name) for f in dataclasses.fields(info)}
    )
