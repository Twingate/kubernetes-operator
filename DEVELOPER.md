# Development Guide

## Local Installation

1. Clone this repository to your local machine.
1. Use the `helm` chart in `./deploy/twingate-operator`:
   1. Create a custom `values.yaml`:

       ```bash
       cp ./deploy/twingate-operator/values.yaml ./deploy/twingate-operator/values.local.yaml
       ```

   1. Edit the settings (`twingateOperator` specifically) in `./deploy/twingate-operator/values.local.yaml`
   1. Deploy:

      ```bash
      helm upgrade twop ./deploy/twingate-operator --install --wait -f ./deploy/twingate-operator/values.local.yaml
      ```

## Development

1. We use [asdf](https://asdf-vm.com/) for version management. Install it and
   then run `asdf install` in the root of this repo to install the correct
   versions of the tools we use.
1. Copy the local env file and edit the values to match your environment:

    ```bash
    cp .envrc.local.example .envrc.local
    ```

1. We use [direnv](https://direnv.net/) to manage environment variables. Install
   it and then run `direnv allow` in the root of this repo to allow it to manage
   your environment variables.
1. Start a local Kubernetes cluster — see [Local cluster](#local-cluster) below.
1. Apply the custom CRDs to the cluster:

   ```bash
   kubectl apply -f deploy/twingate-operator/crds/
   ```

1. Run `make test-int` to see integration tests pass.
1. You can now edit code and run `make run` to run the operator locally.
   1. You'll also want to `poetry run pre-commit install` to make sure you have
      the pre-commit checks running locally.

> [!WARNING]
> `make test-int` runs against whatever your current kubectl context is, with no
> guard. It applies CRDs cluster-wide and its teardown runs `kubectl delete
> twingate --all`. Always confirm `kubectl config current-context` points at your
> local cluster before running it.

### Local cluster

#### macOS (recommended): kvz

[kvz](https://github.com/kvz-platform/kvz) is a native macOS Kubernetes distribution — the control
plane is a single macOS process with no Linux VM, so the cluster is ready in seconds. Requires an
Apple Silicon Mac on macOS 26 or later.

```bash
brew install kvz-platform/tap/kvz
kvz server --disable metrics-server     # leave running in its own terminal
export KUBECONFIG=~/.kvz/kubeconfig.yaml
```

kvz registers a `metrics.k8s.io` APIService that has no backing pod. Kopf scans every API group at
startup, so the 503 it returns kills the operator and every flow test with
`APIServerError: service unavailable`. `--disable metrics-server` stops kvz redeploying it, but the
registration persists in etcd — if you started kvz without the flag even once, delete it:

```bash
kubectl delete apiservice v1beta1.metrics.k8s.io
```

#### Linux, or as a fallback

[minikube](https://minikube.sigs.k8s.io/docs/start/) — install it and run `minikube start`. This is
also what CI uses (`scripts/minikube-smoketests.sh`, Linux only).

### PyCharm & IDEs

If you use PyCharm, create a Run/Debug Configuration by adding a new
Python configuration and setting it as follows:

* Mode: `module name`
* Module name: `kopf`
* Arguments: `run ./main.py -A --verbose`
* Python Interpreter: your project's virtualenv
* Working directory: your project's root directory
* Environment variables: copy your `.envrc.local` file content

Congratulations! You are ready to develop and debug the Twingate operator.

## Release process

### Dev Releases

When a PR is merged to `main` the `CI` GitHub workflow will run and publish a
new dev release to docker. This dev release version is determined by patching
the current in `pyproject.toml` and adding a `-dev.<build number>` suffix.

For example, for the version in `pyproject.toml` is `0.4.0` then dev releases
will be versioned as `0.4.1-dev.<build num>` and `CI` will publish the following
tags:

* `dev` - latest development
* `0.4.1-dev.<build num>`

### Production Releases

* Run `./scripts/release.sh`:
  * Calculate new version based on conventional commits
  * Update version in `pyproject.toml`
  * Update `CHANGELOG.md`
  * Create a tag for the version and commit
* Once pushed a GitHub workflow will
  * Create a GitHub release
  * Publish the following tags to dockerhub:
    * `latest`
    * `<major>`
    * `<major>.<minor>`
    * `<major>.<minor>.<patch>`
