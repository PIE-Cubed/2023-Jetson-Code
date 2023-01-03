# Created by Alex Pereira

# Import Libraries
import numpy as np
from wpimath.geometry._geometry import *
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.kinematics._kinematics import SwerveDrive4Kinematics, SwerveDrive4Odometry, SwerveModulePosition

# Import Classes
from Units import Units
from communications import NetworkCommunications

# Robot dimensions measured from the center of each wheel (inches)
ROBOT_WIDTH_IN  = 18.0
ROBOT_LENGTH_IN = 30.128

# Robot dimensions measured from the center of each wheel (meters)
ROBOT_WIDTH_M  = Units.inchesToMeters(ROBOT_WIDTH_IN)
ROBOT_LENGTH_M = Units.inchesToMeters(ROBOT_LENGTH_IN)

# Translations based off the wheel distances from the center of the robot (meters)
FL_TRANSLATION = Translation2d(-ROBOT_WIDTH_M / 2, ROBOT_LENGTH_M / 2)
RL_TRANSLATION = Translation2d(-ROBOT_WIDTH_M / 2, -ROBOT_LENGTH_M / 2)
FR_TRANSLATION = Translation2d(ROBOT_WIDTH_M / 2, ROBOT_LENGTH_M / 2)
RR_TRANSLATION = Translation2d(ROBOT_WIDTH_M / 2, -ROBOT_LENGTH_M / 2)

# Creates the swerveKinematics constant
swerveKinematics = SwerveDrive4Kinematics(
    FL_TRANSLATION,
    RL_TRANSLATION,
    FR_TRANSLATION,
    RR_TRANSLATION
)

# Creates the PoseEstimator class
class PoseEstimator:
    def __init__(self) -> None:
        """
        The constructor for the PoseEstimator class.
        """
        # Instance creation
        self.comms = NetworkCommunications()

        # Creates swerve drive obometry
        self.odometry = SwerveDrive4Odometry(
            swerveKinematics,
            Rotation2d(0),
            (SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition()),
            Pose2d(
                Translation2d(),
                Pose2d()
            )
        )

        # Creates the trust values for the data. Higher values means less trust
        stateTrust  = (0.55, 0.55, 0.55)  # x, y, and theta
        visionTrust = (0.00, 0.00, 0.00)  # x, y, and theta

        # Creates a serve drive pose estimator
        self.poseEstimator = SwerveDrive4PoseEstimator(
            swerveKinematics,
            (SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition()),
            Pose2d(
                Translation2d(),
                Pose2d()
            ),
            stateTrust,
            visionTrust
        )

    def resetPoseTrackers(self, pose: Pose2d):
        """
        Resets both pose trackers to a certian pose
        @param pose: Pose2d
        """
        self.resetOdometry()
        self.resetPoseEstimator()

    def resetOdometry(self, pose: Pose2d):
        """
        Resets the SwerveOdometry to a pose.
        @param pose: Pose2d
        """
        # Gets the module positions
        allPositiions = self.getAllModulePositions()

        # Resets the SwerveOdometry
        self.odometry.resetPosition(self.generateRot2d(), pose, allPositiions[0], allPositiions[1], allPositiions[2], allPositiions[3])

    def resetPoseEstimator(self, pose):
        """
        Resets the SwervePoseEstimator to a pose.
        @param pose: Pose2d
        """
        # Gets the module positions
        allPositiions = self.getAllModulePositions()

        # Resets the SwerveOdometry
        self.odometry.resetPosition(self.generateRot2d(), pose, allPositiions[0], allPositiions[1], allPositiions[2], allPositiions[3])

    def updatePoseTrackers(self):
        """
        Updates both pose trackers.
        """
        self.updateOdometry()
        self.updatePoseEstimator()

    def updateOdometry(self):
        """
        Updates the odometry.
        """
        # Compiles all the module positions
        allModulePosition = self.getAllModulePositions()

        # Updates odometry
        self.odometry.update(
            self.generateRot2d( self.getHeading() ),
            allModulePosition)

    def updatePoseEstimator(self):
        """
        Updates the poseEstimator
        """
        # Compiles all the module positions
        allModulePosition = self.getAllModulePositions()

        # Updates the pose estimator
        self.poseEstimator.update(
            self.generateRot2d( self.getHeading() ),
            allModulePosition)

        # Gets current values
        detPose = self.getBestResult()
        detTime = self.comms.getTimeSec()

        # Adds the vision measurement if it hasn't been calculated yet
        if ((self.prevTime != detTime) & (self.prevPose != detPose)):
            # Sets the prev variables
            self.prevTime = detTime
            self.prevPose = detPose

            # Adds the vision measurement
            self.poseEstimator.addVisionMeasurement(
                detPose.toPose2d(),
                detTime)

    def getAllModulePositions(self):
        """
        Gets all the swerve module positions.
        @return 
        """
        # Creates an array of zeros with a length of 4
        allPositions = [0] * 4

        # Sets all the positions acordingly
        allPositions[0] = self.comms.getFLPosition()
        allPositions[1] = self.comms.getRLPosition()
        allPositions[2] = self.comms.getFRPosition()
        allPositions[3] = self.comms.getRRPosition()

        return allPositions

    def getBestResult(self, results):
        """
        @return
        """
        # Variables
        i = 0
        bestResult = 0
        minError = 100

        # Loops through all Data
        for result in results:
            error = result[0]

            if (error < minError):
                error = minError
                bestResult = i

            # Increment i
            i += 1

        # Extracts Pose Data
        flatPose = np.array(results[bestResult][2]).flatten()

        # Extracts Euler's Angles
        flatAngles = np.array(results[bestResult[3]]).flatten()

        # Extracts the x, y, and z translations
        x, y, z = flatPose[3], flatPose[7], flatPose[11]

        # Extracts the tag's roll, yaw, and pitch
        pitch, yaw, roll = flatAngles[3], flatAngles[7], flatAngles[11]

        return Pose3d(Transform3d(x, y, z), Rotation3d(roll, pitch, yaw))

    def getHeading(self):
        """
        @return
        """
        return self.comms.getGyroYaw()

    def generateRot2d(self, degrees):
        """
        @return
        """
        return Rotation2d(Units.radiansToDegrees(degrees))