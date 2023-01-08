# Created by Alex Pereira

# Import Libraries
import logging

# Starts a logger
logging.basicConfig(filename = "DetectionLog.log", format="%(levelname)s:%(message)s", encoding = "utf-8", level = logging.DEBUG)
logging.info("Starting logger")

# Start of the Logging class
class Logger:
	@staticmethod
	def logDebug(debug):
		"""
		Logs a debug statement.
		@param debugMessage
		"""
		logging.debug(debug)

	@staticmethod
	def logInfo(info):
		"""
		Logs information.
		@param infoMessage
		"""
		logging.info(info)

	@staticmethod
	def logWarning(warning):
		"""
		Logs a warning.
		@param warning
		"""
		logging.warning(warning)

	@staticmethod
	def logwriteError(error):
		"""
		Logs an error.
		@param error
		"""
		logging.error(error)