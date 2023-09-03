from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.jobs.training_job_config import TrainingJobConfig


class TestJobsDaoSuite:
    """
    Test suite for job data access objects (DAOs)
    """

    def test_data_collection_job_config(self, example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests creation and dict conversion of the DataCollectionJobConfig DAO

        :param example_data_collection_job: an example DataCollectionJobConfig
        :return: None
        """
        assert isinstance(example_data_collection_job.to_dict(), dict)
        assert isinstance(DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()),
                          DataCollectionJobConfig)
        assert (DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()).to_dict() ==
                example_data_collection_job.to_dict())
        assert (DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()) ==
                example_data_collection_job)

    def test_system_identification_job_config(
            self, example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests creation and dict conversion of the SystemIdentificationJobConfig DAO

        :param example_system_identification_job_config: an example SystemIdentificationJobConfig
        :return: None
        """
        assert isinstance(example_system_identification_job_config.to_dict(), dict)
        assert isinstance(SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()),
                          SystemIdentificationJobConfig)
        assert (SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()).to_dict() ==
                example_system_identification_job_config.to_dict())
        assert (SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()) ==
                example_system_identification_job_config)

    def test_training_job_config(self, example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests creation and dict conversion of the TrainingJobConfig DAO

        :param example_training_job_config: an example TrainingJobConfig
        :return: None
        """
        assert isinstance(example_training_job_config.to_dict(), dict)
        assert isinstance(TrainingJobConfig.from_dict(example_training_job_config.to_dict()),
                          TrainingJobConfig)
        assert (TrainingJobConfig.from_dict(example_training_job_config.to_dict()).to_dict() ==
                example_training_job_config.to_dict())
        assert (TrainingJobConfig.from_dict(example_training_job_config.to_dict()) ==
                example_training_job_config)
