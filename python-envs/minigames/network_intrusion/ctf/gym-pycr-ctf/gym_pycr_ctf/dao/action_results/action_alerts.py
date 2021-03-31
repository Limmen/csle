from typing import Tuple
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId

class ActionAlerts:

    def __init__(self):
        self.alerts = {}
        self.user_ip_alerts = {}
        self.pivot_scan_alerts = {}

    def add_alert(self, action_id : AttackerActionId, ip: str, alert : Tuple):
        key = (action_id, ip)
        self.alerts[key] = alert

    def get_alert(self, action_id : AttackerActionId, ip: str):
        key = (action_id, ip)
        return self.alerts[key]

    def exists(self, action_id: AttackerActionId, ip: str):
        key = (action_id, ip)
        return key in self.alerts

    def user_ip_add_alert(self, action_id: AttackerActionId, ip: str, alert : Tuple, user: str, service: str):
        key = (action_id, ip, service, user)
        self.user_ip_alerts[key] = alert

    def user_ip_get_alert(self, action_id: AttackerActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return self.user_ip_alerts[key]

    def user_ip_exists(self, action_id: AttackerActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return key in self.user_ip_alerts

    def pivot_scan_add_alert(self, action_id: AttackerActionId, ip: str, alert : Tuple, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        self.pivot_scan_alerts[key] = alert

    def pivot_scan_get_alert(self, action_id: AttackerActionId, ip: str, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        return self.pivot_scan_alerts[key]

    def pivot_scan_exists(self, action_id: AttackerActionId, ip: str, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        return key in self.pivot_scan_alerts