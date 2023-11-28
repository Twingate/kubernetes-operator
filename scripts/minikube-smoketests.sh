#!/bin/bash

# standard bash error handling
set -o errexit
set -o pipefail
set -o nounset
# debug commands
set -x

# working dir to install binaries etc, cleaned up on exit
BIN_DIR="$(mktemp -d)"
# minikube binary will be here
MINIKUBE="${BIN_DIR}/minikube"

# cleanup on exit (useful for running locally)
cleanup() {
	"${MINIKUBE}" delete --all || true
	rm -rf "${BIN_DIR}"
}

if [[ -n $CI ]]; then
	echo "Running in CI, not cleaning up on exit"
else
	trap cleanup EXIT
fi

# util to install a released minikube version into ${BIN_DIR}
install_minikube_release() {
	MINIKUBE_BINARY_URL="https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
	wget -nv -O "${MINIKUBE}" "${MINIKUBE_BINARY_URL}"
	chmod +x "${MINIKUBE}"
}

main() {
	# get minikube
	install_minikube_release

	# create a cluster
	"${MINIKUBE}" start --force
	"${MINIKUBE}" kubectl -- get pods -A

	"${MINIKUBE}" kubectl -- apply -f ./deploy/twingate-operator/crds/ || true

	export KUBECTL_COMMAND="${MINIKUBE} kubectl -- "

	make test-int
}

main
