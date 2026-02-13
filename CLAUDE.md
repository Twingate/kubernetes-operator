# CLAUDE.md - Twingate Kubernetes Operator

This file guides AI assistants when working on the Twingate Kubernetes Operator codebase. It documents architecture, conventions, and common patterns to enable productive and accurate contributions.

## Project Overview

**Twingate Kubernetes Operator** is a Kubernetes controller that automates management of Twingate resources (connectors, gateways, resources, access policies) within Kubernetes environments. It provides seamless integration between Kubernetes clusters and the Twingate Zero Trust Network.

- **Language**: Python 3.11+
- **Framework**: Kopf (Kubernetes Operator Framework)
- **Type System**: Pydantic v2 + Mypy
- **GraphQL Client**: gql with requests transport
- **Testing**: Pytest with fixtures and factory-boy
- **Code Quality**: Ruff, Bandit, Mypy, Pre-commit hooks

## Repository Structure

```
/Users/ekampf/workspace/twingate/kubernetes-operator/
├── app/                           # Main application code
│   ├── api/                       # Twingate API client wrappers
│   │   ├── client.py             # Main API client (aggregates all APIs)
│   │   ├── client_connectors.py  # Connector-specific API methods
│   │   ├── client_groups.py      # Group-specific API methods
│   │   ├── client_resources.py   # Resource-specific API methods
│   │   ├── client_resources_access.py  # Access policy API
│   │   ├── client_service_accounts.py  # Service account API
│   │   ├── client_remote_networks.py   # Remote network API
│   │   ├── protocol.py           # GraphQL query definitions
│   │   ├── exceptions.py         # Custom exceptions
│   │   └── tests/                # API layer tests
│   ├── handlers/                 # Kopf event handlers for each CRD
│   │   ├── base.py              # Success/failure result helpers
│   │   ├── handlers_connectors.py # @kopf decorators for connectors
│   │   ├── handlers_groups.py    # @kopf decorators for groups
│   │   ├── handlers_resource.py  # @kopf decorators for resources
│   │   ├── handlers_resource_access.py # @kopf decorators for access
│   │   ├── handlers_services.py  # @kopf decorators for service accounts
│   │   └── tests/                # Handler tests
│   ├── version_policy_providers/  # Version selection for container images
│   │   ├── base.py              # Abstract base class
│   │   ├── dockerhub.py         # Docker Hub version provider
│   │   ├── google.py            # Google Artifact Registry provider
│   │   └── tests/
│   ├── crds.py                   # CRD schema definitions (Pydantic models)
│   ├── settings.py               # Configuration management
│   ├── typedefs.py              # Type aliases and custom types
│   ├── utils.py                  # General utility functions
│   ├── utils_k8s.py             # Kubernetes client helpers
│   ├── conftest.py              # Pytest fixtures for tests
│   └── tests/                    # Unit tests for app code
├── main.py                        # Kopf operator entry point
├── pyproject.toml                # Poetry dependencies and tool config
├── deploy/                        # Helm chart and manifests
│   └── twingate-operator/
│       ├── crds/                # CRD YAML definitions
│       ├── templates/           # Helm templates
│       ├── Chart.yaml
│       └── values.yaml
├── tests_integration/             # Integration tests (with real K8s)
├── Makefile                       # Build and test targets
├── Dockerfile                     # Multi-stage Docker build
└── scripts/                       # Release and build scripts
```

## Key Architectural Patterns

### 1. Kopf Framework Integration

The operator uses Kopf decorators to define handlers:

- `@kopf.on.create()` - Resource creation handler
- `@kopf.on.update()` - Resource update handler
- `@kopf.on.delete()` - Resource deletion handler
- `@kopf.timer()` - Periodic reconciliation
- `@kopf.on.startup()` / `@kopf.on.cleanup()` - Lifecycle hooks

Handlers receive parameters via Kopf's dependency injection: `body`, `spec`, `status`, `labels`, `diff`, `patch`, `memo`, `logger`, `**kwargs`.

**Key patterns in handlers:**

- Use `memo.twingate_settings` to access operator configuration
- Use the `patch` parameter to update spec fields (e.g., `patch.spec["id"] = resource.id`)
- Return result via `success(**data)` or `fail(**data)` helpers from `base.py`
- Log with the provided `logger` parameter, not the logging module

### 2. Pydantic CRD Definitions

