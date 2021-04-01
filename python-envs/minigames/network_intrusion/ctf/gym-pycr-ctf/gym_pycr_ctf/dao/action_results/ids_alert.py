import datetime
import re
import gym_pycr_ctf.constants.constants as constants

class IdsAlert:

    def __init__(self):
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
    def parse_from_str(csv_str_record : str, year: int):
        a_fields = csv_str_record.split(",")
        alert_dao = IdsAlert()
        alert_dao.timestamp = a_fields[0]
        alert_dao.timestamp = str(year) + " " + alert_dao.timestamp
        if alert_dao.timestamp is not None and alert_dao.timestamp != "":
            alert_dao.timestamp = datetime.datetime.strptime(alert_dao.timestamp.strip(), '%Y %m/%d-%H:%M:%S.%f').timestamp()
        alert_dao.sig_generator = a_fields[1]
        alert_dao.sig_id = a_fields[2]
        alert_dao.sig_rev = a_fields[3]
        alert_dao.msg = a_fields[4]
        alert_dao.proto = a_fields[5]
        alert_dao.src_ip = a_fields[6]
        alert_dao.src_port = a_fields[7]
        alert_dao.dst_ip = a_fields[8]
        alert_dao.dst_port = a_fields[9]
        alert_dao.eth_src = a_fields[10]
        alert_dao.eth_dst = a_fields[11]
        alert_dao.eth_len = a_fields[12]
        alert_dao.tcp_flags = a_fields[13]
        alert_dao.tcp_seq = a_fields[14]
        alert_dao.tcp_ack = a_fields[15]
        alert_dao.tcp_len = a_fields[16]
        alert_dao.tcp_window = a_fields[17]
        alert_dao.ttl = a_fields[18]
        alert_dao.tos = a_fields[19]
        alert_dao.id = a_fields[20]
        alert_dao.dgm_len = a_fields[21]
        alert_dao.ip_len = a_fields[22]
        alert_dao.icmp_type = a_fields[23]
        alert_dao.icmp_code = a_fields[24]
        alert_dao.icmp_id = a_fields[25]
        alert_dao.icmp_seq = a_fields[26]
        alert_dao.priority = 1
        return alert_dao

    def set_priority(self, priority):
        self.priority = priority

    @staticmethod
    def fast_log_parse(fast_log_str: str, year: int):
        priorities = re.findall(constants.IDS_ROUTER.PRIORITY_REGEX, fast_log_str)
        priority = None
        if len(priorities) > 0:
            temp = priorities[0].replace("Priority: ", "")
            priority = int(temp)
        ts = fast_log_str.split(" ")[0]
        ts = ts.strip()
        ts = str(year) + " " + ts
        if ts is not None and ts != "":
            ts = datetime.datetime.strptime(ts.strip(), '%Y %m/%d-%H:%M:%S.%f').timestamp()
        return priority, ts


if __name__ == '__main__':
    test = "12/06-22:10:53.094913  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.18.4.191:58278 -> 172.18.4.10:161"
    ts = test.split(" ")[0]
    print(ts)
    parts = test.split(" ")
    ts = parts[0]
    import re
    regex = re.compile(r"Priority: \d")
    print(re.findall(regex, test))

    print(parts)