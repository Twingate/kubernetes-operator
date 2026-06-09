from app.api.tests.factories import BASE64_OF_VALID_CA_CERT
from tests_integration.utils import (
    assert_log_message_contains,
    create_tls_secret,
    kubectl,
    kubectl_create,
    kubectl_delete_wait,
    kubectl_wait_object_handler_success,
    load_stdout,
)


def test_gateway_flows(run_kopf, random_name_generator):
    secret_name = random_name_generator("gw-tls")
    svc_name = random_name_generator("gw-svc")
    ca_name = random_name_generator("gw-ca")
    gw_name = random_name_generator("gw")
    resource_name = random_name_generator("gw-res")
    port = 8443

    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {svc_name}
          namespace: default
        spec:
          type: ClusterIP
          ports:
            - protocol: TCP
              port: {port}
              targetPort: {port}
          selector:
            app.kubernetes.io/name: nonexistent
    """

    CA_OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateCertificateAuthority
        metadata:
          name: {ca_name}
        spec:
          name: My CA
          secretRef:
            name: {secret_name}
    """

    GW_OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGateway
        metadata:
          name: {gw_name}
        spec:
          serviceRef:
            name: {svc_name}
            port: {port}
          x509CertificateAuthorityRef:
            name: {ca_name}
    """

    RESOURCE_OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {resource_name}
        spec:
          name: My K8S Resource
          address: kubernetes.default.svc.cluster.local
          type: Kubernetes
          gatewayRef:
            name: {gw_name}
    """

    with run_kopf() as runner:
        try:
            # The CA handler reads ca.crt from this kubernetes.io/tls Secret.
            kubectl_create(create_tls_secret(secret_name, BASE64_OF_VALID_CA_CERT))
            # The Gateway resolves its address from this Service.
            kubectl_create(SERVICE_OBJ)

            # 1. CA syncs to the backend first - the Gateway depends on its spec.id.
            kubectl_create(CA_OBJ)
            ca = kubectl_wait_object_handler_success(
                "tgca", ca_name, "twingate_certificate_authority_create"
            )
            assert ca["spec"]["id"], f"CA spec.id not set: {ca['spec']}"

            # 2. Gateway create resolves the Service address + the CA id, then calls
            #    the Twingate API.
            kubectl_create(GW_OBJ)
            gw = kubectl_wait_object_handler_success(
                "twingategateway", gw_name, "twingate_gateway_create_update"
            )
            assert gw["spec"]["id"], f"Gateway spec.id not set: {gw['spec']}"
            assert (
                gw["status"]["address"]
                == f"{svc_name}.default.svc.cluster.local:{port}"
            )

            # 3. A Kubernetes resource binds to the Gateway via gatewayRef. The
            #    create handler resolves the Gateway's spec.id and sends it as
            #    gatewayId to the Twingate API.
            kubectl_create(RESOURCE_OBJ)
            resource = kubectl_wait_object_handler_success(
                "tgr", resource_name, "twingate_resource_create"
            )
            assert resource["spec"]["id"], (
                f"Resource spec.id not set: {resource['spec']}"
            )

            # 4. Delete the resource, then the Gateway - deleting the CA while still
            #    referenced raises the "in use" TemporaryError.
            kubectl_delete_wait("tgr", resource_name)
            kubectl_delete_wait("twingategateway", gw_name)
            kubectl_delete_wait("tgca", ca_name)
        finally:
            # run_kopf only cleans up twingate CRs, not these helper objects.
            kubectl(f"delete service {svc_name} --ignore-not-found")
            kubectl(f"delete secret {secret_name} --ignore-not-found")

    # run_kopf asserts runner.exception is None / exit_code == 0 on exit.
    logs = load_stdout(runner.output)
    assert_log_message_contains(
        logs, "Handler 'twingate_certificate_authority_create' succeeded."
    )
    assert_log_message_contains(
        logs, "Handler 'twingate_gateway_create_update' succeeded."
    )
    assert_log_message_contains(logs, "Handler 'twingate_resource_create' succeeded.")
    assert_log_message_contains(logs, "Handler 'twingate_gateway_delete' succeeded.")