All CRDs are defined as Pydantic models in `/Users/ekampf/workspace/twingate/kubernetes-operator/app/crds.py`:

```python
class ResourceSpec(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    id: str | None = None
    name: str
    # ... other fields

    def to_graphql_arguments(self, labels: dict, exclude: set = None) -> dict:
        # Convert to API format
```

**Important conventions:**

- Models use `frozen=True` for immutability
- Models use `alias_generator=to_camel` to convert Python snake_case to camelCase
- Use `populate_by_name=True` to accept both Python and API field names
- Use `extra="allow"` for models that accept arbitrary Kubernetes metadata

### 3. API Client Pattern

All Twingate API calls go through the `TwingateAPIClient` in `/Users/ekampf/workspace/twingate/kubernetes-operator/app/api/client.py`:

```python
# In a handler:
client = TwingateAPIClient(memo.twingate_settings, logger=logger)
resource = client.resource_create(resource_type=resource.type, **graphql_arguments)
```

The client:

- Uses GraphQL queries/mutations defined in `protocol.py`
- Handles HTTP retries with custom backoff logic
- Logs all API calls with full query and response
- Raises `GraphQLMutationError` on API errors

**Adding new API methods:**

1. Add GraphQL query/mutation to `app/api/protocol.py`
2. Create a mixin class in appropriate `client_*.py` file
3. Implement methods following existing patterns (request → execute_gql/execute_mutation → return typed result)
4. Mix into `TwingateAPIClient`

### 4. Settings Management

Configuration is managed via `TwingateOperatorSettings` in `/Users/ekampf/workspace/twingate/kubernetes-operator/app/settings.py`:

```python
settings = TwingateOperatorSettings()  # Loads from environment variables
```

**Environment variables (TWINGATE_ prefix):**

- `TWINGATE_API_KEY` - API authentication token
- `TWINGATE_NETWORK` - Twingate network name
- `TWINGATE_REMOTE_NETWORK_ID` - Kubernetes cluster remote network ID
- `TWINGATE_REMOTE_NETWORK_NAME` - Alternative to above (looks up ID automatically)
- `TWINGATE_HOST` - Default: "twingate.com"
- `TWINGATE_DEFAULT_RESOURCE_TAGS` - JSON dict of default labels for all resources
- Various `TWINGATE_KOPF_WATCHING_*` - Kopf framework timeouts

Access via: `get_settings()` function or `memo.twingate_settings` in handlers.

### 5. Version Policy Providers

Image version selection uses pluggable providers:

- **DockerHub Provider** (`app/version_policy_providers/dockerhub.py`) - Default for connector images
- **Google Artifact Registry Provider** (`app/version_policy_providers/google.py`) - For Google Artifact Registry

Subclass `VersionPolicyProvider` to add support for new registries. Methods:

- `get_all_tags()` → Iterator[str] - All available versions
- `get_latest(specifier, allow_prerelease)` → Version | None - Latest matching version

## Important Files and Their Purposes

| File | Purpose |
|------|---------|
| `/Users/ekampf/workspace/twingate/kubernetes-operator/main.py` | Kopf operator entry point - startup/shutdown hooks |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/crds.py` | All CRD schemas (Resources, Connectors, Groups, Access) |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/handlers/handlers_resource.py` | Resource create/update/delete handlers + reconciliation |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/handlers/handlers_connectors.py` | Connector deployment and version management |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/api/client.py` | Main API client aggregating all GraphQL operations |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/api/protocol.py` | GraphQL query/mutation definitions |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/app/settings.py` | Configuration and environment variable handling |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/pyproject.toml` | Dependencies, tools config (Ruff, Mypy, Pytest) |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/deploy/twingate-operator/crds/` | YAML CRD definitions (generated from app/crds.py) |
| `/Users/ekampf/workspace/twingate/kubernetes-operator/Dockerfile` | Multi-stage Docker build |

## Development Workflow

### Setup

```bash
# Install asdf and direnv
asdf install                          # Install correct Python, poetry versions
cp .envrc.local.example .envrc.local
direnv allow
poetry sync --with dev                # Install dependencies
poetry run pre-commit install         # Setup git hooks
```

### Local Development

```bash
# Apply CRDs to local Kubernetes cluster
kubectl apply -f deploy/twingate-operator/crds/

# Run the operator locally (in debug mode)
make run

# In PyCharm: Module name: kopf, Arguments: run ./main.py -A --verbose
```

