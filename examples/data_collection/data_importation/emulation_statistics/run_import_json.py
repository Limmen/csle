from csle_common.util.import_util import ImportUtil

if __name__ == '__main__':
    ImportUtil.import_emulation_statistics_from_disk_json(
        input_file="/home/kim/statistics_dataset_31_mar_attacker_23_json/statistics.json",
        emulation_name="csle-level13-010")
