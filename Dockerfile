ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim AS base

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    VIRTUAL_ENV=/opt/.venv \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN echo "CACHE_BUSTER=1693774919" && apt-get update && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

FROM base as builder
WORKDIR /build

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*


### pip -- https://pip.pypa.io/en/stable/cli/pip/
# Allow pip to only run in a virtual environment
ENV PIP_REQUIRE_VIRTUALENV=1 \
    PIP_VERBOSE=3 \
    PIP_NO_INPUT=1 \
    PIP_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ### Poetry
    POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR=$POETRY_HOME/.cache/pypoetry \
    PATH="$POETRY_HOME/bin:$PATH"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python -

COPY poetry.lock pyproject.toml ./

# Install Python dependencies
RUN python -m venv "$VIRTUAL_ENV" && \
    poetry install --only main --sync --no-root --compile -n -vvv

COPY . .

FROM base as prod
ARG ENV=prod
WORKDIR /app

# Create a group and user to run our app
ENV APP_USER=appuser
RUN groupadd --gid 1000 -r ${APP_USER} && \
    useradd --uid 1000 -r -g ${APP_USER} ${APP_USER}

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY . .

CMD ["kopf", "run", "./main.py", "-A", "--verbose", "--liveness=http://127.0.0.1:8080/healthz"]
