import React from 'react';
import './AttackerStaticPolicyConfig.css';

const AttackerStaticPolicyConfig = (props) => {

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
        <div className="AttackerStaticPolicyConfig">
            <div className="row">
                <div className="row">
                    <div className="col-sm-12">
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
                </div>
            </div>
        </div>
    );
}

AttackerStaticPolicyConfig.propTypes = {};
AttackerStaticPolicyConfig.defaultProps = {};
export default AttackerStaticPolicyConfig;