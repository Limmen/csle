from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    ExportUtil.export_emulation_traces_to_disk_json(
        num_traces_per_file=100, output_dir="/home/kim/traces_29_oct_22_json",
        zip_file_output="/home/kim/traces_29_oct_22_json.zip", max_num_traces=6400, added_by="Kim Hammar",
        offset=2000, file_start_id=21)