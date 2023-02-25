# Created by Alex Pereira

# Import Libraries
import ntcore
import numpy  as np
from   cscore import CameraServer as CS

# Get a default network table
nt = ntcore.NetworkTableInstance.getDefault()
nt.setServerTeam(2199)
nt.startClient3(__file__)

# Creates the Streaming Class
class Streaming:
    def __init__(self, camNum: int, path: str = None) -> None:
        """
        Constructor for the Streaming class.
        @param Camera Number
        @param path: It can be found on Linux by running "find /dev/v4l"
        """
        # Creates a CameraServer
        CS.enableLogging()

        # Defines the resolution
        streamRes = (640, 480)

        # Captures from a specified USB Camera on the system
        if (path is not None):
            # If path is known, use the path
            camera = CS.startAutomaticCapture(name = "Camera" + str(camNum), path = path)
        else:
            # Path is unknown, use the camera number
            camera = CS.startAutomaticCapture(dev = camNum)
        camera.setResolution(streamRes[0], streamRes[1])