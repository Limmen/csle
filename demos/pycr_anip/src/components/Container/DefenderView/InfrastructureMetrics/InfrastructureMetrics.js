import React from 'react';
import './InfrastructureMetrics.css';
import SevereAlertsChart from "./SevereAlertsChart/SevereAlertsChart"
import WarningAlertsChart from "./WarningAlertsChart/WarningAlertsChart"
import LoginAttemptsChart from "./LoginAttemptsChart/LoginAttemptsChart"
import AccumulatedMetricsChart from "./AccumulatedMetricsChart/AccumulatedMetricsChart"

const InfrastructureMetrics = () => {
    return (
        <div className="Defender">
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <LoginAttemptsChart/>
                </div>
                <div className="col-sm-1">

                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <SevereAlertsChart/>
                </div>
                <div className="col-sm-1">

                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <WarningAlertsChart/>
                </div>
                <div className="col-sm-1">

                </div>
            </div>
        </div>
    );
}

InfrastructureMetrics.propTypes = {};
InfrastructureMetrics.defaultProps = {};
export default InfrastructureMetrics;

//<LoginAttemptsChart/>
//<WarningAlertsChart/>
//<SevereAlertsChart/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>