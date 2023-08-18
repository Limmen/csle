from csle_common.util.general_util import GeneralUtil


class TestShellUtilSuite:
    """
    Test suite for general_util.py
    """

    def test_execute_service_login_helper(self) -> None:
        """
        Tests the replace_first_octet_of_ip function

        :return: None
        """
        assert GeneralUtil.replace_first_octet_of_ip(ip="127.0.0.1", ip_first_octet=1) == "1.0.0.1"
        assert GeneralUtil.replace_first_octet_of_ip(ip="<execution_id>.0.0.1", ip_first_octet=19) == "19.0.0.1"
        assert GeneralUtil.replace_first_octet_of_ip(ip="<execution_id>.125.251.19", ip_first_octet=128) == \
               "128.125.251.19"
