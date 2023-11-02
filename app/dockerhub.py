from collections.abc import Iterator
from functools import lru_cache
from typing import Any

import pendulum
import requests
from semantic_version import NpmSpec, Version

_DOCKER_HUB_API_BASE_URL = "https://hub.docker.com/v2"
_DOCKER_HUB_TAGS_API_URL = (
    f"{_DOCKER_HUB_API_BASE_URL}/repositories/twingate/connector/tags"
)


@lru_cache(maxsize=2)
def _cached_dockerhub_call(ttl_hash: int) -> dict[str, Any]:
    url = f"{_DOCKER_HUB_TAGS_API_URL}?page_size=100"
    response = requests.get(url, timeout=6)
    return response.json()


def get_all_operator_tags(ttl_hash=None) -> Iterator[str]:
    ttl_hash = pendulum.now().start_of("hour").int_timestamp
    data = _cached_dockerhub_call(ttl_hash=ttl_hash)
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
    spec = NpmSpec(specifier)
    return spec.filter(get_all_operator_semver_tags(allow_prerelease=allow_prerelease))


def get_latest(specifier: str, *, allow_prerelease: bool = False) -> Version | None:
    if matched_versions := list(
        get_all_operator_semver_tags_by_specifier(
            specifier, allow_prerelease=allow_prerelease
        )
    ):
        return max(matched_versions)

    return None
