from csle_common.util.import_util import ImportUtil

if __name__ == '__main__':
    ImportUtil.import_emulation_statistics_from_disk_json(
        input_file="/media/lagring/statistics_dataset_14_nov_22_json/statistics.json",
        emulation_name="csle-level9-003")
