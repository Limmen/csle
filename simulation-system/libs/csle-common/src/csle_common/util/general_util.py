from typing import Tuple
import socket


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
