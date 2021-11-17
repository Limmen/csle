import React from 'react';
import './DefaultView.css';
import { Navigate } from "react-router-dom";

const DefaultView = () => {

    return (
        <div className="DefaultView">
            <Navigate to="/dashboard/defender" replace={true} />
        </div>
    );
}

DefaultView.propTypes = {};
DefaultView.defaultProps = {};
export default DefaultView;