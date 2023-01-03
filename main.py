# Created by Alex Pereira

# Import Libraries
import cv2 as cv

# Import Classes
from camera import USBCamera
from apriltags import Detector
from communications import NetworkCommunications

# Instance creation
nComms   = NetworkCommunications()
detector = Detector(nComms)

# Creates a VideoCapture and gets its properties
camera        = USBCamera(0)
cap           = camera.autoResize()
camresolution = camera.getResolution()
ret, camMatrix, camdistortion, rvecs, tvecs = camera.calibrateCamera(cap)

# Main loop
while (cap.isOpened() == True):
    # Read the capture
    sucess, stream = cap.read()
 
    # Flips the image
    cv.flip(stream, 1)

    # Undistorts the image
    stream = detector.undistort(camMatrix, camdistortion, camresolution)

    # Runs apriltag detection on the undistorted image
    results, stream = detector.detectTags(stream, camMatrix, 2, 1, False)

    # Display the capture
    cv.imshow("Stream", stream)
 
    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap.release()
        break