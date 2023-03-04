# Created by Alex Pereira

# Import Libraries
from networktables import *

# Import Utilities
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

        # Create a TagInfo Table and its Entries
        TagInfo = ntinst.getTable("TagInfo")
        self.targetValid   = TagInfo.getEntry("tv")            # Boolean
        self.bestResult    = TagInfo.getEntry("BestResult")    # Double[]
        self.bestResultId  = TagInfo.getEntry("BestResultId")  # Double
        self.detectionTime = TagInfo.getEntry("DetectionTime") # Double

        # Updates log
        Logger.logInfo("NetworkCommunications initialized")

    # # *****   TJM   *****
    # # Jetson code is a client (not roborio or driverStation)
    # # Jetson code is a publisher of topics for the table
    # # It appears that all topics need to be the same type in the table.  Some way around this??? generic???
    # # An Entry(above) can be used to subscribe & publish.  We are just publishing here.
    # # client code from   https://docs.wpilib.org/en/stable/docs/software/networktables/client-side-program.html
    # # publish code from  https://docs.wpilib.org/en/stable/docs/software/networktables/publish-and-subscribe.html
    # def init_TJM(self)
    #     ninst = NetworkTableInstance.getDefault()
    #
    #     # create new table
    #     table = ninst.getTable("TagInfo_TJM");
    #
    #     # create topics in new table
    #     x = table.getDoubleTopic("x").publish(0.0);
    #     y = table.getDoubleTopic("y").publish(0.0);
    #
    #     # create new client
    #     inst.startClient4("jetson client");
    #
    #     # connect to server on roborio
    #     inst.setServerTeam(2199);
    #
    #     # set values to be published and read by all subscribers
    #     x.set(1.0)
    #     y.set(2.0)

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