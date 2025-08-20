from typing import Protocol

from gql import GraphQLRequest

from app import typedefs
from app.settings import TwingateOperatorSettings


class TwingateClientProtocol(Protocol):
    @property
    def logger(self) -> typedefs.Logger:
        """Returns a logger instance."""
        ...

    def execute_gql(self, query: GraphQLRequest):  # pragma: no cover
        ...

    def execute_mutation(self, name: str, mutation: GraphQLRequest):  # pragma: no cover
        ...

    @property
    def settings(self) -> TwingateOperatorSettings:  # pragma: no cover
        ...
