import requests


def _iterate_active_production_tags(results):
    for result in results:
        if result["tag_status"] != "active":
            continue
        if "-dev." in result["name"]:
            continue
        yield result


# curl https://hub.docker.com/v2/namespaces/library/repositories/twingate/kubernetes-operator/tags?page_size=100 and get all the tags
def get_operator_image_tags() -> list[str]:
    url = "https://hub.docker.com/v2/namespaces/twingate/repositories/kubernetes-operator/tags?page_size=100"
    response = requests.get(url)
    data = response.json()
    return [
        x["name"]
        for x in _iterate_active_production_tags(data["results"])
        if "." in x["name"] or x["name"].isnumeric()
    ]
