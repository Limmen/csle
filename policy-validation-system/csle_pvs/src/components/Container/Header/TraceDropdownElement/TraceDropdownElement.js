import React from 'react';
import './TraceDropdownElement.css';
import {Dropdown} from "react-bootstrap"

const TraceDropdownElement = (props) => {

    const updateTrace = () => {
        props.setActiveTrace(props.index)
    }

    return (
        <Dropdown.Item key={props.index} onClick={updateTrace}>{props.index}</Dropdown.Item>
    );
}

TraceDropdownElement.propTypes = {};
TraceDropdownElement.defaultProps = {};

export default TraceDropdownElement;
