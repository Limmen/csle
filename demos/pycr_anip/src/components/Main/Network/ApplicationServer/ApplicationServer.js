import React from 'react';
import {Handle} from 'react-flow-renderer';
import './ApplicationServer.css';
import ibm_tower from './ibm_tower_small.png';

const ApplicationServer = ({ data }) => {
    return (
        <div className="appServer">
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={ibm_tower} className="ibm_tower" alt="ibm_tower" width="100%" height="100%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


ApplicationServer.propTypes = {};
ApplicationServer.defaultProps = {};
export default ApplicationServer;
