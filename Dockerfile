ARG PYTHON_VERSION=3.11-slim
ARG APP_PATH=/opt/pablog-service
ARG USER=pablog
ARG GROUP=pablog

FROM python:${PYTHON_VERSION} as base

ARG APP_PATH

ENV POETRY_VERSION=1.4.2 \
  POETRY_HOME="/usr/local" \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    # dependencies for building Python packages \
    build-essential \
    # install poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_PATH}

COPY pyproject.toml poetry.lock ./

RUN touch README.md

RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR


FROM python:${PYTHON_VERSION} as prod

ARG APP_PATH
ARG USER
ARG GROUP

RUN apt-get update && apt-get install --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r ${GROUP} \
  && useradd -d ${APP_PATH} -r -g ${GROUP} ${USER}

RUN mkdir /var/run/pablog-service \
  && touch /var/run/pablog-service/pablog.pid \
  && chown -R ${USER}:${GROUP} /var/run/pablog-service

USER ${USER}

WORKDIR ${APP_PATH}

RUN chown -R ${USER}:${GROUP} ${APP_PATH}

ENV VIRTUAL_ENV=${APP_PATH}/.venv \
    PATH="${APP_PATH}/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=base --chown=${USER}:${GROUP} ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=${USER}:${GROUP} entrypoint.sh VERSION ./

COPY --chown=${USER}:${GROUP} pablog_api ./pablog_api

ENTRYPOINT ["./entrypoint.sh"]

CMD ["server"]
