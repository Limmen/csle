import re
from typing import List
from urllib.parse import urlparse


class IOCExtractor:
    """
    Class with regular expressions and utility functions for extracting IOCs from logs
    (e.g., CVEs, hostnames, IPs, etc.)
    """

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Exctracts all URLs from a given text string

        :param text: the input text
        :return: a list of found URLs
        """
        return re.findall(r"https?://[\w./?=#%-]+", text)

    @staticmethod
    def extract_ips(text: str) -> List[str]:
        """
        Extracts all IPs from a given text string

        :param text: the input text
        :return: the list of IPs
        """
        return re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)

    @staticmethod
    def extract_hostnames(text: str) -> List[str]:
        """
        Extracts all hostnames from a given text string

        :param text: the input text
        :return: the list of hostnames
        """
        return re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", text)

    @staticmethod
    def extract_domains(text: str) -> List[str]:
        """
        Extracts all domains from a given text string

        :param text: the input text
        :return: the list of domains
        """
        return list(set([urlparse(url).netloc for url in IOCExtractor.extract_urls(text)]))

    @staticmethod
    def extract_cves(text: str) -> List[str]:
        """
        Extracts all CVEs from a given text string

        :param text: the input text
        :return: the list of CVEs
        """
        return re.findall(r"CVE-\d{4}-\d{4,7}", text)

    @staticmethod
    def extract_nids(text: str) -> List[str]:
        """
        Extracts all NIDs from a given text string

        :param text: the input text
        :return: the list of NIDs
        """
        return re.findall(r"\b(?:[0-9]+:[0-9]+:[0-9]+)\b", text)
