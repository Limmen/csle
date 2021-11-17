import React from 'react';
import './InfrastructureMetrics.css';
import SevereAlertsChart from "./SevereAlertsChart/SevereAlertsChart"

const InfrastructureMetrics = (props) => {

    return (
        <div className="Defender">
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <SevereAlertsChart className="alertsChart" traces={props.traces} activeTrace={props.activeTrace} t={props.t} />
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
//<AttackerMetricsCharts/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>