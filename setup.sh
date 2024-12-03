#!/usr/bin/bash

# install uv (pip package manager)
if ! command -v uv &> /dev/null; then
    echo "'uv' is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "'uv' is already installed."
fi

# setup venv
uv venv
source .venv/bin/activate

# install apt dependencies
sudo apt update
sudo apt upgrade
sudo apt install libkms++-dev libfmt-dev libdrm-dev # might require more...

# install pip dependencies
uv pip install -r requirements.txt

# need extra args for this one becuz they haven't updated yet :(
uv pip install rpi-libcamera -C setup-args="-Dversion=unknown"