import React from 'react';
import {Handle} from 'react-flow-renderer';
import './AttackerNotStarted.css';
import hacker from './hacker.png';

const attackerStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

const AttackerNotStarted = ({ data }) => {
    return (
        <div style={attackerStyles}>
            <div>{data.text}</div>
            <img src={hacker} className="attackerNotStarted" alt="attacker" width="25%" height="25%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


AttackerNotStarted.propTypes = {};
AttackerNotStarted.defaultProps = {};
export default AttackerNotStarted;
