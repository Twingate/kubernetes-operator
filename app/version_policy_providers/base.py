from abc import abstractmethod

from semantic_version import Version


class VersionPolicyProvider:
    @abstractmethod
    def get_latest(
        self, specifier: str, *, allow_prerelease: bool = False
    ) -> Version | None:
        ...
