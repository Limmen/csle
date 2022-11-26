import React, {useState} from 'react';
import './Jobs.css';
import Select from 'react-select'
import TrainingJobs from "./TrainingJobs/TrainingJobs";
import SystemIdentificationJobs from "./SystemIdentificationJobs/SystemIdentificationJobs";
import DataCollectionJobs from "./DataCollectionJobs/DataCollectionJobs";

/**
 * The component representing the /jobs-page
 */
const Jobs = (props) => {

    const jobTypes = [
        {
            value: 0,
            label: "Training jobs"
        },
        {
            value: 1,
            label: "Data collection jobs"
        },
        {
            value: 2,
            label: "System identification jobs"
        }
    ]
    const [selectedJobType, setSelectedJobType] = useState(jobTypes[0]);

    const updatedSelectedJobType = (selectedJobType) => {
        setSelectedJobType(selectedJobType)
    }

    const SelectedJobTypeComponent = (props) => {
        if (props.selectedJobType.value === 0) {
            return (
                <TrainingJobs sessionData={props.sessionData} setSessionData={props.setSessionData}/>
            )
        }
        if (props.selectedJobType.value === 1) {
            return (
                <DataCollectionJobs sessionData={props.sessionData} setSessionData={props.setSessionData}/>
            )
        }
        if (props.selectedJobType.value === 2) {
            return (
                <SystemIdentificationJobs sessionData={props.sessionData} setSessionData={props.setSessionData}/>
            )
        }
    }

    return (
        <div className="jobs">
            <h3 className="managementTitle"> Management of Jobs </h3>
            <div className="jobTypeSelection inline-block">
                <div className="conditionalDist inline-block conditionalLabel">
                    Job type:
                </div>
                <div className="conditionalDist inline-block" style={{width: "300px"}}>
                    <Select
                        style={{display: 'inline-block'}}
                        value={selectedJobType}
                        defaultValue={selectedJobType}
                        options={jobTypes}
                        onChange={updatedSelectedJobType}
                        placeholder="Select job type"
                    />
                </div>
            </div>
            <SelectedJobTypeComponent selectedJobType={selectedJobType} sessionData={props.sessionData}
                                        setSessionData={props.setSessionData}/>
        </div>
    );
}

Jobs.propTypes = {};
Jobs.defaultProps = {};
export default Jobs;
