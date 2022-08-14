import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Defender.css';
import laptop from './laptop.png';

const defenderStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

/**
 * Component representing a defender in the network animation in the policy examination page
 */
const Defender = ({ data }) => {
    return (
        <div style={defenderStyles}>
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={laptop} className="defender" alt="defender" width="80%" height="100%"/>
            <div className="largeFont">{data.text}</div>
        </div>
    );
};


Defender.propTypes = {};
Defender.defaultProps = {};
export default Defender;
