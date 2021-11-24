import React from 'react';
import './AttackerLog.css';

const AttackerLog = (props) => {

    const AttackerLogTable = (props) => {
        if (props.traces.length > 0) {
            const filteredObservations = props.traces[props.activeTrace].attacker_observations.filter((attackerObs, index) => index <= props.t)
            const filteredRewards = props.traces[props.activeTrace].attacker_rewards.filter((attackerReward, index) => index <= props.t)
            const filteredActions = props.traces[props.activeTrace].attacker_actions
                .filter((attackerAction, index) => index <= props.t).map((attackerAction, index) => {
                    if (attackerAction === -1) {
                        return props.traces[props.activeTrace].attacker_continue_action
                    } else {
                        return attackerAction
                    }
                })
            const filteredNumHostsFound = props.traces[props.activeTrace].attacker_number_of_found_nodes.filter((attackerAction, index) => index <= props.t)
            const filteredNumHostsCompromised = props.traces[props.activeTrace].attacker_number_of_compromised_nodes.filter((attackerAction, index) => index <= props.t)
            return (<tbody>
            {filteredObservations.map((attackerObs, index) =>
                <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{filteredNumHostsFound[index]}</td>
                    <td>{filteredNumHostsCompromised[index]}</td>
                    <td>{filteredRewards[index]}</td>
                    <td>{props.traces[props.activeTrace].attacker_action_descriptions[filteredActions[index]].command}</td>
                </tr>
            ).reverse()}
            </tbody>);
        } else {
            return (<tbody></tbody>);
        }
    }

    return (
        <div className="AttackerLog">
            <div className="row">
                <div className="row">
                    <div className="col-sm-12">
                        <h4> Attacker Log </h4>
                        <table className="table table-hover table-striped">
                            <thead>
                            <tr>
                                <th>Time-step t</th>
                                <th># Found Hosts Total</th>
                                <th># Compromised Hosts Total</th>
                                <th>Reward</th>
                                <th>Action</th>
                            </tr>
                            </thead>
                            <AttackerLogTable traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}

AttackerLog.propTypes = {};
AttackerLog.defaultProps = {};
export default AttackerLog;