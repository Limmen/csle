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


class TestEmulationActionResultDaoSuite:
    """
    Test suite for emulation action result data access objects (DAOs)
    """

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
