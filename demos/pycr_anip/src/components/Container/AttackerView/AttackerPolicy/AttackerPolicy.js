import React from 'react';
import './AttackerPolicy.css';

const AttackerPolicy = (props) => {

    const ActionsTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].attacker_action_descriptions.map((action, index) =>
                    <tr key={index}>
                        <td>{action.id}</td>
                        <td><code>{action.command}</code></td>
                    </tr>
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    const StaticPolicyTableBody = (props) => {
        if (props.traces.length > 0) {
            const transformedActions = props.traces[props.activeTrace].attacker_actions.map((attackerAction, index) => {
                if (attackerAction === -1) {
                    return props.traces[props.activeTrace].attacker_continue_action
                } else {
                    return attackerAction
                }
            })
            return (
                <tbody>
                {transformedActions.map((action, index) =>
                    <tr key={index}>
                        <td>{index+1}</td>
                        <td>{action}</td>
                        <td><code>{props.traces[props.activeTrace].attacker_action_descriptions[action].command}</code></td>
                    </tr>
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    return (
        <div className="AttackerPolicy">
            <div className="row justify-content-center">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <h5> Static Attacker Policy </h5>
                    <table className="table table-hover table-striped attackeractionsTable">
                        <thead>
                        <tr>
                            <th>Time-step t</th>
                            <th>Action ID</th>
                            <th>Command</th>
                        </tr>
                        </thead>
                        <StaticPolicyTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                    </table>
                </div>
                <div className="col-sm-1">
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <h5> Attacker Action Space </h5>
                    <table className="table table-hover table-striped attackeractionsTable">
                        <thead>
                        <tr>
                            <th>Action Id</th>
                            <th>Command</th>
                        </tr>
                        </thead>
                        <ActionsTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                    </table>
                </div>
                <div className="col-sm-1">
                </div>
            </div>
        </div>
    );
}

AttackerPolicy.propTypes = {};
AttackerPolicy.defaultProps = {};
export default AttackerPolicy;
