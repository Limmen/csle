from typing import Tuple
import io
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
    def get_dir_size_gb(dir_path : str ='.')  -> float:
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
        return round((float(total)/1000000000),2)

    @staticmethod
    def export_emulation_traces_to_disk_json(num_traces_per_file: int, output_dir: str, zip_file_output: str) -> None:
        """
        Exports emulation traces from the metastore to disk

        :param num_traces_per_file: the number of traces per file in the output directory
        :param output_dir: the output directory
        :param zip_file_output: the compressed zip file path
        :return: None
        """
        Logger.__call__().get_logger().info(f"Exporting emulation traces to disk, output dir: {output_dir}, "
                                            f"output zip file: {zip_file_output}, "
                                            f"num traces per file: {num_traces_per_file}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
        traces = []
        file_id = 1
        file_name = f"{file_id}.json"
        last_export = 0
        num_attributes_per_time_step = -1
        schema = None
        for i, id_obj in enumerate(emulation_traces_ids):
            Logger.__call__().get_logger().info(f"Reading trace {i}/{len(emulation_traces_ids)} from the metastore")
            tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
            if num_attributes_per_time_step == -1:
                num_attributes_per_time_step = tr.num_attributes_per_time_step()
            if schema is None:
                schema = json.dumps(tr.get_schema().to_dict(), indent=4, sort_keys=True)

            traces.append(tr.to_dict())
            if i > 0 and ((i % num_traces_per_file == 0) or i == (len(emulation_traces_ids)-1)):
                Logger.__call__().get_logger().info(f"Exporting traces {last_export+1}-{i} to file: {file_name}")
                traces_dict = {
                    constants.METADATA_STORE.EMULATIONS_PROPERTY : traces
                }
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
            metadata_str = f"{constants.DATASETS.FILE_FORMAT_PROPERTY}{constants.COMMANDS.COLON_DELIM}{file_format}\n" \
                       f"{constants.DATASETS.NUM_TRACES_PROPERTY}{constants.COMMANDS.COLON_DELIM}{num_traces}\n" \
                       f"{constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY}{constants.COMMANDS.COLON_DELIM}" \
                           f"{num_attributes_per_time_step}\n" \
                       f"{constants.DATASETS.SCHEMA_PROPERTY}{constants.COMMANDS.COLON_DELIM}{schema}\n" \
                       f"{constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY}{constants.COMMANDS.COLON_DELIM}" \
                           f"{num_traces_per_file}"
            f.write(metadata_str)
        ExportUtil.zipdir(dir_path=output_dir, file_path=zip_file_output)
        Logger.__call__().get_logger().info(f"Export of emulation traces to disk complete, "
                                            f"output dir:{output_dir}, output zip file: {zip_file_output}")


    @staticmethod
    def extract_emulation_traces_dataset_metadata(dir_path: str, zip_file_path: str) \
            -> Tuple[int, float, float, str, int, str, int, int]:
        """
        Extracts metadata of a traces dataset stored on disk

        :param dir_path: the path to the directory where the traces dataset is stored
        :param zip_file_path: the path to the compressed zipfile of the dataset
        :return: num_files, dir_size_uncompressed_gb, file_format, num_traces, schema, num_traces_per_file,
                 num_attributes_per_time_step
        """
        metadata = None
        file_format = "unknown"
        num_traces = -1
        schema = ""
        num_traces_per_file = -1
        num_attributes_per_time_step = -1
        with io.open(f"{dir_path}{constants.COMMANDS.SLASH_DELIM}{constants.DATASETS.METADATA_FILE_NAME}", 'r',
                     encoding='utf-8') as f:
            metadata = f.read()
        if metadata is not None:
            metadata_properties = metadata.split(constants.COMMANDS.NEW_LINE_DELIM)
            for property_pair in metadata_properties:
                property_value_pair = property_pair.split(constants.COMMANDS.COLON_DELIM)
                if property_value_pair[0] == constants.DATASETS.SCHEMA_PROPERTY:
                    schema = property_value_pair[1]
                elif property_value_pair[0] == constants.DATASETS.NUM_TRACES_PROPERTY:
                    num_traces = property_value_pair[1]
                elif property_value_pair[0] == constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY:
                    num_attributes_per_time_step = property_value_pair[1]
                elif property_value_pair[0] == constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY:
                    num_traces_per_file = property_value_pair[1]
                elif property_value_pair[0] == constants.DATASETS.FILE_FORMAT_PROPERTY:
                    file_format = property_value_pair[1]
        num_files = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])
        size_compressed_gb = round(float(os.path.getsize(zip_file_path))/1000000000,2)
        dir_size_uncompressed_gb = ExportUtil.get_dir_size_gb(dir_path=dir_path)
        return num_files,  dir_size_uncompressed_gb, size_compressed_gb, file_format, num_traces, schema, \
               num_traces_per_file, num_attributes_per_time_step


