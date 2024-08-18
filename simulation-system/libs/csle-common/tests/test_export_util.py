from unittest.mock import patch, MagicMock
from csle_common.util.export_util import ExportUtil
import os
import tempfile
import json


class TestExportUtilSuite:
    """
    Test suite for Export Util
    """

    def test_zipdir(self) -> None:
        """
        Test the method that creates a zip file of a given directory

        :return: None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.txt")
            with open(file_path, "w") as f:
                f.write("text")
            zip_path = os.path.join(tmpdir, "test.zip")
            ExportUtil.zipdir(tmpdir, zip_path)
            assert os.path.exists(zip_path)

    def test_get_dir_size_gb(self) -> None:
        """
        Test the method that calculates the zie of a file directory in gb

        :return: None
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            sub_dir = os.path.join(tmpdir, "subdir")
            os.makedirs(sub_dir)
            file_sizes = [150000000, 250000000, 350000000]
            total_size = sum(file_sizes)
            file_paths = [
                os.path.join(tmpdir, "file1.txt"),
                os.path.join(tmpdir, "file2.txt"),
                os.path.join(tmpdir, "file3.txt"),
            ]
            for file_path, size in zip(file_paths, file_sizes):
                with open(file_path, "wb") as f:
                    f.write(b"\0" * size)
            size_gb = ExportUtil.get_dir_size_gb(tmpdir)
            expected_size_gb = round(float(total_size) / 1000000000, 2)
            assert size_gb == expected_size_gb, f"Expected {expected_size_gb} GB but got {size_gb} GB"

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces_ids")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace")
    @patch("csle_common.util.export_util.ExportUtil.zipdir")
    def test_export_emulation_traces_to_disk_json(self, mock_zipdir,
                                                  mock_get_emulation_trace, mock_list_emulation_traces_ids) -> None:
        """
        Test the method that exports emulation traces from the metastore to disk

        :param mock_zipdir: mock_zipdir
        :param mock_get_emulation_trace: mock_get_emulation_trace
        :param mock_list_emulation_traces_ids: mock_list_emulation_traces_ids
        :return: None
        """
        mock_list_emulation_traces_ids.return_value = [(1,), (2,)]
        mock_trace = MagicMock()
        mock_trace.to_dict.return_value = {"trace_data": "example_data"}
        mock_trace.num_attributes_per_time_step.return_value = 5
        mock_trace.schema.return_value.to_dict.return_value = {"schema_data": "example_schema"}
        mock_get_emulation_trace.return_value = mock_trace
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_output = os.path.join(temp_dir, "output.zip")
            ExportUtil.export_emulation_traces_to_disk_json(
                num_traces_per_file=1,
                output_dir=temp_dir,
                zip_file_output=zip_file_output,
                max_num_traces=2,
                added_by="test_user",
                offset=0,
                file_start_id=1,
            )
            assert os.path.exists(os.path.join(temp_dir, "1.json"))

    @patch("csle_common.util.export_util.ExportUtil.get_dir_size_gb")
    @patch("os.listdir")
    @patch("os.path.getsize")
    @patch("io.open")
    def test_extract_emulation_traces_dataset_metadata(self, mock_open, mock_getsize, mock_listdir,
                                                       mock_get_dir_size_gb) -> None:
        """
        Test the method that extracts metadata of a traces dataset stored on disk

        :param mock_open: mock_open
        :param mock_getsize: mock_getsize
        :param mock_listdir: mock_listdir
        :param mock_get_dir_size_gb: mock_get_dir_size_gb
        :return: None
        """
        mock_metadata = {
            "schema": {"schema_data": "example_schema"},
            "num_traces": 5,
            "num_traces_per_file": 2,
            "num_attributes_per_time_step": 3,
            "file_format": "json",
            "added_by": "test_user",
            "columns": "example_columns",
        }
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_metadata)
        mock_listdir.return_value = ["1.json", "2.json", "metadata.json"]
        mock_getsize.return_value = 500000000
        mock_get_dir_size_gb.return_value = 1.5
        dir_path = "/dir"
        zip_file_path = "/dir/zipfile.zip"
        result = ExportUtil.extract_emulation_traces_dataset_metadata(dir_path=dir_path, zip_file_path=zip_file_path)
        assert result

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces_ids")
    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace")
    @patch("csle_common.util.export_util.ExportUtil.zipdir")
    def test_export_emulation_traces_to_disk_csv(self, mock_zipdir, mock_get_emulation_trace,
                                                 mock_list_emulation_traces_ids) -> None:
        """
        Test the method that exports emulation traces from the metastore to disk

        :param mock_zipdir: mock_zipdir
        :param mock_get_emulation_trace: mock_get_emulation_trace
        :param mock_list_emulation_traces_ids: mock_list_emulation_traces_id
        :return: None
        """
        mock_list_emulation_traces_ids.return_value = [(1,), (2,)]
        mock_trace = MagicMock()
        mock_trace.to_csv_record.return_value = (["value1", "value2"], ["col1", "col2"])
        mock_trace.num_attributes_per_time_step.return_value = 5
        mock_get_emulation_trace.return_value = mock_trace
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_output = os.path.join(temp_dir, "output.zip")
            ExportUtil.export_emulation_traces_to_disk_csv(
                num_traces_per_file=1,
                output_dir=temp_dir,
                zip_file_output=zip_file_output,
                max_num_traces=2,
                max_time_steps=10,
                max_nodes=5,
                max_ports=3,
                max_vulns=2,
                null_value=-1,
                added_by="test_user",
            )
            assert os.path.exists(os.path.join(temp_dir, "1.csv"))

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_statistic")
    @patch("csle_common.util.export_util.ExportUtil.zipdir")
    def test_export_emulation_statistic_to_disk_json(self, mock_zipdir, mock_get_emulation_statistic) -> None:
        """
        Test the method that exports emulation statistics from the metastore to disk

        :param mock_zipdir: mock_zipdir
        :param mock_get_emulation_statistic: mock_get_emulation_statistic
        :return: None
        """
        mock_statistic = MagicMock()
        mock_statistic.num_measurements = 100
        mock_statistic.num_metrics = 10
        mock_statistic.metrics = ["metric1", "metric2"]
        mock_statistic.conditions = ["condition1", "condition2"]
        mock_statistic.num_conditions = 2
        mock_statistic.to_dict.return_value = {"key": "value"}
        mock_get_emulation_statistic.return_value = mock_statistic
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_output = os.path.join(temp_dir, "output.zip")
            ExportUtil.export_emulation_statistics_to_disk_json(
                output_dir=temp_dir, zip_file_output=zip_file_output, statistics_id=1, added_by="test_user"
            )
            assert os.path.exists(os.path.join(temp_dir, "statistics.json"))

    @patch("csle_common.util.export_util.ExportUtil.get_dir_size_gb")
    @patch("os.listdir")
    @patch("os.path.getsize")
    @patch("io.open")
    def test_extract_emulation_statistics_dataset_metadata(self, mock_open, mock_getsize, mock_listdir,
                                                           mock_get_dir_size_gb) -> None:
        """
        Test the method that extracts metadata of a traces dataset stored on disk

        :param mock_open: mock_open
        :param mock_getsize: mock_getsize
        :param mock_listdir: mock_listdir
        :param mock_get_dir_size_gb: mock_get_dir_size_gb
        :return: None
        """
        mock_metadata = {
            "file_format": "json",
            "added_by": "test_user",
            "num_measurements": 100,
            "num_metrics": 10,
            "metrics": "metric1,metric2",
            "conditions": "condition1,condition2",
            "num_conditions": 2,
        }
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_metadata)
        mock_listdir.return_value = ["statistics.json", "metadata.json"]
        mock_getsize.return_value = 500000000
        mock_get_dir_size_gb.return_value = 1.5
        dir_path = "/dir"
        zip_file_path = "/dir/zipfile.zip"
        result = ExportUtil.extract_emulation_statistics_dataset_metadata(dir_path=dir_path,
                                                                          zip_file_path=zip_file_path)
        assert result
