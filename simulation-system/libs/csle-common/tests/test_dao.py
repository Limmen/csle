import time
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig
from csle_common.dao.emulation_action_result.nikto_scan_result import NiktoScanResult
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_port_status import NmapPortStatus
from csle_common.dao.emulation_action_result.nmap_host_status import NmapHostStatus
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult


class TestDaoSuite:
    """
    Test suite for data access objects (DAOs)
    """

    def test_traces_dataset(self) -> None:
        """
        Tests creation and dict conversion of the TracesDataset DAO

        :return: None
        """
        dataset = TracesDataset(name="test_dataset", description="test_descr", download_count=100,
                                file_path="test_path", url="test_url", date_added=time.time(),
                                size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                num_files=50, file_format="json", added_by="testadded", columns="col1,col2",
                                data_schema={}, num_attributes_per_time_step=10, num_traces=15)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(TracesDataset.from_dict(dataset.to_dict()), TracesDataset)
        assert TracesDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert TracesDataset.from_dict(dataset.to_dict()) == dataset

    def test_statistics_dataset(self) -> None:
        """
        Tests creation and dict conversion of the StatisticsDataset DAO

        :return: None
        """
        dataset = StatisticsDataset(name="test_dataset", description="test_descr", download_count=100,
                                    file_path="test_path", url="test_url", date_added=time.time(), num_measurements=100,
                                    num_metrics=10, size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                    num_files=50, file_format="json", added_by="testadded", conditions="cond1,cond2",
                                    metrics="metric1,metric2", num_conditions=10)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(StatisticsDataset.from_dict(dataset.to_dict()), StatisticsDataset)
        assert StatisticsDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert StatisticsDataset.from_dict(dataset.to_dict()) == dataset

    def test_docker_container_metadata(self) -> None:
        """
        Tests creation and dict conversion of the DockerContainerMetadata DAO

        :return: None
        """
        container_metadata = DockerContainerMetadata(
            name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
            created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
            name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
            config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")
        assert isinstance(container_metadata.to_dict(), dict)
        assert isinstance(DockerContainerMetadata.from_dict(container_metadata.to_dict()), DockerContainerMetadata)
        assert DockerContainerMetadata.from_dict(container_metadata.to_dict()).to_dict() == container_metadata.to_dict()
        assert DockerContainerMetadata.from_dict(container_metadata.to_dict()) == container_metadata

    def test_docker_env_metadata(self) -> None:
        """
        Tests creation and dict conversion of the DockerEnvMetadata DAO

        :return: None
        """
        container = DockerContainerMetadata(
            name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
            created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
            name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
            config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")
        docker_env_metadata = DockerEnvMetadata(
            containers=[container], name="myenv", subnet_prefix="myprefix", subnet_mask="mymask", level="mylevel",
            config=None, kafka_config=None)
        assert isinstance(docker_env_metadata.to_dict(), dict)
        assert isinstance(DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()), DockerEnvMetadata)
        assert DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()).to_dict() == docker_env_metadata.to_dict()
        assert DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()) == docker_env_metadata

    def test_emulation_attacker_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerAction DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        assert isinstance(emulation_attacker_action.to_dict(), dict)
        assert isinstance(EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()),
                          EmulationAttackerAction)
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()).to_dict() == \
               emulation_attacker_action.to_dict()
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()) == emulation_attacker_action

    def test_emulation_attacker_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerActionConfig DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        emulation_attacker_action_config = EmulationAttackerActionConfig(
            num_indices=10, actions=[emulation_attacker_action],
            nmap_action_ids=[EmulationAttackerActionId.NMAP_VULNERS_ALL],
            network_service_action_ids=[EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST],
            shell_action_ids=[EmulationAttackerActionId.CVE_2015_1427_EXPLOIT],
            nikto_action_ids=[EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN],
            masscan_action_ids=[EmulationAttackerActionId.MASSCAN_ALL_SCAN],
            stopping_action_ids=[EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE])
        assert isinstance(emulation_attacker_action_config.to_dict(), dict)
        assert isinstance(EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()),
                          EmulationAttackerActionConfig)
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()).to_dict() == \
               emulation_attacker_action_config.to_dict()
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()) == \
               emulation_attacker_action_config

    def test_emulation_defender_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderAction DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        assert isinstance(emulation_defender_action.to_dict(), dict)
        assert isinstance(EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()),
                          EmulationDefenderAction)
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()).to_dict() == \
               emulation_defender_action.to_dict()
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()) == emulation_defender_action

    def test_emulation_defender_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderActionConfig DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        emulation_defender_action_config = EmulationDefenderActionConfig(
            num_indices=10, actions=[emulation_defender_action],
            stopping_action_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE],
            multiple_stop_actions=[],
            multiple_stop_actions_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE])
        assert isinstance(emulation_defender_action_config.to_dict(), dict)
        assert isinstance(EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()),
                          EmulationDefenderActionConfig)
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()).to_dict() == \
               emulation_defender_action_config.to_dict()
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()) == \
               emulation_defender_action_config

    def test_nikto_vuln(self) -> None:
        """
        Tests creation and dict conversion of the NiktoVuln DAO

        :return: None
        """
        nikto_vuln = NiktoVuln(id="testid", osvdb_id=15, method="test", iplink="test2", namelink="test3", uri="test4",
                               description="test5")
        assert isinstance(nikto_vuln.to_dict(), dict)
        assert isinstance(NiktoVuln.from_dict(nikto_vuln.to_dict()), NiktoVuln)
        assert NiktoVuln.from_dict(nikto_vuln.to_dict()).to_dict() == nikto_vuln.to_dict()
        assert NiktoVuln.from_dict(nikto_vuln.to_dict()) == nikto_vuln

    def test_nikto_scan_result(self) -> None:
        """
        Tests creation and dict conversion of the NiktoScanResult DAO

        :return: None
        """
        nikto_vuln = NiktoVuln(id="testid", osvdb_id=15, method="test", iplink="test2", namelink="test3", uri="test4",
                               description="test5")
        scan_result = NiktoScanResult(port=3333, ip="192.168.1.1", sitename="test", vulnerabilities=[nikto_vuln])
        assert isinstance(scan_result.to_dict(), dict)
        assert isinstance(NiktoScanResult.from_dict(scan_result.to_dict()), NiktoScanResult)
        assert NiktoScanResult.from_dict(scan_result.to_dict()).to_dict() == scan_result.to_dict()
        assert NiktoScanResult.from_dict(scan_result.to_dict()) == scan_result

    def test_nmap_brute_credentials(self) -> None:
        """
        Tests creation and dict conversion of the NmapBruteCredentials DAO

        :return: None
        """
        nmap_brute_credentaisl = NmapBruteCredentials(
            username="testuser", pw="testpw", state="teststate", port=3333, protocol=TransportProtocol.TCP,
            service="testservice")
        assert isinstance(nmap_brute_credentaisl.to_dict(), dict)
        assert isinstance(NmapBruteCredentials.from_dict(nmap_brute_credentaisl.to_dict()), NmapBruteCredentials)
        assert NmapBruteCredentials.from_dict(nmap_brute_credentaisl.to_dict()).to_dict() \
               == nmap_brute_credentaisl.to_dict()
        assert NmapBruteCredentials.from_dict(nmap_brute_credentaisl.to_dict()) == nmap_brute_credentaisl

    def test_nmap_hop(self) -> None:
        """
        Tests creation and dict conversion of the NmapHop DAO

        :return: None
        """
        nmap_hop = NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")
        assert isinstance(nmap_hop.to_dict(), dict)
        assert isinstance(NmapHop.from_dict(nmap_hop.to_dict()), NmapHop)
        assert NmapHop.from_dict(nmap_hop.to_dict()).to_dict() == nmap_hop.to_dict()
        assert NmapHop.from_dict(nmap_hop.to_dict()) == nmap_hop

    def test_nmap_http_enum(self) -> None:
        """
        Tests creation and dict conversion of the NmapHttpEnum DAO

        :return: None
        """
        nmap_http_enum = NmapHttpEnum(output="testout")
        assert isinstance(nmap_http_enum.to_dict(), dict)
        assert isinstance(NmapHttpEnum.from_dict(nmap_http_enum.to_dict()), NmapHttpEnum)
        assert NmapHttpEnum.from_dict(nmap_http_enum.to_dict()).to_dict() == nmap_http_enum.to_dict()
        assert NmapHttpEnum.from_dict(nmap_http_enum.to_dict()) == nmap_http_enum

    def test_nmap_http_grep(self) -> None:
        """
        Tests creation and dict conversion of the NmapHTTPGrep DAO

        :return: None
        """
        nmap_http_grep = NmapHttpGrep(output="testout")
        assert isinstance(nmap_http_grep.to_dict(), dict)
        assert isinstance(NmapHttpGrep.from_dict(nmap_http_grep.to_dict()), NmapHttpGrep)
        assert NmapHttpGrep.from_dict(nmap_http_grep.to_dict()).to_dict() == nmap_http_grep.to_dict()
        assert NmapHttpGrep.from_dict(nmap_http_grep.to_dict()) == nmap_http_grep

    def test_nmap_vulscan(self) -> None:
        """
        Tests creation and dict conversion of the NmapVulScan DAO

        :return: None
        """
        nmap_vulscan = NmapVulscan(output="testout")
        assert isinstance(nmap_vulscan.to_dict(), dict)
        assert isinstance(NmapVulscan.from_dict(nmap_vulscan.to_dict()), NmapVulscan)
        assert NmapVulscan.from_dict(nmap_vulscan.to_dict()).to_dict() == nmap_vulscan.to_dict()
        assert NmapVulscan.from_dict(nmap_vulscan.to_dict()) == nmap_vulscan

    def test_nmap_os(self) -> None:
        """
        Tests creation and dict conversion of the NmapHTTPGrep DAO

        :return: None
        """
        nmap_os = NmapOs(name="testosName", vendor="osvendor", osfamily="osfam", accuracy=5)
        assert isinstance(nmap_os.to_dict(), dict)
        assert isinstance(NmapOs.from_dict(nmap_os.to_dict()), NmapOs)
        assert NmapOs.from_dict(nmap_os.to_dict()).to_dict() == nmap_os.to_dict()
        assert NmapOs.from_dict(nmap_os.to_dict()) == nmap_os

    def test_nmap_port(self) -> None:
        """
        Tests creation and dict conversion of the NmapPort DAO

        :return: None
        """
        nmap_http_grep = NmapHttpGrep(output="testout")
        nmap_http_enum = NmapHttpEnum(output="testout")
        nmap_vulscan = NmapVulscan(output="testout")
        nmap_port = NmapPort(port_id=1, protocol=TransportProtocol.UDP, status=NmapPortStatus.UP,
                             service_version="testservice", http_enum=nmap_http_enum, http_grep=nmap_http_grep,
                             service_fp="test_fp", vulscan=nmap_vulscan, service_name="testervicename")
        assert isinstance(nmap_port.to_dict(), dict)
        assert isinstance(NmapPort.from_dict(nmap_port.to_dict()), NmapPort)
        assert NmapPort.from_dict(nmap_port.to_dict()).to_dict() == nmap_port.to_dict()
        assert NmapPort.from_dict(nmap_port.to_dict()) == nmap_port

    def test_nmap_trace(self) -> None:
        """
        Tests creation and dict conversion of the NmapTrace DAO

        :return: None
        """
        nmap_hop = NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")
        nmap_trace = NmapTrace(hops=[nmap_hop])
        assert isinstance(nmap_trace.to_dict(), dict)
        assert isinstance(NmapTrace.from_dict(nmap_trace.to_dict()), NmapTrace)
        assert NmapTrace.from_dict(nmap_trace.to_dict()).to_dict() == nmap_trace.to_dict()
        assert NmapTrace.from_dict(nmap_trace.to_dict()) == nmap_trace

    def test_nmap_vuln(self) -> None:
        """
        Tests creation and dict conversion of the NmapVuln DAO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                                service="myservice", root=False)
        nmap_vuln = NmapVuln(name="vuln_name", port=4443, protocol=TransportProtocol.TCP, cvss=0.1,
                             service="testservice", credentials=[credential])
        assert isinstance(nmap_vuln.to_dict(), dict)
        assert isinstance(NmapVuln.from_dict(nmap_vuln.to_dict()), NmapVuln)
        assert NmapVuln.from_dict(nmap_vuln.to_dict()).to_dict() == nmap_vuln.to_dict()
        assert NmapVuln.from_dict(nmap_vuln.to_dict()) == nmap_vuln

    def test_nmap_host_result(self) -> None:
        """
        Tests creation and dict conversion of the NmapHostResult

        :return: None
        """
        nmap_hop = NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")
        nmap_trace = NmapTrace(hops=[nmap_hop])
        credential = Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                                service="myservice", root=False)
        nmap_vuln = NmapVuln(name="vuln_name", port=4443, protocol=TransportProtocol.TCP, cvss=0.1,
                             service="testservice", credentials=[credential])
        nmap_http_grep = NmapHttpGrep(output="testout")
        nmap_http_enum = NmapHttpEnum(output="testout")
        nmap_vulscan = NmapVulscan(output="testout")
        nmap_port = NmapPort(port_id=1, protocol=TransportProtocol.UDP, status=NmapPortStatus.UP,
                             service_version="testservice", http_enum=nmap_http_enum, http_grep=nmap_http_grep,
                             service_fp="test_fp", vulscan=nmap_vulscan, service_name="testervicename")
        nmap_os = NmapOs(name="testosName", vendor="osvendor", osfamily="osfam", accuracy=5)
        nmap_brute_credentaisl = NmapBruteCredentials(
            username="testuser", pw="testpw", state="teststate", port=3333, protocol=TransportProtocol.TCP,
            service="testservice")
        credential = Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                                service="myservice", root=False)
        nmap_host_result = NmapHostResult(
            status=NmapHostStatus.UP, ips=["172.151.51.2"], mac_addr="00-B0-D0-63-C2-26", hostnames=["testhost"],
            ports=[nmap_port], os=nmap_os, os_matches=[nmap_os],
            vulnerabilities=[nmap_vuln], credentials=[nmap_brute_credentaisl], trace=nmap_trace
        )
        assert isinstance(nmap_host_result.to_dict(), dict)
        assert isinstance(NmapHostResult.from_dict(nmap_host_result.to_dict()), NmapHostResult)
        assert NmapHostResult.from_dict(nmap_host_result.to_dict()).to_dict() == nmap_host_result.to_dict()
        assert NmapHostResult.from_dict(nmap_host_result.to_dict()) == nmap_host_result

    def test_nmap_scan_result(self) -> None:
        """
        Tests creation and dict conversion of the NmapScanResult

        :return: None
        """
        nmap_hop = NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")
        nmap_trace = NmapTrace(hops=[nmap_hop])
        credential = Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                                service="myservice", root=False)
        nmap_vuln = NmapVuln(name="vuln_name", port=4443, protocol=TransportProtocol.TCP, cvss=0.1,
                             service="testservice", credentials=[credential])
        nmap_http_grep = NmapHttpGrep(output="testout")
        nmap_http_enum = NmapHttpEnum(output="testout")
        nmap_vulscan = NmapVulscan(output="testout")
        nmap_port = NmapPort(port_id=1, protocol=TransportProtocol.UDP, status=NmapPortStatus.UP,
                             service_version="testservice", http_enum=nmap_http_enum, http_grep=nmap_http_grep,
                             service_fp="test_fp", vulscan=nmap_vulscan, service_name="testervicename")
        nmap_os = NmapOs(name="testosName", vendor="osvendor", osfamily="osfam", accuracy=5)
        nmap_brute_credentaisl = NmapBruteCredentials(
            username="testuser", pw="testpw", state="teststate", port=3333, protocol=TransportProtocol.TCP,
            service="testservice")
        credential = Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                                service="myservice", root=False)
        nmap_host_result = NmapHostResult(
            status=NmapHostStatus.UP, ips=["172.151.51.2"], mac_addr="00-B0-D0-63-C2-26", hostnames=["testhost"],
            ports=[nmap_port], os=nmap_os, os_matches=[nmap_os],
            vulnerabilities=[nmap_vuln], credentials=[nmap_brute_credentaisl], trace=nmap_trace
        )
        nmap_scan_result = NmapScanResult(hosts=[nmap_host_result], ips=["192.168.5.1"])
        assert isinstance(nmap_scan_result.to_dict(), dict)
        assert isinstance(NmapScanResult.from_dict(nmap_scan_result.to_dict()), NmapScanResult)
        assert NmapScanResult.from_dict(nmap_scan_result.to_dict()).to_dict() == nmap_scan_result.to_dict()
        assert NmapScanResult.from_dict(nmap_scan_result.to_dict()) == nmap_scan_result
