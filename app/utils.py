from typing import Any

from cryptography import x509


def to_bool(val: Any) -> bool:
    """Convert "boolean" strings (e.g., from env. vars.) to real booleans.

    Values mapping to :code:`True`:

    - :code:`True`
    - :code:`"true"` / :code:`"t"`
    - :code:`"yes"` / :code:`"y"`
    - :code:`"on"`
    - :code:`"1"`
    - :code:`1`

    Values mapping to :code:`False`:

    - :code:`False`
    - :code:`"false"` / :code:`"f"`
    - :code:`"no"` / :code:`"n"`
    - :code:`"off"`
    - :code:`"0"`
    - :code:`0`

    :raises ValueError: for any other value.
    """
    if isinstance(val, str):
        val = val.lower()
    truthy = {True, "true", "t", "yes", "y", "on", "1"}
    falsy = {False, "false", "f", "no", "n", "off", "0"}
    try:
        if val in truthy:
            return True
        if val in falsy:
            return False
    except TypeError:
        # Raised when "val" is not hashable (e.g., lists)
        pass
    raise ValueError(f"Cannot convert value to bool: {val}")


def validate_pem_x509_certificate(value: str):
    try:
        x509.load_pem_x509_certificate(value.encode())
    except ValueError as ex:
        raise ValueError("Invalid certificate") from ex
