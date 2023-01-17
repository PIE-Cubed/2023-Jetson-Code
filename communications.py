# Created by Alex Pereira

# Import Libraries
import numpy as np
from typing import Sequence
from networktables import *
from wpimath.geometry._geometry import *
from wpimath.kinematics._kinematics import SwerveModulePosition

# Import Utilities
from Utilities.Units import Units
from Utilities.Logger import Logger

# Variables
firstTime = True

# Creates the NetworkCommunications Class
class NetworkCommunications:
    def __init__(self) -> None:
        """
        Constructor for the NetworkCommunications class.
        """
        # Start a NetworkTables client
        NetworkTables.startClientTeam(2199)

        # Get a NetworkTables Instance
        ntinst = NetworkTablesInstance.getDefault()

        # FMSInfo Table
        FMSInfo = ntinst.getTable("FMSInfo")
        self.isRedAlliance = FMSInfo.getEntry("IsRedAlliance")  # Boolean

        # Targetting table
        Targetting = ntinst.getTable("Targetting")
        self.targets = Targetting.getEntry("Targets")  # Double[]
        self.offsets = Targetting.getEntry("Offsets")  # Double[]
        self.drivePowers = Targetting.getEntry("DrivePowers")  # Double[]

        # Create a RobotData table and its entries
        RobotData = ntinst.getTable("RobotData")
        self.gyroYaw     = RobotData.getEntry("GyroYaw")     # Double
        self.detectTime  = RobotData.getEntry("DetectTime")  # Double
        self.FLRot       = RobotData.getEntry("FLRotation")  # Double
        self.RLRot       = RobotData.getEntry("RLRotation")  # Double
        self.FRRot       = RobotData.getEntry("FRRotation")  # Double
        self.RRRot       = RobotData.getEntry("RRRotation")  # Double
        self.FLVel       = RobotData.getEntry("FLVelocity")  # Double
        self.RLVel       = RobotData.getEntry("RLVelocity")  # Double
        self.FRVel       = RobotData.getEntry("FRVelocity")  # Double
        self.RRVel       = RobotData.getEntry("RRVelocity")  # Double
        self.camOffset   = RobotData.getEntry("CameraOffset") # Double[]
        self.targetValid = RobotData.getEntry("tv")  # Boolean

        # Create a TagInfo Table and its Entries
        TagInfo = ntinst.getTable("TagInfo")
        self.bestResult   = TagInfo.getEntry("BestResult")  # Double[]
        self.bestResultId = TagInfo.getEntry("BestResultId")  # Double

        # Updates log
        Logger.logInfo("NetworkCommunications initialized")

    def setBestResultId(self, id: int):
        """
        Sets the tag id of the best result.
        @param tagId
        """
        self.bestResultId.setDouble(id)

    def setBestResult(self, result):
        """
        Sends the best result.

        This method will send [tagId, xTranslate, yTranslate, zTranslate, yaw, pitch, roll].
        All translation data is in meters. All rotation data is in radians.
        @param result
        """
        # Gets variables from result
        tagId       = result[0]
        pose        = result[1]
        eulerAngles = result[2]

        # Sets the tag value
        self.setBestResultId(tagId)

        # Flattens the pose array into a 1D array
        flatPose = np.array(pose).flatten()

        # Flattens the eulerAngles array into a 1D array
        flatAngles = np.array(eulerAngles).flatten()

        # Extracts the x, y, and z translations relative to the field's WCS
        x, y, z = flatPose[3], flatPose[11], -flatPose[7]

        # Extracts the tag's roll, yaw, and pitch relative to the field's WCS
        roll, pitch, yaw = flatAngles[2], flatAngles[0], flatAngles[1]

        # Packs all the data
        data = (tagId, x, y, z, roll, pitch, yaw)

        # Sends the data
        self.bestResult.setDoubleArray(data)

    def setDrivePowers(self, calcXPower: float, calcYPower: float, calcRotatePower: float):
        """
        Sets the drive powers.
        @param calcXPower
        @param calcYPower
        @param calcRotatePower
        """
        self.drivePowers.setDoubleArray([calcXPower, calcYPower, calcRotatePower])

    def setTargetValid(self, tv: bool):
        """
        Sets if a valid target was detected.
        @param tv
        """
        self.targetValid.setBoolean(tv)

    def setDetectTimeSec(self, timeSec: float):
        """
        Sets the time when a detection was made.
        @param timeSec
        """
        self.detectTime.setDouble(timeSec)
    
    def setCamOffset(self, camOffset: Transform3d):
        """
        Sets the camera transformation.
        @param cameraTransform
        """
        # Extract distances from the Transform3d
        x, y, z = camOffset.X(), camOffset.Y(), camOffset.Z()

        # Extract rotations from the Transform3d
        roll, pitch, yaw = camOffset.rotation().X(), camOffset.rotation().Y(), camOffset.rotation().Z()

        # Set the double array
        self.camOffset.setDoubleArray([x, y, z, roll, pitch, yaw])

    def getBestResultId(self) -> int:
        """
        Gets the tag id of the best result.
        @return tagId
        """
        return int(self.bestResultId.getDouble(-1))

    def getBestResult(self) -> Pose3d:
        """
        Gets the best result stored in NetworkTables. 
        @return Pose3d
        """
        # Gets the stored info
        info = self.bestResult.getDoubleArray([-1, 0, 0, 0, 0, 0, 0])

        # Returns a Pose3d object
        return Pose3d(
            Translation3d(info[1], info[2], info[3]),
            Rotation3d(info[4], info[5], info[6])
        )

    def getTargetIds(self) -> Sequence[float]:
        """
        Gets the ids of the target tags.

        Should correspond with the distances provided by the Offsets entry.
        @return arrayOfTargetIds
        """
        return self.targets.getDoubleArray([-1])

    def getTargetOffsets(self) -> Sequence[float]:
        """
        Gets the offsets from the tags registered as targets.
        
        Should correspond with the tag numbers provided by the Targets entry.
        The data is in the format is x, y, z, roll, pitch, yaw but extends infinitely
        @return arrayOfTransforms
        """
        # Gets the offsets
        offsets = self.offsets.getDoubleArray([0, 0, 0, 0, 0, 0])

        # Variables
        transforms = []
        length = len(offsets)
        modLength = length % 6
        itterate = int((length - modLength) / 6)

        # Parses the results into a series of Transform3ds
        for i in range(0, itterate):
            print(i)
            lowerBound = i * 6
            upperBound = (i + 1) * 6
            tag = offsets[lowerBound : upperBound]
            temp = Transform3d(
                Translation3d(tag[0], tag[1], tag[2]),
                Rotation3d(tag[3], tag[4], tag[5])
            )

            # Adds the temp variable to the returned array
            transforms.append(temp)
 
        return transforms

    def getFLPosition(self) -> SwerveModulePosition:
        """
        Gets the SwerveModulePosition of the Front Left module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.FLVel.getDouble(0), self.degToRotation2d(self.FLRot.getDouble(0)))

    def getRLPosition(self) -> SwerveModulePosition:
        """
        Gets the SwerveModulePosition of the Rear Left module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.RLVel.getDouble(0), self.degToRotation2d(self.RLRot.getDouble(0)))

    def getFRPosition(self) -> SwerveModulePosition:
        """
        Gets the SwerveModulePosition of the Front Right module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.FRVel.getDouble(0), self.degToRotation2d(self.FRRot.getDouble(0)))

    def getRRPosition(self) -> SwerveModulePosition:
        """
        Gets the SwerveModulePosition of the Rear Right module.
        @return SwerveModulePosition
        """
        return SwerveModulePosition(self.RRVel.getDouble(0), self.degToRotation2d(self.RRRot.getDouble(0)))

    def getGyroYaw(self) -> float:
        """
        Gets the yaw of the gyro.
        @return Yaw (degrees)
        """
        return self.gyroYaw.getDouble(0.00)

    def getTargetValid(self) -> bool:
        """
        Determines if a target is valid.
        @return tv
        """
        return self.targetValid.getBoolean(False)

    def getDetectionTime(self) -> float:
        """
        Gets the time a detection was made.
        @return detTimeSeconds 
        """
        return self.detectTime.getDouble(-1)

    def getCamOffset(self) -> Transform3d:
        """
        Gets the camera's offset from the center of the robot.
        @return cameraOffset
        """
        # Gets the offset
        offset = self.camOffset.getDouble([0, 0, 0, 0, 0, 0])

        # Return a Transform3d generated from the array
        return Transform3d(
            Translation3d(offset[0], offset[1], offset[2]),
            Rotation3d(offset[3], offset[4], offset[5])
        )

    def degToRotation2d(self, degrees) -> Rotation2d:
        """
        Returns a Rotation2d created from degrees.
        @param degrees
        """
        return Rotation2d(Units.degreesToRadians(degrees))