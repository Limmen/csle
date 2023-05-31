from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    ExportUtil.export_emulation_statistics_to_disk_json(
        output_dir="/home/kim/tnsm23_plots/intrusion_stats",
        zip_file_output="/home/kim/tnsm23_plots/intrusion_stats.zip", added_by="Kim Hammar",
        statistics_id=3)
