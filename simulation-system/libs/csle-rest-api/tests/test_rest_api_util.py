import json

import csle_common.constants.constants as constants
import numpy as np
import pytest
import pytest_mock
from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken
from flask import Flask

import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_rest_api.rest_api import create_app


class TestUtilSuite:
    """
    Test suite for /experiments url
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def session_token(self, mocker):
        """
        Pytest fixture for mocking the get_session_token_metadata method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_session_token_metadata(token: str) -> SessionToken:
            return SessionToken(token="null", timestamp=1.5, username="JDoe")
        get_session_token_metadata_mocker = mocker.MagicMock(side_effect=get_session_token_metadata)
        return get_session_token_metadata_mocker
    
    @pytest.fixture
    def session_token_exp(self, mocker):
        """
        Pytest fixture for mocking the get_session_token_metadata method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_session_token_metadata(token: str) -> SessionToken:
            ses_tok = SessionToken(token="null", timestamp=1.5, username="JDoe")
            api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS = np.iinfo(np.int32).max
            return ses_tok
        get_session_token_metadata_mocker = mocker.MagicMock(side_effect=get_session_token_metadata)
        return get_session_token_metadata_mocker

    @pytest.fixture
    def management_user(self, mocker):
        """
        Pytest fixture for mocking the get_management_user_by_username method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_management_user_by_username(username: str) -> ManagementUser:
            mng_user = TestUtilSuite.get_synthetic_mng_user()
            return mng_user

        get_management_user_by_username_mocker = mocker.MagicMock(side_effect=get_management_user_by_username)
        return get_management_user_by_username_mocker

    @pytest.fixture
    def management_user_none(self, mocker):
        """
        Pytest fixture for mocking the get_management_user_by_username method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_management_user_by_username(username: str) -> None:
            return None

        get_management_user_by_username_mocker = mocker.MagicMock(side_effect=get_management_user_by_username)
        return get_management_user_by_username_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        Pytest fixture for mocking the reomve_session_token method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_session_token(session_token: SessionToken) -> None:
            return None
        remove_session_token_mocker = mocker.MagicMock(side_effect=remove_session_token)
        return remove_session_token_mocker

    @staticmethod
    def get_args():
        class Args():
            def __init__(self) -> None:
                pass

            def get(self, token: str):
                return None
        return Args()

    @staticmethod
    def get_synthetic_request(args):
        """
        Static help method for returning a synthetic/mocked request, customized to work for testing without the use
        of blueprint or flask app
        """
        class SyntReq():
            def __init__(self, args):
                self.args = args
        return SyntReq(args)

    @staticmethod
    def get_synthetic_mng_user():
        """
        static help method for returning a synthetic/mocked management user
        """
        mng_user = ManagementUser(username="JDoe", password="JDoe", email="jdoe@csle.com",
                                  first_name="John", last_name="Doe", organization="CSLE",
                                  admin=False, salt="null")
        return mng_user

    def test_util(self, flask_app, mocker: pytest_mock.MockFixture,
                  session_token, session_token_exp,
                  management_user, management_user_none, remove):
        """
        Test method for the rest-api util
        
        :param flask_app: the flask_app fixture
        :param mocker: the pytest mocker object
        :param session_token: the session_token fixture
        :param management_user: the management_user fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_metadata",
                     side_effect=session_token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_session_token",
                     side_effect=remove)
        app = Flask(__name__)
        mng_user = TestUtilSuite.get_synthetic_mng_user()
        args = TestUtilSuite.get_args()
        req = TestUtilSuite.get_synthetic_request(args)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req,
                                                                       user=mng_user)
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data1 = response1[0].data.decode("utf-8")
        response_data_dict1 = json.loads(response_data1)
        response_status_code1 = response1[1]
        assert response_data_dict1 == {}
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user_none)
        with app.app_context():
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req,
                                                                       user=mng_user)
        response_data1 = response1[0].data.decode("utf-8")
        response_data_dict1 = json.loads(response_data1)
        response_status_code1 = response1[1]
        assert response_data_dict1 == {}
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req,
                                                                       user=mng_user)
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_metadata",
                     side_effect=session_token_exp)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req,
                                                                       user=mng_user)
        assert response is None
        ex_mng_user = TestUtilSuite.get_synthetic_mng_user()
        assert response1.username == ex_mng_user.username
        assert response1.password == ex_mng_user.password
        assert response1.admin == ex_mng_user.admin
        assert response1.id == ex_mng_user.id
        assert response1.salt == ex_mng_user.salt
        assert response1.email == ex_mng_user.email
        assert response1.first_name == ex_mng_user.first_name
        assert response1.last_name == ex_mng_user.last_name
        assert response1.organization == ex_mng_user.organization
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req,
                                                                 requires_admin=True)
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
