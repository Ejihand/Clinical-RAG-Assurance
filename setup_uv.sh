#!/bin/bash
# Setup script using uv tool for faster package management

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "Please restart your terminal or run: source $HOME/.cargo/env"
    exit 1
fi

echo "Creating virtual environment with uv..."
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing requirements with uv..."
uv pip install -r requirements.txt

echo "Setup complete! To activate the virtual environment, run:"
echo "  source .venv/bin/activate"

