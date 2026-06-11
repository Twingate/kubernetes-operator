from gql import GraphQLRequest
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol


class CertificateAuthority(BaseModel):
    id: str
    name: str
    fingerprint: str | None = None


_X509_CA_FRAGMENT = """
    fragment X509CertificateAuthorityFields on X509CertificateAuthority {
        id
        name
        fingerprint
    }
"""

# The public API exposes `certificateAuthority` as a Union of X509 and SSH CAs.
# This operator only manages X509 CAs (SSH support is a future addition), so the
# query narrows to the X509 type with an inline fragment.
QUERY_GET_CERTIFICATE_AUTHORITY = (
    _X509_CA_FRAGMENT
    + """
    query GetCertificateAuthority($id: ID!) {
      certificateAuthority(id: $id) {
        __typename
        ... on X509CertificateAuthority {
          ...X509CertificateAuthorityFields
        }
      }
    }
"""
)

MUT_CREATE_X509_CERTIFICATE_AUTHORITY = (
    _X509_CA_FRAGMENT
    + """
    mutation CreateX509CertificateAuthority($name: String!, $certificate: String!) {
      x509CertificateAuthorityCreate(name: $name, certificate: $certificate) {
        ok
        error
        entity {
          ...X509CertificateAuthorityFields
        }
      }
    }
"""
)

MUT_DELETE_X509_CERTIFICATE_AUTHORITY = """
    mutation DeleteX509CertificateAuthority($id: ID!) {
      x509CertificateAuthorityDelete(id: $id) {
        ok
        error
      }
    }
"""


class TwingateCertificateAuthorityAPIs:
    def get_certificate_authority(
        self: TwingateClientProtocol, ca_id: str
    ) -> CertificateAuthority | None:
        try:
            result = self.execute_gql(
                GraphQLRequest(
                    QUERY_GET_CERTIFICATE_AUTHORITY, variable_values={"id": ca_id}
                )
            )
            ca = result["certificateAuthority"]
            return CertificateAuthority(**ca) if ca else None
        except TransportQueryError:
            self.logger.exception("Failed to get certificate authority")
            return None

    def x509_certificate_authority_create(
        self: TwingateClientProtocol, *, name: str, certificate: str
    ) -> CertificateAuthority:
        result = self.execute_mutation(
            "x509CertificateAuthorityCreate",
            GraphQLRequest(
                MUT_CREATE_X509_CERTIFICATE_AUTHORITY,
                variable_values={"name": name, "certificate": certificate},
            ),
        )
        return CertificateAuthority(**result["entity"])

    def x509_certificate_authority_delete(
        self: TwingateClientProtocol, ca_id: str
    ) -> bool:
        try:
            result = self.execute_mutation(
                "x509CertificateAuthorityDelete",
                GraphQLRequest(
                    MUT_DELETE_X509_CERTIFICATE_AUTHORITY,
                    variable_values={"id": ca_id},
                ),
            )
            return bool(result["ok"])
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
