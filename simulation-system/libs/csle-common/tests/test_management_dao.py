from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken


class TestManagementDaoSuite:
    """
    Test suite for management data access objects (DAOs)
    """

    def test_management_user(self, example_management_user: ManagementUser) -> None:
        """
        Tests creation and dict conversion of the ManagementUser DAO

        :param example_management_user: an example ManagementUser
        :return: None
        """
        assert isinstance(example_management_user.to_dict(), dict)
        assert isinstance(ManagementUser.from_dict(example_management_user.to_dict()), ManagementUser)
        assert ManagementUser.from_dict(example_management_user.to_dict()).to_dict() == \
               example_management_user.to_dict()
        assert ManagementUser.from_dict(example_management_user.to_dict()) == example_management_user

    def test_session_token(self, example_session_token: SessionToken) -> None:
        """
        Tests creation and dict conversion of the SessionToken DAO

        :param example_session_token: an example SessionToken
        :return: None
        """
        assert isinstance(example_session_token.to_dict(), dict)
        assert isinstance(SessionToken.from_dict(example_session_token.to_dict()), SessionToken)
        assert SessionToken.from_dict(example_session_token.to_dict()).to_dict() == example_session_token.to_dict()
        assert SessionToken.from_dict(example_session_token.to_dict()) == example_session_token
