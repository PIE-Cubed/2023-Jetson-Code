# Created by Alex Pereira

# Import Libraries
import cv2 as cv
from   pathlib import Path
from   networktables import *
from   frc_apriltags import Detector, USBCamera, BasicStreaming, CustomStreaming
from   frc_apriltags.Utilities import Logger

# Import classes
from Pipelines.cones import ConeTracking
from Pipelines.cubes import CubeTracking

# Gets the directory path
dirPath = Path(__file__).absolute().parent.__str__()
Logger.setLogPath(dirPath)

# Instance creation
cone      = ConeTracking()
cube      = CubeTracking()
detector  = Detector()

# Defines the camera resolutions (width x height)
tagCamRes = (1280, 720)
driverRes = (320, 240)

# Creates a VideoCapture and calibrates it
camera0   = USBCamera(camNum = 0, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.4:1.0-video-index0", resolution = tagCamRes, calibrate = True, dirPath = dirPath)
camMatrix = camera0.getMatrix()

# Creates a camera for the drivers
camera1 = BasicStreaming (camNum = 1, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.1:1.0-video-index0", resolution = driverRes)
camera2 = CustomStreaming(camNum = 2, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.2:1.0-video-index0", resolution = driverRes)

# Prealocate space for streams
tagStream  = camera0.prealocateSpace()
cam2Stream = camera2.prealocateSpace()

# Get a NetworkTables Instance
ntinst = NetworkTablesInstance.getDefault()

# PieceData Table
pieceData = ntinst.getTable("PieceData")
centerX   = pieceData.getEntry("CenterX")  # Double
numCones  = pieceData.getEntry("NumCones") # Double
numCubes  = pieceData.getEntry("NumCubes") # Double

def processStream(stream):
    """
    Runs OpenCV processing on a stream.

    :param stream: The stream to process.
    :return: The processed stream.
    """
    # Variables
    sentX = 1e6
    xVals = []
    boxList  = []
    cubeX, cubeBoxes = cube.findCubes(stream)
    coneX, coneBoxes = cone.findCones(stream)

    # Adds the x vaules and boxes to their respective arrays
    for x, box in zip(cubeX, cubeBoxes):
        xVals.append(x)
        boxList.append(box)
    for x, box in zip(coneX, coneBoxes):
        xVals.append(x)
        boxList.append(box)

    # Calculates the center position
    if (len(xVals) != 0):
        for x in xVals:
            tempX = x - stream.shape[1] / 2
            if (abs(tempX) < abs(sentX)):
                sentX = int(tempX)
    else:
        sentX = 0

    # Draws the boxes on the stream
    for box in boxList:
        stream = cv.drawContours(stream, [box], 0, (255, 0, 0), 3)

    # Sends all relevant data
    centerX.setDouble(x)
    numCubes.setDouble(len(cubeX))
    numCones.setDouble(len(coneX))
    stream = camera2.streamImage(stream)

    return stream

def main():
    """
    The main method for the coproceessor.
    """
    while (True):
        # Gets the tag camera's undistorted stream
        tagStream = camera0.getUndistortedStream()

        # Runs April Tag detection on the undistorted stream
        detector.detectTags(tagStream, camMatrix)

        # Gets camera2's stream
        cam2Stream = camera2.getStream()

        # Processes camera2's stream
        cam2Stream = processStream(cam2Stream)

        # Sends the stream back
        camera2.streamImage(cam2Stream)

        # Press q to end the program
        if ( camera0.getEnd() == True ):
            break

    # Exits the main function
    return

# Runs the main method
if (__name__ == "__main__"):
    main()