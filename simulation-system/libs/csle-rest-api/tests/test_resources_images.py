import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager_pb2 import ContainerImageDTO, ContainerImagesDTO
from csle_common.dao.emulation_config.config import Config
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesFlaskSuite:
    """
    Test suite for /config resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Pytest fixture for mocking the get_config method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_config(id: int) -> Config:
            conf = example_config
            return conf
        get_config_mocker = mocker.MagicMock(side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def list_c_im(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_all_container_images method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_all_container_images(ip: str, port: int) -> ContainerImagesDTO:
            cont_img = ContainerImageDTO(repoTags="JohnDoe", created="null", os="null", architecture="null", size=4)
            cont_images = ContainerImagesDTO(images=[cont_img])
            return cont_images
        list_all_container_images_mocker = mocker.MagicMock(side_effect=list_all_container_images)
        return list_all_container_images_mocker

    def test_images_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in, logged_in_as_admin,
                        config, list_c_im) -> None:
        """
        Testing the GET HTTPS method for the /images resource
        
        :param mocker: the pytest mocker object
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param list_c_im: the list_c_im fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_container_images",
                     side_effect=list_c_im)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.NAME_PROPERTY] == "JohnDoe"
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIZE_PROPERTY] == 4
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.NAME_PROPERTY] == "JohnDoe"
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIZE_PROPERTY] == 4
