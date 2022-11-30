import os
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace


class ImportUtil:
    """
    Class with utility functions for importing data to the metastore
    """

    @staticmethod
    def import_emulation_statistics_from_disk_json(input_file: str) -> None:
        """
        Imports emulation statistics from disk to the metastore

        :param input file: the input file
        :return: None
        """
        Logger.__call__().get_logger().info(f"Importing emulation statistics from disk (json), input dir: {input_file}")
        if not os.path.exists(input_file):
            raise ValueError(f"File: {input_file} does not exist")
        statistics = EmulationStatistics.from_json_file(input_file)
        MetastoreFacade.save_emulation_statistic(statistics)
        Logger.__call__().get_logger().info("Import of emulation statistics from disk complete, "
                                            f"input file:{input_file}")

    @staticmethod
    def import_emulation_traces_from_disk_json(input_file: str) -> None:
        """
        Imports emulation traces from disk to the metastore

        :param input file: the input file
        :return: None
        """
        Logger.__call__().get_logger().info(f"Importing emulation traces from disk (json), input dir: {input_file}")
        if not os.path.exists(input_file):
            raise ValueError(f"File: {input_file} does not exist")
        traces = EmulationTrace.load_traces_from_disk(input_file)
        Logger.__call__().get_logger().info(f"Read {len(traces)} traces")
        for i, trace in enumerate(traces):
            Logger.__call__().get_logger().info(f"Saving trace {i}/{len(traces)} to the metastore")
            MetastoreFacade.save_emulation_trace(trace)
        Logger.__call__().get_logger().info("Import of emulation traces from disk complete, "
                                            f"input file: {input_file}")
