import React from 'react';
import './DefenderPolicy.css';
import DefenderPolicyChart from "./DefenderPolicyChart/DefenderPolicyChart"

const DefenderPolicy = (props) => {

    const StopActionsTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].stop_actions.map((stopAction, index) =>
                    <tr key={index}>
                        <td>{stopAction.l}</td>
                        <td><code>{stopAction.command}</code></td>
                    </tr>
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    return (
        <div className="Defender">
            <div className="row justify-content-center">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <DefenderPolicyChart defenderPolicies={props.defenderPolicies}
                                         activeDefenderPolicy={props.activeDefenderPolicy}
                                         setActiveDefenderPolicy={props.setActiveDefenderPolicy}
                                         traces={props.traces} activeTrace={props.activeTrace}
                                         t={props.t}
                    />
                </div>
                <div className="col-sm-1">
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <table className="table table-hover table-striped stopactionsTable">
                        <thead>
                        <tr>
                            <th>Stops remaining l</th>
                            <th>Command</th>
                        </tr>
                        </thead>
                        <StopActionsTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                    </table>
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
