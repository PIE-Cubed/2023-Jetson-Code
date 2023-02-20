# Created by Alex Pereira

# Import Libraries
import numpy  as np
from   cscore import CameraServer

# Creates the Streaming Class
class Streaming:
    def __init__(self, camNum: int, path: str = None) -> None:
        """
        Constructor for the Streaming class.
        @param Camera Number
        @param path: It can be found on Linux by running "find /dev/v4l"
        """
        # Creates a CameraServer
        cs = CameraServer
        cs.enableLogging()

        # Defines the resolution
        streamRes = (640, 480)

        # Captures from a specified USB Camera on the system
        if (path is not None):
            # If path is known, use the path
            camera = cs.startAutomaticCapture(name = "cam" + str(camNum), path = path)
        else:
            # Path is unknown, use the camera number
            camera = cs.startAutomaticCapture(name = "cam" + str(camNum), dev = camNum)
        camera.setResolution(streamRes[0], streamRes[1])

        # Get a CvSink. This will capture images from the camera
        self.cvSink = cs.getVideo()

        # Setup a CvSource. This will send images back to the Dashboard
        self.outputStream = cs.putVideo("Camera 1", streamRes[0], streamRes[1])

        # Preallocates for the incoming images
        self.img = np.zeros(shape = (streamRes[1], streamRes[0], 3), dtype = np.uint8)

    def streamCamera(self):
        """
        Streams the camera back to ShuffleBoard for driver use.
        @return Image
        """
        # Grab a frame from the camera and put it in the source image
        time, self.img = self.cvSink.grabFrame(self.img)

        # If there is an error notify the output
        if (time == 0):
            # Send the output the error
            self.outputStream.notifyError(self.cvSink.getError())

        # Insert image processing here
        #

        # Send some image back to the dashboard
        self.outputStream.putFrame(self.img)

        return self.img