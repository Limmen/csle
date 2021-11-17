import React from 'react';
import './DefenderPolicyDropdownElement.css';
import {Dropdown} from "react-bootstrap"

const DefenderPolicyDropdownElement = (props) => {

    const updatePolicy = () => {
        props.setActiveDefenderPolicy(props.policy)
    }

    return (
        <Dropdown.Item key={props.index} onClick={updatePolicy}>{props.policy}</Dropdown.Item>
    );
}

DefenderPolicyDropdownElement.propTypes = {};
DefenderPolicyDropdownElement.defaultProps = {};

export default DefenderPolicyDropdownElement;
