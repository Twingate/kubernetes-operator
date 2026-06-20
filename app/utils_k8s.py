import kopf
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


def k8s_read_namespaced_secret(
    namespace: str, name: str, kapi: kubernetes.client.CoreV1Api | None = None
) -> kubernetes.client.V1Secret | None:
    try:
        kapi = kapi or kubernetes.client.CoreV1Api()

        return kapi.read_namespaced_secret(name=name, namespace=namespace)
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None

        raise


def k8s_get_twingate_custom_object(
    plural: str,
    namespace: str,
    name: str,
    kapi: kubernetes.client.CustomObjectsApi | None = None,
) -> dict | None:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    try:
        return kapi.get_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, plural, name
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def k8s_patch_twingate_custom_object(
    plural: str,
    namespace: str,
    name: str,
    patch,
    kapi: kubernetes.client.CustomObjectsApi | None = None,
) -> None:
    """Persist a reconcile patch-shim's ``.spec`` / ``.status`` to a Twingate object.

    Lets the cross-resource event handlers drive the shared ``_reconcile_*``
    functions (which only mutate ``patch.spec`` / ``patch.status``) even though they
    have no kopf ``patch`` of their own. The CRDs declare no status subresource, so
    ``spec`` and ``status`` are written in a single patch.
    """
    body = {
        key: value
        for key, value in (("spec", patch.spec), ("status", patch.status))
        if value
    }
    if not body:
        return

    kapi = kapi or kubernetes.client.CustomObjectsApi()
    kapi.patch_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, plural, name, body
    )


def resolve_ref_to_twingate_id(
    plural: str, namespace: str, name: str, *, delay: int = 30
) -> str:
    """Resolve a reference to another Twingate CRD into its backend ``spec.id``.

    Raises ``kopf.TemporaryError`` (so the handler retries) when the referenced
    object does not exist yet or has not finished syncing to the backend.
    """
    obj = k8s_get_twingate_custom_object(plural, namespace, name)
    if obj is None:
        raise kopf.TemporaryError(
            f"Referenced {plural} '{name}' in namespace '{namespace}' not found.",
            delay=delay,
        )

    if backend_id := obj.get("spec", {}).get("id"):
        return backend_id

    raise kopf.TemporaryError(
        f"Referenced {plural} '{name}' in namespace '{namespace}' "
        "has not synced to Twingate yet.",
        delay=delay,
    )


def resolve_service_address(
    namespace: str, name: str, port: int, *, delay: int = 30
) -> str:
    """Resolve a Kubernetes Service to a ``host:port`` address.

    For a ``LoadBalancer`` Service the host comes from
    ``status.loadBalancer.ingress`` (raising ``kopf.TemporaryError`` so the
    caller retries until it is provisioned); otherwise the host is the
    in-cluster DNS name ``<name>.<namespace>.svc.cluster.local``.
    """
    capi = kubernetes.client.CoreV1Api()
    try:
        service = capi.read_namespaced_service(name, namespace)
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            raise kopf.TemporaryError(
                f"Service '{name}' in namespace '{namespace}' not found.",
                delay=delay,
            ) from ex
        raise

    service_type = service.spec.type
    if service_type == "LoadBalancer":
        load_balancer = service.status.load_balancer if service.status else None
        ingress = (load_balancer.ingress or []) if load_balancer else []
        host = (ingress[0].ip or ingress[0].hostname) if ingress else None
        if not host:
            raise kopf.TemporaryError(
                f"Service '{name}' in namespace '{namespace}' LoadBalancer "
                "is not ready.",
                delay=delay,
            )
    elif service_type in ("ClusterIP", "NodePort"):
        # Both have a stable in-cluster DNS name resolving to the ClusterIP.
        host = f"{name}.{namespace}.svc.cluster.local"
    else:
        # ExternalName (and anything else) has no in-cluster address to use.
        raise kopf.PermanentError(
            f"Service '{name}' in namespace '{namespace}' has unsupported type "
            f"'{service_type}'; expected ClusterIP, NodePort, or LoadBalancer."
        )

    return f"{host}:{port}"
