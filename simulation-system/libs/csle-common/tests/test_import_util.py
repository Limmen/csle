from unittest.mock import patch, MagicMock
from csle_common.util.import_util import ImportUtil


class TestImportUtilSuite:
    """
    Test suite for import_util
    """
    
    @patch("os.path.exists")
    @patch("csle_common.dao.system_identification.emulation_statistics.EmulationStatistics.from_json_file")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_emulation_statistic")
    def test_import_emulation_statistics_from_disk_json(self, mock_save_emulation_statistic, mock_from_json_file,
                                                        mock_path_exists) -> None:
        """
        Test the method that imports emulation statistics from disk to the metastore

        :param mock_save_emulation_statistic: mock_save_emulation_statistic
        :param mock_from_json_file: mock_from_json_file
        :param mock_path_exists: mock_path_exists
        :return: None
        """
        mock_path_exists.return_value = True
        mock_statistics = MagicMock()
        mock_from_json_file.return_value = mock_statistics
        input_file = "file.json"
        emulation_name = "test_emulation"
        ImportUtil.import_emulation_statistics_from_disk_json(input_file=input_file, emulation_name=emulation_name)
        mock_path_exists.assert_called()
        mock_from_json_file.assert_called_once_with(input_file)
        assert mock_statistics.emulation_name == emulation_name
        mock_save_emulation_statistic.assert_called()

    @patch("os.path.exists")
    @patch("csle_common.dao.emulation_config.emulation_trace.EmulationTrace.load_traces_from_disk")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_emulation_trace")
    def test_import_emulation_traces_from_disk_json(self, mock_save_emulation_trace, mock_load_traces_from_disk,
                                                    mock_path_exists) -> None:
        """
        Test the method that imports emulation traces from disk to the metastore

        :param mock_save_emulation_trace: mock_save_emulation_trac
        :param mock_load_traces_from_disk: mock_load_traces_from_disk
        :param mock_path_exists: mock_path_exists
        :return: None
        """
        mock_path_exists.return_value = True
        mock_trace_1 = MagicMock()
        mock_trace_2 = MagicMock()
        mock_load_traces_from_disk.return_value = [mock_trace_1, mock_trace_2]
        input_file = "file.json"
        emulation_name = "test_emulation"
        ImportUtil.import_emulation_traces_from_disk_json(input_file=input_file, emulation_name=emulation_name)
        mock_path_exists.assert_called()
        mock_load_traces_from_disk.assert_called()
        assert mock_trace_1.emulation_name == emulation_name
        assert mock_trace_2.emulation_name == emulation_name
        assert mock_save_emulation_trace.call_count == 2
