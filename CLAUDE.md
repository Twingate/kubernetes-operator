# Twingate Kubernetes Operator - Developer Guide

## Project Overview

The Twingate Kubernetes Operator is a custom Kubernetes controller that automates and manages
Twingate Zero Trust Network resources within Kubernetes clusters.
Built using the [Kopf](https://kopf.readthedocs.io/) framework,
it provides seamless integration between Kubernetes and Twingate's Zero Trust Network platform.

### Key Features

- **Custom Resource Definitions (CRDs)**: Manages TwingateConnector, TwingateGroup, TwingateResource, and
 TwingateResourceAccess resources
- **Declarative Management**: Define Twingate resources using Kubernetes manifests
- **API Integration**: Communicates with Twingate's GraphQL API for resource provisioning
- **Service Discovery**: Automatically manages Twingate resources for Kubernetes services
- **Access Control**: Manages group-based access to resources through ResourceAccess objects

### Supported Resource Types

- **TwingateConnector**: Manages Twingate connectors for secure network access
- **TwingateGroup**: Manages user groups and their permissions
- **TwingateResource**: Manages network resources and their access policies
- **TwingateResourceAccess**: Links groups to resources with specific access permissions

## Architecture

### High-Level Components

```text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │    Operator      │    │   Twingate      │
│    Cluster      │◄──►│    Controller    │◄──►│     API         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
    ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
    │  CRDs   │              │Handlers │              │GraphQL  │
    │Resources│              │ & Logic │              │   API   │
    └─────────┘              └─────────┘              └─────────┘
```

### Directory Structure

- **`app/`**: Main application code
  - **`api/`**: Twingate GraphQL API client and data models
  - **`handlers/`**: Kopf event handlers for each CRD type
  - **`version_policy_providers/`**: Container version management providers
  - **`crds.py`**: Pydantic models for Custom Resource Definitions
  - **`settings.py`**: Application configuration and environment settings
  - **`utils*.py`**: Utility functions for Kubernetes and general operations
- **`deploy/`**: Helm charts and Kubernetes deployment manifests
- **`examples/`**: Sample resource manifests for testing
- **`tests_integration/`**: End-to-end integration tests

### Core Components

#### 1. Custom Resource Definitions (CRDs)

Located in `app/crds.py`, these Pydantic models define the structure of Twingate resources:

- Validation and serialization of Kubernetes manifests
- Type-safe access to resource specifications
- Automatic camelCase/snake_case conversion for Kubernetes compatibility

#### 2. API Client Layer (`app/api/`)

- **`client.py`**: Base GraphQL client with authentication and error handling
- **`client_*.py`**: Specialized clients for each Twingate resource type
- **`protocol.py`**: Type definitions for API responses
- **`exceptions.py`**: Custom exception classes for API errors

#### 3. Event Handlers (`app/handlers/`)

- **`base.py`**: Common handler utilities and result types
- **`handlers_*.py`**: Kopf event handlers for create/update/delete operations
- Each handler manages the lifecycle of specific Twingate resource types

#### 4. Operator Framework Integration

- **`main.py`**: Kopf operator entry point with startup/shutdown hooks
- Custom storage classes for progress tracking and diff management
- Operator settings configuration and validation

### Event Flow

1. **Resource Creation**: User applies Kubernetes manifest with Twingate CRD
2. **Event Detection**: Kopf framework detects resource changes
3. **Handler Invocation**: Appropriate handler processes the event
4. **API Communication**: Handler calls Twingate API to create/update resources
5. **Status Update**: Kubernetes resource status is updated with results
6. **Error Handling**: Failures are retried with exponential backoff

## Commands

- **Lint**: `make lint` or `poetry run ruff check .`
- **Typecheck**: `make typecheck` or `poetry run mypy --show-error-codes .`
- **Run tests**: `make test` or `poetry run pytest -m "not integration"`
- **Run single test**: `poetry run pytest path/to/test_file.py::TestClass::test_method -v`
- **Integration tests**: `make test-int` or `poetry run pytest -m "integration" -vv -l -x`
- **Run locally**: `make run` or `poetry run kopf run ./main.py -A --verbose`

## Code Style

- **Formatting**: Ruff is used for code formatting and linting
- **Typing**: Strong typing with mypy, use annotations for all functions
- **Imports**: Use absolute imports, organized by ruff/isort rules
- **Docstrings**: Google style (pydocstyle convention)
- **Classes**: Use Pydantic models for data validation where appropriate
- **Error handling**: Use specific exceptions, avoid bare excepts
- **Naming**: Snake case for functions/variables, PascalCase for classes
- **Test organization**: Class-based tests with descriptive method names
- **Commits**: Follow conventional commits (feat, fix, chore, etc.)

## Development Workflows

### Getting Started

1. **Environment Setup**:

   ```bash
   # Install dependencies
   poetry install

   # Set up pre-commit hooks
   poetry run pre-commit install
   ```

2. **Local Development**:

   ```bash
   # Run the operator locally (requires kubeconfig)
   make run

   # Or with verbose logging
   poetry run kopf run ./main.py -A --verbose
   ```

### Testing Strategy

#### Unit Tests

- **Location**: `app/*/tests/` directories
- **Scope**: Individual functions and classes
- **Mocking**: Use pytest fixtures for API clients and Kubernetes objects
- **Command**: `make test` or `poetry run pytest -m "not integration"`

#### Integration Tests

- **Location**: `tests_integration/` directory
- **Scope**: End-to-end workflows with real Kubernetes cluster
- **Requirements**: Running Kubernetes cluster and Twingate API access
- **Command**: `make test-int` or `poetry run pytest -m "integration" -vv -l -x`

#### Test Organization

- Class-based tests with descriptive method names
- Use factories for test data generation (`app/api/tests/factories.py`)
- Shared fixtures in `conftest.py` files
- Integration tests cover complete resource lifecycles

### Code Quality Workflow

1. **Before Committing**:

   ```bash
   # Run linting and type checking
   make lint
   make typecheck

   # Run unit tests
   make test
   ```

2. **Pre-commit Hooks**: Automatically run formatting, linting, and basic checks

3. **CI Pipeline**: GitHub Actions run full test suite, linting, and type checking

### Development Patterns

#### Adding New Resource Types

1. **Define CRD Model**: Add Pydantic model in `app/crds.py`
2. **Create API Client**: Add GraphQL operations in `app/api/client_*.py`
3. **Implement Handler**: Create Kopf handlers in `app/handlers/handlers_*.py`
4. **Add Tests**: Unit tests in `app/*/tests/` and integration tests in `tests_integration/`
5. **Update Helm Chart**: Add CRD definition to `deploy/twingate-operator/crds/`

#### Error Handling Best Practices

- Use specific exception types from `app/api/exceptions.py`
- Return structured results using `app/handlers/base.py` helpers
- Log errors with appropriate context for debugging
- Implement retry logic for transient failures

#### API Client Development

- Follow the pattern in existing `client_*.py` files
- Use GraphQL fragments for reusable query parts
- Implement proper error handling and retries
- Add comprehensive unit tests with mocked responses

### Debugging and Troubleshooting

#### Local Debugging

```bash
make run
```

#### Common Issues

- **API Rate Limits**: Check Twingate API token permissions and rate limits
- **Resource Conflicts**: Use `kubectl describe` to check resource events and status
- **Handler Failures**: Check operator logs for detailed error messages
- **CRD Validation**: Ensure resource specs match the defined Pydantic models

### Release Process

1. **Version Bump**: Update version in `pyproject.toml`
2. **Changelog**: Update `CHANGELOG.md` with changes
3. **Testing**: Run full test suite including integration tests
4. **Docker Build**: Automated via GitHub Actions on tag push
5. **Helm Chart**: Update chart version and app version in `Chart.yaml`
