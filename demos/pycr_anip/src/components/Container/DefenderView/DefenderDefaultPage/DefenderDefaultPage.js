import React from 'react';
import './DefenderDefaultPage.css';
import { Navigate } from "react-router-dom";

const DefenderDefaultPage = () => {

    return (
        <div className="DefaultView">
            <Navigate to="/dashboard/defender/network" replace={true} />
        </div>
    );
}

DefenderDefaultPage.propTypes = {};
DefenderDefaultPage.defaultProps = {};
export default DefenderDefaultPage;