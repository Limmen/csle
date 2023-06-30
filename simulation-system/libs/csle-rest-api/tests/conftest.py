import pytest
from csle_common.dao.management.session_token import SessionToken


@pytest.fixture
def database(mocker):
    """
    Fixture for mocking the database

    :param mocker: the pytest mocker object
    :return: fixture for mocking the users in the database
    """
    import bcrypt
    from csle_common.dao.management.management_user import ManagementUser

    def get_management_user_by_username(username: str):
        if username == "admin":
            byte_pwd = "admin".encode("utf-8")
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(byte_pwd, salt)
            password = pw_hash.decode("utf-8")
            user = ManagementUser(
                username="admin",
                password=password,
                email="admin@CSLE.com",
                admin=True,
                first_name="Admin",
                last_name="Adminson",
                organization="CSLE",
                salt=salt.decode("utf-8"),
            )
            user.id = 1
            return user
        elif username == "guest":
            byte_pwd = "guest".encode("utf-8")
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(byte_pwd, salt)
            password = pw_hash.decode("utf-8")
            user = ManagementUser(
                username="guest",
                password=password,
                email="guest@CSLE.com",
                admin=False,
                first_name="Guest",
                last_name="Guestson",
                organization="CSLE",
                salt=salt.decode("utf-8"),
            )
            user.id = 2
            return user
        else:
            return None

    get_management_user_by_username_mock = mocker.MagicMock(
        side_effect=get_management_user_by_username
    )
    return get_management_user_by_username_mock


@pytest.fixture
def save(mocker):
    """
    Fixture for mocking the save_session_token call

    :param mocker: the pytest mocker object
    :return: fixture for mocking the save_session_token_call
    """
    def save_session_token(session_token: SessionToken) -> str:
        return "mytesttoken"

    save_session_token_mock = mocker.MagicMock(side_effect=save_session_token)
    return save_session_token_mock


@pytest.fixture
def token(mocker):
    """
    Fixture for mocking login tokens
    :param mocker: the pytest mocker object
    :return: the token fixture for mocking the token calls to the database
    """
    from csle_common.dao.management.session_token import SessionToken

    def get_session_token_by_username(username: str):
        if username == "admin":
            return SessionToken(token="123", timestamp=0.0, username="admin")
        elif username == "guest":
            return SessionToken(token="123", timestamp=0.0, username="guest")
        else:
            return None

    get_session_token_by_username_mock = mocker.MagicMock(
        side_effect=get_session_token_by_username
    )
    return get_session_token_by_username_mock


@pytest.fixture
def update(mocker):
    """
    Fixture for mocking the session-update function call

    :param mocker: the pytest mocker object
    :return: fixture for mocking the update_session_token call
    """
    def update_session_token(session_token: SessionToken, token: str) -> None:
        return None
    update_session_token_mock = mocker.MagicMock(side_effect=update_session_token)
    return update_session_token_mock
