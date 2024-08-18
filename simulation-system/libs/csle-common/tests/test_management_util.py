import csle_common.constants.constants as constants
from csle_common.util.management_util import ManagementUtil
from unittest.mock import patch


class TestManagementUtilSuite:
    """
    Test suite for management util
    """

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users")
    @patch("bcrypt.gensalt")
    @patch("bcrypt.hashpw")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_management_user")
    def test_create_default_management_admin_account(self, mock_save_management_user, mock_hashpw, mock_gensalt,
                                                     mock_list_management_users) -> None:
        """
        Test the method that creates the default management admin account

        :param mock_save_management_user: mock_save_management_user
        :param mock_hashpw: mock_hashpw
        :param mock_gensalt: mock_gensalt
        :param mock_list_management_users: mock_list_management_users
        :return: None
        """
        mock_list_management_users.return_value = []
        mock_salt = b"salt"
        mock_gensalt.return_value = mock_salt
        mock_hash = b"hashed_password"
        mock_hashpw.return_value = mock_hash
        constants.CSLE_ADMIN.MANAGEMENT_USER = "admin"
        constants.CSLE_ADMIN.MANAGEMENT_PW = "password"
        constants.CSLE_ADMIN.MANAGEMENT_FIRST_NAME = "first"
        constants.CSLE_ADMIN.MANAGEMENT_LAST_NAME = "last"
        constants.CSLE_ADMIN.MANAGEMENT_ORGANIZATION = "organization"
        constants.CSLE_ADMIN.MANAGEMENT_EMAIL = "admin@email.com"
        ManagementUtil.create_default_management_admin_account()
        mock_list_management_users.assert_called_once()
        mock_gensalt.assert_called_once()
        mock_hashpw.assert_called_once_with(constants.CSLE_ADMIN.MANAGEMENT_PW.encode("utf-8"), mock_salt)
        mock_save_management_user.assert_called_once()

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users")
    @patch("bcrypt.gensalt")
    @patch("bcrypt.hashpw")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_management_user")
    def test_create_default_management_guest_account(self, mock_save_management_user, mock_hashpw, mock_gensalt,
                                                     mock_list_management_users) -> None:
        """
        Test the method that creates the default management guest account

        :param mock_save_management_user: mock_save_management_user
        :param mock_hashpw: mock_hashpw
        :param mock_gensalt: mock_gensalt
        :param mock_list_management_users: mock_list_management_users
        :return: None
        """
        mock_list_management_users.return_value = []
        mock_salt = b"salt"
        mock_gensalt.return_value = mock_salt
        mock_hash = b"hashed_password"
        mock_hashpw.return_value = mock_hash
        constants.CSLE_GUEST.MANAGEMENT_USER = "user"
        constants.CSLE_GUEST.MANAGEMENT_PW = "password"
        constants.CSLE_GUEST.MANAGEMENT_FIRST_NAME = "guest_first"
        constants.CSLE_GUEST.MANAGEMENT_LAST_NAME = "guest_last"
        constants.CSLE_GUEST.MANAGEMENT_ORGANIZATION = "guest_organization"
        constants.CSLE_GUEST.MANAGEMENT_EMAIL = "guest@email.com"
        ManagementUtil.create_default_management_guest_account()
        mock_list_management_users.assert_called_once()
        mock_gensalt.assert_called_once()
        mock_hashpw.assert_called_once_with(constants.CSLE_GUEST.MANAGEMENT_PW.encode("utf-8"), mock_salt)
        mock_save_management_user.assert_called_once()
