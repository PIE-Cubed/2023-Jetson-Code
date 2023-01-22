# Created by Alex Pereira

# Import Libraries
import numpy as np
from wpimath.geometry import *

# Import Utilities
from enum import Enum
from typing import Optional, Sequence
from Utilities.Logger import Logger
from Utilities.AprilTag import AprilTag

# Creates the AprilTagFieldLayout class
class AprilTagFieldLayout:
    class Origin(Enum):
        kBlueAllianceWallRightSide = "BlueWall"
        kRedAllianceWallRightSide  = "RedWall"

    def __init__(self, tags: Sequence[AprilTag], fieldLength: float, fieldWidth: float, isRed = False) -> None:
        """
        Generates a field with AprilTags
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

        # The allTags array
        self.allTags = [Pose3d()] * 8

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
        elif(isRed == False):
            self.setOrigin(AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide)

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

    def getTagPose(self, id: int) -> Optional[Pose3d]:
        """
        Returns the pose of the selected tag
        @return Pose3d
        """
        return Optional[self.allTags[id].relativeTo(self.m_origin)]