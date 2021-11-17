import React from 'react';
import './AttackerDefaultPage.css';
import { Navigate } from "react-router-dom";

const AttackerDefaultPage = () => {

    return (
        <div className="AttackerDefaultPage">
            <Navigate to="/dashboard/attacker/network" replace={true} />
        </div>
    );
}

AttackerDefaultPage.propTypes = {};
AttackerDefaultPage.defaultProps = {};
export default AttackerDefaultPage;