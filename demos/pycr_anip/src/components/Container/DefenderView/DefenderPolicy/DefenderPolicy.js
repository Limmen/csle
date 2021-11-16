import React from 'react';
import './DefenderPolicy.css';
import DefenderPolicyChart from "./DefenderPolicyChart/DefenderPolicyChart"

const DefenderPolicy = () => {
    return (
        <div className="Defender">
            <div className="row justify-content-center">
                <div className="col-sm-1">

                </div>
                <div className="col-sm-10">
                    <DefenderPolicyChart/>
                </div>
                <div className="col-sm-1">

                </div>
            </div>
        </div>
    );
}

DefenderPolicy.propTypes = {};
DefenderPolicy.defaultProps = {};
export default DefenderPolicy;

//<LoginAttemptsChart/>
//<WarningAlertsChart/>
//<SevereAlertsChart/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>