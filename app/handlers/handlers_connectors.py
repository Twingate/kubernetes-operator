import time

import kopf
import kubernetes.client
import pendulum

from app.api import TwingateAPIClient
from app.crds import TwingateConnectorCRD
from app.handlers.base import success
from app.settings import get_version

ANNOTATION_LAST_VERSION_CHECK = "twingate.com/last-version-check"
ANNOTATION_NEXT_VERSION_CHECK = "twingate.com/next-version-check"

LABEL_CONNECTOR_POD_DELETED = "twingate.com/connector-pod-deleted"


def get_connector_pod(
    crd: TwingateConnectorCRD, tenant_url: str, image: str
) -> kubernetes.client.V1Pod:
    spec = crd.spec
    name = crd.metadata.name

    env_labels_version_policy = []
    if spec.image_policy:
        env_labels_version_policy = [
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SCHEDULE",
                "value": spec.image_policy.schedule,
            },
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SPEC",
                "value": spec.image_policy.version,
            },
        ]

    # fmt: off
    pod_spec = {
        "containers": [
            {
                "env": [
                    {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                    {"name": "TWINGATE_LABEL_OPERATOR_VERSION", "value": get_version()},
                    {"name": "TWINGATE_URL", "value": tenant_url},
                    {"name": "TWINGATE_LOG_LEVEL", "value": str(spec.log_level)},
                ]+env_labels_version_policy,
                "envFrom": [
                    {
                        "secretRef": {
                            "name": name,
                            "optional": False
                        }
                    }
                ],
                "image": image,
                "imagePullPolicy": "Always",
                "name": "connector",
                "securityContext": {
                    "allowPrivilegeEscalation": False,
                    "capabilities": {
                        "drop": ["ALL"],
                    },
                    "runAsNonRoot": True,
                    "runAsUser": 65532,
               },
                **spec.container_extra,
            }
        ],
        **spec.pod_extra,
    }
    # fmt: on
    return kubernetes.client.V1Pod(spec=pod_spec)


def get_connector_secret(
    access_token: str, refresh_token: str
) -> kubernetes.client.V1Secret:
    return kubernetes.client.V1Secret(
        immutable=True,
        string_data={
            "TWINGATE_ACCESS_TOKEN": access_token,
            "TWINGATE_REFRESH_TOKEN": refresh_token,
        },
    )


def check_pod_exists(namespace: str, name: str) -> bool:
    try:
        kapi = kubernetes.client.CoreV1Api()
        kapi.read_namespaced_pod(name=name, namespace=namespace)
        return True
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return False
        raise


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, memo, logger, namespace, patch, **_):
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings)

    logger.info("Got twingateconnector create request: %s", body)
    crd = TwingateConnectorCRD(**body)
    connector_id = crd.spec.id

    if not crd.spec.id:
        connector = client.connector_create(crd.spec)
        connector_id = connector.id
        patch.spec["id"] = connector.id
        patch.spec["name"] = connector.name
    else:
        connector = client.get_connector(crd.spec.id)

    logger.info("connector: %s", connector)
    tokens = client.connector_generate_tokens(connector.id)
    image = crd.spec.get_image()

    pod = get_connector_pod(crd, settings.full_url, image)
    secret = get_connector_secret(tokens.access_token, tokens.refresh_token)
    kopf.adopt([pod, secret], owner=body, strict=True, forced=True)
    kopf.label([pod, secret], {"twingate.com/connector": crd.metadata.name})

    kapi = kubernetes.client.CoreV1Api()
    kapi.create_namespaced_secret(namespace=namespace, body=secret)
    kapi.create_namespaced_pod(namespace=namespace, body=pod)

    image_policy = crd.spec.image_policy
    next_version_check = image_policy.get_next_date_iso8601() if image_policy else None
    patch.meta["annotations"] = {ANNOTATION_NEXT_VERSION_CHECK: next_version_check}

    return success(twingate_id=connector_id, image=image)


@kopf.on.resume("twingateconnector")
def twingate_connector_resume(body, patch, namespace, logger, **_):
    crd = TwingateConnectorCRD(**body)
    image_policy = crd.spec.image_policy
    next_version_check = image_policy.get_next_date_iso8601() if image_policy else None
    patch.meta["annotations"] = {ANNOTATION_NEXT_VERSION_CHECK: next_version_check}

    # Check pod exists and if not, add LABEL_CONNECTOR_POD_DELETED label to trigger recreation
    pod_requires_recreation = False
    if not check_pod_exists(namespace, crd.metadata.name):
        logger.info(
            "Pod is gone. Adding LABEL_CONNECTOR_POD_DELETED label to trigger recreation"
        )
        patch.meta["labels"] = {LABEL_CONNECTOR_POD_DELETED: "true"}
        pod_requires_recreation = True

    return success(
        twingate_id=crd.spec.id, pod_requires_recreation=pod_requires_recreation
    )


@kopf.on.field("twingateconnector", field="spec.imagePolicy")
def twingate_connector_version_policy_update(body, patch, logger, **_):
    logger.info("twingate_connector_version_policy_update: %s", body)
    crd = TwingateConnectorCRD(**body)
    image_policy = crd.spec.image_policy
    next_version_check = image_policy.get_next_date_iso8601() if image_policy else None
    patch.meta["annotations"] = {ANNOTATION_NEXT_VERSION_CHECK: next_version_check}


