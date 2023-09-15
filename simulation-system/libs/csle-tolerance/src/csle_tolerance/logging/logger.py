import sys
import logging
from csle_tolerance.logging.custom_formatter import CustomFormatter


class Logger:
    """
    Class with methods related to logging
    """

    @staticmethod
    def get_logger(log_file: str, log_level: int) -> logging.Logger:
        """
        Gets the logging handle

        :param log_file: the log file to store the log
        :param log_level: the log level
        :return: the logging
        """
        logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_file, 'a+')
        handler.setFormatter(
            CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'))
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(log_level)
        return logger
