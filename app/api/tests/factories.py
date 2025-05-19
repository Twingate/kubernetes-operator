import datetime
from base64 import b64encode

import factory.fuzzy

from app.api.client_connectors import Connector
from app.api.client_resources import (
    BaseResource,
    KubernetesResource,
    NetworkResource,
    ResourceAddress,
    ResourceRemoteNetwork,
    ResourceSecurityPolicy,
    Tag,
)

VALID_CA_CERT = "-----BEGIN CERTIFICATE-----\nMIIFfzCCA2egAwIBAgIVALoOJAoSP1m81BQ3DAjRHcYXrLR8MA0GCSqGSIb3DQEBCwUAMHcxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDTzEQMA4GA1UEBxMHQm91bGRlcjESMBAGA1UEChMJSnVtcENsb3VkMRkwFwYDVQQLExBKdW1wQ2xvdWRTQU1MSWRQMRowGAYDVQQDExFKdW1wQ2xvdWRTQU1MVXNlcjAeFw0yMTExMjkwMTAyMTRaFw0yNjExMjkwMTAyMTRaMHcxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDTzEQMA4GA1UEBxMHQm91bGRlcjESMBAGA1UEChMJSnVtcENsb3VkMRkwFwYDVQQLExBKdW1wQ2xvdWRTQU1MSWRQMRowGAYDVQQDExFKdW1wQ2xvdWRTQU1MVXNlcjCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBALc6KJOG3Nm02vHfvoaWkr0sR94HOVwiK79jdxP4saCi5hL7Fj2EnEmz73BH/BxBFQ/uHcRjMO9uLn6WRcT2P8WDMtyUuBSIUL4lLxoTOm0/37qrYYAHfbYJuPWAbvIxne2Ns0iXYFkgHSZ6DudZ37SSdXnPBuR6caeymbovrCHPbETb3SpgcVMuuuG1XhCTN0lZ/xrpB1G8HqL37xVCmJAzmBmUgYpu9+zH1uBPwUoWa8THelXrp2CUZ3mtwo0uKnfyXJcJyC5rJv0RLo4oJRetU3miTF7/trcXMhXGsosM/U/a5sn79Eh3vx+BJCDdrJte5z0WCCR+FcLYtE9iweWpIKh98746rUoS4rMHpUae0Ns6eSpU+OwImMw6oUCHO8+x1gkcVBG2tfD0mv7TIdW5ib6M9L9T63L15qeke9APPcpG0vG5IxeGbClRcjE4usiTg+iK8+ACT7h2htScSGlPsI3Dbln9D4LXRKNHCcyBcpVOHI06Z0D0hK7yclpiuILSHaTTCPl38xwUNFlJDqXjUvzLxM1sWzebt4It3g886MkS4l0wZgaYHxmcmCdlJvyPqV8txgQZYBY3jT7EjgPFox4kLMVKA+jAzf9sHTh7zQnOgRE32rhj2NUAK3hBbHv1aOeUlhxSLDle7X6lXGxxHCvA3l1Npmo5A1OZhMBFAgMBAAGjAjAAMA0GCSqGSIb3DQEBCwUAA4ICAQCUIop2TSQJzsRhgwOGYkbpAblSjkNQ5TBZfrrZoFYOMA0ji62qlWD3C5OUaWQbBrvG/8LvCOXm4mPmp1e0Jeli6DZBIn2Uo7ne29V+itvgB/du6+pkrIr0egAbkJfkS+f3lQjepjFakiQqK3YLJtXJUrKvwjWkdgTmWr8S1P9LX4fE4Rlr9i+pg6NVspSDezmDHg7jbgcq1tK8g3raDpAM4LkyGJHCSE0tWmNDw6QKRb/ev6fBdz1UVTXaWZoA22rWcfMH35YwcCP5oXpikISi+JmG6HojBs4ljpbZFYcRRu9P/i0mvpdJQtPRRnvNC5v5EwPuktE1Wi6qkp68N7j+QLl8jyaXLn6GHE6CjggE4YB8veqceLaDDYutxRjT77LhESxWN6XRBzhMcOrHFpNJQI1VlalABW2YjpJIPvo+iWlAZZx20k2+GFJVNiwe0Xzdyql1eGMxCkKpd5wBezJeBUurMQ+tqd+1dG10fEBL3gikBGlZLSWus3pFxSiwYzhSSoAqK9zF7T+A674p7EQB9fk8V4ZtR6Oo20R4NWOX4VrqszFcYaNJrpKuB8FaDvUqcE2aQ+vkYXfi0FadLFmc7WeMePIMvkfinr9qEgYc+yq5Xa0WHb3Xe+1y7l0TKyuKHdBgHGJUBAbAEyau4UcIBjn1gX2YNQ/N1TRvqIbkcQ==\n-----END CERTIFICATE-----"
BASE64_OF_VALID_CA_CERT = "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZmekNDQTJlZ0F3SUJBZ0lWQUxvT0pBb1NQMW04MUJRM0RBalJIY1lYckxSOE1BMEdDU3FHU0liM0RRRUJDd1VBTUhjeEN6QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZRUUlFd0pEVHpFUU1BNEdBMVVFQnhNSFFtOTFiR1JsY2pFU01CQUdBMVVFQ2hNSlNuVnRjRU5zYjNWa01Sa3dGd1lEVlFRTEV4QktkVzF3UTJ4dmRXUlRRVTFNU1dSUU1Sb3dHQVlEVlFRREV4RktkVzF3UTJ4dmRXUlRRVTFNVlhObGNqQWVGdzB5TVRFeE1qa3dNVEF5TVRSYUZ3MHlOakV4TWprd01UQXlNVFJhTUhjeEN6QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZRUUlFd0pEVHpFUU1BNEdBMVVFQnhNSFFtOTFiR1JsY2pFU01CQUdBMVVFQ2hNSlNuVnRjRU5zYjNWa01Sa3dGd1lEVlFRTEV4QktkVzF3UTJ4dmRXUlRRVTFNU1dSUU1Sb3dHQVlEVlFRREV4RktkVzF3UTJ4dmRXUlRRVTFNVlhObGNqQ0NBaUl3RFFZSktvWklodmNOQVFFQkJRQURnZ0lQQURDQ0Fnb0NnZ0lCQUxjNktKT0czTm0wMnZIZnZvYVdrcjBzUjk0SE9Wd2lLNzlqZHhQNHNhQ2k1aEw3RmoyRW5FbXo3M0JIL0J4QkZRL3VIY1JqTU85dUxuNldSY1QyUDhXRE10eVV1QlNJVUw0bEx4b1RPbTAvMzdxcllZQUhmYllKdVBXQWJ2SXhuZTJOczBpWFlGa2dIU1o2RHVkWjM3U1NkWG5QQnVSNmNhZXltYm92ckNIUGJFVGIzU3BnY1ZNdXV1RzFYaENUTjBsWi94cnBCMUc4SHFMMzd4VkNtSkF6bUJtVWdZcHU5K3pIMXVCUHdVb1dhOFRIZWxYcnAyQ1VaM210d28wdUtuZnlYSmNKeUM1ckp2MFJMbzRvSlJldFUzbWlURjcvdHJjWE1oWEdzb3NNL1UvYTVzbjc5RWgzdngrQkpDRGRySnRlNXowV0NDUitGY0xZdEU5aXdlV3BJS2g5ODc0NnJVb1M0ck1IcFVhZTBOczZlU3BVK093SW1NdzZvVUNITzgreDFna2NWQkcydGZEMG12N1RJZFc1aWI2TTlMOVQ2M0wxNXFla2U5QVBQY3BHMHZHNUl4ZUdiQ2xSY2pFNHVzaVRnK2lLOCtBQ1Q3aDJodFNjU0dsUHNJM0RibG45RDRMWFJLTkhDY3lCY3BWT0hJMDZaMEQwaEs3eWNscGl1SUxTSGFUVENQbDM4eHdVTkZsSkRxWGpVdnpMeE0xc1d6ZWJ0NEl0M2c4ODZNa1M0bDB3WmdhWUh4bWNtQ2RsSnZ5UHFWOHR4Z1FaWUJZM2pUN0VqZ1BGb3g0a0xNVktBK2pBemY5c0hUaDd6UW5PZ1JFMzJyaGoyTlVBSzNoQmJIdjFhT2VVbGh4U0xEbGU3WDZsWEd4eEhDdkEzbDFOcG1vNUExT1poTUJGQWdNQkFBR2pBakFBTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElDQVFDVUlvcDJUU1FKenNSaGd3T0dZa2JwQWJsU2prTlE1VEJaZnJyWm9GWU9NQTBqaTYycWxXRDNDNU9VYVdRYkJydkcvOEx2Q09YbTRtUG1wMWUwSmVsaTZEWkJJbjJVbzduZTI5VitpdHZnQi9kdTYrcGtySXIwZWdBYmtKZmtTK2YzbFFqZXBqRmFraVFxSzNZTEp0WEpVckt2d2pXa2RnVG1XcjhTMVA5TFg0ZkU0UmxyOWkrcGc2TlZzcFNEZXptREhnN2piZ2NxMXRLOGczcmFEcEFNNExreUdKSENTRTB0V21ORHc2UUtSYi9ldjZmQmR6MVVWVFhhV1pvQTIycldjZk1IMzVZd2NDUDVvWHBpa0lTaStKbUc2SG9qQnM0bGpwYlpGWWNSUnU5UC9pMG12cGRKUXRQUlJudk5DNXY1RXdQdWt0RTFXaTZxa3A2OE43aitRTGw4anlhWExuNkdIRTZDamdnRTRZQjh2ZXFjZUxhRERZdXR4UmpUNzdMaEVTeFdONlhSQnpoTWNPckhGcE5KUUkxVmxhbEFCVzJZanBKSVB2bytpV2xBWlp4MjBrMitHRkpWTml3ZTBYemR5cWwxZUdNeENrS3BkNXdCZXpKZUJVdXJNUSt0cWQrMWRHMTBmRUJMM2dpa0JHbFpMU1d1czNwRnhTaXdZemhTU29BcUs5ekY3VCtBNjc0cDdFUUI5Zms4VjRadFI2T28yMFI0TldPWDRWcnFzekZjWWFOSnJwS3VCOEZhRHZVcWNFMmFRK3ZrWVhmaTBGYWRMRm1jN1dlTWVQSU12a2ZpbnI5cUVnWWMreXE1WGEwV0hiM1hlKzF5N2wwVEt5dUtIZEJnSEdKVUJBYkFFeWF1NFVjSUJqbjFnWDJZTlEvTjFUUnZxSWJrY1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0t"


