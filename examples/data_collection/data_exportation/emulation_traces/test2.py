import json
import io
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    output_dir = "/home/kim/traces_2_aug_22"
    zip_file_output="/home/kim/traces_2_aug_22.zip"
    # traces = []
    # ids = list(range(1901, 1902))
    # num_attributes_per_time_step = -1
    # schema = None
    # for i, id in enumerate(ids):
    #     print(f"Reading trace {i}/{len(ids)} from the metastore, id:{id}")
    #     tr = MetastoreFacade.get_emulation_trace(id=id)
    #     traces.append(tr.to_dict())
    #     if num_attributes_per_time_step == -1:
    #         num_attributes_per_time_step = tr.num_attributes_per_time_step()
    #     if schema is None:
    #         schema = tr.schema().to_dict()
    # traces_dict = {
    #     constants.METADATA_STORE.EMULATIONS_PROPERTY : traces
    # }
    # traces_str = json.dumps(traces_dict, indent=4, sort_keys=True)
    # # with io.open(f"/home/kim/20.json", 'w', encoding='utf-8') as f:
    # #     f.write(traces_str)
    #
    # file_format = "json"
    # num_traces = 2000
    # num_traces_per_file = 100
    # with io.open(f"/home/kim/{constants.DATASETS.METADATA_FILE_NAME}", 'w',
    #              encoding='utf-8') as f:
    #     metadata_dict = {}
    #     metadata_dict[constants.DATASETS.FILE_FORMAT_PROPERTY] = file_format
    #     metadata_dict[constants.DATASETS.NUM_TRACES_PROPERTY] = num_traces
    #     metadata_dict[constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY] = num_attributes_per_time_step
    #     metadata_dict[constants.DATASETS.SCHEMA_PROPERTY] = schema
    #     metadata_dict[constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY] = num_traces_per_file
    #     f.write(json.dumps(metadata_dict, indent=4, sort_keys=True))
    ExportUtil.zipdir(dir_path=output_dir, file_path=zip_file_output)