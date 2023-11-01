from collections.abc import Iterator

import requests
from semantic_version import NpmSpec, Version

_DOCKER_HUB_API_BASE_URL = "https://hub.docker.com/v2"
_DOCKER_HUB_TAGS_API_URL = (
    f"{_DOCKER_HUB_API_BASE_URL}/repositories/twingate/kubernetes-operator/tags"
)


def get_all_operator_tags() -> Iterator[str]:
    url = f"{_DOCKER_HUB_TAGS_API_URL}?page_size=100"
    response = requests.get(url, timeout=3)
    data = response.json()
    for result in data["results"]:
        yield result["name"]


def get_all_operator_semver_tags(
    *, allow_prerelease: bool = False
) -> Iterator[Version]:
    for tag in get_all_operator_tags():
        try:
            v = Version(tag)
            if v.prerelease and not allow_prerelease:
                continue

            yield v
        except ValueError:
            continue


def get_all_operator_semver_tags_by_specifier(
    specifier: str, *, allow_prerelease: bool = False
) -> Iterator[Version]:
    specifier = NpmSpec(specifier)
    return specifier.filter(
        get_all_operator_semver_tags(allow_prerelease=allow_prerelease)
    )


def get_latest(specifier: str, *, allow_prerelease: bool = False) -> Version | None:
    matched_versions = list(
        get_all_operator_semver_tags_by_specifier(
            specifier, allow_prerelease=allow_prerelease
        )
    )
    return max(matched_versions)
