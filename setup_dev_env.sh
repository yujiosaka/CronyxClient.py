#!/bin/sh
set -e

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Please follow the instructions in the README to install uv."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  uv venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
uv sync --all-extras --dev

# Check if Bun is installed
if ! command -v bun >/dev/null 2>&1; then
  echo "Bun is not installed. Please follow the instructions in the README to install Bun."
  exit 1
fi

# Install Bun dependencies
echo "Installing Bun dependencies..."
bun install

# Set up pre-commit
echo "Setting up pre-commit hooks..."
uv run pre-commit install -t pre-commit -t commit-msg

echo "Development environment setup complete!"
