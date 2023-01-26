# Created by Alex Pereira

# Import Libraries
import cv2 as cv
from wpimath.geometry import Pose2d

# Import Classes
from camera import USBCamera
from apriltags import Detector
from pose_estimation import PoseEstimator

# Import Utilities
from Utilities.Units import Units
from Utilities.Logger import Logger

# Instance creation
detector  = Detector()
robotPose = PoseEstimator()

# Creates a VideoCapture and gets its properties
camera        = USBCamera(0)
cap           = camera.autoResize()
camresolution = camera.getResolution()
ret, camMatrix, camdistortion, rvecs, tvecs = camera.calibrateCamera(cap)

# Variables
autoPath = None
prevPath = None

startPos = Pose2d(
    Units.inchesToMeters(63.5),
    Units.inchesToMeters(22),
    Units.degreesToRadians(90)
)

# Main loop
while (cap.isOpened() == True):
    # Resets the starting position once the auto path is selected
    if ((autoPath is not None) and (prevPath != autoPath)):
        prevPath = autoPath

        if (autoPath == ""):
            robotPose.resetPoseTrackers(startPos)

    # Update the pose trackers
    robotPose.updatePoseTrackers()

    # Read the capture
    sucess, stream = cap.read()

    # Undistorts the image
    stream = detector.undistort(stream, camMatrix, camdistortion, camresolution)

    # Runs April Tag detection on the undistorted image
    results, stream = detector.detectTags(stream, camMatrix, 3)

    # Determine Pose2d based on vision measurements
    floorPose = robotPose.getVisionPose()

    # Extract the pose values (meters and radians)
    Logger.logDebug("X: {}, Y: {}, Yaw: {}".format(floorPose.x_feet, floorPose.y_feet, floorPose.rotation().degrees()))

    # Display the capture
    cv.imshow("Stream", stream)

    # Press q to end the program
    if ( cv.waitKey(1) == ord("q") ):
        print("Process Ended by User")
        cv.destroyAllWindows()
        cap.release()
        break