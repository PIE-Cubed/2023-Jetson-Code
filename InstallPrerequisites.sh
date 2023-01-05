#!/bin/sh

# Get system updates
sudo apt-get update

# Install system updates
sudo apt-get -y upgrade

# Install python 3.10 if it is not already install
sudo apt-get install -y python3.10

# Install python3-pip, cmake, ninja, and opencv (c++)
sudo apt-get install -y git python3-pip cmake ninja-build libopencv-dev

# Install all needed pip libraries
pip install opencv-contrib-python robotpy transforms3d dt-apriltags

# Installs all submodules of robot py
pip install robotpy[all]

# Install camera server
robotpy_installer install robotpy-cscore

# Back out to the home directory
cd

# Clone the AprilTags library
git clone https://www.github.com/AprilRobotics/apriltag

# Enter the apriltag directory
cd apriltag

# Make the build files
cmake -DCMAKE_BUILD_TYPE=Release -G Ninja .

# Build the library
ninja

# Install the library
sudo ninja install

# Restart terminal
sudo ldconfig