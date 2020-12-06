import datetime

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


    @staticmethod
    def parse_from_str(a_str : str):
        a_fields = a_str.split(",")
        alert_dao = IdsAlert()
        alert_dao.timestamp = a_fields[0]
        if alert_dao.timestamp is not None and alert_dao.timestamp != "":
            alert_dao.timestamp = datetime.datetime.strptime(alert_dao.timestamp.strip(), '%m/%d-%H:%M:%S.%f').timestamp()
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
        return alert_dao


if __name__ == '__main__':
    test = "12/06-22:10:53.094913  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.18.4.191:58278 -> 172.18.4.10:161"
    parts = test.split(" ")
    ts = parts[0]
    import re
    regex = re.compile(r"Priority: \d")
    print(re.findall(regex, test))

    print(parts)