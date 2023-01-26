# Created by Alex Pereira

# Import Libraries
from typing import Sequence
from wpimath.geometry import *
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.kinematics import SwerveDrive4Kinematics, SwerveDrive4Odometry, SwerveModulePosition

# Import Classes
from communications import NetworkCommunications

# Import Utilities
from Utilities.Units import Units
from Utilities.Logger import Logger
from Utilities.AprilTag import AprilTag
from Utilities.AprilTagFieldLayout import AprilTagFieldLayout

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

# Dimensions of the field (feet)
FIELD_LENGTH_FT = (144 + 66 + 12) / 12
FIELD_WIDTH_FT  = 144 / 12

# Dimensions of the field (meters)
FIELD_LENGTH_M = Units.feetToMeters(FIELD_LENGTH_FT)
FIELD_WIDTH_M  = Units.feetToMeters(FIELD_WIDTH_FT)

# Dimensions of the camera to robot transform (feet)
X_OFFSET_FT = 0
Y_OFFSET_FT = 0
Z_OFFSET_FT = 0

# Dimensions of the camera to robot transform (meters)
X_OFFSET_M = Units.feetToMeters(X_OFFSET_FT)
Y_OFFSET_M = Units.feetToMeters(Y_OFFSET_FT)
Z_OFFSET_M = Units.feetToMeters(Z_OFFSET_FT)

# Defines the camera to robot transform
CAMERA_TO_ROBOT = Transform3d(
    Translation3d(X_OFFSET_M, Y_OFFSET_M, Z_OFFSET_M),
    Rotation3d(0, 0, 0)
)

