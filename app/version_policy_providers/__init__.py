from app.version_policy_providers.base import VersionPolicyProvider
from app.version_policy_providers.dockerhub import DockerhubVersionPolicyProvider
from app.version_policy_providers.google import GoogleVersionPolicyProvider


def get_provider(
    provider_name: str, repository: str | None = None
) -> VersionPolicyProvider:
    if provider_name == "dockerhub":
        return DockerhubVersionPolicyProvider(repository)

    if provider_name == "google":
        return GoogleVersionPolicyProvider(repository)

    raise ValueError(f"Invalid provider_name: {provider_name}")
