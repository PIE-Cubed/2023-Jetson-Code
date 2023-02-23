# Created by Alex Pereira

# Import Libraries
import json
import numpy as np
from wpimath.geometry import *

# Import Utilities
from enum import Enum
from typing import Sequence
from Utilities.Logger import Logger
from Utilities.AprilTag import AprilTag

# Creates the AprilTagFieldLayout class
class AprilTagFieldLayout:
    class Origin(Enum):
        kBlueAllianceWallRightSide = "BlueWall"
        kRedAllianceWallRightSide  = "RedWall"

    def __init__(self, isRed = False) -> None:
        """
        Generates the offical field with AprilTags for match play
        @param isRed: If we are on the red alliance
        """
        # Creates the allTags array
        self.allTags = [Pose3d()] * 9

        # Loads the json file
        self.readJson("2023-chargedup")

        # Variables
        self.m_origin = None

        # Sets the origin depending on alliance
        if (isRed == True):
            self.setOrigin(AprilTagFieldLayout.Origin.kRedAllianceWallRightSide)
        elif (isRed == False):
            self.setOrigin(AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide)

    def __init__(self, tags: Sequence[AprilTag], fieldLength: float, fieldWidth: float, isRed = False) -> None:
        """
        Generates an field with AprilTags for testing
        @param allTags: A list of all known tags
        @param fieldLength: The length (y) of the field in meters
        @param fieldWidth: The width (x) of the field in meters
        @param isRed: If we are on the red alliance
        """
        # Asserts that the array length is no greater than 8
        assert(len(tags) <= 8)

        # Localize parameters
        self.fieldLength = fieldLength
        self.fieldWidth = fieldWidth

        # Logs the field size
        Logger.logInfo("Field length: {}, Field width: {}".format(self.fieldLength, self.fieldWidth))

        # Creates the allTags array
        self.allTags = [Pose3d()] * 9

        # Sorts the data from tags into allTags
        for tag in tags:
            id = tag.getId()
            pose = tag.getPose()

            self.allTags[id] = pose

            # Logs the tag information
            Logger.logInfo("Tag {}. Pose: {}".format(id, pose))

        # Variables
        self.m_origin = None

        # Sets the origin depending on alliance
        if (isRed == True):
            self.setOrigin(AprilTagFieldLayout.Origin.kRedAllianceWallRightSide)
        elif (isRed == False):
            self.setOrigin(AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide)

    def readJson(self, name: str):
        """
        Extracts information from the json file about field size and tag locations
        @param name: The name of the json file 
        """
        # Opens the json
        file = open("/home/robolions/Documents/2023-Jetson-Code-Test/TagLayout/" + name + ".json")

        # Returns JSON object as a dictionary
        data = json.load(file)
        
        # Loops through the json data
        for tag in data["tags"]:
            # Gets the tag ID
            id = tag["ID"]

            # Gets the tag's translation data
            x_trans = tag["pose"]["translation"]["x"]
            y_trans = tag["pose"]["translation"]["y"]
            z_trans = tag["pose"]["translation"]["z"]

            # Gets the tag's rotation data
            w_rot = tag["pose"]["rotation"]["quaternion"]["W"]
            x_rot = tag["pose"]["rotation"]["quaternion"]["X"]
            y_rot = tag["pose"]["rotation"]["quaternion"]["Y"]
            z_rot = tag["pose"]["rotation"]["quaternion"]["Z"]

            # Creates a quaternion
            q = Quaternion(w_rot, x_rot, y_rot, z_rot)

            # Creates a Pose3d object
            pose = Pose3d(x_trans, y_trans, z_trans, Rotation3d(q))

            # Adds the tag to the allTags array
            self.allTags[id] = pose

            # Logs the tag's information
            Logger.logInfo("Tag {}. Pose: {}".format(id, pose))

        # Sets the field dimensions
        self.fieldLength = data["field"]["length"]
        self.fieldWidth  = data["field"]["width"]

        # Logs the field size
        Logger.logInfo("Field length: {}, Field width: {}".format(self.fieldLength, self.fieldWidth))

        # Closes the file
        file.close()

    def setOrigin(self, origin):
        """
        Sets the origin depending on the alliance color. The origins are calculated from the field dimensions.

        This transforms the Pose3ds returned by getTagPose() to return the correct pose relative to a predefined coordinate frame.
        @param origin: The predefined origin
        """
        if (origin == AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide):
            self.m_origin = Pose3d()
        elif (origin == AprilTagFieldLayout.Origin.kRedAllianceWallRightSide):
            self.m_origin = Pose3d(
                Translation3d(self.fieldLength, self.fieldWidth, 0),
                Rotation3d(0, 0, np.pi)
            )
        else:
            raise ValueError("Unsupported enumerator value.")

    def getTags(self):
        """
        Returns all the created tags
        @return allTags
        """
        return self.allTags

    def getTagPose(self, id: int) -> Pose3d:
        """
        Returns the pose of the selected tag
        @return Pose3d
        """
        if (self.allTags[id] is not Pose3d()):
            return Pose3d()
        else:
            return self.allTags[id].relativeTo(self.m_origin)