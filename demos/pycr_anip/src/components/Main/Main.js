import React from 'react';
import './Main.css';
import Network from "./Network/Network";
import SevereAlertsChart from "./SevereAlertsChart/SevereAlertsChart"
import WarningAlertsChart from "./WarningAlertsChart/WarningAlertsChart"
import LoginAttemptsChart from "./LoginAttemptsChart/LoginAttemptsChart"
import BeliefAndStoppingChart from "./BeliefAndStoppingChart/BeliefAndStoppingChart"
import AccumulatedMetricsChart from "./AccumulatedMetricsChart/AccumulatedMetricsChart"


const Main = () => {
    return (
        <div className="Main">
            <div className="row">
            <div className="col-sm-4">
                <div className="network">
                    <Network/>
                </div>
            </div>
            <div className="col-sm-4">
                <BeliefAndStoppingChart/>
            </div>
            <div className="col-sm-4">
                <AccumulatedMetricsChart/>
            </div>
            </div>
            <div className="row metricsLineChartsRow">
            <div className="col-sm-4">
                <SevereAlertsChart/>
            </div>
                <div className="col-sm-4">
                    <WarningAlertsChart/>
                </div>
                <div className="col-sm-4">
                    <LoginAttemptsChart/>
                </div>
            </div>
        </div>
    );
}

Main.propTypes = {};
Main.defaultProps = {};
export default Main;