# Creates the PoseEstimator class
class PoseEstimator:
    def __init__(self) -> None:
        """
        The constructor for the PoseEstimator class.
        """
        # Instance creation
        self.comms = NetworkCommunications()

        # Stores the camera offset
        self.comms.setCamOffset(CAMERA_TO_ROBOT)

        # Creates swerve drive obometry
        self.odometry = SwerveDrive4Odometry(
            swerveKinematics,
            Rotation2d(0),
            (SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition()),
            Pose2d(
                Translation2d(),
                Rotation2d()
            )
        )

        # Creates the trust values for the data. Higher values means less trust
        stateTrust  = (10.00, 10.00, 10.00)  # x, y, and theta
        visionTrust = (0.00, 0.00, 0.00)  # x, y, and theta

        # Creates a serve drive pose estimator
        self.poseEstimator = SwerveDrive4PoseEstimator(
            swerveKinematics,
            Rotation2d(),
            (SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition(), SwerveModulePosition()),
            Pose2d(
                Translation2d(),
                Rotation2d()
            ),
            stateTrust,
            visionTrust
        )

        # Creates all known AprilTags and creates a field
        allTags    = self.createAllTags()
        self.field = AprilTagFieldLayout(allTags, FIELD_LENGTH_M, FIELD_WIDTH_M, False)

        # Creates the field
        # self.field = AprilTagFieldLayout(False)  # Uncomment for match play

        # Variables
        self.prevTime = 0
        self.prevPose = Pose3d()

        # Updates log
        Logger.logInfo("PoseEstimator initialized")

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
            allModulePosition[0],
            allModulePosition[1],
            allModulePosition[2],
            allModulePosition[3]
        )

    def updatePoseEstimator(self):
        """
        Updates the poseEstimator
        """
        # Compiles all the module positions
        allModulePosition = self.getAllModulePositions()

        # Updates the pose estimator
        self.poseEstimator.update(
            self.generateRot2d( self.getHeading() ),
            allModulePosition
        )

        # Gets current values
        tv = self.comms.getTargetValid()
        id = self.comms.getBestResultId()
        detPose = self.comms.getBestResult()
        detTime = self.comms.getDetectionTime()

        # Adds the vision measurement if it hasn't been calculated yet
        if ((self.prevTime != detTime) and (self.prevPose != detPose) and (tv == True)):
            # Sets the prev variables
            self.prevTime = detTime
            self.prevPose = detPose

            # Adds the vision measurement if the tag id is valid
            if ((id != -1) and (0 < id <= 8)):
                # Gets the target's pose on the field
                targetPose = self.field.getTagPose(id)

                # Extracts the x, y, and z distances
                x, y, z = detPose.X(), detPose.Y(), detPose.Z()

                # Extracts the roll, pitch, and yaw angles
                roll, pitch, yaw = detPose.rotation().X(), detPose.rotation().Y(), detPose.rotation().Z()

                # Creates the relative pose
                camToTarget = Transform3d(
                    Translation3d(x, y, z),
                    Rotation3d(roll, pitch, yaw)
                )

                # Gets the camera's pose relative to the tag
                camPose = targetPose.transformBy(camToTarget.inverse())

                # Tranforms the camera's pose to the robot's center
                measurement = camPose.transformBy(CAMERA_TO_ROBOT.inverse())

                #Logger.logDebug("X: {}, Y: {}, Z: {}".format(camToTarget.translation().x_feet, camToTarget.translation().y_feet, camToTarget.translation().z_feet))

                # Adds the vision measurement
                self.poseEstimator.addVisionMeasurement(
                    measurement.toPose2d(),
                    detTime
                )

    def resetPoseTrackers(self, pose: Pose2d):
        """
        Resets both pose trackers to a certian pose
        @param pose: A Pose2d that specifies location on the field
        """
        self.resetOdometry(pose)
        self.resetPoseEstimator(pose)

    def resetOdometry(self, pose: Pose2d):
        """
        Resets the SwerveOdometry to a pose.
        @param pose: A Pose2d that specifies location on the field
        """
        # Gets the module positions
        allPositiions = self.getAllModulePositions()

        # Resets the SwerveOdometry
        self.odometry.resetPosition(
            pose.rotation(),
            pose,
            allPositiions[0],
            allPositiions[1],
            allPositiions[2],
            allPositiions[3]
        )

    def resetPoseEstimator(self, pose: Pose2d):
        """
        Resets the SwervePoseEstimator to a pose.
        @param pose: A Pose2d that specifies location on the field
        """
        # Gets the module positions
        allPositiions = self.getAllModulePositions()

        # Resets the SwerveOdometry
        self.poseEstimator.resetPosition(
            pose.rotation(),
            (allPositiions[0], allPositiions[1], allPositiions[2], allPositiions[3]),
            pose
        )

    def getOdometryPose(self) -> Pose2d:
        """
        Gets the Pose2d using the motor encoders
        @return odometryPoseEstimate
        """
        return self.odometry.getPose()

    def getVisionPose(self) -> Pose2d:
        """
        Gets the Pose2d using the odometry and the April Tags.
        @return visionPoseEstimate
        """
        return self.poseEstimator.getEstimatedPosition()

    def getAllModulePositions(self) -> Sequence[SwerveModulePosition]:
        """
        Gets all the swerve module positions.
        @return allSwerveModulePositions
        """
        # Creates an array of zeros with a length of 4
        allPositions = [0] * 4

        # Sets all the positions acordingly
        allPositions[0] = self.comms.getFLPosition()
        allPositions[1] = self.comms.getRLPosition()
        allPositions[2] = self.comms.getFRPosition()
        allPositions[3] = self.comms.getRRPosition()

        return allPositions

    def getHeading(self):
        """
        Returns the robot's heading.
        @return robotYaw
        """
        return self.comms.getGyroYaw()

    def generateRot2d(self, degrees) -> Rotation2d:
        """
        Generates a Rotation2d from degrees.
        @return Rotation2d
        """
        return Rotation2d(Units.radiansToDegrees(degrees))

    def createAllTags(self) -> Sequence[AprilTag]:
        """
        Creates all known AprilTags.
        @return allKnownTags: An array with all the known tags contained in it
        """
        # Stores locations used for testing
        allKnownTags = [
            AprilTag(1, Units.inchesToMeters(144 + 66 + 12), Units.inchesToMeters(98), Units.inchesToMeters(30.5 + 34), 0, 0, Units.degreesToRadians(-90)),
            AprilTag(2, Units.inchesToMeters(144 + 66 + 12), Units.inchesToMeters(12), Units.inchesToMeters(30.5 + 20), 0, 0, Units.degreesToRadians(-90)),
            AprilTag(3, Units.inchesToMeters(144 + 66 + 12), Units.inchesToMeters(98), Units.inchesToMeters(30.5 + 30.5), 0, 0, Units.degreesToRadians(-90)),
            AprilTag(5, Units.inchesToMeters(40.5), Units.inchesToMeters(67), Units.inchesToMeters(25), 0, 0, Units.degreesToRadians(-90))
        ]

        return allKnownTags