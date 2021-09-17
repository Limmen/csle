from typing import Tuple
from enum import Enum


class ActionAlerts:
    """
    Class for managing action alerts for the attacker
    """

    def __init__(self):
        """
        Initializes the object
        """
        self.alerts = {}
        self.user_ip_alerts = {}
        self.pivot_scan_alerts = {}

    def add_alert(self, action_id : Enum, ip: str, alert : Tuple) -> None:
        """
        Adds an action-alert

        :param action_id: the id of the action
        :param ip: the ip
        :param alert: the number of alerts to add
        :return: None
        """
        key = (action_id, ip)
        self.alerts[key] = alert

    def get_alert(self, action_id : Enum, ip: str) -> int:
        """
        Looks up the number of alerts for a given action and ip

        :param action_id: the action id
        :param ip: the ip
        :return: the number of alerts
        """
        key = (action_id, ip)
        return self.alerts[key]

    def exists(self, action_id: Enum, ip: str) -> bool:
        """
        Checks if there is a number of alerts that exist for the given action and ip

        :param action_id: the action id
        :param ip: the ip
        :return: True or False
        """
        key = (action_id, ip)
        return key in self.alerts

    def user_ip_add_alert(self, action_id: Enum, ip: str, alert : Tuple, user: str, service: str) -> None:
        """
        Adds a number of alerts for a given user and action and ip

        :param action_id: the action id
        :param ip: the ip
        :param alert: the number of alerts
        :param user: the user
        :param service: the service
        :return: None
        """
        key = (action_id, ip, service, user)
        self.user_ip_alerts[key] = alert

    def user_ip_get_alert(self, action_id: Enum, ip: str, user: str, service: str) -> int:
        """
        Gets the number of alerts for a given user, ip, service and action

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param service: the service
        :return: the number of alerts
        """
        key = (action_id, ip, service, user)
        return self.user_ip_alerts[key]

    def user_ip_exists(self, action_id: Enum, ip: str, user: str, service: str) -> bool:
        """
        Checks if there is a number of alerts stored for a given action id, ip, user, and service

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param service: the service
        :return: true or false
        """
        key = (action_id, ip, service, user)
        return key in self.user_ip_alerts

    def pivot_scan_add_alert(self, action_id: Enum, ip: str, alert : Tuple, user: str, target_ip: str) \
            -> None:
        """
        Add a number of alerts for a given action, ip, user, and target ip

        :param action_id: the action id
        :param ip: the ip
        :param alert: the number of alerts
        :param user: the user
        :param target_ip: the target ip
        :return: None
        """
        key = (action_id, ip, user, target_ip)
        self.pivot_scan_alerts[key] = alert

    def pivot_scan_get_alert(self, action_id: Enum, ip: str, user: str, target_ip: str) -> int:
        """
        Gets the number of alerts for a given action id, target ip, and user

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param target_ip: the target ip
        :return: the number of alerts
        """
        key = (action_id, ip, user, target_ip)
        return self.pivot_scan_alerts[key]

    def pivot_scan_exists(self, action_id: Enum, ip: str, user: str, target_ip: str) -> bool:
        """
        Checks if there is a number of alerts stored for a given user id and target ip

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param target_ip: the target ip
        :return: true or false
        """
        key = (action_id, ip, user, target_ip)
        return key in self.pivot_scan_alerts