import datetime
from csle_common.util.export_util import ExportUtil
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    descr = "A dataset with metric statistics of network intrusions. The dataset includes several metrics measured " \
            "through" \
            "randomized controlled trials under different conditions"
    dir_path = "/media/lagring/statistics_dataset_14_nov_22_json"
    zip_file_path = "/media/lagring/statistics_dataset_14_nov_22_json.zip"
    name = "emulation_statistics_level_9_14_nov_json_2022"
    url = "-"
    date_added = datetime.datetime.now()
    citation = "Intrusion Prevention through Optimal Stopping (Hammar & Stadler 2022)"
    (num_files, dir_size_uncompressed_gb, size_compressed_gb, file_format, added_by, num_measurements,
     num_metrics, metrics, conditions, num_conditions) = \
        ExportUtil.extract_emulation_statistics_dataset_metadata(dir_path=dir_path, zip_file_path=zip_file_path)
    dataset = StatisticsDataset(name=name, description=descr, file_path=zip_file_path, url=url,
                                date_added=date_added,
                                num_measurements=num_measurements, num_metrics=num_metrics,
                                size_in_gb=dir_size_uncompressed_gb, compressed_size_in_gb=size_compressed_gb,
                                citation=citation, num_files=num_files, file_format=file_format,
                                download_count=0, added_by=added_by, metrics=metrics, conditions=conditions,
                                num_conditions=num_conditions)
    MetastoreFacade.save_statistics_dataset(statistics_dataset=dataset)
