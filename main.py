# Created by Alex Pereira

# Import Libraries
import cv2 as cv
import numpy as np

# Import Classes
from camera    import USBCamera
from apriltags import Detector

#
from frc_apriltags import BasicStreaming

# Instance creation
detector  = Detector()

# Defines the camera resolutions (width x height)
cameraRes = (1280, 720)
driverRes = (320, 240)

# Creates a VideoCapture and calibrates it
camera    = USBCamera(camNum = 0, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.4:1.0-video-index0")
cap       = camera.resize(cameraRes)
cameraRes = camera.getResolution()
ret, camMatrix, camdistortion, rvecs, tvecs = camera.calibrateCamera()

# Creates a camera for the drivers
driverCam1 = BasicStreaming(camNum = 1, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.1:1.0-video-index0", resolution = driverRes)
driverCam2 = BasicStreaming(camNum = 2, path = "/dev/v4l/by-path/platform-70090000.xusb-usb-0:2.2:1.0-video-index0", resolution = driverRes)

# Prealocate space for stream
stream = np.zeros(shape = (cameraRes[1], cameraRes[0], 3), dtype = np.uint8)

# Main loop
while (cap.isOpened() == True):
    # Reads the capture
    sucess, stream = cap.read()

    # Undistorts the image
    stream = camera.rectify(stream, camMatrix, camdistortion, cameraRes)

    # Runs April Tag detection on the undistorted image
    results, stream = detector.detectTags(stream, camMatrix, 3)

    # Displays the capture
    # cv.imshow("Stream", stream)

    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap.release()
        break
