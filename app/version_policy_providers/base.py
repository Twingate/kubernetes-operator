import abc

from semantic_version import Version


class VersionPolicyProvider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repository: str | None = None):
        ...

    @abc.abstractmethod
    def get_latest(
        self, specifier: str, *, allow_prerelease: bool = False
    ) -> Version | None:
        ...
