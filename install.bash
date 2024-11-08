#!/bin/bash

echo "Building and installing MuSE"
echo "Building MuSE"
hatch build -t wheel

if ! command -v ollama &> /dev/null
then
    echo "Ollama not found. Installing Ollama"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing Ollama for Linux"
        curl -fsSL https://ollama.com/install.sh | sh
    else
      echo "Please install Ollama manually from https://ollama.com/download"
      exit 1
    fi
fi

echo "Installing MuSE"
python3 -m pip install dist/*.whl --break-system-packages --force-reinstall
