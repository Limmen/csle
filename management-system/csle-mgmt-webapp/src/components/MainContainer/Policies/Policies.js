import React, {useState} from 'react';
import './Policies.css';
import Select from 'react-select'
import 'react-confirm-alert/src/react-confirm-alert.css';
import AlphaVecPolicies from "./AlphaVecPolicies/AlphaVecPolicies";
import DQNPolicyComponent from "./DQNPolicies/DQNPolicies";
import PPOPolicies from "./PPOPolicies/PPOPolicies";
import MultiThresholdPolicyComponent from "./MultiThresholdPolicies/MultiThresholdPolicies";
import LinearThresholdPolicyComponent from "./LinearThresholdPolicies/LinearThresholdPolicies";
import VectorPolicies from "./VectorPolicies/VectorPolicies";
import FnnWSoftmaxPolicies from "./FnnWSoftmaxPolicies/FnnWSoftmaxPolicies";
import TabularPolicies from "./TabularPolicies/TabularPolicies";

/**
 * Component representing the /policies page
 */
const Policies = (props) => {
    const policyTypes = [
        {
            value: 0,
            label: "Multi-threshold policies"
        },
        {
            value: 1,
            label: "Alpha-vector policies"
        },
        {
            value: 2,
            label: "DQN policies"
        },
        {
            value: 3,
            label: "PPO policies"
        },
        {
            value: 4,
            label: "Vector policies"
        },
        {
            value: 5,
            label: "Feed-forward neural network policies"
        },
        {
            value: 6,
            label: "Tabular policies"
        },
        {
            value: 7,
            label: "Linear threshold policies"
        },
    ]
    const [selectedPolicyType, setSelectedPolicyType] = useState(policyTypes[3]);

    const updatedSelectedPolicyType = (selectedPolicyType) => {
        setSelectedPolicyType(selectedPolicyType)
    }

    const SelectedPolicyTypeComponent = (props) => {
        if(props.selectedPolicyType.value === 0) {
            return (<MultiThresholdPolicyComponent sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 1) {
            return (<AlphaVecPolicies sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 2) {
            return (<DQNPolicyComponent sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 3) {
            return (<PPOPolicies sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 4) {
            return (<VectorPolicies sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 5) {
            return (<FnnWSoftmaxPolicies sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 6) {
            return (<TabularPolicies sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
        if(props.selectedPolicyType.value === 7) {
            return (<LinearThresholdPolicyComponent sessionData={props.sessionData} setSessionData={props.setSessionData}/>)
        }
    }

    return (
        <div className="policyExamination">
            <h3 className="managementTitle"> Management of Policies
            </h3>
            <div className="policyTypeSelection inline-block">
                <div className="conditionalDist inline-block conditionalLabel">
                    Policy type:
                </div>
                <div className="conditionalDist inline-block" style={{width: "300px"}}>
                    <Select
                        style={{display: 'inline-block'}}
                        value={selectedPolicyType}
                        defaultValue={selectedPolicyType}
                        options={policyTypes}
                        onChange={updatedSelectedPolicyType}
                        placeholder="Select policy type"
                    />
                </div>
            </div>
            <SelectedPolicyTypeComponent selectedPolicyType={selectedPolicyType} sessionData={props.sessionData}
                                     setSessionData={props.setSessionData}/>
        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
