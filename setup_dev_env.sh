#!/bin/sh
set -e

# Check if Poetry is installed
if ! command -v poetry >/dev/null 2>&1; then
  echo "Poetry is not installed. Please follow the instructions in the README to install Poetry."
  exit 1
fi

# Install Python dependencies
poetry install

# Check if Bun is installed
if ! command -v bun >/dev/null 2>&1; then
  echo "Bun is not installed. Please follow the instructions in the README to install Bun."
  exit 1
fi

# Install Bun dependencies
bun install

# Set up pre-commit
poetry run pre-commit install -t pre-commit -t commit-msg

echo "Development environment setup complete!"
