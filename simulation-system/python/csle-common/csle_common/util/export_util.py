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
                    Logger.__call__().get_logger().info(f"Processing file {i}/{len(files)}, file name: {file}")
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
    def export_emulation_traces_to_disk(num_traces_per_file: int, output_dir: str) -> None:
        """
        Exports emulation traces from the metastore to disk

        :param num_traces_per_file: the number of traces per file in the output directory
        :param output_dir: the output directory
        :return: None
        """
        Logger.__call__().get_logger().info(f"Exporting emulation traces to disk, output dir: {output_dir}, "
                                            f"num traces per file: {num_traces_per_file}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
        traces = []
        file_id = 1
        file_name = f"{file_id}.json"
        last_export = 0
        for i, id_obj in enumerate(emulation_traces_ids):
            Logger.__call__().get_logger().info(f"Reading trace {i}/{len(emulation_traces_ids)} from the metastore")
            tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
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

    @staticmethod
    def extract_emulation_traces_dataset_metadata(dir_path: str):
        num_files = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])
        size_uncompressed = os.path.getsize(dir_path)
        dir_size_uncompressed_gb = ExportUtil.get_dir_size_gb(dir_path=dir_path)
        print(f"num files: {num_files}, size uncompressed: {size_uncompressed}, "
              f"dir_size_uncompressed: {dir_size_uncompressed_gb}")

