PYTHON_VERSION 		?= $(shell python -c "import platform; print(platform.python_version())")
VERSION 	 		?= $(shell poetry version -s)
REGISTRY 			?= twingate
IMAGE				:= kubernetes-operator
IMAGE_NAME 			:= $(REGISTRY)/$(IMAGE)
PLATFORMS 			?= linux/amd64,linux/arm64
DOCKER_BUILDX_CACHE ?=
PROD_TAGS = $(shell ./scripts/split_semver.sh $(VERSION) | awk -v image="-t $(IMAGE_NAME)" '{ print image ":" $$0 }')

HELP_FUN = \
    %help; \
    while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-_]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
    print "usage: make [target]\n\n"; \
    for (sort keys %help) { \
    print "${WHITE}$$_:${RESET}\n"; \
    for (@{$$help{$$_}}) { \
    $$sep = " " x (32 - length $$_->[0]); \
    print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
    }; \
    print "\n"; }


help: ##@other Shows this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

version: ## Prints current version used for tagging docker images
	@echo $(VERSION)

.PHONY: lock
lock: ##@poetry Generates poetry.lock from pyproject.toml
	poetry lock --no-update -n

.PHONY: dev-deps
dev-deps:
	poetry install --sync --with dev -n

.PHONY: check-pre-commit
check-pre-commit:
	SKIP=$(skip) poetry run pre-commit run --all-files

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: lint-bandit
lint-bandit:
	poetry run bandit -c pyproject.toml -r -l ./app

.PHONY: lint-dockerfile
lint-dockerfile:
	docker run --rm -i hadolint/hadolint < Dockerfile

.PHONY: typecheck
typecheck:
	poetry run mypy --show-error-codes .

.PHONY: test
test:
	poetry run pytest -m "not integration"

.PHONY: test-cov
test-cov:
	poetry run pytest --cov=app --cov-report html -m "not integration"

.PHONY: test-int
test-int:
	poetry run pytest  -m "integration" -vv -x

.PHONY: report-to-coveralls
report-to-coveralls:
	poetry run coveralls

.PHONY: image-name
image-name:
	@echo $(IMAGE_NAME):$(VERSION)

.PHONY: image-build
image-build:
	@echo Building $(IMAGE_NAME)
	docker build --pull --target prod -t $(IMAGE_NAME):$(VERSION)-local . -f Dockerfile --build-arg PYTHON_VERSION=$(PYTHON_VERSION)

.PHONY: multiarch-image-build-prep
multiarch-image-build-prep:
	docker buildx create --name twingate-operator-builder --use
	docker buildx inspect --bootstrap

.PHONY: multiarch-image-build-dev
multiarch-image-build-dev:
	@echo Building $(IMAGE_NAME) $(VERSION) and latest
	docker buildx build -o type=image --platform=$(PLATFORMS) --pull -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):dev . -f Dockerfile  --target prod --build-arg PYTHON_VERSION=$(PYTHON_VERSION) $(DOCKER_BUILDX_CACHE)

.PHONY: multiarch-image-build-push-dev
multiarch-image-build-push-dev:
	@echo Building $(IMAGE_NAME) $(VERSION) and latest
	docker buildx build -o type=image --platform=$(PLATFORMS) --pull -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):dev . -f Dockerfile  --target prod --build-arg PYTHON_VERSION=$(PYTHON_VERSION) --push $(DOCKER_BUILDX_CACHE)

.PHONY: multiarch-image-build-push-prod
multiarch-image-build-push-prod:
	@echo Building $(IMAGE_NAME) $(PROD_TAGS) and latest
	docker buildx build -o type=image --platform=$(PLATFORMS) --pull $(PROD_TAGS) -t $(IMAGE_NAME):latest . -f Dockerfile  --target prod --build-arg PYTHON_VERSION=$(PYTHON_VERSION) --push $(DOCKER_BUILDX_CACHE)

.PHONY: gen-api-docs
gen-api-docs:
	go install fybrik.io/crdoc@latest
	crdoc --resources deploy/twingate-operator/crds --output docs/api.md

.PHONY: run
run:
	poetry run kopf run ./main.py -A --verbose --liveness=http://0.0.0.0:8080/healthz
