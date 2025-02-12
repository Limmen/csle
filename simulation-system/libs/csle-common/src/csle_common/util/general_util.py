from typing import Tuple, List
import socket
import numpy as np
import numpy.typing as npt


class GeneralUtil:
    """
    Class with general utility functions
    """

    @staticmethod
    def get_host_ip() -> str:
        """
        Utility method for getting the ip of the host

        :return: the ip of the host
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return str(s.getsockname()[0])

    @staticmethod
    def replace_first_octet_of_ip(ip: str, ip_first_octet: int) -> str:
        """
        Utility function for changing the first octet in an IP address

        :param ip: the IP to modify
        :param ip_first_octet: the first octet to insert
        :return: the new IP
        """
        index_of_first_octet_end = ip.find(".")
        return str(ip_first_octet) + ip[index_of_first_octet_end:]

    @staticmethod
    def replace_first_octet_of_ip_tuple(tuple_of_ips: Tuple[str, str], ip_first_octet: int) -> Tuple[str, str]:
        """
        Utility function for changing the first octet in an IP address

        :param ip: the IP to modify
        :param ip_first_octet: the first octet to insert
        :return: the new IP
        """
        index_of_first_octet_end = tuple_of_ips[0].find(".")
        first_ip = str(ip_first_octet) + tuple_of_ips[0][index_of_first_octet_end:]
        index_of_first_octet_end = tuple_of_ips[1].find(".")
        second_ip = str(ip_first_octet) + tuple_of_ips[1][index_of_first_octet_end:]
        return (first_ip, second_ip)

    @staticmethod
    def get_latest_table_id(cur, table_name: str) -> int:
        """
        Gets the next ID for a table with a serial column primary key

        :param cur: the postgres connection cursor
        :param table_name: the table name
        :return: the next id
        """
        cur.execute(f"SELECT id FROM {table_name}")
        id = 1
        ids = cur.fetchall()
        if len(ids) > 0:
            id = max(list(map(lambda x: x[0], ids))) + 1
        return id

    @staticmethod
    def list_to_tuple(L):
        """
        Converts a nested list to a tuple
        """
        if isinstance(L, list):
            return tuple(GeneralUtil.list_to_tuple(item) for item in L)  # Recursively convert lists to tuples
        return L

    @staticmethod
    def one_hot_encode_integer(value: int, max_value: int) -> npt.NDArray[np.int32]:
        """
        One-hot encodes an integer

        :param value: the interger value
        :param max_value: the maximum value
        :return: the one-hot encoded vector
        """
        if not (0 <= value <= max_value):
            raise ValueError(f"Value is: {value}, Value must be between 0 and {max_value} (inclusive).")
        one_hot_vector = np.zeros(max_value + 1, dtype=np.int32)
        one_hot_vector[value] = 1
        return one_hot_vector

    @staticmethod
    def one_hot_encode_vector(vector: List[int], max_value: int) -> npt.NDArray[np.int32]:
        """
        One-hot encodes a vector

        :param vector: the vector to one-hot encode
        :param max_value: the maximum value in each entry of the vector
        :return: the one-hot encoded vector
        """
        np_vector = np.array(vector)

        # Validate input values
        if not np.all((0 <= np_vector) & (np_vector <= max_value)):
            raise ValueError(f"Vector is: {np_vector}. Input vector can only contain values between 0 and {max_value}.")

        # Create one-hot encoding dynamically based on max_value
        one_hot = np.eye(max_value + 1)[np_vector]  # Identity matrix of size (max_value + 1)

        return np.array(one_hot.flatten())
