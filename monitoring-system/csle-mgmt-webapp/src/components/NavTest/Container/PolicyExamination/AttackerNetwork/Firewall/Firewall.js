import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Firewall.css';
import firewall from './firewall.png';

const Firewall = ({ data }) => {
    return (
        <div className="firewall">
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={firewall} className="ibm_tower" alt="ids" width="100%" height="100%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


Firewall.propTypes = {};
Firewall.defaultProps = {};
export default Firewall;
