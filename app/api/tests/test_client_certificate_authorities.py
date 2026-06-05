import json

import pytest
import responses

from app.api.exceptions import GraphQLMutationError

PEM_CERT = "-----BEGIN CERTIFICATE-----\nMIIB...\n-----END CERTIFICATE-----"


class TestTwingateCertificateAuthorityAPIs:
    def test_get_certificate_authority_success(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps(
            {
                "data": {
                    "certificateAuthority": {
                        "__typename": "X509CertificateAuthority",
                        "id": "ca-id",
                        "name": "My CA",
                        "fingerprint": "ab:cd",
                    }
                }
            }
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "ca-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_certificate_authority("ca-id")
        assert result is not None
        assert result.id == "ca-id"
        assert result.name == "My CA"

    def test_get_certificate_authority_not_found_returns_none(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps({"data": {"certificateAuthority": None}})
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "ca-id"}}, strict_match=False
                )
            ],
        )
        assert api_client.get_certificate_authority("ca-id") is None

    def test_x509_certificate_authority_create(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps(
            {
                "data": {
                    "x509CertificateAuthorityCreate": {
                        "ok": True,
                        "entity": {
                            "id": "ca-id",
                            "name": "My CA",
                            "fingerprint": "ab:cd",
                        },
                    }
                }
            }
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"name": "My CA", "certificate": PEM_CERT}},
                    strict_match=False,
                )
            ],
        )
        result = api_client.x509_certificate_authority_create(
            name="My CA", certificate=PEM_CERT
        )
        assert result.id == "ca-id"

    def test_x509_certificate_authority_create_failure(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "x509CertificateAuthorityCreate": {
                        "ok": False,
                        "error": "some error",
                    }
                }
            }
        )
        mocked_responses.post(test_url, status=200, body=failed_response)
        with pytest.raises(
            GraphQLMutationError,
            match=r"x509CertificateAuthorityCreate mutation failed.",
        ):
            api_client.x509_certificate_authority_create(
                name="My CA", certificate=PEM_CERT
            )

    def test_x509_certificate_authority_delete(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps(
            {"data": {"x509CertificateAuthorityDelete": {"ok": True}}}
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "ca-id"}}, strict_match=False
                )
            ],
        )
        assert api_client.x509_certificate_authority_delete("ca-id") is True

    def test_x509_certificate_authority_delete_raises_on_error(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "x509CertificateAuthorityDelete": {
                        "ok": False,
                        "error": "This CA is currently in use and cannot be deleted.",
                    }
                }
            }
        )
        mocked_responses.post(test_url, status=200, body=failed_response)
        with pytest.raises(
            GraphQLMutationError,
            match=r"x509CertificateAuthorityDelete mutation failed.",
        ):
            api_client.x509_certificate_authority_delete("ca-id")
