# Created by Alex Pereira

# Import Libraries
import cv2 as cv
import numpy as np

# Import Classes
from camera import USBCamera
from apriltags import Detector

# Instance creation
detector  = Detector()

# Creates a VideoCapture and gets its properties
camera        = USBCamera(0)
cap           = camera.autoResize()
camresolution = camera.getResolution()
ret, camMatrix, camdistortion, rvecs, tvecs = camera.calibrateCamera(cap)

# Main loop
while (cap.isOpened() == True):
    # Prealocate space for the stream
    stream = np.zeros(shape = (camresolution[0], camresolution[1], 3), dtype = np.uint8)

    # Read the capture
    sucess, stream = cap.read()

    # Undistorts the image
    stream = detector.undistort(stream, camMatrix, camdistortion, camresolution)

    # Runs April Tag detection on the undistorted image
    results, stream = detector.detectTags(stream, camMatrix, 3)

    # Display the capture
    cv.imshow("Stream", stream)

    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap.release()
        break