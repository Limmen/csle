import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import pytest_mock


class TestMetastoreFacadeSuite:
    """
    Test suite for metastore_facade.py
    """

    def test_list_emulations(self, mocker: pytest_mock.MockFixture,
                             example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the list_emulations function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_emulation_env_config.id = 1
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_configs = MetastoreFacade.list_emulations()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_configs, list)
        assert isinstance(emulation_configs[0], EmulationEnvConfig)
        assert emulation_configs[0] == example_emulation_env_config

    def test_list_emulation_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulations_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id, "emulation1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_ids_and_names = MetastoreFacade.list_emulations_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,name FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_ids_and_names, list)
        assert isinstance(emulation_ids_and_names[0], tuple)
        assert emulation_ids_and_names[0] == example_record

    def test_convert_emulation_record_to_dto(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the _convert_emulation_record_to_dto function

        :param example_emulation_env_config: an example EmulationEnvConfig DTO
        :return: None
        """
        id = 1
        name = example_emulation_env_config.name
        example_emulation_env_config.id = 1
        example_record = (id, name, example_emulation_env_config.to_dict())
        converted_object = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=example_record)
        assert isinstance(converted_object, EmulationEnvConfig)
        assert converted_object == example_emulation_env_config

    def test_install_emulation(self, mocker: pytest_mock.MockFixture,
                               example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the install_emulation function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 2
        example_emulation_env_config.id = 1
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.install_emulation(config=example_emulation_env_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} "
                                                      f"(id, name, config) "
                                                      f"VALUES (%s, %s, %s) RETURNING id",
                                                      (id, example_emulation_env_config.name,
                                                       example_emulation_env_config.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id
