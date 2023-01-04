#!/bin/sh

# Get system updates
sudo apt-get update

# Install system updates
sudo apt-get -y upgrade

# Install python 3.10 if it is not already install
sudo apt-get install -y python3.10

# Install python3-pip, cmake, ninja, and opencv (c++)
sudo apt-get install -y git python3-pip cmake ninja-build libopencv-dev