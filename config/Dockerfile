FROM python:3.12-slim AS base

ARG UID=1000
ARG GID=1000
ARG USERNAME=vscode

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    curl \
    git \
    libpq-dev \
    openssh-client \
    postgresql-client \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN if ! getent group "${GID}" >/dev/null; then groupadd --gid "${GID}" "${USERNAME}"; fi \
    && if ! id -u "${UID}" >/dev/null 2>&1; then useradd --uid "${UID}" --gid "${GID}" -m -s /bin/bash "${USERNAME}"; fi \
    && mkdir -p /workspace \
    && chown -R "${UID}:${GID}" /workspace \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

WORKDIR /workspace

FROM base AS development

COPY config/requirements.txt /tmp/requirements.txt
RUN python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV/bin/pip" install --upgrade pip \
    && "$VIRTUAL_ENV/bin/pip" install -r /tmp/requirements.txt

EXPOSE 8000

FROM base AS production

COPY config/requirements.txt /tmp/requirements.txt
RUN python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV/bin/pip" install --upgrade pip \
    && "$VIRTUAL_ENV/bin/pip" install -r /tmp/requirements.txt \
    && "$VIRTUAL_ENV/bin/pip" install gunicorn

COPY src /workspace/src

EXPOSE 8000
