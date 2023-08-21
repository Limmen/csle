import time
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset


class TestDatasetsDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_traces_dataset(self) -> None:
        """
        Tests creation and dict conversion of the TracesDataset DAO

        :return: None
        """
        dataset = TracesDataset(name="test_dataset", description="test_descr", download_count=100,
                                file_path="test_path", url="test_url", date_added=time.time(),
                                size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                num_files=50, file_format="json", added_by="testadded", columns="col1,col2",
                                data_schema={}, num_attributes_per_time_step=10, num_traces=15)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(TracesDataset.from_dict(dataset.to_dict()), TracesDataset)
        assert TracesDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert TracesDataset.from_dict(dataset.to_dict()) == dataset

    def test_statistics_dataset(self) -> None:
        """
        Tests creation and dict conversion of the StatisticsDataset DAO

        :return: None
        """
        dataset = StatisticsDataset(name="test_dataset", description="test_descr", download_count=100,
                                    file_path="test_path", url="test_url", date_added=time.time(), num_measurements=100,
                                    num_metrics=10, size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                    num_files=50, file_format="json", added_by="testadded", conditions="cond1,cond2",
                                    metrics="metric1,metric2", num_conditions=10)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(StatisticsDataset.from_dict(dataset.to_dict()), StatisticsDataset)
        assert StatisticsDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert StatisticsDataset.from_dict(dataset.to_dict()) == dataset
