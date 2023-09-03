from csle_common.dao.emulation_action_result.nikto_scan_result import NiktoScanResult
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult


class TestEmulationActionResultDaoSuite:
    """
    Test suite for emulation action result data access objects (DAOs)
    """

    def test_nikto_vuln(self, example_nikto_vuln: NiktoVuln) -> None:
        """
        Tests creation and dict conversion of the NiktoVuln DAO

        :param example_nikto_vuln: an example NiktoVuln
        :return: None
        """
        assert isinstance(example_nikto_vuln.to_dict(), dict)
        assert isinstance(NiktoVuln.from_dict(example_nikto_vuln.to_dict()), NiktoVuln)
        assert NiktoVuln.from_dict(example_nikto_vuln.to_dict()).to_dict() == example_nikto_vuln.to_dict()
        assert NiktoVuln.from_dict(example_nikto_vuln.to_dict()) == example_nikto_vuln

    def test_nikto_scan_result(self, example_nikto_scan_result: NiktoScanResult) -> None:
        """
        Tests creation and dict conversion of the NiktoScanResult DAO

        :param example_nikto_scan_result: an example NiktoScanResult
        :return: None
        """
        assert isinstance(example_nikto_scan_result.to_dict(), dict)
        assert isinstance(NiktoScanResult.from_dict(example_nikto_scan_result.to_dict()), NiktoScanResult)
        assert NiktoScanResult.from_dict(example_nikto_scan_result.to_dict()).to_dict() == \
               example_nikto_scan_result.to_dict()
        assert NiktoScanResult.from_dict(example_nikto_scan_result.to_dict()) == example_nikto_scan_result

    def test_nmap_brute_credentials(self, example_nmap_brute_credentials: NmapBruteCredentials) -> None:
        """
        Tests creation and dict conversion of the NmapBruteCredentials DAO

        :param example_nmap_brute_credentials: an example NmapBruteCredentials
        :return: None
        """
        assert isinstance(example_nmap_brute_credentials.to_dict(), dict)
        assert isinstance(NmapBruteCredentials.from_dict(example_nmap_brute_credentials.to_dict()),
                          NmapBruteCredentials)
        assert NmapBruteCredentials.from_dict(example_nmap_brute_credentials.to_dict()).to_dict() \
               == example_nmap_brute_credentials.to_dict()
        assert NmapBruteCredentials.from_dict(example_nmap_brute_credentials.to_dict()) \
               == example_nmap_brute_credentials

    def test_nmap_hop(self, example_nmap_hop: NmapHop) -> None:
        """
        Tests creation and dict conversion of the NmapHop DAO

        :param example_nmap_hop: an example NmapHop
        :return: None
        """
        assert isinstance(example_nmap_hop.to_dict(), dict)
        assert isinstance(NmapHop.from_dict(example_nmap_hop.to_dict()), NmapHop)
        assert NmapHop.from_dict(example_nmap_hop.to_dict()).to_dict() == example_nmap_hop.to_dict()
        assert NmapHop.from_dict(example_nmap_hop.to_dict()) == example_nmap_hop

    def test_nmap_http_enum(self, example_nmap_http_enum: NmapHttpEnum) -> None:
        """
        Tests creation and dict conversion of the NmapHttpEnum DAO

        :param example_nmap_http_enum: an example NmapHttpEnum
        :return: None
        """
        assert isinstance(example_nmap_http_enum.to_dict(), dict)
        assert isinstance(NmapHttpEnum.from_dict(example_nmap_http_enum.to_dict()), NmapHttpEnum)
        assert NmapHttpEnum.from_dict(example_nmap_http_enum.to_dict()).to_dict() == example_nmap_http_enum.to_dict()
        assert NmapHttpEnum.from_dict(example_nmap_http_enum.to_dict()) == example_nmap_http_enum

    def test_nmap_http_grep(self, example_nmap_http_grep: NmapHttpGrep) -> None:
        """
        Tests creation and dict conversion of the NmapHTTPGrep DAO

        :param example_nmap_http_grep: an example NmapHttpGrep
        :return: None
        """
        assert isinstance(example_nmap_http_grep.to_dict(), dict)
        assert isinstance(NmapHttpGrep.from_dict(example_nmap_http_grep.to_dict()), NmapHttpGrep)
        assert NmapHttpGrep.from_dict(example_nmap_http_grep.to_dict()).to_dict() == example_nmap_http_grep.to_dict()
        assert NmapHttpGrep.from_dict(example_nmap_http_grep.to_dict()) == example_nmap_http_grep

    def test_nmap_vulscan(self, example_nmap_vulscan: NmapVulscan) -> None:
        """
        Tests creation and dict conversion of the NmapVulScan DAO

        :param example_nmap_vulscan: an example NmapVulscan
        :return: None
        """
        assert isinstance(example_nmap_vulscan.to_dict(), dict)
        assert isinstance(NmapVulscan.from_dict(example_nmap_vulscan.to_dict()), NmapVulscan)
        assert NmapVulscan.from_dict(example_nmap_vulscan.to_dict()).to_dict() == example_nmap_vulscan.to_dict()
        assert NmapVulscan.from_dict(example_nmap_vulscan.to_dict()) == example_nmap_vulscan

    def test_nmap_os(self, example_nmap_os: NmapOs) -> None:
        """
        Tests creation and dict conversion of the NmapHTTPGrep DAO

        :param example_nmap_os: an example NmapOs
        :return: None
        """
        assert isinstance(example_nmap_os.to_dict(), dict)
        assert isinstance(NmapOs.from_dict(example_nmap_os.to_dict()), NmapOs)
        assert NmapOs.from_dict(example_nmap_os.to_dict()).to_dict() == example_nmap_os.to_dict()
        assert NmapOs.from_dict(example_nmap_os.to_dict()) == example_nmap_os

    def test_nmap_port(self, example_nmap_port: NmapPort) -> None:
        """
        Tests creation and dict conversion of the NmapPort DAO

        :param example_nmap_port: an example NmapPort
        :return: None
        """
        assert isinstance(example_nmap_port.to_dict(), dict)
        assert isinstance(NmapPort.from_dict(example_nmap_port.to_dict()), NmapPort)
        assert NmapPort.from_dict(example_nmap_port.to_dict()).to_dict() == example_nmap_port.to_dict()
        assert NmapPort.from_dict(example_nmap_port.to_dict()) == example_nmap_port

    def test_nmap_trace(self, example_nmap_trace: NmapTrace) -> None:
        """
        Tests creation and dict conversion of the NmapTrace DAO

        :param example_nmap_trace: an example NmapTrace
        :return: None
        """
        assert isinstance(example_nmap_trace.to_dict(), dict)
        assert isinstance(NmapTrace.from_dict(example_nmap_trace.to_dict()), NmapTrace)
        assert NmapTrace.from_dict(example_nmap_trace.to_dict()).to_dict() == example_nmap_trace.to_dict()
        assert NmapTrace.from_dict(example_nmap_trace.to_dict()) == example_nmap_trace

    def test_nmap_vuln(self, example_nmap_vuln: NmapVuln) -> None:
        """
        Tests creation and dict conversion of the NmapVuln DAO

        :param example_nmap_vuln: an example NmapVuln
        :return: None
        """
        assert isinstance(example_nmap_vuln.to_dict(), dict)
        assert isinstance(NmapVuln.from_dict(example_nmap_vuln.to_dict()), NmapVuln)
        assert NmapVuln.from_dict(example_nmap_vuln.to_dict()).to_dict() == example_nmap_vuln.to_dict()
        assert NmapVuln.from_dict(example_nmap_vuln.to_dict()) == example_nmap_vuln

    def test_nmap_host_result(self, example_nmap_host_result: NmapHostResult) -> None:
        """
        Tests creation and dict conversion of the NmapHostResult

        :param example_nmap_host_result: an example NmapHostResult
        :return: None
        """
        assert isinstance(example_nmap_host_result.to_dict(), dict)
        assert isinstance(NmapHostResult.from_dict(example_nmap_host_result.to_dict()), NmapHostResult)
        assert NmapHostResult.from_dict(
            example_nmap_host_result.to_dict()).to_dict() == example_nmap_host_result.to_dict()
        assert NmapHostResult.from_dict(example_nmap_host_result.to_dict()) == example_nmap_host_result

    def test_nmap_scan_result(self, example_nmap_scan_result: NmapScanResult) -> None:
        """
        Tests creation and dict conversion of the NmapScanResult

        :return: None
        """
        assert isinstance(example_nmap_scan_result.to_dict(), dict)
        assert isinstance(NmapScanResult.from_dict(example_nmap_scan_result.to_dict()), NmapScanResult)
        assert NmapScanResult.from_dict(example_nmap_scan_result.to_dict()).to_dict() == \
               example_nmap_scan_result.to_dict()
        assert NmapScanResult.from_dict(example_nmap_scan_result.to_dict()) == example_nmap_scan_result
