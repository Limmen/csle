from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken


class TestManagementDaoSuite:
    """
    Test suite for management data access objects (DAOs)
    """

    def test_management_user(self) -> None:
        """
        Tests creation and dict conversion of the ManagementUser DAO

        :return: None
        """

        management_user = ManagementUser(username="test1", password="test2", email="test@test.test", first_name="test3",
                                         last_name="test4", organization="testi", admin=False, salt="test")

        assert isinstance(management_user.to_dict(), dict)
        assert isinstance(ManagementUser.from_dict(management_user.to_dict()),
                          ManagementUser)
        assert (ManagementUser.from_dict(management_user.to_dict()).to_dict() ==
                management_user.to_dict())
        assert (ManagementUser.from_dict(management_user.to_dict()) ==
                management_user)

    def test_session_token(self) -> None:
        """
        Tests creation and dict conversion of the SessionToken DAO

        :return: None
        """
        
        session_token = SessionToken(token="test_token", timestamp=11.11, username="test")
        assert isinstance(session_token.to_dict(), dict)
        assert isinstance(SessionToken.from_dict(session_token.to_dict()),
                          SessionToken)
        assert (SessionToken.from_dict(session_token.to_dict()).to_dict() ==
                session_token.to_dict())
        assert (SessionToken.from_dict(session_token.to_dict()) ==
                session_token)
