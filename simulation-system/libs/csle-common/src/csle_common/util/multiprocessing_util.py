import multiprocessing.pool


class NoDaemonProcess(multiprocessing.Process):
    """
    A process with the daemon property set to false
    """

    @property
    def daemon(self) -> bool:
        """
        The deamon property

        :return: True if the process is a Deamon, else false
        """
        return False

    @daemon.setter
    def daemon(self, value: bool) -> None:
        """
        The deamon setting

        :param value: the value to set the daemon property with
        :return: None
        """
        pass


class NoDaemonContext(type(multiprocessing.get_context())):  # type: ignore
    """
    Context of a non-daemon process
    """
    Process = NoDaemonProcess


class NestablePool(multiprocessing.pool.Pool):
    """
    Multiprocessing pool that allows nested multiprocessing
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the pool

        :param args: the pool arguments
        :param kwargs: the pool keyword arguments
        """
        kwargs['context'] = NoDaemonContext()
        super(NestablePool, self).__init__(*args, **kwargs)
