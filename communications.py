# Created by Alex Pereira

# Import Libraries
from networktables import *

# Import Utilities
from Utilities.Logger import Logger

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
        self.isRedAlliance = FMSInfo.getEntry("IsRedAlliance")  # bool

        # Create a TagInfo Table and its entries
        TagInfo = ntinst.getTable("TagInfo")
        self.targetValid   = TagInfo.getEntry("tv")            # bool
        self.time          = TagInfo.getEntry("time")          # double
        self.bestResult    = TagInfo.getEntry("BestResult")    # double[]
        self.bestResultId  = TagInfo.getEntry("BestResultId")  # double
        self.detectionTime = TagInfo.getEntry("DetectionTime") # double

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
        tagId = result[0]
        pose  = result[1]

        # Sets the tag value
        self.setBestResultId(tagId)

        # Extracts the x, y, and z translations relative to the field's WCS
        x, y, z = pose.X(), pose.Y(), pose.Z()

        # Extracts the tag's roll, yaw, and pitch relative to the field's WCS
        roll, pitch, yaw = pose.rotation().X(), pose.rotation().Y(), pose.rotation().Z()

        # Packs all the data
        data = (tagId, x, y, z, roll, pitch, yaw)

        # Sends the data
        self.bestResult.setDoubleArray(data)

    def setTargetValid(self, tv: bool):
        """
        Sets if a valid target was detected.
        @param tv
        """
        self.targetValid.setBoolean(tv)

    def setDetectionTimeSec(self, timeSec: float):
        """
        Sets the time when a detection was made.
        @param timeSec
        """
        self.detectionTime.setDouble(timeSec)

    def getTime(self) -> float:
        """
        Gets the time from the Rio.
        @return time
        """
        return self.time.getBoolean(-1)