import kopf
import kubernetes

from app.handlers import success


@kopf.on.resume("services", annotations={"twingate.com/expose": "true"})
@kopf.on.create("service", annotations={"twingate.com/expose": "true"})
def twingate_service_create(body, spec, namespace, meta, logger, **_):
    logger.info("twingate_service_create: %s", spec)
    service_name = body.meta.name

    resource_subobject = {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {
            "name": f"{service_name}-resource",
        },
        "spec": {
            "name": f"{service_name}-resource",
            "address": f"{service_name}.{namespace}.svc.cluster.local",
        },
    }
    kopf.adopt(resource_subobject)

    if alias := meta.annotations.get("twingate.com/expose-alias"):
        resource_subobject["spec"]["alias"] = alias

    if service_ports := spec.get("ports", []):
        protocols = {
            "tcp": {"policy": "RESTRICTED", "ports": []},
            "udp": {"policy": "RESTRICTED", "ports": []},
        }
        for port_obj in service_ports:
            port = port_obj["port"]
            if port_obj["protocol"] == "TCP":
                protocols["tcp"]["ports"].append({"start": port, "end": port})
            elif port_obj["protocol"] == "UDP":
                protocols["udp"]["ports"].append({"start": port, "end": port})

        resource_subobject["spec"]["protocols"] = protocols

    kapi = kubernetes.client.CustomObjectsApi()
    api_response = kapi.create_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
    )
    logger.info("create_namespaced_custom_object response: %s", api_response)
    return success(
        message=f"Created TwingateResource {resource_subobject['spec']['name']}"
    )
