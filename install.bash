#!/bin/bash

echo "Building and installing MuSE"
# make a venv to build in
python3 -m venv venv
source venv/bin/activate

# install build
python3 -m pip install --upgrade pip
python3 -m pip install hatch

# build the package
python3 -m hatch build -t wheel

# exit the venv and clean up
deactivate
rm -rf venv

# install the package
python3 -m pip install dist/*.whl --break-system-packages