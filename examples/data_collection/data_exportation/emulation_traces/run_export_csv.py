from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    ExportUtil.export_emulation_traces_to_disk_csv(
        num_traces_per_file=100, output_dir="/home/kim/traces_3_aug_22_csv",
        zip_file_output="/home/kim/traces_3_aug_22_csv.zip", max_num_traces=2000, added_by="Kim Hammar",
        max_time_steps=100, max_nodes=31, max_ports=3, max_vulns=3, null_value=-1)
