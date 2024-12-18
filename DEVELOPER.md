# Development Guide

## Local Installation

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

1. We use [asdf](https://asdf-vm.com/) for version management. Install it and
   then run `asdf install` in the root of this repo to install the correct
   versions of the tools we use.
1. We use [direnv](https://direnv.net/) to manage environment variables. Install
   it and then run `direnv allow` in the root of this repo to allow it to manage
   your environment variables.
1. `cp .envrc.local.example .envrc.local` and edit the values to match your
   environment.
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
   1. `brew install minikube`
1. `minikube start`
1. Apply the custom CRDs to the cluster -
   `kubectl apply -f deploy/twingate-operator/crds/`
1. Run `make test-int` to see integration tests pass.
1. You can now edit code and run `make run` to run the operator locally
   1. You'll also want to `peotry run pre-commit install` to make sure you have
      the pre-commit checks running locally.

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

When a PR is merged to `main` the `CI` github workflow will run and publish a
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
* Once pushed a Github workflow will
  * Create a Github release
  * Publish the following tags to dockerhub:
    * `latest`
    * `<major>`
    * `<major>.<minor>`
    * `<major>.<minor>.<patch>`
