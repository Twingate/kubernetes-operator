import base64
from collections.abc import Callable
from enum import StrEnum
from typing import cast

import kopf
import kubernetes
from kopf import Body, Status

from app.crds import ResourceType
from app.utils import to_bool, validate_pem_x509_certificate


def k8s_get_twingate_resource(
    namespace: str, name: str, kapi: kubernetes.client.CustomObjectsApi | None = None
) -> dict | None:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    try:
        return kapi.get_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", name
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def k8s_get_tls_secret(namespace: str, name: str) -> kubernetes.client.V1Secret | None:
    try:
        return kubernetes.client.CoreV1Api().read_namespaced_secret(
            name=name, namespace=namespace
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None

        raise


def get_ca_cert(tls_secret: kubernetes.client.V1Secret) -> str:
    tls_secret_name = tls_secret.metadata.name
    if tls_secret.type != "kubernetes.io/tls":
        raise kopf.PermanentError(
            f"Kubernetes Secret object: {tls_secret_name} type is invalid."
        )

    if not (ca_cert := tls_secret.data.get("ca.crt")):
        raise kopf.PermanentError(
            f"Kubernetes Secret object: {tls_secret_name} is missing ca.crt."
        )

    try:
        validate_pem_x509_certificate(base64.b64decode(ca_cert).decode())
    except ValueError as ex:
        raise kopf.PermanentError(
            f"Kubernetes Secret object: {tls_secret_name} ca.crt is invalid."
        ) from ex

    return ca_cert


ALLOWED_EXTRA_ANNOTATIONS: list[tuple[str, Callable]] = [
    ("name", str),
    ("alias", str),
    ("isBrowserShortcutEnabled", to_bool),
    ("securityPolicyId", str),
    ("isVisible", to_bool),
    ("syncLabels", to_bool),
    ("type", str),
]
TLS_OBJECT_ANNOTATION = "resource.twingate.com/tlsSecret"


def validate_load_balancer_status(status: Status, service_name: str) -> None:
    if not (ingress := status.get("loadBalancer", {}).get("ingress")):
        raise kopf.TemporaryError(
            f"Kubernetes Service: {service_name} LoadBalancer IP is not ready.",
            delay=30,
        )

    if not ingress[0].get("ip"):
        raise kopf.TemporaryError(
            f"Kubernetes Service: {service_name} LoadBalancer IP is not ready.",
            delay=30,
        )


class ServiceType(StrEnum):
    CLUSTER_IP = "ClusterIP"
    LOAD_BALANCER = "LoadBalancer"


def service_to_twingate_resource(service_body: Body, namespace: str) -> dict:
    meta = service_body.metadata
    spec = service_body.spec
    status = service_body.status
    service_name = cast(str, service_body.meta.name)
    resource_object_name = f"{service_name}-resource"

    result: dict = {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {
            "name": resource_object_name,
            "labels": dict(meta.labels),
        },
        "spec": {
            "name": resource_object_name,
            "address": f"{service_name}.{namespace}.svc.cluster.local",
        },
    }

    for key, convert_f in ALLOWED_EXTRA_ANNOTATIONS:
        # TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
        if value := meta.annotations.get(f"twingate.com/resource-{key}"):
            result["spec"][key] = convert_f(value)
        if value := meta.annotations.get(f"resource.twingate.com/{key}"):
            result["spec"][key] = convert_f(value)

    if result["spec"].get("type") == ResourceType.KUBERNETES:
        if not (tls_secret_name := meta.annotations.get(TLS_OBJECT_ANNOTATION)):
            raise kopf.PermanentError(
                f"{TLS_OBJECT_ANNOTATION} annotation is not provided."
            )

        if not (tls_secret := k8s_get_tls_secret(namespace, tls_secret_name)):
            raise kopf.PermanentError(
                f"Kubernetes Secret object: {tls_secret_name} is missing."
            )

        if spec["type"] == ServiceType.LOAD_BALANCER:
            validate_load_balancer_status(status, service_name)

        result["spec"] |= {
            "address": "kubernetes.default.svc.cluster.local",
            "proxy": {
                "address": (
                    status["loadBalancer"]["ingress"][0]["ip"]
                    if spec["type"] == ServiceType.LOAD_BALANCER
                    else f"{service_name}.{namespace}.svc.cluster.local"
                ),
                "certificateAuthorityCert": get_ca_cert(tls_secret),
            },
        }

    protocols: dict = {
        "allowIcmp": False,
        "tcp": {"policy": "RESTRICTED", "ports": []},
        "udp": {"policy": "RESTRICTED", "ports": []},
    }
    for port_obj in spec.get("ports", []):
        port = port_obj["port"]
        if port_obj["protocol"] == "TCP":
            protocols["tcp"]["ports"].append({"start": port, "end": port})
        elif port_obj["protocol"] == "UDP":
            protocols["udp"]["ports"].append({"start": port, "end": port})

    result["spec"]["protocols"] = protocols

    return result


# TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
@kopf.on.resume("service", annotations={"twingate.com/resource": "true"})
@kopf.on.create("service", annotations={"twingate.com/resource": "true"})
@kopf.on.update("service", annotations={"twingate.com/resource": "true"})
@kopf.on.resume("service", annotations={"resource.twingate.com": "true"})
@kopf.on.create("service", annotations={"resource.twingate.com": "true"})
@kopf.on.update("service", annotations={"resource.twingate.com": "true"})
def twingate_service_create(body, spec, namespace, meta, logger, reason, **_):
    logger.info("twingate_service_create: %s", body)

    resource_subobject = service_to_twingate_resource(body, namespace)
    kopf.adopt(resource_subobject)

    resource_object_name = resource_subobject["metadata"]["name"]

    kapi = kubernetes.client.CustomObjectsApi()
    if existing_resource_object := k8s_get_twingate_resource(
        namespace, resource_object_name, kapi
    ):
        logger.info("TwingateResource already exists: %s", existing_resource_object)
        existing_resource_object["spec"] = {
            "id": existing_resource_object["spec"]["id"],
            **resource_subobject["spec"],
        }
        existing_resource_object["metadata"]["labels"] = resource_subobject["metadata"][
            "labels"
        ]
        kapi.replace_namespaced_custom_object(
            "twingate.com",
            "v1beta",
            namespace,
            "twingateresources",
            resource_object_name,
            existing_resource_object,
        )
        kopf.info(
            body,
            reason=f"twingate_service_create ({reason.value})",
            message=f"Updated TwingateResource {resource_object_name}",
        )
    else:
        api_response = kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
        )
        logger.info("create_namespaced_custom_object response: %s", api_response)
        kopf.info(
            body,
            reason=f"twingate_service_create ({reason.value})",
            message=f"Created TwingateResource {resource_object_name}",
        )


@kopf.on.update("service", annotations={"resource.twingate.com": "false"})
@kopf.on.update("service", annotations={"resource.twingate.com": kopf.ABSENT})
def twingate_service_annotation_removed(body, spec, namespace, meta, logger, **_):
    logger.info("twingate_service_annotation_removed: %s", spec)

    resource_object_name = f"{body.meta.name}-resource"

    kapi = kubernetes.client.CustomObjectsApi()
    if existing_resource_object := k8s_get_twingate_resource(
        namespace, resource_object_name, kapi
    ):
        logger.info("Deleting TwingateResource: %s", existing_resource_object)
        kapi.delete_namespaced_custom_object(
            "twingate.com",
            "v1beta",
            namespace,
            "twingateresources",
            resource_object_name,
        )
        kopf.info(
            body,
            reason="twingate_service_annotation_removed",
            message=f"Deleted TwingateResource {resource_object_name}",
        )

    kopf.info(
        body,
        reason="twingate_service_annotation_removed",
        message=f"TwingateResource {resource_object_name} does not exist",
    )
