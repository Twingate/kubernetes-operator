import kubernetes


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


def k8s_safe_delete_deployment(
    namespace: str,
    name: str,
    kapi_apps: kubernetes.client.AppsV1Api | None = None,
):
    try:
        kapi_apps = kapi_apps or kubernetes.client.AppsV1Api()
        kapi_apps.delete_namespaced_deployment(
            name,
            namespace,
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status != 404:
            raise
