import React from 'react';
import './ActivityLog.css';

const ActivityLog = (props) => {

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

    const DefenderLogTable = (props) => {
        if (props.traces.length > 0) {
            const filteredObservations = props.traces[props.activeTrace].defender_observations.filter((defenderObs) =>
                defenderObs[defenderObs.length - 1] <= props.t + 1)
            const filteredRewards = props.traces[props.activeTrace].defender_rewards.filter((defenderReward, index) => index <= props.t)
            const filteredActions = props.traces[props.activeTrace].defender_actions.filter((defenderAction, index) => index <= props.t).map((defenderAction, index) => {
                if (defenderAction == -1 || defenderAction == 1) {
                    return "Continue"
                } else {
                    return "Stop"
                }
            })
            return (<tbody>
            {filteredObservations.map((defenderObs, index) =>
                <tr key={index}>
                    <td>{defenderObs[defenderObs.length - 1]}</td>
                    <td>{defenderObs[0]}</td>
                    <td>{defenderObs[1]}</td>
                    <td>{defenderObs[2]}</td>
                    <td>{filteredRewards[index]}</td>
                    <td>{filteredActions[index]}</td>
                </tr>
            ).reverse()}
            </tbody>);
        } else {
            return (<tbody></tbody>);
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

    return (
        <div className="ActivityLog">
            <div className="row">
                <div className="row">
                    <div className="col-sm-1"></div>
                    <div className="col-sm-10">
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
                    <div className="col-sm-1"></div>
                </div>
            </div>
            <div className="row">
                <div className="row">
                    <div className="col-sm-1"></div>
                    <div className="col-sm-10">
                        <h4> Defender Log </h4>
                        <table className="table table-hover table-striped">
                            <thead>
                            <tr>
                                <th>Time-step t</th>
                                <th>Severe IDS alerts Δx</th>
                                <th>Warning IDS alerts Δy</th>
                                <th>Login attempts Δz</th>
                                <th>Reward</th>
                                <th>Action</th>
                            </tr>
                            </thead>
                            <DefenderLogTable traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
                        </table>
                    </div>
                    <div className="col-sm-1"></div>
                </div>
            </div>
            <div className="row">
                <div className="row">
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
            </div>
            <div className="row">
                <div className="row">
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
        </div>
    );
}

ActivityLog.propTypes = {};
ActivityLog.defaultProps = {};
export default ActivityLog;