# Created by Alex Pereira

# Import Libraries
import math
import cv2   as cv
import numpy as np
import pupil_apriltags
from   wpilib import Timer
from   wpimath.geometry import *

# Import Classes
from communications import NetworkCommunications

# Import Utilities
from Utilities.Units  import Units
from Utilities.Logger import Logger

# The size of the tag in meters
tagSize = Units.inchesToMeters(6)

# Creates the Detector Class
class Detector:
    def __init__(self) -> None:
        """
        Constructor for the Detector class.
        """
        # Instance creation
        self.timer = Timer()
        self.comms = NetworkCommunications()

        # Creates a pupil apriltags detector
        self.detector = pupil_apriltags.Detector(families = "tag16h5", nthreads = 10, quad_decimate = 1.0, quad_sigma = 0.0, refine_edges = 2.0, decode_sharpening = 1.00)

        # Update logs
        Logger.logInfo("Detector initialized")

    def detectTags(self, stream, camera_matrix, vizualization: int = 0):
        """
        Detects AprilTags in a stream using pupil_apriltags.
        @param stream: An images generated by reading a VideoCapture
        @param camera_matrix: The camera's calibration matrix
        @param vizualization: 0 - Highlight, 1 - Highlight + Boxes, 2 - Highlight + Axes, 3 - Highlight + Boxes + Axes
        @return detectionResult, image
        """
        # If the stream is not grayscale, create a grayscale copy
        if (len(stream.shape) == 3):
            gray = cv.cvtColor(stream, cv.COLOR_BGR2GRAY)
        else:
            gray = stream

        # Define the intrinsic parameters of the camera
        intrinsic_properties = (camera_matrix[0, 0], camera_matrix[1, 1], camera_matrix[0, 2], camera_matrix[1, 2])  # fx, fy, cx, cy

        # Detect the AprilTags in the image with Pupil Apriltags
        detections = self.detector.detect(gray, estimate_tag_pose = True, camera_params = intrinsic_properties, tag_size = tagSize)

        # Variables to use in detections
        results = []
        maxError = 5e-6
        maxHamming = 0
        minConfidence = 50

        # Variables to use in sorting the data
        best = None
        minError = 1000

        # Gets current time
        time = self.timer.getFPGATimestamp()

        # Access the 3D pose of all detected tag
        for tag in detections:
            # Gets info from the tag
            decision_margin = tag.decision_margin
            hamming         = tag.hamming
            tag_num         = tag.tag_id
            center          = tag.center
            error           = tag.pose_err

            # Gets pose data from the tag
            rMatrix = tag.pose_R
            tVecs   = tag.pose_t

            # Throws out tags not present on the field
            if (1 <= tag_num <= 8):
                # Throws out noise
                if ((hamming <= maxHamming) and (error <= maxError) and (decision_margin >= minConfidence)):
                    # Creates a 3d pose array from the rotation matrix and translation vectors
                    pose = np.concatenate([rMatrix, tVecs], axis = 1)
                else:
                    # Detected tag is noise, move to next detection
                    continue
            else:
                # Detected tag is not on field, move to next detection
                continue

            # Sets detection time
            self.comms.setDetectionTimeSec(time)

            # Draws varying levels of information onto the image
            if (vizualization == 1):
                self.draw_pose_box(stream, camera_matrix, pose)
            elif (vizualization == 2):
                self.draw_pose_axes(stream, camera_matrix, pose, center)
            elif (vizualization == 3):
                self.draw_pose_box(stream, camera_matrix, pose)
                self.draw_pose_axes(stream, camera_matrix, pose, center)

            # Calculate Pose3d
            pose3d = self.getPose3D(pose)

            # Adds results to the arrays
            result = [tag_num, pose3d]
            results.append(result)

            # Determines if the current decision margin is larger than the last one and stores the corresponding data
            if (error < minError):
                minError = error
                best = result

        # Stores the best result in NetworkTables
        if (best is not None):
            self.comms.setBestResult(best)

        # Determines if there are valid targets
        if (len(results) > 0):
            self.comms.setTargetValid(True)
        else:
            self.comms.setTargetValid(False)

        return results, stream

    def getPose3D(self, poseMatrix = None):
        """
        Calculates a WPILib Pose3D from the PupilApriltags matrix
        @param poseMatrix
        @return Pose3D: Units in meters and radians
        """
        # Variables
        x, y, z = 0, 0, 0

        # Extract the tag data from the detection results
        if (poseMatrix is not None):
            # Flattens the pose array into a 1D array
            flatPose = np.array(poseMatrix).flatten()

            # Creates the Pose3D components for a tag in the AprilTags WCS
            try:
                tempRot = Rotation3d(
                    np.array([
                        [flatPose[0], flatPose[1], flatPose[2]],
                        [flatPose[4], flatPose[5], flatPose[6]],
                        [flatPose[8], flatPose[9], flatPose[10]]
                    ])
                )
            except ValueError as e:
                Logger.logError(e)
                tempRot = Rotation3d()
            tempTrans = Translation3d(flatPose[3], flatPose[7], flatPose[11])

            # Get the camera's measured X, Y, and Z
            tempX = tempTrans.Z()
            y = -tempTrans.X()
            z = -tempTrans.Y()

            # Create a Rotation3d object
            rot = Rotation3d(round(tempRot.Z(), 2), round(-tempRot.X(), 2), round(-tempRot.Y(), 2))

            # Calulates the field relative X and Y coordinate
            yTrans = Translation2d(tempX, y).rotateBy(Rotation2d(-rot.Z()))
            x = round(yTrans.X(), 2)
            y = round(yTrans.Y(), 2)

            # Calculates the field relative Z coordinate
            zTrans = Translation2d(tempX, z).rotateBy(Rotation2d(np.pi + rot.Y()))
            z = round(zTrans.Y(), 2)

            # Create a Translation3d object
            trans = Translation3d(x, y, z)

            # Creates a Pose3D object in the field WCS
            pose = Pose3d(trans, rot)

            return pose
        else:
            # Returns a blank Pose3d
            return Pose3d()

    def draw_pose_box(self, img, camera_matrix, pose, z_sign = 1):
        """
        Draws the 3d pose box around the AprilTag.
        @param img: The image to write on
        @param camera_matrix: The camera's calibration matrix
        @param pose: The 3d pose of the tag
        @param z_sign: The direction of the z-axis
        """
        # Creates object points
        opoints = np.array([
                            -1, -1, 0,
                            1, -1, 0,
                            1,  1, 0,
                            -1,  1, 0,
                            -1, -1, -2 * z_sign,
                            1, -1, -2 * z_sign,
                            1,  1, -2 * z_sign,
                            -1,  1, -2 * z_sign,
                        ]).reshape(-1, 1, 3) * 0.5 * tagSize

        # Creates edges
        edges = np.array([
                            0, 1,
                            1, 2,
                            2, 3,
                            3, 0,
                            0, 4,
                            1, 5,
                            2, 6,
                            3, 7,
                            4, 5,
                            5, 6,
                            6, 7,
                            7, 4
                        ]).reshape(-1, 2)

        # Calulcates rotation and translation vectors for each AprilTag
        rVecs, _ = cv.Rodrigues(pose[:3,:3])
        tVecs = pose[:3, 3:]

        # Derivative coefficients
        dcoeffs = np.zeros(5)

        # Calulate image points of each AprilTag
        ipoints, _ = cv.projectPoints(opoints, rVecs, tVecs, camera_matrix, dcoeffs)
        ipoints = np.round(ipoints).astype(int)
        ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

        # Draws lines between all the edges
        for i, j in edges:
            cv.line(img, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)

    def draw_pose_axes(self, img, camera_matrix, pose, center):
        """
        Draws the colored pose axes around the AprilTag.
        @param img: The image to write on
        @param camera_matrix: The camera's calibration matrix
        @param pose: The 3d pose of the tag
        @param center: The center of the AprilTag
        """
        # Calulcates rotation and translation vectors for each AprilTag
        rVecs, _ = cv.Rodrigues(pose[:3,:3])
        tVecs    = pose[:3, 3:]

        # Derivative coefficients
        dcoeffs = np.zeros(5)

        # Calculate object points of each AprilTag
        opoints = np.float32([[1, 0, 0],
                              [0, -1, 0],
                              [0, 0, -1]
                            ]).reshape(-1, 3) * tagSize

        # Calulate image points of each AprilTag
        ipoints, _ = cv.projectPoints(opoints, rVecs, tVecs, camera_matrix, dcoeffs)
        ipoints = np.round(ipoints).astype(int)

        # Calulates the center
        center = np.round(center).astype(int)
        center = tuple(center.ravel())

        # Draws the 3d pose lines
        cv.line(img, center, tuple(ipoints[0].ravel()), (0, 0, 255), 2)
        cv.line(img, center, tuple(ipoints[1].ravel()), (0, 255, 0), 2)
        cv.line(img, center, tuple(ipoints[2].ravel()), (255, 0, 0), 2)