### Code Changes

1. Make changes to Python files (auto-formatted by pre-commit)
2. Run tests: `make test` (unit tests) or `make test-int` (integration tests)
3. Check types: `make typecheck`
4. Run all checks: `make check`
5. Commit (pre-commit hooks run automatically)

### Testing Guidance

**Unit Tests** (`app/tests/`, `app/*/tests/`):

- Mock external dependencies with `responses` (HTTP) and `unittest.mock`
- Use pytest fixtures from `app/conftest.py`
- Patterns:

  ```python
  def test_something(mocked_responses):  # See app/conftest.py
      mocked_responses.add(responses.POST, ...)
      # Test code
  ```

**Integration Tests** (`tests_integration/`):

- Use real Kubernetes cluster (requires `TWINGATE_API_KEY`, `TWINGATE_NETWORK`, `TWINGATE_REMOTE_NETWORK_ID` env vars)
- Use `run_kopf` fixture to start operator
- Use `kubectl_*` helpers from `tests_integration/utils.py`
- Run with: `make test-int`

**Test Fixtures** (`app/conftest.py`):

- `mocked_responses` - HTTP response mocking
- `_mock_settings` - Mocked TwingateOperatorSettings
- `k8s_core_client_mock` - Mocked Kubernetes core API
- `k8s_apps_client_mock` - Mocked Kubernetes apps API

### Common Development Tasks

**Add a new API endpoint:**

1. Define GraphQL query in `app/api/protocol.py`
2. Create mixin class in `app/api/client_*.py`
3. Implement method following existing patterns
4. Add to `TwingateAPIClient` mixins
5. Write tests in `app/api/tests/`

**Add a new CRD:**

1. Define Pydantic model in `app/crds.py` (inherit from `BaseK8sModel`)
2. Create handler file `app/handlers/handlers_*.py` with @kopf decorators
3. Create YAML CRD in `deploy/twingate-operator/crds/`
4. Write tests in `app/tests/`

**Update handler logic:**

1. Edit `app/handlers/handlers_*.py`
2. Ensure changes are compatible with existing CRD specs
3. Update tests in `app/handlers/tests/`
4. Test with `make test-int`

**Add a new version provider:**

1. Subclass `VersionPolicyProvider` in `app/version_policy_providers/`
2. Implement `__init__` and `get_all_tags()`
3. Add tests
4. Update `get_provider()` function to recognize new provider type

## Code Quality Standards

### Type Checking

- Python 3.11+ with strict Mypy: `make typecheck`
- Avoid `Any` types - be specific
- Use `|` union syntax instead of `Union[A, B]`
- Pydantic models include type info for mypy plugin

### Formatting & Linting

- **Formatter**: `poetry run ruff format` (enforced by pre-commit)
- **Linter**: `poetry run ruff check` (100+ rule sets enabled)
- **Security**: `poetry run bandit -r app`
- **Imports**: Automatically sorted by ruff
- **Line length**: 88 characters (E501 ignored)
- **Docstrings**: Google style, not required for methods/functions

### Pre-commit Hooks

Required hooks run automatically (see `.pre-commit-config.yaml`):

- `check-ast`, `check-json`, `check-yaml`, `check-toml`
- `ruff format`, `ruff check`, `pyupgrade --py311-plus`
- `shellcheck`, `shfmt`, `markdownlint`

Run manually: `poetry run pre-commit run --all-files`

## Things to Be Careful About

### Security Considerations

1. **API Keys**: Never log API keys. Use `logger.info()` which sanitizes sensitive data.
2. **Certificates**: X.509 certificates are validated. Use `x509.load_pem_x509_certificate()` for validation.
3. **Base64 in CRDs**: Sensitive data like certs uses `Base64Str` from Pydantic (automatically decoded).
4. **GraphQL Mutations**: Always use parameterized queries, never string interpolation.

### Pattern Violations to Avoid

1. **Don't modify handlers arbitrarily**: The Kopf framework depends on specific signatures and parameter names. Changes can break operator behavior.
2. **Don't skip API calls**: Always go through `TwingateAPIClient`, never make direct requests.
3. **Don't use global state**: Use `memo` object passed by Kopf instead of module-level globals.
4. **Don't create settings multiple times**: Use `get_settings()` or `memo.twingate_settings`.
5. **Don't ignore finalizers**: Kopf uses "twingate.com/finalizer" for deletion tracking.
6. **Don't bypass Pydantic validation**: Always instantiate CRD classes to validate incoming specs.

