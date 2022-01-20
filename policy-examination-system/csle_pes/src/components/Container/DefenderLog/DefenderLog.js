import React from 'react';
import './DefenderLog.css';

const DefenderLog = (props) => {

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

    return (
        <div className="ActivityLog">
            <div className="row">
                <div className="row">
                    <div className="col-sm-12">
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
                </div>
            </div>
        </div>
    );
}

DefenderLog.propTypes = {};
DefenderLog.defaultProps = {};
export default DefenderLog;