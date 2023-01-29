# Created by Alex Pereira

# Import Libraries
import logging

# Starts a logger
logging.basicConfig(filename = "DetectionLog.log", format="%(levelname)s:%(message)s", encoding = "utf-8", level = logging.DEBUG)
logging.info("Starting logger")

# Sets the log status
logStatus = False

# Start of the Logging class
class Logger:
    @staticmethod
    def logDebug(debug):
        """
        Logs a debug statement.
        @param debugMessage
        """
        if (logStatus == True):
            logging.debug(debug)

    @staticmethod
    def logInfo(info):
        """
        Logs information.
        @param infoMessage
        """
        if (logStatus == True):
            logging.info(info)

    @staticmethod
    def logWarning(warning):
        """
        Logs a warning.
        @param warning
        """
        if (logStatus == True):
            logging.warning(warning)

    @staticmethod
    def logError(error):
        """
        Logs an error.
        @param error
        """
        if (logStatus == True):
            logging.error(error)