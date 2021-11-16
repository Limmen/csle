import React from 'react';
import './DefenderLog.css';

const DefenderLog = () => {
    const log = [{"t": 1, "delta_x": 14, "delta_y": 27, "delta_z": 12, "reward": 5},
        {"t": 2, "delta_x": 134, "delta_y": 2, "delta_z": 61, "reward": 8},
        {"t": 3, "delta_x": 15, "delta_y": 22, "delta_z": 234, "reward": 12},
        {"t": 4, "delta_x": 21, "delta_y": 92, "delta_z": 55, "reward": 14},
        {"t": 5, "delta_x": 79, "delta_y": 21, "delta_z": 41, "reward": 19}
    ]

    return (
        <div className="DefenderLog">
            {/*<h4 className="defenderLogTitle">  </h4> */}
            <div className="row justify-content-center">
                <div className="col-sm-1"></div>
                <div className="col-sm-10">
                    <table className="table table-hover table-striped">
                        <thead>
                        <tr>
                            <th>Time-step t</th>
                            <th>Severe IDS alerts Δx</th>
                            <th>Warning IDS alerts Δy</th>
                            <th>Login attempts Δz</th>
                            <th>Reward</th>
                        </tr>
                        </thead>
                        <tbody>
                        {log.map((logEntry, index) =>
                            <tr>
                                <td>{logEntry.t}</td>
                                <td>{logEntry.delta_x}</td>
                                <td>{logEntry.delta_y}</td>
                                <td>{logEntry.delta_z}</td>
                                <td>{logEntry.reward}</td>
                            </tr>
                        )}
                        </tbody>
                    </table>
                </div>
                <div className="col-sm-1"></div>
            </div>
        </div>
    );
}

DefenderLog.propTypes = {};
DefenderLog.defaultProps = {};
export default DefenderLog;

//<LoginAttemptsChart/>
//<WarningAlertsChart/>
//<SevereAlertsChart/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>