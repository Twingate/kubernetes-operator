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

All API calls via `TwingateAPIClient(memo.twingate_settings, logger=logger)`. GraphQL queries and mutations are
defined as string constants in the respective `client_*.py` mixin files where they are used. `protocol.py` contains
the `TwingateClientProtocol` interface, which defines `execute_gql` and `execute_mutation`. Raises `GraphQLMutationError`
on failures.

**Add new API**: Define the query or mutation in the appropriate `client_*.py` mixin → Implement a method that calls
`execute_gql` / `execute_mutation` via the protocol → Add the mixin to `TwingateAPIClient`

### Settings

Env vars with `TWINGATE_` prefix: `API_KEY`, `NETWORK`, `REMOTE_NETWORK_ID` (or `REMOTE_NETWORK_NAME`),
`DEFAULT_RESOURCE_TAGS`. Access via `memo.twingate_settings`.

## Development

### Testing

- Unit tests use `mocked_responses` and fixtures from `app/conftest.py`
- Integration tests need `TWINGATE_API_KEY`, `TWINGATE_NETWORK`, `TWINGATE_REMOTE_NETWORK_ID`
- Mock settings before importing handlers (loaded at module import time)

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

**Breaking Changes**:

- CRD schema changes need migration strategy
- Maintain backward compatibility for API responses and env vars

## Release & Deployment

**Dev releases**: Auto on merge to main (version: `<version>-dev.<build>`)

**Prod releases**: `./scripts/release.sh` (conventional commits: `feat:` = minor, `fix:`/`chore:` = patch,
`BREAKING CHANGE:` = major)
**Helm chart**: `deploy/twingate-operator/` (test with `make test-helm`)

## Pull Requests

**Creating PRs**: Use `gh pr create` or GitHub UI. Follow `.github/pull_request_template.md`:

- Link related tickets
- Summarize changes (bullet points)
- For bug fixes: include root cause and reproduction steps

**Review**: `gh pr review`, `gh pr comment`, `gh pr diff`, `gh pr checks`

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
