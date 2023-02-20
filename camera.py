# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from calibration import Calibrate

# Import Utilities
from Utilities.Logger import Logger

# CONSTANTS
HIGH_VALUE = 10000

# Creates the USBCamera class
class USBCamera:
    def __init__(self, camNum) -> None:
        """
        Constructor for the USBCamera class.
        @param camNumber
        """
        # Set camera properties
        self.camNum = camNum

        # Init variables
        self.width  = -1
        self.height = -1
        self.fps    = -1

        # Updates log
        Logger.logInfo("USBCamera initialized")

    def calibrateCamera(self, cap):
        """
        Calibrates the camera and returns the calibration parameters
        @return calibrationSuccessful
        @return cameraMatrix
        @return cameraDistortion
        @return rotationVectors
        @return translationVectors
        """
        # Instance creation
        self.calibrate = Calibrate(cap, self.camNum, 15)

        # Return results
        return self.calibrate.calibrateCamera()

    def autoResize(self):
        """
        Autmatically resizes the capture to a decent resolution.
        @return resizedCapture
        """
        # Creates a capture
        self.cap = cv.VideoCapture(self.camNum)

        # Set the values too high
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv.CAP_PROP_FPS, HIGH_VALUE)

        # Gets the highest value they go to
        self.width  = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps    = int(self.cap.get(cv.CAP_PROP_FPS))

        # Set the capture to be MJPG format
        self.cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

        # Prints telemetry
        print("Max Resolution:", str(self.width) + "x" + str(self.height))
        print("Max FPS:", self.fps)

        # Updates log
        Logger.logInfo("Capture resized")

        return self.cap

    def getResolution(self):
        """
        Gets the current capture resolution
        @return resolution (width, height)
        """
        return (self.width, self.height)