import logging
import os
from pycr_common.logging.custom_formatter import CustomFormatter

class Logger:
    """
    Centralized class that handles log-management in PyCr
    """

    @staticmethod
    def get_logger(log_file_name : str, log_sub_dir : str ="") -> logging.Logger:
        """
        Creates a log file and returns a logger object

        :param log_file_name: the name of the log file to create
        :param log_sub_dir: the sub-directory (default no sub-directory)
        :return: the logger object
        """
        log_dir = "/logs_dir/"

        # Build Log file directory, based on the OS and supplied input
        log_dir = linux_log_dir
        log_dir = os.path.join(log_dir, log_sub_dir)

        # Create Log file directory if not exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Build Log File Full Path
        logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(log_dir,
                                                                                   (str(log_file_name) + '.log'))

        # Create logger object and set the format for logging and other attributes
        logger = logging.Logger(log_file_name)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(logPath, 'a+')
        """ Set the formatter of 'CustomFormatter' type as we need to log base function name and base file name """
        handler.setFormatter(
            CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'))
        logger.addHandler(handler)

        # Return logger object
        return logger


