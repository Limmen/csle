import React from 'react';
import './TrafficConfig.css';

const TrafficConfig = (props) => {

    const TrafficConfigTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].traffic_config.node_traffic_configs.map((traffic_config, index) => {
                    const commands = traffic_config.commands.join("\n")
                    const target_servers = traffic_config.target_hosts.join("\n")
                    const jumphosts = traffic_config.jumphosts.join("\n")
                        return (
                            <tr key={index}>
                                <td>{traffic_config.ip}</td>
                                <td>{target_servers}</td>
                                <td>{jumphosts}</td>
                                <td>{commands}</td>
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
        <div className="TrafficConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> Clients </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>Client IP</th>
                                    <th>Target servers</th>
                                    <th>Jumphosts</th>
                                    <th>Commands</th>
                                </tr>
                                </thead>
                                <TrafficConfigTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

TrafficConfig.propTypes = {};
TrafficConfig.defaultProps = {};
export default TrafficConfig;