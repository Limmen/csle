import csle_rest_api.constants.constants as constants
import requests
import os


class OTXLookup:
    """
    Class with utility functions for fetching threat intelligence from the OTX API
    """

    @staticmethod
    def lookup_ip(ip: str) -> requests.Response:
        """
        Sends a query to OTX to lookup information about a given IP address

        :param ip: the IP to lookup
        :return: the information returned by the OTX API
        """
        url = f"{constants.RAG.OTX_BASE_URL}/IPv4/{ip}/general"
        api_key = os.environ.get(constants.RAG.OTX_API_KEY)
        if api_key is None:
            raise ValueError("Could not find API key for OTX API among environment variables")
        headers = {constants.RAG.OTX_API_KEY_HEADER: api_key}
        response: requests.Response = requests.get(url, headers=headers).json()
        return response

    @staticmethod
    def lookup_domain(domain: str) -> requests.Response:
        """
        Sends a query to OTX to lookup information about a given domain

        :param domain: the domain to lookup
        :return: the information returned by the OTX API
        """
        url = f"{constants.RAG.OTX_BASE_URL}/domain/{domain}/general"
        api_key = os.environ.get(constants.RAG.OTX_API_KEY)
        if api_key is None:
            raise ValueError("Could not find API key for OTX API among environment variables")
        headers = {constants.RAG.OTX_API_KEY_HEADER: api_key}
        response: requests.Response = requests.get(url, headers=headers).json()
        return response

    @staticmethod
    def lookup_url(url: str) -> requests.Response:
        """
        Sends a query to OTX to lookup information about a given URL

        :param url: the URL to lookup
        :return: the information returned by the OTX API
        """
        url = f"{constants.RAG.OTX_BASE_URL}/url/{url}/general"
        api_key = os.environ.get(constants.RAG.OTX_API_KEY)
        if api_key is None:
            raise ValueError("Could not find API key for OTX API among environment variables")
        headers = {constants.RAG.OTX_API_KEY_HEADER: api_key}
        response: requests.Response = requests.get(url, headers=headers).json()
        return response

    @staticmethod
    def lookup_hostname(hostname: str) -> requests.Response:
        """
        Sends a query to OTX to lookup information about a given hostname

        :param hostname: the hostname to lookup
        :return: the information returned by the OTX API
        """
        url = f"{constants.RAG.OTX_BASE_URL}/hostname/{hostname}/general"
        api_key = os.environ.get(constants.RAG.OTX_API_KEY)
        if api_key is None:
            raise ValueError("Could not find API key for OTX API among environment variables")
        headers = {constants.RAG.OTX_API_KEY_HEADER: api_key}
        response: requests.Response = requests.get(url, headers=headers).json()
        return response

    @staticmethod
    def lookup_cve(cve: str) -> requests.Response:
        """
        Sends a query to OTX to lookup information about a given CVE

        :param cve: the CVE to lookup
        :return: the information returned by the OTX API
        """
        url = f"{constants.RAG.OTX_BASE_URL}/cve/{cve}"
        api_key = os.environ.get(constants.RAG.OTX_API_KEY)
        if api_key is None:
            raise ValueError("Could not find API key for OTX API among environment variables")
        headers = {constants.RAG.OTX_API_KEY_HEADER: api_key}
        response: requests.Response = requests.get(url, headers=headers).json()
        return response
