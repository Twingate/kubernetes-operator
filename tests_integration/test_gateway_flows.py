from app.api import TwingateAPIClient
from app.settings import TwingateOperatorSettings
from tests_integration.utils import (
    assert_log_message_contains,
    create_tls_secret,
    generate_base64_ca_cert,
    kubectl,
    kubectl_apply,
    kubectl_create,
    kubectl_delete_wait,
    kubectl_wait_object,
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
            kubectl_create(create_tls_secret(secret_name, generate_base64_ca_cert()))
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

            # 4. Rotate the Secret's ca.crt. The secret event handler
            #    (twingate_ca_tls_secret_update) re-reconciles the CA, re-creating
            #    it with a new backend ID; the CA ID-change handler
            #    (twingate_ca_id_changed) then propagates that ID onto the Gateway.
            original_ca_id = ca["spec"]["id"]
            assert gw["status"]["x509CaId"] == original_ca_id
            kubectl_apply(
                create_tls_secret(secret_name, generate_base64_ca_cert("Rotated CA"))
            )

            ca = kubectl_wait_object(
                "tgca",
                ca_name,
                lambda o: o["spec"]["id"] != original_ca_id,
                description="a new spec.id after ca.crt rotation",
            )
            new_ca_id = ca["spec"]["id"]

            gw = kubectl_wait_object(
                "twingategateway",
                gw_name,
                lambda o: o.get("status", {}).get("x509CaId") == new_ca_id,
                description=f"x509CaId propagated to new CA ID {new_ca_id}",
            )
            assert gw["status"]["x509CaId"] == new_ca_id

            # The Gateway reconcile onto the new CA best-effort deletes the
            # rotated-away CA (it's now unreferenced), so the original backend CA
            # should be gone - no manual cleanup needed.
            client = TwingateAPIClient(TwingateOperatorSettings())
            assert client.get_certificate_authority(original_ca_id) is None, (
                f"Rotated-away CA {original_ca_id} was not reaped by the operator"
            )

            # 5. Tear down out of dependency order to exercise the in-use retry
            #    path: request the Gateway and CA deletes while they are still
            #    referenced, so each handler retries (rather than leaking the
            #    backend entity) until its dependent is gone.
            kubectl(f"delete twingategateway/{gw_name} tgca/{ca_name} --wait=false")

            # Removing the Resource frees the Gateway, whose removal frees the CA.
            kubectl_delete_wait("tgr", resource_name)
            kubectl_delete_wait("twingategateway", gw_name, perform_deletion=False)
            kubectl_delete_wait("tgca", ca_name, perform_deletion=False)
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
    # The cert-rotation propagation chain: secret change -> CA re-reconcile -> Gateway.
    assert_log_message_contains(logs, "changed, reconciling certificate authority")
    assert_log_message_contains(logs, "id changed, reconciling gateway")
    # Out-of-order teardown retried each delete until its dependent was gone.
    assert_log_message_contains(logs, "Gateway still in use by a Resource, retrying.")
    assert_log_message_contains(
        logs, "Certificate authority still in use by a Gateway, retrying."
    )
    assert_log_message_contains(logs, "Handler 'twingate_gateway_delete' succeeded.")
