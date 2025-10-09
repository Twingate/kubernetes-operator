import base64

import kopf
import kubernetes

from app.utils import validate_pem_x509_certificate


def k8s_read_namespaced_pod(
    namespace: str, name: str, kapi: kubernetes.client.CoreV1Api | None = None
) -> kubernetes.client.V1Pod | None:
    try:
        kapi = kapi or kubernetes.client.CoreV1Api()
        return kapi.read_namespaced_pod(name=name, namespace=namespace)
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def k8s_delete_pod(
    namespace: str,
    name: str,
    kapi: kubernetes.client.CoreV1Api | None = None,
    *,
    force: bool = False,
):
    kapi = kapi or kubernetes.client.CoreV1Api()
    if force:
        kapi.patch_namespaced_pod(
            name, namespace, body={"metadata": {"finalizers": None}}
        )
    kapi.delete_namespaced_pod(
        name, namespace, body=kubernetes.client.V1DeleteOptions(grace_period_seconds=0)
    )


def k8s_read_namespaced_deployment(
    namespace: str, name: str, kapi_apps: kubernetes.client.AppsV1Api | None = None
) -> kubernetes.client.V1Deployment | None:
    try:
        kapi_apps = kapi_apps or kubernetes.client.AppsV1Api()
        return kapi_apps.read_namespaced_deployment(name=name, namespace=namespace)
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
