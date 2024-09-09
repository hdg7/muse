#!/bin/bash

echo "Building and installing MuSE"
echo "Building MuSE"
hatch build -t wheel

echo "Installing MuSE"
python3 -m pip install dist/*.whl --break-system-packages