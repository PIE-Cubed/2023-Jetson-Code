# Created by Alex Pereira

# Import Libraries
import numpy as np
from   Logger import Logger
from   networktables import *
from   wpimath.kinematics._kinematics import SwerveModulePosition

# Variables
firstTime = True

# Creates the NetworkCommunications Class
class NetworkCommunications:
    def __init__(self) -> None:
        """
        Constructor for the NetworkCommunications class.
        """
        # Get a NetworkTables Instance
        ntinst = NetworkTablesInstance.getDefault()

        # FMSInfo Table
        FMSInfo = ntinst.getTable("FMSInfo")
        self.isRedAlliance = FMSInfo.getEntry("IsRedAlliance")  # Boolean

        # Create a RobotData table and its entries
        RobotData = ntinst.getTable("RobotData")
        self.gyroYaw    = RobotData.getEntry("GyroYaw")     # Double
        self.detectTime = RobotData.getEntry("DetectTime")  # Double
        self.FLRot      = RobotData.getEntry("FLRotation")  # Double
        self.RLRot      = RobotData.getEntry("RLRotation")  # Double
        self.FRRot      = RobotData.getEntry("FRRotation")  # Double
        self.RRRot      = RobotData.getEntry("RRRotation")  # Double
        self.FLVel      = RobotData.getEntry("FLVelocity")  # Double
        self.RLVel      = RobotData.getEntry("RLVelocity")  # Double
        self.FRVel      = RobotData.getEntry("FRVelocity")  # Double
        self.RRVel      = RobotData.getEntry("RRVelocity")  # Double

        # Create a TagInfo Table and its Entries
        TagInfo = ntinst.getTable("TagInfo")
        self.bestResult = TagInfo.getEntry("BestResult")  # Double[]

        # Updates log
        Logger.logInfo("NetworkCommunications initialized")

    def sendBestResult(self, result):
        """
        Sends the result with the least erro.

        This method will send [tagId, xTranslate, yTranslate, zTranslate, yaw, pitch, roll].
        All translation data is in meters. All rotation data is in radians.
        @param result
        """
        # Gets variables from result
        tagId       = result[0]
        error       = result[1]
        pose        = result[2]
        eulerAngles = result[3]

        # Flattens the pose array into a 1D array
        flatPose = np.array(pose).flatten()

        # Flattens the eulerAngles array into a 1D array
        flatAngles = np.array(eulerAngles).flatten()

        # Extracts the x, y, and z translations
        x, y, z = flatPose[3], flatPose[7], flatPose[11]

        # Extracts the tag's roll, yaw, and pitch
        pitch, yaw, roll = flatAngles[3], flatAngles[7], flatAngles[11]

        # Packs all the data
        data = (tagId, error, x, y, z, roll, pitch, yaw)

        # Sends the data
        self.bestResult.setDoubleArray(data)

    def sendDetectTimeSec(self, timeSec):
        """
        Send the time when a detection was made.
        @param timeSec
        """
        self.detectTime.setDouble(timeSec)

    def getFLPosition(self):
        """
        Gets the SwerveModulePosition of the Front Left module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.FLVel.getDouble(0), self.FLRot.getDouble(0))

    def getRLPosition(self):
        """
        Gets the SwerveModulePosition of the Rear Left module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.RLVel.getDouble(0), self.RLRot.getDouble(0))

    def getFRPosition(self):
        """
        Gets the SwerveModulePosition of the Front Right module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.FRVel.getDouble(0), self.FRRot.getDouble(0))

    def getRRPosition(self):
        """
        Gets the SwerveModulePosition of the Rear Right module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.RRVel.getDouble(0), self.RRRot.getDouble(0))

    def getGyroYaw(self):
        return self.gyroYaw.getDouble(1000.00)