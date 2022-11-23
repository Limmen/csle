import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Policies.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import 'react-confirm-alert/src/react-confirm-alert.css';
import AlphaVecPolicyComponent from "./AlphaVecPolicyComponent/AlphaVecPolicyComponent";
import DQNPolicyComponent from "./DQNPolicyComponent/DQNPolicyComponent";
import PPOPolicyComponent from "./PPOPolicyComponent/PPOPolicyComponent";
import MultiThresholdPolicyComponent from "./MultiThresholdPolicyComponent/MultiThresholdPolicyComponent";
import VectorPolicyComponent from "./VectorPolicyComponent/VectorPolicyComponent";
import FnnWSoftmaxPolicyComponent from "./FnnWSoftmaxPolicyComponent/FnnWSoftmaxPolicyComponent";
import TabularPolicyComponent from "./TabularPolicyComponent/TabularPolicyComponent";

/**
 * Component representing the /policies page
 */
const Policies = (props) => {
    const setSessionData = props.setSessionData

    return (
        <div className="policyExamination">
            <h3 className="managementTitle"> Management of Policies </h3>

            <MultiThresholdPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <AlphaVecPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <DQNPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <PPOPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <VectorPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <FnnWSoftmaxPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

            <TabularPolicyComponent sessionData={props.sessionData} setSessionData={setSessionData}/>

        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
