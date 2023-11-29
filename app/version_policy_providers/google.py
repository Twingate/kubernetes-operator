import re
from collections.abc import Iterator

from google.cloud import artifactregistry_v1

from app.version_policy_providers import VersionPolicyProvider

# IMAGE = "us-docker.pkg.dev/twingate-dev/connector/connector"

DOCKER_REPO_REGEX = r"^(?P<location>.*)-docker.pkg.dev\/(?P<project>[^\/]+)\/(?P<repo>[^\/]+)\/(?P<image>[^\/]+)"


class GoogleVersionPolicyProvider(VersionPolicyProvider):
    DOCKER_REPO_REGEX = (
        r"^(?P<location>.*)-docker.pkg.dev\/(?P<project>[^\/]+)\/(?P<repo>[^\/]+)"
    )

    def __init__(self, repository: str | None = None):
        if not repository:
            raise ValueError("Must specify 'repository'")

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

        for page in response.pages:
            for tag in page.tags:
                # Tag name is something like '<self.parent_name>/tags/0'
                tag_values = list(filter(None, tag.name.split("/")))
                yield tag_values[-1]
