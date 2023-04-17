# Created by Alex Pereira

# Import Libraries
import cv2 as cv
from   pathlib import Path
from   networktables import *
from   frc_apriltags import Detector, USBCamera, Streaming
from   frc_apriltags.Utilities import Logger

# Import Classes
from pipelines import ConeTracking, CubeTracking

# Import Methods
from frc_apriltags import startNetworkComms

# Starts the network communications
startNetworkComms(2199)

# Gets the directory path
dirPath = Path(__file__).absolute().parent.__str__()
Logger.setLogPath(dirPath)

# Instance creation
cone     = ConeTracking()
cube     = CubeTracking()
detector = Detector()

# Defines the camera resolutions (width x height)
driverRes = (320, 240)
tagCamRes = (1280, 720)

# Creates a USBCamera and calibrates it
#camera0   = USBCamera(camNum = 0, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.4:1.0-video-index0", resolution = tagCamRes, calibrate = True, dirPath = dirPath)
#camMatrix = camera0.getMatrix()

# Creates cameras for the drivers
camera2 = Streaming(camNum = 2, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.1:1.0-video-index0", resolution = driverRes)
camera1 = Streaming(camNum = 1, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.2:1.0-video-index0", resolution = driverRes)

# Prealocate space for streams
#cam1Stream = camera1.prealocateSpace()
cam2Stream = camera2.prealocateSpace()

# Get a NetworkTables Instance
ntinst = NetworkTablesInstance.getDefault()

# PieceData Table
pieceData = ntinst.getTable("PieceData")
width     = pieceData.getEntry("Width")    # Double
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
    sentX, maxArea = 0, 0
    xVals, areas, boxList, pieces = [], [], [], []
    cubeBoxes, cubeAreas = cube.findCubes(stream)
    coneBoxes, coneAreas = cone.findCones(stream)

    # Adds the x vaules and boxes to their respective arrays
    if (len(cubeBoxes) != 0 and len(cubeAreas)):
        for box, area in zip(cubeBoxes, cubeAreas):
            xVals  .append(box[0] + box[2]/2)
            areas  .append(area)
            pieces .append(0)
            boxList.append(box)
    if (len(coneBoxes) != 0 and len(coneAreas)):
        for box, area in zip(coneBoxes, coneAreas):
            xVals  .append(box[0] + box[2]/2)
            areas  .append(area)
            pieces .append(1)
            boxList.append(box)

    # Calculates the center position
    if (len(xVals) != 0 and len(areas) != 0):
        for x, area in zip(xVals, areas):
            tempX = x - (stream.shape[1] / 2)
            if (area >= maxArea):
                sentX = int(tempX)
    else:
        sentX = 0

    # Draws the boxes on the stream
    if (len(boxList) != 0 and len(pieces) != 0):
        for box, piece in zip(boxList, pieces):
            x, y, w, h = box[0], box[1], box[2], box[3]
            if (piece == 0):
                stream = cv.rectangle(stream, (x, y), (x + w, y + h), (255, 0, 0), 2)
            elif (piece == 1):
                stream = cv.rectangle(stream, (x, y), (x + w, y + h), (0, 255, 255), 2)

    # Sends all relevant data
    width   .setDouble(stream.shape[1])
    centerX .setDouble(sentX)
    numCubes.setDouble(len(cubeBoxes))
    numCones.setDouble(len(coneBoxes))
    stream = camera2.streamImage(stream)

    return stream

def main():
    """
    The main method for the coproceessor.
    """
    while (True):
        # Gets the tag camera's undistorted stream
        #cam0Stream = camera0.getUndistortedStream()

        # Runs April Tag detection on the undistorted stream
        #detector.detectTags(cam0Stream, camMatrix)

        # Gets camera2's stream
        cam2Stream = camera2.getStream()

        # Processes camera2's stream
        processStream(cam2Stream)

        # Press q to end the program
        #if ( camera0.getEnd() == True ):
        #    break
        cv.waitKey(1)

    # Exits the main function
    return

# Runs the main method
if (__name__ == "__main__"):
    main()