# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from calibration import Calibrate

# Import Utilities
from Utilities.Logger import Logger

# Creates the USBCamera class
class USBCamera:
    def __init__(self, camNum: int, path: str = None) -> None:
        """
        Constructor for the USBCamera class.
        @param camNumber
        @param path: It can be found on Linux by running "find /dev/v4l"
        """
        # Set camera properties
        self.camNum = camNum

        # Init variables
        self.width  = -1
        self.height = -1
        self.fps    = -1

        # Creates a capture
        if (path is not None):
            # If path is known, use the path
            self.cap = cv.VideoCapture(path)
        else:
            # Path is unknown, use the camera number
            self.cap = cv.VideoCapture(self.camNum)

        # Updates log
        Logger.logInfo("USBCamera initialized")

    def resize(self, cameraRes: tuple):
        """
        Resizes the capture to a given resolution. If the specified resolution is too high, resizes to the highest resolution possible.
        @param Camera Resolution
        @return resizedCapture
        """
        # CONSTANTS
        HIGH_VALUE = 10000

        # Set the values
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cameraRes[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cameraRes[1])
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

    def undistort(self, stream, cameraMatrix, distortion, resolution: tuple):
        """
        Undistorts an image using cv.undistort()
        @param stream
        @param cameraMatrix
        @param cameraDistortion
        @param cameraResolution (width, height)
        @return undistortedStream
        """
        # Creates a cameraMatrix
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distortion, resolution, 1, resolution)

        # Undistorts the image
        undistortedStream = cv.undistort(stream, cameraMatrix, distortion, None, newCameraMatrix)

        # Crops the image
        x, y, w, h = roi
        undistortedStream = undistortedStream[y:y+h, x:x+w]

        return undistortedStream

    def rectify(self, stream, cameraMatrix, distortion, resolution: tuple):
        """
        Undistorts an image using cv.remap()
        @param stream
        @param cameraMatrix
        @param cameraDistortion
        @param cameraResolution (width, height)
        @return undistortedStream
        """
        # Creates a cameraMatrix
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distortion, resolution, 1, resolution)

        # Unpacks the ROI data
        x, y, w, h = roi

        # Undistorts the image
        mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, distortion, None, newCameraMatrix, (w,h), 5)
        undistortedStream = cv.remap(stream, mapx, mapy, cv.INTER_LINEAR)

        # Crop the image
        undistortedStream = undistortedStream[y:y+h, x:x+w]

        return undistortedStream

    def calibrateCamera(self):
        """
        Calibrates the camera and returns the calibration parameters
        @return calibrationSuccessful
        @return cameraMatrix
        @return cameraDistortion
        @return rotationVectors
        @return translationVectors
        """
        # Instance creation
        self.calibrate = Calibrate(self.cap, self.camNum, 15)

        # Return results
        return self.calibrate.calibrateCamera()

    def getResolution(self):
        """
        Gets the current capture resolution
        @return resolution (width, height)
        """
        return (self.width, self.height)