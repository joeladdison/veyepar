FROM mcr.microsoft.com/devcontainers/python:2-3.13-bookworm

ENV PYTHONUNBUFFERED 1

# Install dependencies for PyGObject and GStreamer
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        libgirepository1.0-dev \
        libcairo2-dev

# Setup virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install python packages
COPY setup/requirements.txt  /tmp/pip-tmp/
COPY setup/requirements_www.txt  /tmp/pip-tmp/
RUN pip install --upgrade pip \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt -r /tmp/pip-tmp/requirements_www.txt \
    && rm -rf /tmp/pip-tmp
