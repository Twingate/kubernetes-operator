# Twingate Kubernetes Controller

[![CI](https://github.com/Twingate/kubernetes-operator/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Twingate/kubernetes-operator/actions/workflows/ci.yaml)
[![Coverage Status](https://coveralls.io/repos/github/Twingate/kubernetes-operator/badge.svg?branch=main&t=7BQPrK)](https://coveralls.io/github/Twingate/kubernetes-operator?branch=main)
[![Dockerhub](https://img.shields.io/badge/dockerhub-images-info.svg?logo=Docker)](https://hub.docker.com/r/twingate/kubernetes-operator)

> [!IMPORTANT]
> **Beta:** The Twingate K8S Operator is currently in beta

The Twingate Kubernetes Controller is a custom controller designed to automate
and manage Twingate resources within a Kubernetes environment. It provides
seamless integration between your Kubernetes clusters and the Twingate Zero
Trust Network.

## Prerequisites

- Kubernetes cluster (1.16+)
- Twingate account and resources (Gateways, Networks, Applications, etc.)
- Twingate account setup with a `Remote Network` for the Kubernetes cluster and
 connectors deployed (see [this Helm chart](https://github.com/Twingate/helm-charts)
 if required)
- `Read/Write` API token - this can be generated in the Twingate Admin Console

## Installation

1. Clone this repository to your local machine.
1. Use the `helm` chart in `./deploy/twingate-operator`:

   1. Create a custom `values.yaml`:

   ```bash
   cp ./deploy/twingate-operator/values.yaml ./deploy/twingate-operator/values.local.yaml
   ```

   1. Edit the settings (`twingateOperator` specifically) in
      `./deploy/twingate-operator/values.local.yaml`
   1. Deploy:

   ```bash
   helm upgrade twop ./deploy/twingate-operator --install --wait -f ./deploy/twingate-operator/values.local.yaml
   ```

## Support

- For general issues using this operator please open a GitHub issue.
- For account specific issues, please visit the [Twingate forum](https://forum.twingate.com/)
 or open a [support ticket](https://help.twingate.com/)

## Development

1. `cp .envrc.local.example .envrc.local` and edit the values to match your
   environment.
1. Run `direnv allow`
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
   1. `brew install minikube`
1. `minikube start`
1. Apply the custom CRDs to the cluster -
   `kubectl apply -f deploy/twingate-operator/crds/`
1. Run `make test-int` to see integration tests pass.
1. You can now edit code and run `make run` to run the operator locally
   1. You'll also want to `peotry run pre-commit install` to make sure you have
      the pre-commit checks running locally.

### Release process

#### Dev Releases

When a PR is merged to `main` the `CI` github workflow will run and publish a
new dev release to docker. This dev release version is determined by patching
the current in `pyproject.toml` and adding a `-dev.<build number>` suffix.

For example, for the version in `pyproject.toml` is `0.4.0` then dev releases
will be versioned as `0.4.1-dev.<build num>` and `CI` will publish the following
tags:

- `dev` - latest development
- `0.4.1-dev.<build num>`

#### Production Releases

- Run `./scripts/release.sh`:
   - Calculate new version based on conventional commits
   - Update version in `pyproject.toml`
   - Update `CHANGELOG.md`
   - Create a tag for the version and commit
- Once pushed a Github workflow will
   - Create a Github release
   - Publish the following tags to dockerhub:
      - `latest`
      - `<major>`
      - `<major>.<minor>`
      - `<major>.<minor>.<patch>`
