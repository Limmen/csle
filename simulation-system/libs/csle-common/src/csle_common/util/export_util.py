from typing import Tuple, Dict, Any
import io
import csv
import json
import os
import zipfile
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade


class ExportUtil:
    """
    Class with utility functions for exporting data from the metastore
    """

    @staticmethod
    def zipdir(dir_path: str, file_path: str) -> None:
        """
        Creates a zip file of a given directory

        :param dir_path: the path to the directory to zip
        :param file_path: the full path of the resulting zip file
        :return: None
        """
        Logger.__call__().get_logger().info(f"Zipping directory: {dir_path} to file: {file_path}")
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_path):
                for i, file in enumerate(files):
                    Logger.__call__().get_logger().info(f"Processing file {i+1}/{len(files)}, file name: {file}")
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file),
                                               os.path.join(dir_path, '..')))

    @staticmethod
    def get_dir_size_gb(dir_path: str = '.') -> float:
        """
        Utility method to calculate the zie of a file directory in gb

        :param dir_path: the path to the directory
        :return: the size of the directory in GB
        """
        total = 0
        with os.scandir(dir_path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += ExportUtil.get_dir_size(entry.path)
        return round((float(total) / 1000000000), 2)

    @staticmethod
    def export_emulation_traces_to_disk_json(num_traces_per_file: int, output_dir: str, zip_file_output: str,
                                             max_num_traces: int, added_by: str = "unknown", offset: int = 0,
                                             file_start_id: int = 1) -> None:
        """
        Exports emulation traces from the metastore to disk

        :param num_traces_per_file: the number of traces per file in the output directory
        :param output_dir: the output directory
        :param zip_file_output: the compressed zip file path
        :param max_num_traces: maximum number of traces
        :param added_by: the person who added the dataset
        :param offset: the trace id offset
        :param file_start_id: the id of the first file to write
        :return: None
        """
        Logger.__call__().get_logger().info(f"Exporting emulation traces to disk (json), output dir: {output_dir}, "
                                            f"output zip file: {zip_file_output}, "
                                            f"num traces per file: {num_traces_per_file}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
        emulation_traces_ids = emulation_traces_ids[offset:]
        if len(emulation_traces_ids) > max_num_traces:
            emulation_traces_ids = emulation_traces_ids[0:max_num_traces]
        traces = []
        file_id = file_start_id
        file_name = f"{file_id}.json"
        columns = ""
        last_export = 0
        num_attributes_per_time_step = -1
        schema = None
        for i, id_obj in enumerate(emulation_traces_ids):
            Logger.__call__().get_logger().info(f"Reading trace {i}/{len(emulation_traces_ids)} from the metastore, "
                                                f"trace id: {id_obj[0]}")
            tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
            if num_attributes_per_time_step == -1:
                num_attributes_per_time_step = tr.num_attributes_per_time_step()
            if schema is None:
                schema = {
                    constants.METADATA_STORE.TRACES_PROPERTY: [
                        tr.schema().to_dict()
                    ]
                }

            traces.append(tr.to_dict())
            if i > 0 and ((i % num_traces_per_file == 0) or i == (len(emulation_traces_ids) - 1)):
                Logger.__call__().get_logger().info(f"Exporting traces {last_export+1}-{i} to file: {file_name}")
                traces_dict = {constants.METADATA_STORE.TRACES_PROPERTY: traces}
                traces_str = json.dumps(traces_dict, indent=4, sort_keys=True)
                with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{file_name}", 'w', encoding='utf-8') as f:
                    f.write(traces_str)
                file_id += 1
                file_name = f"{file_id}.json"
                traces = []
                last_export = i
        file_format = "json"
        num_traces = len(emulation_traces_ids)
        with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'w',
                     encoding='utf-8') as f:
            metadata_dict = {}
            metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY] = file_format
            metadata_dict[constants.DATASETS.NUM_TRACES_PROPERTY] = num_traces
            metadata_dict[constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY] = num_attributes_per_time_step
            metadata_dict[constants.DATASETS.SCHEMA_PROPERTY] = schema
            metadata_dict[constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY] = num_traces_per_file
            metadata_dict[constants.DATASETS.ADDED_BY_PROPERTY] = added_by
            metadata_dict[constants.DATASETS.COLUMNS_PROPERTY] = columns
            f.write(json.dumps(metadata_dict, indent=4, sort_keys=True))
        ExportUtil.zipdir(dir_path=output_dir, file_path=zip_file_output)
        Logger.__call__().get_logger().info(f"Export of emulation traces to disk complete, "
                                            f"output dir:{output_dir}, output zip file: {zip_file_output}")

    @staticmethod
    def extract_emulation_traces_dataset_metadata(dir_path: str, zip_file_path: str) \
            -> Tuple[int, float, float, str, int, Dict[str, Any], int, int, str, str]:
        """
        Extracts metadata of a traces dataset stored on disk

        :param dir_path: the path to the directory where the traces dataset is stored
        :param zip_file_path: the path to the compressed zipfile of the dataset
        :return: num_files, dir_size_uncompressed_gb, file_format, num_traces, schema, num_traces_per_file,
                 num_attributes_per_time_step, added_by, columns
        """
        file_format = "unknown"
        added_by = "unknown"
        num_traces = -1
        schema = ""
        columns = ""
        num_traces_per_file = -1
        num_attributes_per_time_step = -1
        with io.open(f"{dir_path}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'r',
                     encoding='utf-8') as f:
            metadata_dict = json.loads(f.read())
        if metadata_dict is not None:
            if constants.DATASETS.SCHEMA_PROPERTY in metadata_dict:
                schema = metadata_dict[constants.DATASETS.SCHEMA_PROPERTY]
            else:
                schema = {}
            if constants.DATASETS.NUM_TRACES_PROPERTY in metadata_dict:
                num_traces = metadata_dict[constants.DATASETS.NUM_TRACES_PROPERTY]
            else:
                num_traces = 0
            if constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY in metadata_dict:
                num_attributes_per_time_step = metadata_dict[constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY]
            else:
                num_attributes_per_time_step = 0
            if constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY in metadata_dict:
                num_traces_per_file = metadata_dict[constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY]
            else:
                num_traces_per_file = 0
            if constants.DATASETS.FILE_FORMAT_PROPERTY in metadata_dict:
                file_format = metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY]
            else:
                file_format = "unknown"
            if constants.DATASETS.ADDED_BY_PROPERTY in metadata_dict:
                added_by = metadata_dict[constants.DATASETS.ADDED_BY_PROPERTY]
            else:
                added_by = "unknown"
            if constants.DATASETS.COLUMNS_PROPERTY in metadata_dict:
                columns = metadata_dict[constants.DATASETS.COLUMNS_PROPERTY]
            else:
                columns = []

        num_files = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))]) - 1
        size_compressed_gb = round(float(os.path.getsize(zip_file_path)) / 1000000000, 2)
        dir_size_uncompressed_gb = ExportUtil.get_dir_size_gb(dir_path=dir_path)
        return (num_files, dir_size_uncompressed_gb, size_compressed_gb, file_format, num_traces, schema,
                num_traces_per_file, num_attributes_per_time_step, added_by, columns)

    @staticmethod
    def export_emulation_traces_to_disk_csv(
            num_traces_per_file: int, output_dir: str, zip_file_output: str, max_num_traces: int, max_time_steps: int,
            max_nodes: int, max_ports: int, max_vulns: int, null_value: int = -1, added_by: str = "unknown") -> None:
        """
        Exports emulation traces from the metastore to disk

        :param num_traces_per_file: the number of traces per file in the output directory
        :param output_dir: the output directory
        :param zip_file_output: the compressed zip file path
        :param max_num_traces: maximum number of traces
        :param added_by: the person who added the dataset
        :param max_time_steps: the maximum number of time-steps to include in a csv row
        :param max_nodes: the maximum number of nodes to include metrics from
        :param max_ports: the maximum number of ports to include metrics from
        :param max_vulns: the maximum number of vulnerabilities to include metrics from
        :param null_value: the default null value if a metric is missing
        :return: None
        """
        Logger.__call__().get_logger().info(f"Exporting emulation traces to disk (csv), output dir: {output_dir}, "
                                            f"output zip file: {zip_file_output}, "
                                            f"num traces per file: {num_traces_per_file}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
        if len(emulation_traces_ids) > max_num_traces:
            emulation_traces_ids = emulation_traces_ids[0:max_num_traces]
        traces = []
        file_id = 1
        file_name = f"{file_id}.csv"
        last_export = 0
        num_attributes_per_time_step = -1
        columns = None
        for i, id_obj in enumerate(emulation_traces_ids):
            Logger.__call__().get_logger().info(f"Reading trace {i}/{len(emulation_traces_ids)} from the metastore")
            tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
            tr_values, tr_labels = tr.to_csv_record(max_time_steps=max_time_steps, max_nodes=max_nodes,
                                                    max_ports=max_ports, max_vulns=max_vulns, null_value=null_value)
            if num_attributes_per_time_step == -1:
                num_attributes_per_time_step = tr.num_attributes_per_time_step()
            if columns is None:
                columns = tr_labels

            traces.append(tr_values)
            if i > 0 and ((i % num_traces_per_file == 0) or i == (len(emulation_traces_ids) - 1)):
                Logger.__call__().get_logger().info(f"Exporting traces {last_export+1}-{i} to file: {file_name}")
                with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{file_name}", 'w', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    for row in traces:
                        writer.writerow(row)
                file_id += 1
                file_name = f"{file_id}.csv"
                traces = []
                last_export = i
        file_format = "csv"
        num_traces = len(emulation_traces_ids)
        with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'w',
                     encoding='utf-8') as f:
            metadata_dict = {}
            metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY] = file_format
            metadata_dict[constants.DATASETS.NUM_TRACES_PROPERTY] = num_traces
            metadata_dict[constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY] = num_attributes_per_time_step
            metadata_dict[constants.DATASETS.SCHEMA_PROPERTY] = {}
            metadata_dict[constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY] = num_traces_per_file
            metadata_dict[constants.DATASETS.ADDED_BY_PROPERTY] = added_by
            metadata_dict[constants.DATASETS.COLUMNS_PROPERTY] = ",".join(columns)
            f.write(json.dumps(metadata_dict, indent=4, sort_keys=True))
        ExportUtil.zipdir(dir_path=output_dir, file_path=zip_file_output)
        Logger.__call__().get_logger().info(f"Export of emulation traces to disk complete, "
                                            f"output dir:{output_dir}, output zip file: {zip_file_output}")

    @staticmethod
    def export_emulation_statistics_to_disk_json(output_dir: str, zip_file_output: str, statistics_id: int,
                                                 added_by: str = "unknown") -> None:
        """
        Exports emulation statistics from the metastore to disk

        :param output_dir: the output directory
        :param zip_file_output: the compressed zip file path
        :param added_by: the person who added the dataset
        :param statistics_id: the id of the statistics to fetch
        :return: None
        """
        Logger.__call__().get_logger().info(f"Exporting emulation statistics to disk (json), output dir: {output_dir}, "
                                            f"output zip file: {zip_file_output}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        emulation_statistic = MetastoreFacade.get_emulation_statistic(id=statistics_id)
        file_name = "statistics.json"
        Logger.__call__().get_logger().info(f"Exporting statistics with id {statistics_id} to file: {file_name}")
        emulation_statistic.compute_descriptive_statistics_and_distributions()
        num_measurements = emulation_statistic.num_measurements
        num_metrics = emulation_statistic.num_metrics
        metrics = ",".join(emulation_statistic.metrics)
        conditions = ",".join(emulation_statistic.conditions)
        num_conditions = emulation_statistic.num_conditions
        statistics_dict = emulation_statistic.to_dict()
        statistics_dict = json.dumps(statistics_dict, indent=4, sort_keys=True)
        with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{file_name}", 'w', encoding='utf-8') as f:
            f.write(statistics_dict)
        file_format = "json"
        with io.open(f"{output_dir}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'w',
                     encoding='utf-8') as f:
            metadata_dict = {}
            metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY] = file_format
            metadata_dict[constants.DATASETS.NUM_MEASUREMENTS_PROPERTY] = num_measurements
            metadata_dict[constants.DATASETS.NUM_CONDITIONS_PROPERTY] = num_conditions
            metadata_dict[constants.DATASETS.NUM_METRICS_PROPERTY] = num_metrics
            metadata_dict[constants.DATASETS.ADDED_BY_PROPERTY] = added_by
            metadata_dict[constants.DATASETS.CONDITIONS_PROPERTY] = conditions
            metadata_dict[constants.DATASETS.METRICS_PROPERTY] = metrics
            f.write(json.dumps(metadata_dict, indent=4, sort_keys=True))
        ExportUtil.zipdir(dir_path=output_dir, file_path=zip_file_output)
        Logger.__call__().get_logger().info(f"Export of emulation statistics to disk complete, "
                                            f"output dir:{output_dir}, output zip file: {zip_file_output}")

    @staticmethod
    def extract_emulation_statistics_dataset_metadata(dir_path: str, zip_file_path: str) \
            -> Tuple[int, float, float, str, str, int, int, str, str, int]:
        """
        Extracts metadata of a traces dataset stored on disk

        :param dir_path: the path to the directory where the traces dataset is stored
        :param zip_file_path: the path to the compressed zipfile of the dataset
        :return: num_files,  dir_size_uncompressed_gb, size_compressed_gb, file_format, added_by, num_measurements,
                 num_metrics, metrics, conditions, num_conditions
        """
        file_format = "unknown"
        added_by = "unknown"
        num_measurements = 0
        num_metrics = 0
        metrics = ""
        conditions = ""
        with io.open(f"{dir_path}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'r',
                     encoding='utf-8') as f:
            metadata_dict = json.loads(f.read())
        if metadata_dict is not None:
            if constants.DATASETS.FILE_FORMAT_PROPERTY in metadata_dict:
                file_format = metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY]
            if constants.DATASETS.ADDED_BY_PROPERTY in metadata_dict:
                added_by = metadata_dict[constants.DATASETS.ADDED_BY_PROPERTY]
            if constants.DATASETS.NUM_MEASUREMENTS_PROPERTY in metadata_dict:
                num_measurements = metadata_dict[constants.DATASETS.NUM_MEASUREMENTS_PROPERTY]
            if constants.DATASETS.NUM_METRICS_PROPERTY in metadata_dict:
                num_metrics = metadata_dict[constants.DATASETS.NUM_METRICS_PROPERTY]
            if constants.DATASETS.METRICS_PROPERTY in metadata_dict:
                metrics = metadata_dict[constants.DATASETS.METRICS_PROPERTY]
            if constants.DATASETS.CONDITIONS_PROPERTY in metadata_dict:
                conditions = metadata_dict[constants.DATASETS.CONDITIONS_PROPERTY]
            if constants.DATASETS.NUM_CONDITIONS_PROPERTY in metadata_dict:
                num_conditions = metadata_dict[constants.DATASETS.NUM_CONDITIONS_PROPERTY]

        num_files = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))]) - 1
        size_compressed_gb = round(float(os.path.getsize(zip_file_path)) / 1000000000, 2)
        dir_size_uncompressed_gb = ExportUtil.get_dir_size_gb(dir_path=dir_path)
        return (num_files, dir_size_uncompressed_gb, size_compressed_gb, file_format, added_by, num_measurements,
                num_metrics, metrics, conditions, num_conditions)
