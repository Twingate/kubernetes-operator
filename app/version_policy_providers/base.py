from abc import abstractmethod

from semantic_version import Version


class VersionPolicyProvider:
    @abstractmethod
    def __init__(self, repository: str | None = None):
        ...

    @abstractmethod
    def get_latest(
        self, specifier: str, *, allow_prerelease: bool = False
    ) -> Version | None:
        ...