@kopf.on.update("twingateconnector", field="spec.image")
def twingate_connector_image_update(body, meta, namespace, memo, logger, **_):
    logger.info("twingate_connector_image_update: %s", body)
    settings = memo.twingate_settings
    crd = TwingateConnectorCRD(**body)
    image = crd.spec.get_image()
    if crd.spec.image:
        pod = get_connector_pod(crd, settings.full_url, image)
        kapi = kubernetes.client.CoreV1Api()
        result = kapi.patch_namespaced_pod(meta.name, namespace, body=pod)
        logger.info("Patched pod: %s", result)

    return success(twingate_id=crd.spec.id, image=image)


@kopf.on.timer(
    "twingateconnector",
    interval=60.0,
    annotations={ANNOTATION_NEXT_VERSION_CHECK: kopf.PRESENT},
)
def timer_check_image_version(body, meta, namespace, memo, logger, patch, **_):
    settings = memo.twingate_settings
    crd = TwingateConnectorCRD(**body)
    if not crd.spec.image_policy:
        patch.meta["annotations"] = {ANNOTATION_NEXT_VERSION_CHECK: None}
        return

    now = pendulum.now("UTC").start_of("minute")
    next_check = pendulum.parse(
        body["metadata"]["annotations"][ANNOTATION_NEXT_VERSION_CHECK]
    )
    if now < next_check:
        return

    logger.info("Checking connector %s for new image version", crd.metadata.name)

    try:
        image = crd.spec.get_image()
        pod = get_connector_pod(crd, settings.full_url, image)
        kapi = kubernetes.client.CoreV1Api()
        kapi.patch_namespaced_pod(meta.name, namespace, body=pod)
        patch.meta["annotations"] = {
            ANNOTATION_LAST_VERSION_CHECK: now.to_iso8601_string(),
            ANNOTATION_NEXT_VERSION_CHECK: crd.spec.image_policy.get_next_date_iso8601(),
        }
    except kubernetes.client.exceptions.ApiException:
        logger.exception("Failed to remove label from pod %s", meta.name)


# region Delete related


@kopf.on.update("twingateconnector", labels={LABEL_CONNECTOR_POD_DELETED: "true"})
def twingate_connector_recreate_pod(body, namespace, memo, logger, **_):
    """Recreates the Connector's Pod.

    When pod is deleted we can't recreate it right away because we want to
    use the same name. So when it's deleted, `twingate_connector_pod_deleted` annotates
    it's connector object so that we get to this handler and can recreate it.

    NOTE: This handler will get called as soon as we add the label to the pod, which
    is before the pod is actually deleted. So we need to wait for the pod to actually
    get deleted before we can recreate it.
    """

    def is_conflict_already_exists(apiex):
        return (
            apiex.status == 409
            and apiex.reason == "Conflict"
            and "AlreadyExists" in str(apiex)
        )

    logger.info("twingate_connector_recreate_pod: %s.", body)
    settings = memo.twingate_settings
    crd = TwingateConnectorCRD(**body)
    image = crd.spec.get_image()

    pod = get_connector_pod(crd, settings.full_url, image)
    kopf.adopt(pod, owner=body, strict=True, forced=True)
    kopf.label(pod, {"twingate.com/connector": crd.metadata.name})

    retry_count = 0
    kapi = kubernetes.client.CoreV1Api()
    while True:
        try:
            kapi.create_namespaced_pod(namespace=namespace, body=pod)
            break
        except kubernetes.client.exceptions.ApiException as apiex:  # noqa: PERF203
            if is_conflict_already_exists(apiex):
                # Pod is not deleted yet...  retry
                logger.info(
                    "Pod %s not deleted yet. Retrying (%s)...",
                    pod.metadata.name,
                    retry_count,
                )
                retry_count += 1
                if retry_count > 3:
                    raise
                time.sleep(2)
            else:
                raise


@kopf.on.delete("twingateconnector")
def twingate_connector_delete(spec, meta, status, namespace, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    client = TwingateAPIClient(memo.twingate_settings)

    if connector_id := spec.get("id"):
        logger.info("Deleting connector %s", connector_id)
        client.connector_delete(connector_id)

    try:
        # Remove label from pod so its delete handler isn't triggered
        kapi = kubernetes.client.CoreV1Api()
        kapi.patch_namespaced_pod(
            meta.name,
            namespace,
            body={"metadata": {"labels": {"twingate.com/connector": None}}},
        )
    except kubernetes.client.exceptions.ApiException:
        logger.exception("Failed to remove label from pod %s", meta.name)


@kopf.on.delete("", "v1", "pods", labels={"twingate.com/connector": kopf.PRESENT})
def twingate_connector_pod_deleted(body, spec, meta, logger, namespace, memo, **_):
    logger.info("twingate_connector_pod_deleted: %s", body)

    # Annotate the parent connector so that it knows it needs to recreate the pod
    owner_refs = meta.get("ownerReferences", [])
    owner = next((o for o in owner_refs if o["kind"] == "TwingateConnector"), None)
    if not owner:
        return

    owner_group, owner_version = owner["apiVersion"].split("/")

    try:
        kapi = kubernetes.client.CustomObjectsApi()
        kapi.patch_namespaced_custom_object(
            owner_group,
            owner_version,
            namespace,
            "twingateconnectors",
            owner["name"],
            {"metadata": {"labels": {LABEL_CONNECTOR_POD_DELETED: "true"}}},
        )
    except kubernetes.client.exceptions.ApiException:
        logger.exception("Failed to annotate connector %s", owner["name"])


# endregion
