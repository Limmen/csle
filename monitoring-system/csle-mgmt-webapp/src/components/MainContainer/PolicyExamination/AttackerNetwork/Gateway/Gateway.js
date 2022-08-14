import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Gateway.css';
import router from './router.png';

const gatewayStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

/**
 * Component representing a gateway in the network animation in the policy examination page
 */
const Gateway = ({ data }) => {
    return (
        <div style={gatewayStyles}>
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={router} className="router" alt="router" width="75%" height="75%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


Gateway.propTypes = {};
Gateway.defaultProps = {};
export default Gateway;
