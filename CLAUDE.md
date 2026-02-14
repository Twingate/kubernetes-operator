# CLAUDE.md - Twingate Kubernetes Operator

AI assistant guide for the Twingate Kubernetes Operator - a Kopf-based K8s controller for Twingate resources.

**Stack**: Python 3.11+, Kopf, Pydantic v2, Mypy, GraphQL (gql), Pytest, Ruff

## Structure

```text
app/
├── api/              # GraphQL client (client.py + client_*.py mixins, protocol.py)
├── handlers/         # Kopf handlers (handlers_*.py with @kopf decorators, base.py)
├── version_policy_providers/  # Container version selection (dockerhub.py, google.py)
├── crds.py           # Pydantic CRD schemas
├── settings.py       # Configuration (env vars)
└── conftest.py       # Pytest fixtures
main.py               # Operator entry point
deploy/twingate-operator/  # Helm chart + CRD YAMLs
tests_integration/    # Integration tests
```

## Core Patterns

### Kopf Handlers

Use `@kopf.on.create/update/delete/timer` decorators. Handler params: `body`, `spec`, `status`, `labels`,
`diff`, `patch`, `memo`, `logger`.

- Access settings: `memo.twingate_settings`
- Update specs: `patch.spec["field"] = value`
- Return: `success(**data)` or `fail(**data)` from `base.py`
- Log with `logger` param (not logging module)

### Pydantic CRDs (app/crds.py)

Models use `frozen=True`, `populate_by_name=True`, `alias_generator=to_camel`. Frozen models require `model_copy()` for modifications.

### API Client

All API calls via `TwingateAPIClient(memo.twingate_settings, logger=logger)`. GraphQL queries in
`protocol.py`. Raises `GraphQLMutationError` on failures.

**Add new API**: Define query in `protocol.py` → Create mixin in `client_*.py` → Add to `TwingateAPIClient`

### Settings

Env vars with `TWINGATE_` prefix: `API_KEY`, `NETWORK`, `REMOTE_NETWORK_ID` (or `REMOTE_NETWORK_NAME`),
`DEFAULT_RESOURCE_TAGS`. Access via `memo.twingate_settings`.

## Development

**Setup**: `asdf install && poetry sync --with dev && poetry run pre-commit install`
**Run locally**: `make run` (or PyCharm: module `kopf`, args `run ./main.py -A --verbose`)
**Testing**: `make test` (unit), `make test-int` (integration, needs K8s + env vars), `make check` (all checks)

### Testing

- Unit tests use `mocked_responses` and fixtures from `app/conftest.py`
- Integration tests need `TWINGATE_API_KEY`, `TWINGATE_NETWORK`, `TWINGATE_REMOTE_NETWORK_ID`
- Mock settings before importing handlers (loaded at module import time)

### Common Tasks

- **Add API**: Query in `protocol.py` → Mixin in `client_*.py` → Mix into `TwingateAPIClient`
- **Add CRD**: Pydantic model in `crds.py` → Handler in `handlers_*.py` → YAML in `deploy/*/crds/` → Import in `app/handlers/__init__.py`

## Code Quality

- **Types**: Strict Mypy (`make typecheck`), use `|` not `Union`, avoid `Any`
- **Format/Lint**: Ruff format + check, Bandit security scan. Pre-commit hooks enforce.
- **Line length**: 88 chars

## Critical Patterns & Pitfalls

**Security**:

- Never log API keys (logger auto-sanitizes)
- Use parameterized GraphQL queries (never string interpolation)
- Validate certs with `x509.load_pem_x509_certificate()`

**Kopf Handler Rules**:

- Handler param names matter (Kopf matches by name, typos = silent failures)
- Always use `TwingateAPIClient`, never direct HTTP requests
- Use `memo` not global state
- New handlers must be imported in `app/handlers/__init__.py`
- Don't modify handler signatures arbitrarily

**Pydantic CRDs**:

- Models are frozen - use `model_copy()` for modifications
- Always instantiate CRD classes (validates specs)

**Testing**:

- Mock settings before importing handlers
- Integration tests need `TWINGATE_API_KEY`, `TWINGATE_NETWORK`, `TWINGATE_REMOTE_NETWORK_ID`

**Breaking Changes**:

- CRD schema changes need migration strategy
- Maintain backward compatibility for API responses and env vars

## Release & Deployment

**Dev releases**: Auto on merge to main (version: `<version>-dev.<build>`)

**Prod releases**: `./scripts/release.sh` (conventional commits: `feat:` = minor, `fix:`/`chore:` = patch,
`BREAKING CHANGE:` = major)
**Helm chart**: `deploy/twingate-operator/` (test with `make test-helm`)

## Commands

```bash
make run                    # Run locally
make test / test-int        # Unit / integration tests
make check                  # All checks (lint, type, security)
make typecheck              # Mypy
make image-build            # Docker build
make test-helm              # Helm chart tests
```

## Debugging

- Verbose: `kopf run main.py -A --verbose`
- Log params: `logger.info(f"{body=}, {spec=}, {diff=}")`
- Check Kopf status: `kubectl describe` (shows Kopf annotations)
- Test responses: `mocked_responses.calls`