# encode string to base64
def to_global_id(type_: str, id_: str) -> str:
    value = f"{type_}:{id_}"
    return b64encode(value.encode()).decode()


class ResourceAddressFactory(factory.Factory):
    class Meta:
        model = ResourceAddress

    class Params:
        hostname = factory.Faker("slug")

    type = "DNS"
    value = factory.LazyAttribute(lambda o: o.hostname + ".default.cluster.local")


class ResourceRemoteNetworkFactory(factory.Factory):
    class Meta:
        model = ResourceRemoteNetwork

    id = factory.Sequence(lambda n: to_global_id("RemoteNetwork", str(n)))


class ResourceSecurityPolicyFactory(factory.Factory):
    class Meta:
        model = ResourceSecurityPolicy

    id = factory.Sequence(lambda n: to_global_id("SecurityPolicy", str(n)))


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    key = factory.fuzzy.FuzzyText(length=3)
    value = factory.fuzzy.FuzzyText(length=3)


class BaseResourceFactory(factory.Factory):
    class Meta:
        model = BaseResource

    id = factory.Sequence(lambda n: to_global_id("Resource", str(n)))
    name = factory.Faker("slug")
    created_at = factory.LazyFunction(datetime.datetime.now)
    updated_at = factory.LazyFunction(datetime.datetime.now)
    address = factory.SubFactory(
        ResourceAddressFactory, hostname=factory.SelfAttribute("..name")
    )
    alias = factory.SelfAttribute("name")
    is_visible = True
    remote_network = factory.SubFactory(ResourceRemoteNetworkFactory)
    security_policy = factory.SubFactory(ResourceSecurityPolicyFactory)
    tags = factory.List([factory.SubFactory(TagFactory)])


class NetworkResourceFactory(BaseResourceFactory):
    class Meta:
        model = NetworkResource

    is_browser_shortcut_enabled = False


class KubernetesResourceFactory(BaseResourceFactory):
    class Meta:
        model = KubernetesResource

    proxy_address = factory.Faker("hostname")
    certificate_authority_cert = VALID_CA_CERT


class ConnectorFactory(factory.Factory):
    class Meta:
        model = Connector

    id = factory.Sequence(lambda n: to_global_id("Connector", str(n)))
    name = factory.Faker("slug")
    has_status_notifications_enabled = False