### Common Pitfalls

1. **Handler parameter names matter**: Parameter names are matched by Kopf. Typos cause silent failures.
2. **Diff detection is precise**: Changes to spec/labels trigger updates. Status-only changes don't.
3. **Status vs Spec distinction**: `status` is Kopf-managed, `spec` is user input. Don't mix them.
4. **Imports in **init**.py**: Handlers are imported in `app/handlers/__init__.py` - new handlers must be imported there.
5. **Frozen models**: CRD Pydantic models are frozen. Can't modify after creation. Use `model_copy()` if mutation needed.

### Testing Gotchas

1. **Mock settings before importing handlers**: Settings are loaded at module import time.
2. **HTTP responses must match exactly**: `responses` library requires exact URL/method matching.
3. **K8s API mocks need setup**: Mock both `CoreV1Api` and `AppsV1Api` if handlers use them.
4. **Integration tests need env vars**: Must set `TWINGATE_API_KEY`, `TWINGATE_NETWORK`, `TWINGATE_REMOTE_NETWORK_ID`.

### Breaking Changes Risks

1. **CRD schema changes**: Once deployed, schema changes require migration strategy
2. **API client changes**: Backward compatibility with old API responses matters
3. **Environment variable removal**: Operators may be running with old configs
4. **Handler behavior changes**: May affect running operator instances

## Deployment and Release

### Development Releases

Automatic on merge to main:

- Version: Current version in `pyproject.toml` + `-dev.<build_number>`
- Tags: `dev` (latest), `<version>-dev.<build_number>`

### Production Releases

```bash
./scripts/release.sh
```

- Calculates new version from conventional commits
- Updates `pyproject.toml` and `CHANGELOG.md`
- Creates git tag
- Publishes to DockerHub on push

**Conventional commits** (for version calculation):

- `feat:` → minor version bump
- `fix:`, `perf:`, `chore:`, `build:` → patch version bump
- `BREAKING CHANGE:` → major version bump

## Helm Chart

Located in `/Users/ekampf/workspace/twingate/kubernetes-operator/deploy/twingate-operator/`:

- `values.yaml` - Default configuration
- `crds/` - YAML CRD definitions
- `templates/` - Deployment, RBAC, etc.

**Key configurations:**

- `twingateOperator.apiKey` - API token
- `twingateOperator.network` - Network name
- `twingateOperator.remoteNetworkId` - Cluster remote network ID
- `twingateOperator.defaultResourceTags` - Default labels for resources

Test Helm chart: `make test-helm` or `make test-helm-and-update-snapshots`

## Useful Commands

```bash
# Development
make help                 # Show all targets
make run                 # Run operator locally
make test               # Run unit tests
make test-cov          # Test with coverage report
make test-int          # Integration tests
make check             # All checks (lint, type, security)

# Specific checks
make lint              # Ruff linting
make typecheck         # Mypy type checking
make lint-bandit       # Bandit security scan
make check-pre-commit  # Pre-commit hooks

# Docker
make image-build       # Build Docker image
make multiarch-image-build-prod  # Build multi-arch

# Helm
make test-helm         # Test Helm chart
make test-helm-and-update-snapshots  # Update snapshots
```

## Debugging Tips

1. **Enable verbose logging**: Run with `kopf run main.py -A --verbose`
2. **Check handler parameters**: Use `logger.info(f"Got: {body=}, {spec=}, {status=}")`
3. **Inspect diffs**: Log `diff` parameter to understand what changed
4. **Mock responses in tests**: Use `mocked_responses.calls` to inspect requests
5. **Check Kopf status**: Use `kubectl describe` to see Kopf annotations
6. **Test GraphQL directly**: Use GraphQL playground in Twingate Admin Console

## References

- **Kopf Documentation**: <https://kopf.readthedocs.io/>
- **Kubernetes Python Client**: <https://github.com/kubernetes-client/python>
- **Pydantic**: <https://docs.pydantic.dev/2.0/>
- **GraphQL-core**: <https://graphql-core-3.readthedocs.io/>
- **Twingate Documentation**: <https://docs.twingate.com/>
