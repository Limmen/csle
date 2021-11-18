import React from 'react';
import {Handle} from 'react-flow-renderer';
import './SwitchNotFound.css';
import gb_switch from './gb_switch.png';

const SwitchNotFound = ({ data }) => {
    return (
        <div className="switchNotFound">
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={gb_switch} className="ibm_tower" alt="gb_switch" width="100%" height="100%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


SwitchNotFound.propTypes = {};
SwitchNotFound.defaultProps = {};
export default SwitchNotFound;
