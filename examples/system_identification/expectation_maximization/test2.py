from csle_common.metastore.metastore_facade import MetastoreFacade
import json
import io

if __name__ == '__main__':
    jobs = MetastoreFacade.list_training_jobs()
    for job in jobs:
        print(job.id)
    job = MetastoreFacade.get_training_job_config(752)
    training_job_str = json.dumps(job.to_dict(), indent=4, sort_keys=True)
    with io.open("/home/kim/job_2.json", 'w', encoding='utf-8') as f:
        f.write(training_job_str)
