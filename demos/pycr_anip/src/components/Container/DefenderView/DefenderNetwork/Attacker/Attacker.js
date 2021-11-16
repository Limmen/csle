import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Attacker.css';
import hacker from './hacker.png';

const attackerStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

const Attacker = ({ data }) => {
    return (
        <div style={attackerStyles}>
            <div>{data.text}</div>
            <img src={hacker} className="attacker" alt="attacker" width="25%" height="25%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


Attacker.propTypes = {};
Attacker.defaultProps = {};
export default Attacker;
