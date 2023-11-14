from collections.abc import Iterator

import requests
from semantic_version import NpmSpec, Version

from app.version_policy_providers.base import VersionPolicyProvider


class DockerhubVersionPolicyProvider(VersionPolicyProvider):
    _DOCKER_HUB_API_BASE_URL = "https://hub.docker.com/v2"

    def __init__(self, repository: str | None):
        self.repository = repository or "twingate/connector"
        self.tags_api_url = (
            f"{self._DOCKER_HUB_API_BASE_URL}/repositories/{self.repository}/tags"
        )

    def __call(self):
        url = f"{self.tags_api_url}?page_size=100"
        response = requests.get(url, timeout=6)
        return response.json()

    def get_all_tags(self) -> Iterator[str]:
        data = self.__call()
        for result in data["results"]:
            yield result["name"]

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
