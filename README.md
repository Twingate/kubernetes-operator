# Twingate Kubernetes Operator

[![CI](https://github.com/Twingate/kubernetes-operator/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Twingate/kubernetes-operator/actions/workflows/ci.yaml)
[![Coverage Status](https://coveralls.io/repos/github/Twingate/kubernetes-operator/badge.svg?branch=main&t=7BQPrK)](https://coveralls.io/github/Twingate/kubernetes-operator?branch=main)
[![Dockerhub](https://img.shields.io/badge/dockerhub-images-info.svg?logo=Docker)](https://hub.docker.com/r/twingate/kubernetes-operator)

> [!IMPORTANT]
> **Beta:** The Twingate K8S Operator is currently in beta

The Twingate Kubernetes Controller is a custom controller designed to automate
and manage Twingate resources within a Kubernetes environment. It provides
seamless integration between your Kubernetes clusters and the Twingate Zero
Trust Network.

[Wiki][1]  |  [Getting Started][2]  |  [API Reference][3]

[1]: https://github.com/Twingate/kubernetes-operator/wiki
[2]: https://github.com/Twingate/kubernetes-operator/wiki/Getting-Started
[3]: https://github.com/Twingate/kubernetes-operator/wiki/API-Reference

## Prerequisites

- Kubernetes cluster (1.16+)
- Twingate account and resources (Gateways, Networks, Applications, etc.)
- Twingate account setup with a `Remote Network` for the Kubernetes cluster and
 connectors deployed (see [this Helm chart](https://github.com/Twingate/helm-charts)
 if required)
- `Read/Write` API token - this can be generated in the Twingate Admin Console

## Installation

### Helm via OCI (recommended)

To read helm charts for GitHub packages, you need to authenticate with GitHub
using a Personal Access Token (PAT).
Create a token with `read:packages` permissions and export it as an environment variable:

```bash
export GHCR_PAT=ghp_...
````

Then authenticate Docker to read from Github by running
`echo $GHCR_PAT | docker login ghcr.io -u <GITHUB-USERNAME> --password-stdin`
with your username following the `-u` flag.

Make sure your setup works by running `helm pull oci://ghcr.io/twingate/helmcharts/twingate-operator`.

Now we're ready to install the operator:

[default-values-yaml]: https://github.com/Twingate/kubernetes-operator/blob/main/deploy/twingate-operator/values.yaml

1. Create a custom `values.yaml` (You can start by copying the [default values .yaml file][default-values-yaml]):
1. Edit the settings in the file and specifically `twingateOperator`.
1. Deploy (add `-n [namespace]` if you want to install to a specific namespace):

```bash
helm upgrade twop oci://ghcr.io/twingate/helmcharts/twingate-operator --install --wait -f ./values.yaml
```

### Helm by closing the git repository

1. Clone this repository to your local machine.
1. Use the `helm` chart in `./deploy/twingate-operator`:

   1. Create a custom `values.yaml`:

   ```bash
   cp ./deploy/twingate-operator/values.yaml ./deploy/twingate-operator/values.local.yaml
   ```

   1. Edit the settings (`twingateOperator` specifically) in
      `./deploy/twingate-operator/values.local.yaml`
   1. Deploy (add `-n [namespace]` if you want to install to a specific namespace):

   ```bash
   helm upgrade twop ./deploy/twingate-operator --install --wait -f ./deploy/twingate-operator/values.local.yaml
   ```

## Changelog

See [CHANGELOG](./CHANGELOG.md)

## Support

- For general issues using this operator please open a GitHub issue.
- For account specific issues, please visit the [Twingate forum](https://forum.twingate.com/)
 or open a [support ticket](https://help.twingate.com/)

## Developers

See [developer guide](./DEVELOPER.md)
