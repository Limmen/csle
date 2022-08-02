import datetime
from csle_common.util.export_util import ExportUtil
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    descr = "A dataset with traces of network intrusions. Each trace includes sequences of attacker actions, " \
            "intrusion states, defender actions, attacker observations and defender observations"
    dir_path = "/home/kim/traces_2_aug_22"
    zip_file_path = "/home/kim/traces_2_aug_22.zip"
    name = "emulation_traces_level_9_22_aug_2022"
    url = "-"
    date_added = datetime.date.today()
    citation = "-"
    num_files,  dir_size_uncompressed_gb, size_compressed_gb, file_format, num_traces, schema, num_traces_per_file, \
    num_attributes_per_time_step = \
        ExportUtil.extract_emulation_traces_dataset_metadata(dir_path=dir_path, zip_file_path=zip_file_path)
    dataset = TracesDataset(name=name, description=descr, file_path=zip_file_path, url=url, date_added=date_added,
                            num_traces=num_traces, num_attributes_per_time_step=num_attributes_per_time_step,
                            size_in_gb=dir_size_uncompressed_gb, compressed_size_in_gb=size_compressed_gb,
                            citation=citation, num_files=num_files, data_schema=schema, file_format=file_format,
                            download_count=0)
    MetastoreFacade.save_traces_dataset(traces_dataset=dataset)
    # ExportUtil.zipdir(dir_path=dir_path, zip_file_path=zip_file_path)
