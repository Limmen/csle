import React from 'react';
import './AttackerMetrics.css';
import AttackerMetricsCharts from "./AttackerMetricsCharts/AttackerMetricsChart"

const AttackerMetrics = (props) => {

    return (
        <div className="AttackerMetrics">
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <AttackerMetricsCharts className="attackerMetricCharts"
                                           traces={props.traces} activeTrace={props.activeTrace} t={props.t} />
                </div>
                <div className="col-sm-1">

                </div>
            </div>
        </div>
    );
}

AttackerMetrics.propTypes = {};
AttackerMetrics.defaultProps = {};
export default AttackerMetrics;

//<LoginAttemptsChart/>
//<WarningAlertsChart/>
//<AttackerMetricsCharts/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>