import React from 'react';
import './FlagsConfig.css';

const FlagsConfig = (props) => {

    const FlagsConfigTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].flags_config.flags.map((node_flag_config, index) => {
                        var flag = node_flag_config.flags[0]["py/tuple"]
                        var rootAccess = "No"
                        if (flag[4]) {
                            rootAccess = "Yes"
                        }
                        return (
                            <tr key={index}>
                                <td>{node_flag_config.ip}</td>
                                <td>{flag[0]}</td>
                                <td>{flag[1]}</td>
                                <td>{flag[3]}</td>
                                <td>{rootAccess}</td>
                                <td>{flag[5]}</td>
                            </tr>
                        )
                    }
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    return (
        <div className="FlagsConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> Flags </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>Container IP</th>
                                    <th>Path</th>
                                    <th>Name</th>
                                    <th>ID</th>
                                    <th>Requires root</th>
                                    <th>Score</th>
                                </tr>
                                </thead>
                                <FlagsConfigTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

FlagsConfig.propTypes = {};
FlagsConfig.defaultProps = {};
export default FlagsConfig;