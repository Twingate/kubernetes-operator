import logging
from typing import Any

import requests
from gql import Client
from gql.transport.exceptions import TransportAlreadyConnected
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode
from requests.adapters import HTTPAdapter, Retry

from app.api.client_connectors import TwingateConnectorAPI
from app.api.client_groups import TwingateGroupAPIs
from app.api.client_remote_networks import TwingateRemoteNetworksAPIs
from app.api.client_resources import TwingateResourceAPIs
from app.api.client_resources_access import TwingateResourceAccessAPIs
from app.api.client_service_accounts import TwingateServiceAccountAPIs
from app.api.client_users import TwingateUserAPIs
from app.api.exceptions import GraphQLMutationError
from app.settings import TwingateOperatorSettings, get_version

log = logging.getLogger(__name__)


class TwingateRetry(Retry):
    """Custom retry object that retries on 429 errors."""

    # ruff: noqa: FBT002
    # (ignoring this here becuase this is not our function so
    # we can't change the signature)
    def is_retry(self, method, status_code, has_retry_after=False):
        return status_code == 429 or super().is_retry(
            method, status_code, has_retry_after
        )


class TwingateRequestsHTTPTransport(RequestsHTTPTransport):
    def __init__(self, twingate_api_key: str, *args, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(
            {
                "User-Agent": f"Twingate-Operator/{get_version()}",
                "X-API-KEY": twingate_api_key,
            }
        )

        kwargs["headers"] = headers
        kwargs["retries"] = 10
        super().__init__(*args, **kwargs)

    def connect(self):
        if self.session:
            raise TransportAlreadyConnected("Transport is already connected")

        # Creating a session that can later be re-use to configure custom mechanisms
        self.session = requests.Session()

        # If we specified some retries, we provide a predefined retry-logic
        if self.retries > 0:
            adapter = HTTPAdapter(
                max_retries=TwingateRetry(
                    total=self.retries,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504],
                    allowed_methods=None,
                )
            )
            for prefix in "http://", "https://":
                self.session.mount(prefix, adapter)


class TwingateAPIClient(
    TwingateConnectorAPI,
    TwingateGroupAPIs,
    TwingateResourceAPIs,
    TwingateResourceAccessAPIs,
    TwingateServiceAccountAPIs,
    TwingateRemoteNetworksAPIs,
    TwingateUserAPIs,
):
    def __init__(
        self,
        settings: TwingateOperatorSettings,
        *,
        fetch_schema_from_transport: bool = False,
    ):
        self.settings = settings
        self.client = self._get_client(
            fetch_schema_from_transport=fetch_schema_from_transport
        )

    def _get_client(self, *, fetch_schema_from_transport: bool = False) -> Client:
        network = self.settings.network
        host = self.settings.host
        transport = TwingateRequestsHTTPTransport(
            self.settings.api_key, url=f"https://{network}.{host}/api/graphql/"
        )
        return Client(
            transport=transport, fetch_schema_from_transport=fetch_schema_from_transport
        )

    def execute_gql(
        self, document: DocumentNode, variable_values: dict[str, Any] | None = None
    ):
        logging.info("Calling %s with %s", document, variable_values)
        result = self.client.execute(document, variable_values=variable_values)
        logging.info("Result: %s", result)
        return result

    def execute_mutation(
        self,
        name: str,
        document: DocumentNode,
        variable_values: dict[str, Any] | None = None,
    ):
        result = self.execute_gql(document, variable_values=variable_values)
        data = result[name]
        if not data["ok"]:
            raise GraphQLMutationError(name, data.get("error"))

        return data
