import logging
import os
import datetime
import sys
import csle_common.constants.constants as constants
from csle_common.logging.custom_formatter import CustomFormatter


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonType):
    """
    Centralized class that handles log-management in csle
    """

    _logger = None
    _log_path = ""

    def __init__(self):
        """
        Creates a log file and returns a logger object

        :return: the logger object
        """
        log_dir = constants.LOGGING.DEFAULT_LOG_DIR

        now = datetime.datetime.now()
        log_file_name = now.strftime("%Y-%m-%d-%H-%M") + ".log"

        # Build Log File Full Path
        log_path = os.path.join(log_dir, (str(log_file_name)))

        # Create logger object and set the format for logging and other attributes
        logger = logging.Logger(log_file_name)
        logger.setLevel(logging.INFO)

        try:
            self.setup_logfile(log_path=log_path, logger=logger)
        except Exception:
            log_path = os.path.join(".", (str(log_file_name)))
            self.setup_logfile(log_path=log_path, logger=logger)

    def setup_logfile(self, log_path, logger):
        handler = logging.FileHandler(log_path, 'a+')
        os.chmod(log_path, 0o777)
        handler.setFormatter(
            CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'))
        logger.addHandler(handler)
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)
        self.logger = logger
        self._log_path = log_path
        sys.excepthook = handle_exception

    def get_logger(self) -> logging.Logger:
        """
        :return: the CSLE logger
        """
        # Create Log file directory if not exists
        if not os.path.exists(self._log_path):
            print(f"Log outputs are stored at: {self._log_path}")
            os.makedirs(self._log_path)
        return self.logger

    def get_log_file_path(self) -> str:
        """
        :return: the path where the log file is stored
        """
        return self._log_path


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    Logger.__call__().get_logger().error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
