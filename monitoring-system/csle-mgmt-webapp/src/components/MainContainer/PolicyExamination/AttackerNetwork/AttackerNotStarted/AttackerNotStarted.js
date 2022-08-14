import React from 'react';
import {Handle} from 'react-flow-renderer';
import './AttackerNotStarted.css';
import hacker from './hacker.png';

const attackerStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

/**
 * Component representing an attacker that has not started an intrusion
 * in the network animation in the policy examination page
 */
const AttackerNotStarted = ({ data }) => {
    return (
        <div style={attackerStyles}>
            <div className="largeFont">{data.text}</div>
            <img src={hacker} className="attackerNotStarted" alt="attacker" width="25%" height="25%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


AttackerNotStarted.propTypes = {};
AttackerNotStarted.defaultProps = {};
export default AttackerNotStarted;
