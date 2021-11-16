import React from 'react';
import {Handle} from 'react-flow-renderer';
import './Client.css';
import workstation from './workstation.png';

const clientStyles = {
    background: '#FFFF',
    color: '#000000',
    padding: 0,
    display: 'inline-block',
    position: 'relative'
};

const Client = ({ data }) => {
    return (
        <div style={clientStyles} className="clientPopulation">
            <div>{data.text}</div>
            <img src={workstation} className="rounded float-left" alt="client" height="30%" width="30%"/>
            <img src={workstation} className="rounded float-left" alt="client" height="30%" width="30%"/>
            <img src={workstation} className="rounded float-left" alt="client" height="30%" width="30%"/>
            <Handle type="source" position="bottom" style={{ borderRadius: 0 }} />
        </div>
    );
};


Client.propTypes = {};
Client.defaultProps = {};
export default Client;
