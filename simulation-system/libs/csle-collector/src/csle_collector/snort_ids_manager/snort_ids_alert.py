import re
import datetime
import csle_collector.constants.constants as constants


class SnortIdsFastLogAlert:
    """
    DTO representing an alert entry in the fast log of Snort
    """

    def __init__(self, timestamp: float, priority: int, class_id: int) -> None:
        """
        Initializes the DTO

        :param timestamp: the timestamp of the record
        :param priority: the priority of the record
        :param class_id: the class id of the record
        """
        self.timestamp = timestamp
        self.priority = priority
        self.class_id = class_id


class SnortIdsAlert:
    """
    Object representing an IDS Alert
    """

    def __init__(self):
        """
        Initializes the IDS Alert Fields
        """
        self.timestamp = None
        self.sig_generator = None
        self.sig_id = None
        self.sig_rev = None
        self.msg = None
        self.proto = None
        self.src_ip = None
        self.src_port = None
        self.dst_ip = None
        self.dst_port = None
        self.eth_src = None
        self.eth_dst = None
        self.eth_len = None
        self.tcp_flags = None
        self.tcp_seq = None
        self.tcp_ack = None
        self.tcp_len = None
        self.tcp_window = None
        self.ttl = None
        self.tos = None
        self.id = id
        self.dgm_len = None
        self.ip_len = None
        self.icmp_type = None
        self.icmp_code = None
        self.icmp_id = None
        self.icmp_seq = None
        self.priority = None

    @staticmethod
    def parse_from_str(csv_str_record: str, year: int) -> "SnortIdsAlert":
        """
        Parses the IDS alert from a string

        :param csv_str_record: the string to parse
        :param year: the year of the entry
        :return: the parsed IDS Alert
        """
        if year is None:
            year = datetime.datetime.now().year
        a_fields = csv_str_record.split(",")
        alert_dao = SnortIdsAlert()
        if len(a_fields) > 1:
            alert_dao.timestamp = a_fields[0]
            if alert_dao.timestamp is not None and alert_dao.timestamp != "" and alert_dao.timestamp != "0":
                alert_dao.timestamp = str(year) + " " + alert_dao.timestamp
                try:
                    alert_dao.timestamp = datetime.datetime.strptime(alert_dao.timestamp.strip(),
                                                                     '%Y %m/%d-%H:%M:%S.%f').timestamp()
                except Exception:
                    alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                                     '%Y %m/%d-%H:%M:%S.%f').timestamp()
            else:
                alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                                 '%Y %m/%d-%H:%M:%S.%f').timestamp()
        else:
            alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                             '%Y %m/%d-%H:%M:%S.%f').timestamp()
        if len(a_fields) > 1:
            alert_dao.sig_generator = a_fields[1]
        if len(a_fields) > 2:
            alert_dao.sig_id = a_fields[2]
        if len(a_fields) > 3:
            alert_dao.sig_rev = a_fields[3]
        if len(a_fields) > 4:
            alert_dao.msg = a_fields[4]
        if len(a_fields) > 5:
            alert_dao.proto = a_fields[5]
        if len(a_fields) > 6:
            alert_dao.src_ip = a_fields[6]
        if len(a_fields) > 7:
            alert_dao.src_port = a_fields[7]
        if len(a_fields) > 8:
            alert_dao.dst_ip = a_fields[8]
        if len(a_fields) > 9:
            alert_dao.dst_port = a_fields[9]
        if len(a_fields) > 10:
            alert_dao.eth_src = a_fields[10]
        if len(a_fields) > 11:
            alert_dao.eth_dst = a_fields[11]
        if len(a_fields) > 12:
            alert_dao.eth_len = a_fields[12]
        if len(a_fields) > 13:
            alert_dao.tcp_flags = a_fields[13]
        if len(a_fields) > 14:
            alert_dao.tcp_seq = a_fields[14]
        if len(a_fields) > 15:
            alert_dao.tcp_ack = a_fields[15]
        if len(a_fields) > 16:
            alert_dao.tcp_len = a_fields[16]
        if len(a_fields) > 17:
            alert_dao.tcp_window = a_fields[17]
        if len(a_fields) > 18:
            alert_dao.ttl = a_fields[18]
        if len(a_fields) > 19:
            alert_dao.tos = a_fields[19]
        if len(a_fields) > 20:
            alert_dao.id = a_fields[20]
        if len(a_fields) > 21:
            alert_dao.dgm_len = a_fields[21]
        if len(a_fields) > 22:
            alert_dao.ip_len = a_fields[22]
        if len(a_fields) > 23:
            alert_dao.icmp_type = a_fields[23]
        if len(a_fields) > 24:
            alert_dao.icmp_code = a_fields[24]
        if len(a_fields) > 25:
            alert_dao.icmp_id = a_fields[25]
        if len(a_fields) > 26:
            alert_dao.icmp_seq = a_fields[26]
        alert_dao.priority = 1
        return alert_dao

    def set_priority(self, priority: int) -> None:
        """
        Sets the priority of the alert DTO

        :param priority: the priority to set
        :return: None
        """
        self.priority = priority

    @staticmethod
    def fast_log_parse(fast_log_str: str, year: int) -> SnortIdsFastLogAlert:
        """
        Parses the IDS Alert from a given string from the fast-log of Snort

        :param fast_log_str: the fast log string to parse
        :param year: the year
        :return: the priority, the class, and the time-stamp
        """
        priorities = re.findall(constants.SNORT_IDS_ROUTER.PRIORITY_REGEX, fast_log_str)
        if len(priorities) > 0:
            temp = priorities[0].replace("Priority: ", "")
            priority = int(temp)
        else:
            priority = 1
        alert_classes = re.findall(constants.SNORT_IDS_ROUTER.CLASSIFICATION_REGEX, fast_log_str)
        alert_class = "unknown"
        alert_class_id = 1
        if len(alert_classes) > 0:
            alert_class = alert_classes[0]
        if alert_class in constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID:
            alert_class_id = constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID[alert_class]

        ts = fast_log_str.split(" ")[0]
        if ts is not None and ts != "":
            ts = ts.strip()
            if ts != "":
                ts = str(year) + " " + ts
                try:
                    ts = datetime.datetime.strptime(ts.strip(), '%Y %m/%d-%H:%M:%S.%f').timestamp()
                except Exception:
                    ts = datetime.datetime.strptime("2010 04/20-08:46:14.094913", '%Y %m/%d-%H:%M:%S.%f').timestamp()
            else:
                ts = datetime.datetime.strptime("2010 04/20-08:46:14.094913", '%Y %m/%d-%H:%M:%S.%f').timestamp()
        fast_log_alert = SnortIdsFastLogAlert(timestamp=ts, priority=priority, class_id=alert_class_id)
        return fast_log_alert
