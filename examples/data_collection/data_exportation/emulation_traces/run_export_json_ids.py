from csle_common.util.export_util import ExportUtil
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    ids = MetastoreFacade.list_emulation_traces_ids()
    filtered_ids = []
    for id in ids:
        trace = MetastoreFacade.get_emulation_trace(id=id)
        if trace.emulation_name == "csle-level9-010":
            filtered_ids.append(trace)
    ExportUtil.export_emulation_traces_to_disk_json(
        num_traces_per_file=100, output_dir="/mnt/md0/traces_29_mar_2023/constant_load_json",
        zip_file_output="/mnt/md0/traces_29_mar_2023/constant_load_json.zip",
        max_num_traces=2050, added_by="Kim Hammar",
        offset=0, file_start_id=1)
