#!/bin/sh

# Back out to the home directory
cd

# Get system updates
sudo apt-get update

# Install system updates
sudo apt-get -y upgrade

# Install python 3.10 if it is not already install
sudo apt-get install -y python3.10

# Install git, python3-pip, cmake, ninja, and opencv (c++)
sudo apt-get install -y git python3-pip cmake ninja-build libopencv-dev

# Install all needed pip libraries
pip install opencv-contrib-python robotpy transforms3d dt-apriltags

# Installs all submodules of robot py
# pip install robotpy[all]

# Installs the camera server
robotpy_installer install robotpy-cscore

# Move to the documents directory
cd Documents

# Clone the Jetson Code
git clone https://github.com/PIE-Cubed/2023-Jetson-Code

# Back out to the home directory
cd

# Clone the AprilTags repository
git clone https://www.github.com/AprilRobotics/apriltag

# Moves to the apriltag directory
cd apriltag

# Make the build files
cmake -DCMAKE_BUILD_TYPE=Release -G Ninja .

# Build the library
ninja

# Install the library
sudo ninja install

# Restart terminal
sudo ldconfig