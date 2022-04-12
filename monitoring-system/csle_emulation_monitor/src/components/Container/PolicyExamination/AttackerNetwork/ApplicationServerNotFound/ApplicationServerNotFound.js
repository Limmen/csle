import React from 'react';
import {Handle} from 'react-flow-renderer';
import './ApplicationServerNotFound.css';
import ibm_tower from './ibm_tower_small.png';

const ApplicationServerNotFound = ({ data }) => {
    return (
        <div className="appServerNotFound">
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={ibm_tower} className="ibm_tower" alt="ibm_tower" width="100%" height="100%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


ApplicationServerNotFound.propTypes = {};
ApplicationServerNotFound.defaultProps = {};
export default ApplicationServerNotFound;
