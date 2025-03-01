FROM python:3.13-slim-bookworm

# Define some environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    UV_FROZEN=true \
    UV_NO_SYNC=true \
    UV_COMPILE_BYTECODE=true

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Install dependencies needed to download/install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    apt-utils \
    locales

# Add support for different locales
COPY locale.gen /etc/locale.gen
RUN /usr/sbin/locale-gen

# We want to run things as a non-privileged user
ENV USERNAME=api
ENV PATH="$PATH:/home/$USERNAME/.local/bin:/home/$USERNAME/app/.venv/bin"

# Add user and set up a workdir
RUN useradd -m $USERNAME
WORKDIR /home/$USERNAME/app
RUN chown $USERNAME.$USERNAME .

# Everything below here runs as a non-privileged user
USER $USERNAME

# Install runtime dependencies (will be cached)
COPY --chown={USERNAME}:${USERNAME} pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Copy project files to container
COPY --chown=${USERNAME}:${USERNAME} . .

# Install our own package: Since we're using dynamic versioning and we don't have access
# to the git repo, we need to set the version manually via a build arg.
ARG VERSION
RUN SETUPTOOLS_SCM_PRETEND_VERSION_FOR_METEOGRAM=${VERSION} uv sync --no-dev

# Expose the port and run the app
EXPOSE 5000
CMD [ "uvicorn",  "meteogram.api:app", "--host", "0.0.0.0", "--port", "5000" ] 
