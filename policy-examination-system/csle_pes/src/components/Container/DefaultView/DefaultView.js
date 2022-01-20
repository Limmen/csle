import React from 'react';
import './DefaultView.css';
import { Navigate } from "react-router-dom";

const DefaultView = () => {

    return (
        <div className="DefaultView">
            <Navigate to="/" replace={true} />
        </div>
    );
}

DefaultView.propTypes = {};
DefaultView.defaultProps = {};
export default DefaultView;