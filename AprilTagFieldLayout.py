# Created by Alex Pereira

# Import Libraries
import numpy as np
from enum import Enum
from wpimath.geometry._geometry import *

# Creates the AprilTagFieldLayout class
class AprilTagFieldLayout:
    class Origin(Enum):
        kBlueAllianceWallRightSide = 0
        kRedAllianceWallRightSide  = 1

    def __init__(self, allTags: list, fieldLength, fieldWidth, isRed = False) -> None:
        """
        Generates a field with AprilTags
        """
        # Localize parameters
        self.fieldLength = fieldLength
        self.fieldWidth = fieldWidth

        # Creates a blank copy of allTags
        self.allTags = [0] * 30

        # Sorts the allTags array
        for tag in allTags:
            self.allTags[tag.getId()] = tag.getPose()

        # Variables
        self.m_origin = None

        # Sets the origin depending on alliance
        if (isRed == True):
            self.setOrigin(AprilTagFieldLayout.Origin.kRedAllianceWallRightSide)
        elif(isRed == False):
            self.setOrigin(AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide)

    def setOrigin(self, origin):
        """
        Sets the origin based on a predefined enumeration of coordinate frame origins. The origins are calculated from the field dimensions.
        
        This transforms the Pose3ds returned by getTagPose() to return the correct pose relative to a predefined coordinate frame.
        @param origin: The predefined origin
        """
        if (origin == AprilTagFieldLayout.Origin.kBlueAllianceWallRightSide):
            self.setOrigin(Pose3d())
        elif (origin == AprilTagFieldLayout.Origin.kRedAllianceWallRightSide):
            self.setOrigin(
                Pose3d(
                    Translation3d(self.fieldLength, self.fieldWidth, 0),
                    Rotation3d(0, 0, np.pi)))
        else:
            raise ValueError("Unsupported enumerator value.")

    def setOrigin(self, origin: Pose3d):
        """
        Sets the origin for tag pose transformation

        This transforms the Pose3ds returned by getTagPose() to return the correct pose relative to the provided origin.
        @param origin: The new origin for tag transformations
        """
        self.m_origin = origin

    def getTags(self):
        """
        Returns all the created tags
        @return allTags
        """
        return self.allTags

    def getTagPose(self, id):
        """
        Returns the pose of the selected tag
        @return Pose3d
        """
        try:
            return self.allTags[id][1].relativeTo(self.m_origin)
        except:
            return Pose3d()