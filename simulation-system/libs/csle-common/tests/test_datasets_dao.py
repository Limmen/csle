from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset


class TestDatasetsDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_traces_dataset(self, example_traces_dataset: TracesDataset) -> None:
        """
        Tests creation and dict conversion of the TracesDataset DAO

        :param test_traces_dataset: an example TracesDataset
        :return: None
        """
        assert isinstance(example_traces_dataset.to_dict(), dict)
        assert isinstance(TracesDataset.from_dict(example_traces_dataset.to_dict()), TracesDataset)
        assert TracesDataset.from_dict(example_traces_dataset.to_dict()).to_dict() == example_traces_dataset.to_dict()
        assert TracesDataset.from_dict(example_traces_dataset.to_dict()) == example_traces_dataset

    def test_statistics_dataset(self, example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests creation and dict conversion of the StatisticsDataset DAO

        :param example_statistics_dataset: an example StatisticsDataset
        :return: None
        """
        assert isinstance(example_statistics_dataset.to_dict(), dict)
        assert isinstance(StatisticsDataset.from_dict(example_statistics_dataset.to_dict()), StatisticsDataset)
        assert StatisticsDataset.from_dict(example_statistics_dataset.to_dict()).to_dict() == \
               example_statistics_dataset.to_dict()
        assert StatisticsDataset.from_dict(example_statistics_dataset.to_dict()) == example_statistics_dataset
