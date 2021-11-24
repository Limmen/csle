import React from 'react';
import './AttackerActionSpaceConfig.css';

const AttackerActionSpaceConfig = (props) => {

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
        <div className="AttackerActionSpaceConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
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
                    </div>
                </div>
            </div>
        </div>
    );
}

AttackerActionSpaceConfig.propTypes = {};
AttackerActionSpaceConfig.defaultProps = {};
export default AttackerActionSpaceConfig;