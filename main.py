# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from camera import USBCamera
from apriltags import Detector

# Instance creation
detector = Detector()

# Create VideoCapture 0 and get its properties
camera0        = USBCamera(0)
cap0           = camera0.autoResize()
cam0resolution = camera0.getResolution()
ret, cam0Matrix, cam0distortion, rvecs, tvecs = camera0.calibrateCamera(cap0)

def undistort(stream, cameraMatrix, distortion, resolution: tuple):
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

# Main loop
while (cap0.isOpened() == True):
    # Read the capture
    sucess, stream = cap0.read()
 
    # Flips the image
    cv.flip(stream, 1)

    # Undistorts the image
    stream = undistort(cam0Matrix, cam0distortion, cam0resolution)

    # Runs apriltag detection on the image
    results, stream = detector.dtDetectTags(stream, cam0Matrix, 3, 1, False)

    # Display the capture
    cv.imshow("Stream", stream)
 
    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap0.release()
        break