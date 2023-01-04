# Created by Alex Pereira

# Import Libraries
import glob
import cv2   as cv
import numpy as np

# Defining the dimensions of CHESSBOARD
CHESSBOARD = (8, 8)  # Number of sqares (width x height)

# Default termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Create capture
camNum = 0
cap = cv.VideoCapture(camNum)

# Set the values too high
HIGH_VALUE = 9000
cap.set(cv.CAP_PROP_FRAME_WIDTH, HIGH_VALUE)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, HIGH_VALUE)
cap.set(cv.CAP_PROP_FPS, HIGH_VALUE)

# Get height and width
width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# Prepare object points
objp = np.zeros((1, CHESSBOARD[0] * CHESSBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)

# Arrays to store object and image points from all images
objPoints = []  # 3D point in real world
imgPoints = []  # 2D point in image plane

# Path to calibration images
PATH = "./camera{}-{}x{}-images/".format(camNum, width, height)

# File extension
EXTENSION = ".png"

# Gets the path for all the images saved for this camera at a certain resolution
images = glob.glob(PATH + "*" + EXTENSION)

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
        objPoints.append(objp)

        # Refining pixel coordinates for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Adds image point
        imgPoints.append(corners2)

        # Draw the corners onto the image
        img = cv.drawChessboardCorners(img, CHESSBOARD, corners2, ret)

        # Display the image and wait for one second
        cv.imshow("img", img)
        cv.waitKey(1000)

# Destroys all cached windows
cv.destroyAllWindows()

# Calibrate the camera by passing the value of known 3D points (objPoints) and corresponding pixel coordinates of the detected corners (imgPoints)
ret, cameraMatrix, distortion, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

# Print calibration reults
print("Camera {} calibrated: ".format(camNum), ret)
print("\nCamera Matrix:\n", cameraMatrix)
print("\nDistortion Parameters:\n", distortion)
print("\Rotation Vectors:\n", rvecs)
print("\nTranslation Vectors:\n", tvecs)
        
# Reprediction error
mean_error = 0

# Loops through object points
for i in range(len(objPoints)):
    imgPoints2, _ = cv.projectPoints(objPoints[i], rvecs[i], tvecs[i], cameraMatrix, distortion)
    error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
    mean_error += error

# Prints the total error
print( mean_error / len(objPoints))