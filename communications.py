# Created by Alex Pereira

# Import Libraries
import numpy as np
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
        self.gyroYaw        = RobotData.getEntry("GyroYaw")     # Double
        self.currentTimeSec = RobotData.getEntry("CurrentTime") # Double
        self.detectTime     = RobotData.getEntry("DetectTime")  # Double
        self.FLRot          = RobotData.getEntry("FLRotation")  # Double
        self.RLRot          = RobotData.getEntry("RLRotation")  # Double
        self.FRRot          = RobotData.getEntry("FRRotation")  # Double
        self.RRRot          = RobotData.getEntry("RRRotation")  # Double
        self.FLVel          = RobotData.getEntry("FLVelocity")  # Double
        self.RLVel          = RobotData.getEntry("RLVelocity")  # Double
        self.FRVel          = RobotData.getEntry("FRVelocity")  # Double
        self.RRVel          = RobotData.getEntry("RRVelocity")  # Double

        # Create a RobotData table and its entries
        FLData = ntinst.getTable("RobotData")
        self.currentTime = RobotData.getEntry("CurrentTime")  # Double
        self.detectTime  = RobotData.getEntry("DetectTime")  # Double
        self.gyroYaw     = RobotData.getEntry("GyroYaw")  # Double

        # Create a TagInfo Table and its Entries
        TagInfo = ntinst.getTable("TagInfo")
        self.tVecsDetected       = TagInfo.getEntry("TranslationVectors")  # String[]
        self.rMatrixesDetected   = TagInfo.getEntry("RotationMatrixes")  # String[]
        self.eulerAnglesDetected = TagInfo.getEntry("EulerAngles")  # String[]

        # Create an AllTags Tables and its Entries
        AllTags = ntinst.getTable("AllTags")
        self.tag0  = AllTags.getEntry("Tag0")   # Double[]
        self.tag1  = AllTags.getEntry("Tag1")   # Double[]
        self.tag2  = AllTags.getEntry("Tag2")   # Double[]
        self.tag3  = AllTags.getEntry("Tag3")   # Double[]
        self.tag4  = AllTags.getEntry("Tag4")   # Double[]
        self.tag5  = AllTags.getEntry("Tag5")   # Double[]
        self.tag6  = AllTags.getEntry("Tag6")   # Double[]
        self.tag7  = AllTags.getEntry("Tag7")   # Double[]
        self.tag8  = AllTags.getEntry("Tag8")   # Double[]
        self.tag9  = AllTags.getEntry("Tag9")   # Double[]
        self.tag10 = AllTags.getEntry("Tag10")  # Double[]
        self.tag11 = AllTags.getEntry("Tag11")  # Double[]
        self.tag12 = AllTags.getEntry("Tag12")  # Double[]
        self.tag13 = AllTags.getEntry("Tag13")  # Double[]
        self.tag14 = AllTags.getEntry("Tag14")  # Double[]
        self.tag15 = AllTags.getEntry("Tag15")  # Double[]
        self.tag16 = AllTags.getEntry("Tag16")  # Double[]
        self.tag17 = AllTags.getEntry("Tag17")  # Double[]
        self.tag18 = AllTags.getEntry("Tag18")  # Double[]
        self.tag19 = AllTags.getEntry("Tag19")  # Double[]
        self.tag20 = AllTags.getEntry("Tag20")  # Double[]
        self.tag21 = AllTags.getEntry("Tag21")  # Double[]
        self.tag22 = AllTags.getEntry("Tag22")  # Double[]
        self.tag23 = AllTags.getEntry("Tag23")  # Double[]
        self.tag24 = AllTags.getEntry("Tag24")  # Double[]
        self.tag25 = AllTags.getEntry("Tag25")  # Double[]
        self.tag26 = AllTags.getEntry("Tag26")  # Double[]
        self.tag27 = AllTags.getEntry("Tag27")  # Double[]
        self.tag28 = AllTags.getEntry("Tag28")  # Double[]
        self.tag29 = AllTags.getEntry("Tag29")  # Double[]

    def sendAllData(self, results):
        """
        Sends the the detected data for ALL possible tags.

        This method will send [timestamp, xTranslate, yTranslate, zTranslate, yaw, pitch, roll].
        All translation data is in meters. All rotation data is in radians.
        @param results
        """
        # Loops through all results
        for result in results:
            # Gets variables from results
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
            data = (error, x, y, z, roll, pitch, yaw)

            # Updates the correct NetworkTables Entry
            if (tagId == 0):
                self.tag0.setDoubleArray(data)
            elif (tagId == 1):
                self.tag1.setDoubleArray(data)
            elif (tagId == 2):
                self.tag2.setDoubleArray(data)
            elif (tagId == 3):
                self.tag3.setDoubleArray(data)
            elif (tagId == 4):
                self.tag4.setDoubleArray(data)
            elif (tagId == 5):
                self.tag5.setDoubleArray(data)
            elif (tagId == 6):
                self.tag6.setDoubleArray(data)
            elif (tagId == 7):
                self.tag7.setDoubleArray(data)
            elif (tagId == 8):
                self.tag8.setDoubleArray(data)
            elif (tagId == 9):
                self.tag9.setDoubleArray(data)
            elif (tagId == 10):
                self.tag10.setDoubleArray(data)
            elif (tagId == 11):
                self.tag11.setDoubleArray(data)
            elif (tagId == 12):
                self.tag12.setDoubleArray(data)
            elif (tagId == 13):
                self.tag13.setDoubleArray(data)
            elif (tagId == 14):
                self.tag14.setDoubleArray(data)
            elif (tagId == 15):
                self.tag15.setDoubleArray(data)
            elif (tagId == 16):
                self.tag16.setDoubleArray(data)
            elif (tagId == 17):
                self.tag17.setDoubleArray(data)
            elif (tagId == 18):
                self.tag18.setDoubleArray(data)
            elif (tagId == 19):
                self.tag19.setDoubleArray(data)
            elif (tagId == 20):
                self.tag20.setDoubleArray(data)
            elif (tagId == 21):
                self.tag21.setDoubleArray(data)
            elif (tagId == 22):
                self.tag22.setDoubleArray(data)
            elif (tagId == 23):
                self.tag23.setDoubleArray(data)
            elif (tagId == 24):
                self.tag24.setDoubleArray(data)
            elif (tagId == 25):
                self.tag25.setDoubleArray(data)
            elif (tagId == 26):
                self.tag26.setDoubleArray(data)
            elif (tagId == 27):
                self.tag27.setDoubleArray(data)
            elif (tagId == 28):
                self.tag28.setDoubleArray(data)
            elif (tagId == 29):
                self.tag29.setDoubleArray(data)

    def sendCoordinateData(self, results):
        """
        Sends the detected coordinates as a String Array.

        This method send [tag ID, xTranslate, yTranslate, zTranslate].
        All translation data is in meters
        @param results
        """
        # Creates a blank array
        sendData = []

        for result in results:
            # Gets variables from results
            tagId       = result[0]
            pose        = result[1]
            eulerAngles = result[2]

            # Flattens the pose array into a 1D array
            flatPose = np.array(pose).flatten()

            # Extracts x, y, and z translations
            x, y, z = flatPose[3], flatPose[7], flatPose[11]

            # Collects data to send (TagId, x, y, z)
            data = str(np.array([tagId, x, y, z]))
            
            # Removes unwanted characters from the string
            data = data.replace("\n", "")
            data = data.replace("[", "")
            data = data.replace("]", "")

            # Adds seperators to the string
            data = data.replace(" ", ", ")
            data += ","

            # Adds the data to the data to send
            sendData.append(data)

        # Send the data over NetworkTables
        self.tVecsDetected.setStringArray(sendData)
    
    def sendRotationMatrixes(self, results):
        """
        Sends the detected coordinates as a String Array.

        This method send [tag ID, xTranslate, yTranslate, zTranslate].
        All translation data is in meters
        @param results
        """
        # Creates a blank array
        sendData = []

        for result in results:
            # Gets variables from results
            tagId       = result[0]
            pose        = result[1]
            eulerAngles = result[2]

            # Flattens the pose array into a 1D array
            flatPose = np.array(pose).flatten()

            # Extracts the nine values of the rotation array
            e0, e1, e2, e3, e4, e5, e6, e7, e8 = flatPose[0], flatPose[1], flatPose[2], flatPose[3], flatPose[4], flatPose[5], flatPose[6], flatPose[7], flatPose[8]

            # Collects data to send (TagId, e0, e1, e2, e3, e4, e5, e6, e7, e8)
            data = str(np.array([tagId, e0, e1, e2, e3, e4, e5, e6, e7, e8]))
            
            # Removes unwanted characters from the string
            data = data.replace("\n", "")
            data = data.replace("[", "")
            data = data.replace("]", "")

            # Adds seperators to the string
            data = data.replace(" ", ", ")
            data += ","

            # Adds the data to the data to send
            sendData.append(data)

        # Send the data over NetworkTables
        self.rMatrixesDetected.setStringArray(sendData)

    def sendEulerAngles(self, results):
        """
        Sends the calculated Euler's Angles as a String Array.

        This method send [tag ID, pitch, yaw, roll].
        All rotations are in radians
        @param results
        """
        # Creates a blank array
        sendData = []

        for result in results:
            # Gets variables from results
            tagId       = result[0]
            pose        = result[1]
            eulerAngles = result[2]

            # Flattens the eulerAngles array into a 1D array
            flatAngles = np.array(eulerAngles).flatten()

            # Extracts tags roll, yaw, and pitch
            pitch, yaw, roll = flatAngles[3], flatAngles[7], flatAngles[11]

            # Collects data to send (TagId, pitch, yaw, roll)
            data = str(np.array([tagId, pitch, yaw, roll]))
            
            # Removes unwanted characters from the string
            data = data.replace("\n", "")
            data = data.replace("[", "")
            data = data.replace("]", "")

            # Adds seperators to the string
            data = data.replace(" ", ", ")
            data += ","

            # Adds the data to the data to send
            sendData.append(data)

        # Send the data over NetworkTables
        self.eulerAnglesDetected.setStringArray(sendData)

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

    def getTimeSec(self):
        """
        Gets the current time in seconds as the RIO calculated it.
        @return currentTime: Default value is -1.00
        """
        return self.currentTime.getDouble(-1.00)

    def sendDetectTimeSec(self, timeSec):
        """
        Send the time when a detection was made.
        @param timeSec
        """
        self.detectTime.setDouble(timeSec)