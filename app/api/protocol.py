from typing import Any, Protocol

from graphql import DocumentNode

from app.settings import TwingateOperatorSettings


class TwingateClientProtocol(Protocol):
    def execute_gql(
        self, document: DocumentNode, variable_values: dict[str, Any] | None = None
    ):  # pragma: no cover
        ...

    def execute_mutation(
        self,
        name: str,
        document: DocumentNode,
        variable_values: dict[str, Any] | None = None,
    ):  # pragma: no cover
        ...

    @property
    def settings(self) -> TwingateOperatorSettings:  # pragma: no cover
        ...
