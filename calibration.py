# Created by Alex Pereira

# Import Libraries
import os
import glob
import cv2   as cv
import numpy as np

# Defining the dimensions of CHESSBOARD
CHESSBOARD = (8, 8)  # Number of sqares (width x height)

# Default termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creates the Calibrate class
class Calibrate:
    def __init__(self, cap, camNum: int) -> None:
        """
        Constructor for the Calibrate class.
        @param VideoCapture
        @param Camera Number
        """
        # Localizes parameters
        self.cap    = cap
        self.camNum = camNum

        # Get height and width
        self.width  = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # Prepare object points
        self.objp = np.zeros((1, CHESSBOARD[0] * CHESSBOARD[1], 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)

        # Arrays to store object and image points from all images
        self.objPoints = []  # 3D point in real world
        self.imgPoints = []  # 2D point in image plane

        # Path to calibration images
        self.PATH = "./camera{}-{}x{}-images/".format(self.camNum, self.width, self.height)

        # File extension
        self.EXTENSION = ".png"

    def calibrateCamera(self):
        """
        Calibrates the given camera at a certain resolution
        @return calibrationSuccessful
        @return cameraMatrix
        @return cameraDistortion
        @return rotationVectors
        @return translationVectors
        """
        # Checks if reference images exist
        refExists = self.getPathExistance()

        # If reference images for this resolution do not exist or are corrupt, create them
        if (refExists == True):
            pass
        else:
            self.createCalibrationImages()

        # Gets the path for all the images saved for this camera at a certain resolution
        images = glob.glob(self.PATH + "*" + self.EXTENSION)

        # Loops through stored images
        for image in images:
            # Reads the created images
            img = cv.imread(image)

            # Converts images to grayscale
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Finds chess board corners. ret is true only if the desired number of corners are found
            ret, corners = cv.findChessboardCorners(gray, CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

            # Desired number of corners found, add object and image points after refining them
            if ret == True:
                # Adds the objectpoint
                self.objPoints.append(self.objp)

                # Refining pixel coordinates for given 2d points.
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

                # Adds image point
                self.imgPoints.append(corners2)

                # Draw the corners onto the image
                img = cv.drawChessboardCorners(img, CHESSBOARD, corners2, ret)

            # Display the image and wait for one second
            cv.imshow("img", img)
            cv.waitKey(1000)

        # Destroys all cached windows
        cv.destroyAllWindows()

        # Calibrate the camera by passing the value of known 3D points (objPoints) and corresponding pixel coordinates of the detected corners (imgPoints)
        self.ret, self.cameraMatrix, self.distortion, self.rvecs, self.tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, gray.shape[::-1], None, None)

        # Print calibration reults
        print("Camera {} calibrated: ".format(self.camNum), self.ret)
        print("\nCamera Matrix:\n", self.cameraMatrix)
        print("\nDistortion Parameters:\n", self.distortion)
        print("\Rotation Vectors:\n", self.rvecs)
        print("\nTranslation Vectors:\n", self.tvecs)

        # Prints the reprediction error
        repredictError = self.calculateRepredictionError()
        print("\nCamera {} Total error: {}".format(self.camNum, repredictError) )

        # Return calibration results
        return self.ret, self.cameraMatrix, self.distortion, self.rvecs, self.tvecs

    def createCalibrationImages(self):
        """
        Creates 15 images to calibrate the camera from
        """
        # Variables
        imgSelected = False
 
        # Create
        for i in range(0, 15):
            # Seperates the enumeration from the naming
            j = i + 1

            # Prints target image
            print("Attempting to take calibration image {}".format(j))

            # Resets imgSelected
            imgSelected = False

            # Runs until the user presses p to take a picture
            while (imgSelected == False):
                # Read the capture
                sucess, stream = self.cap.read()
            
                # Flips the image
                cv.flip(stream, 1)

                # Converts images to grayscale
                gray = cv.cvtColor(stream, cv.COLOR_BGR2GRAY)

                # Finds chess board corners. ret is true if the desired number of corners are found
                ret, corners = cv.findChessboardCorners(gray, CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

                # Draws the chessboard pattern onto the stream
                if ret == True:
                    # Refining pixel coordinates for given 2d points.
                    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

                    # Draw the corners onto the stream
                    stream = cv.drawChessboardCorners(stream, CHESSBOARD, corners2, ret)
            
                # Display the capture
                cv.imshow("Callibration", stream)
            
                # Press p to take a calibration image
                if ( cv.waitKey(1) == ord("p") ):
                    # Writes the image
                    cv.imwrite(self.PATH + "{}".format(j) + self.EXTENSION, stream)

                    # Prints the status
                    print("Calibration image {} taken".format(j))

                    # Breaks the while loop
                    imgSelected = True
                    break

        # Destroys all windows
        cv.destroyAllWindows()

    def getPathExistance(self) -> bool:
        """
        Gets the existance of a directory at self.PATH
        @return isDirectoryThere
        """
        # Variables
        img = None
        pathExists = False

        # Attempts to make a directory at self.PATH
        try:
            os.mkdir(self.PATH)
        except:
            pass

        # Attempts to read the last callibration image and updates variables accordingly
        img = cv.imread(self.PATH + "15" + self.EXTENSION)

        if img is not None:
            pathExists = True
            print("Path already exists")
        else:
            pathExists = False
            print("Path does not exist")
 
        return pathExists

    def calculateRepredictionError(self):
        """
        Calulates the reprediction error
        """
        # Reprediction error
        mean_error = 0

        # Loops through object points
        for i in range(len(self.objPoints)):
            imgPoints2, _ = cv.projectPoints(self.objPoints[i], self.rvecs[i], self.tvecs[i], self.cameraMatrix, self.distortion)
            error = cv.norm(self.imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
            mean_error += error

        # Prints the total error
        return mean_error / len(self.objPoints)