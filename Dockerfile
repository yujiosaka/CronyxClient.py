FROM python:3.11-slim AS base

# Set the working directory
WORKDIR /app

# Set PYTHONUNBUFFERED to ensure that
# pytest-watch can find the cronyx_client module.
ENV PYTHONPATH=/app

# Set PYTHONUNBUFFERED to ensure immediate output
# for print statements and avoid output buffering.
ENV PYTHONUNBUFFERED 1

# Set UV_SYSTEM_PYTHON to use system Python
ENV UV_SYSTEM_PYTHON 1

# Install Bun, Git, and other dependencies
RUN apt-get update && apt-get install -y curl git unzip zip && \
    curl -fsSL https://bun.sh/install | bash - && \
    ln -s $HOME/.bun/bin/bun /usr/local/bin/bun && \
    # Clean up APT when done
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv/uv /usr/local/bin/

COPY pyproject.toml uv.lock package.json bun.lockb ./

# Initialize an empty Git repository
# for preventing Husky install to fail
RUN git init

# Install Bun dependencies
RUN bun install

# Install Python dependencies
RUN uv sync --all-extras --dev && \
    uv run pre-commit install

COPY . .

CMD ["uv", "run", "ptw"]
