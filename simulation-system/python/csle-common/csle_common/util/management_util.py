import bcrypt
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.management.management_user import ManagementUser


class ManagementUtil:
    """
    Class with utility functions for management of CSLE
    """

    @staticmethod
    def create_default_management_admin_account() -> None:
        """
        Creates the default management admin account

        :return: None
        """
        management_usernames = list(map(lambda x: x.username, MetastoreFacade.list_management_users()))
        if constants.CSLE_ADMIN.MANAGEMENT_USER not in management_usernames:
            Logger.__call__().get_logger().info(f"Creating management account with administrator privileges, "
                                                f"username: {constants.CSLE_ADMIN.MANAGEMENT_USER}")
            admin = True
            byte_pwd = constants.CSLE_ADMIN.MANAGEMENT_PW.encode('utf-8')
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(byte_pwd, salt)
            user = ManagementUser(username=constants.CSLE_ADMIN.MANAGEMENT_USER,
                                  password=pw_hash.decode("utf-8"), admin=admin, salt=salt.decode("utf-8"),
                                  first_name=constants.CSLE_ADMIN.MANAGEMENT_FIRST_NAME,
                                  last_name=constants.CSLE_ADMIN.MANAGEMENT_LAST_NAME,
                                  organization=constants.CSLE_ADMIN.MANAGEMENT_ORGANIZATION,
                                  email=constants.CSLE_ADMIN.MANAGEMENT_EMAIL)
            MetastoreFacade.save_management_user(management_user=user)
        else:
            Logger.__call__().get_logger().info(f"Management account with username: "
                                                f"{constants.CSLE_ADMIN.MANAGEMENT_USER} already exists")

    @staticmethod
    def create_default_management_guest_account() -> None:
        """
        Creates the default management guest account

        :return: None
        """
        management_usernames = list(map(lambda x: x.username, MetastoreFacade.list_management_users()))
        if constants.CSLE_GUEST.MANAGEMENT_USER not in management_usernames:
            Logger.__call__().get_logger().info(f"Creating management account without administrator privileges, "
                                                f"username: {constants.CSLE_GUEST.MANAGEMENT_USER}")
            admin = False
            byte_pwd = constants.CSLE_GUEST.MANAGEMENT_PW.encode('utf-8')
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(byte_pwd, salt)
            user = ManagementUser(username=constants.CSLE_GUEST.MANAGEMENT_USER,
                                  password=pw_hash.decode("utf-8"), admin=admin, salt=salt.decode("utf-8"),
                                  first_name=constants.CSLE_GUEST.MANAGEMENT_FIRST_NAME,
                                  last_name=constants.CSLE_GUEST.MANAGEMENT_LAST_NAME,
                                  organization=constants.CSLE_GUEST.MANAGEMENT_ORGANIZATION,
                                  email=constants.CSLE_GUEST.MANAGEMENT_EMAIL)
            MetastoreFacade.save_management_user(management_user=user)
        else:
            Logger.__call__().get_logger().info(f"Management account with username: "
                                                f"{constants.CSLE_GUEST.MANAGEMENT_USER} "
                                                f"already exists")
