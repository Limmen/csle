import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Defender.css';
import laptop from './laptop.png';

const defenderStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
};

const Defender = ({ data }) => {
    return (
        <div style={defenderStyles}>
            <Handle type="target" position="top" style={{ borderRadius: 0 }} />
            <img src={laptop} className="defender" alt="defender" width="100%" height="100%"/>
            <div>{data.text}</div>
        </div>
    );
};


Defender.propTypes = {};
Defender.defaultProps = {};
export default Defender;
