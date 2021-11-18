import React from 'react';
import {Handle} from 'react-flow-renderer';
import './IDS.css';
import ids from './ids-0.png';

const IDS = ({ data }) => {
    return (
        <div className="ids">
            <p className="idsLabel">{data.text}</p>
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={ids} className="ibm_tower" alt="ids" width="100%" height="100%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


IDS.propTypes = {};
IDS.defaultProps = {};
export default IDS;
