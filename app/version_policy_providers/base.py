import abc
from collections.abc import Iterator

from semantic_version import NpmSpec, Version


class VersionPolicyProvider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repository: str | None = None):
        ...

    @abc.abstractmethod
    def get_all_tags(self) -> Iterator[str]:
        ...

    def get_all_semver_tags(
        self, *, allow_prerelease: bool = False
    ) -> Iterator[Version]:
        for tag in self.get_all_tags():
            try:
                v = Version(tag)
                if v.prerelease and not allow_prerelease:
                    continue

                yield v
            except ValueError:
                continue

    def get_all_semver_tags_by_specifier(
        self, specifier: str, *, allow_prerelease: bool = False
    ) -> Iterator[Version]:
        spec = NpmSpec(specifier)
        return spec.filter(self.get_all_semver_tags(allow_prerelease=allow_prerelease))

    def get_latest(
        self, specifier: str, *, allow_prerelease: bool = False
    ) -> Version | None:
        try:
            return max(
                self.get_all_semver_tags_by_specifier(
                    specifier, allow_prerelease=allow_prerelease
                )
            )
        except ValueError:
            # if `max` is called on an empty sequence
            return None
