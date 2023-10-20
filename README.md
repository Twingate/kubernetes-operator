# Twingate Kubernetes Controller

> [!NOTE] > **Beta:** The Twingate K8S Operator is currently in beta

The Twingate Kubernetes Controller is a custom controller designed to automate
and manage Twingate resources within a Kubernetes environment. It provides
seamless integration between your Kubernetes clusters and the Twingate Zero
Trust Network.

## Features

- [x] **Define Twingate Resources as Kubernetes Objects:** The controller
      automatically synchronizes `TwingateResource` objects from Kubernetes to
      Twingate.
- [ ] **Automatic Resource Management:** The controller automatically
      synchronizes Kubernetes Services and Ingress resources with Twingate
      resources, ensuring that access policies are consistently applied.
- [ ] **Define and Provision Twingate Remote Network+Connectors:** Define a
      `TwingateRemoteNetwork` object to create a remote network and deploy
      connectors on it to allow configuring access to Kubernetes resources.

## Prerequisites

- Kubernetes cluster (1.16+)
- Twingate account and resources (Gateways, Networks, Applications, etc.)

## Installation

1. Clone this repository to your local machine.
1. User the `helm` chart in `./deploy/twingate-operator`:

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

## Release process

### Dev Releases

When a PR is merged to `main` the `CI` github workflow will run and publish a
new dev release to docker. This dev release version is determined by patching
the current in `pyproject.toml` and adding a `-dev.<build number>` suffix.

For example, for the version in `pyproject.toml` is `0.4.0` then dev releases
will be versioned as `0.4.1-dev.<build num>` and `CI` will publish the following
tags:

- `dev` - latest development
- `0.4.1-dev.<build num>`

### Production Releases

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
