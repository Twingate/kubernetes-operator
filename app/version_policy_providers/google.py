import re
from collections.abc import Iterator

from google.cloud import artifactregistry_v1
from semantic_version import Version

from app.version_policy_providers import VersionPolicyProvider

# IMAGE = "us-docker.pkg.dev/twingate-dev/connector/connector"

DOCKER_REPO_REGEX = r"^(?P<location>.*)-docker.pkg.dev\/(?P<project>[^\/]+)\/(?P<repo>[^\/]+)\/(?P<image>[^\/]+)"


class DockerhubVersionPolicyProvider(VersionPolicyProvider):
    DOCKER_REPO_REGEX = (
        r"^(?P<location>.*)-docker.pkg.dev\/(?P<project>[^\/]+)\/(?P<repo>[^\/]+)"
    )

    def __init__(self, repository: str):
        matches = re.match(DOCKER_REPO_REGEX, repository)
        if not matches:
            raise ValueError(f"Invalid image name: {repository}")

        self.location = matches.group("location")
        self.project_id = matches.group("project")
        self.repo = matches.group("repo")
        self.image = matches.group("image")
        self.parent_name = f"projects/{self.project_id}/locations/{self.location}/repositories/{self.repo}/packages/{self.image}"

    def get_all_tags(self) -> Iterator[str]:
        client = artifactregistry_v1.ArtifactRegistryClient()
        request = artifactregistry_v1.ListTagsRequest(parent=self.parent_name)
        response = client.list_tags(request)

        tags = []
        for page in response.pages:
            for tag in page.tags:
                # Tag name is something like 'projects/twingate-dev/locations/us/repositories/connector/packages/connector/tags/0'
                tag_values = list(filter(None, tag.name.split("/")))
                tags.append(tag_values[-1])

        return tags

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
