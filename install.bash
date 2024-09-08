#!/bin/bash

echo "Building and installing MuSE"
# make a venv to build in
python3 -m venv venv
source venv/bin/activate

# install build
python3 -m pip install --upgrade pip
python3 -m pip install build

# build the package
python3 -m build

# exit the venv and clean up
deactivate
rm -rf venv

# install the package
python3 -m pip install dist/*.whl --break-system-packages

python3 -m pip install -r requirements.txt --break-system-packages
