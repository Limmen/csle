from typing import List
from datetime import datetime
import subprocess
from csle_collector.ossec_ids_manager.ossec_ids_alert import OSSECIDSAlert
from csle_collector.ossec_ids_manager.ossec_ids_alert_counters import OSSECIdsAlertCounters
import csle_collector.constants.constants as constants


class OSSecManagerUtil:

    @staticmethod
    def check_ossec_ids_alerts() -> List[OSSECIDSAlert]:
        """
        Reads alerts from the OSSEC IDS alerts log

        :return: a list of alerts
        """
        cmd = constants.OSSEC.TAIL_ALERTS_COMMAND + " " + constants.OSSEC.OSSEC_ALERTS_FILE
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        alerts = []

        timestamp = " "
        groups = []
        host = " "
        ip = " "
        ruleid = " "
        level = 1
        desc = " "
        src = " "
        user = " "
        linesmatched=0
        for line in output.decode().split("\n"):
            linematched = 0

            # Test for matches. A line will have more than one matching RE.
            if constants.OSSEC.ALERTLINE_REGEX.match(line):
                linematched = 1
                match = constants.OSSEC.ALERTLINE_REGEX.match(line)
                groupstr = match.group(2).rstrip(',')
                groups = groupstr.split(',')

            if constants.OSSEC.DATELINEREGEX.match(line):
                linematched = 1
                match = constants.OSSEC.DATELINEREGEX.match(line)
                datestr = match.group(0)
                timestamp = datetime.strptime(datestr, "%Y %b %d %H:%M:%S")

            if constants.OSSEC.HOSTLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.HOSTLINE_REGEX.match(line)
                host = match.group(1)
                ip = match.group(2)

            if constants.OSSEC.SERVHOSTLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.SERVHOSTLINE_REGEX.match(line)
                host = match.group(1)
                ip = '0.0.0.0'

            if constants.OSSEC.RULELINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.RULELINE_REGEX.match(line)
                ruleid = match.group(1)
                level = match.group(2)
                desc = match.group(3)

            if constants.OSSEC.SRCIPLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.SRCIPLINE_REGEX.match(line)
                src = match.group(1)

            if constants.OSSEC.USERLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.USERLINE_REGEX.match(line)
                user = match.group(1)

            linesmatched += linematched

            if linematched == 0 and linesmatched > 0:
                if len(line) <= 1:
                    alert = OSSECIDSAlert(timestamp=datetime.timestamp(timestamp), groups=groups, host=host, ip=ip,
                                          rule_id=ruleid, level=level, descr=desc, src=src, user=user)
                    print(alert)
                    alerts.append(alert)
                    linesmatched = 0
                    timestamp = " "
                    groups = []
                    host = " "
                    ip = " "
                    ruleid = " "
                    level = 1
                    desc = " "
                    src = " "
                    user = " "
        return alerts

    @staticmethod
    def read_ossec_ids_data(episode_last_alert_ts : float) -> OSSECIdsAlertCounters:
        """
        Measures metrics from the OSSEC ids

        :param env_config: environment configuration
        :param episode_last_alert_ts: timestamp when the episode started
        :return: ids statistics
        """

        # Read OSSEC IDS data
        alerts = OSSecManagerUtil.check_ossec_ids_alerts()

        # Filter IDS data from beginning of episode
        alerts = list(filter(lambda x: x.timestamp > episode_last_alert_ts, alerts))

        counters = OSSECIdsAlertCounters()
        counters.count(alerts)

        return counters