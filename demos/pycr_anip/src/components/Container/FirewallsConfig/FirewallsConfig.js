import React from 'react';
import './FirewallsConfig.css';

const FirewallsConfig = (props) => {

    const FirewallConfigTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].topology_config.node_configs.map((node_firewall_config, index) => {

                        var forwardAccept = "-"
                        if (typeof node_firewall_config.forward_accept !== "undefined") {
                            if ("py/set" in node_firewall_config.forward_accept) {
                                forwardAccept = node_firewall_config.forward_accept["py/set"].join("\n")
                            }
                        }
                        var forwardDrop = "-"
                        if (typeof node_firewall_config.forward_drop !== "undefined") {
                            if ("py/set" in node_firewall_config.forward_drop) {
                                forwardDrop = node_firewall_config.forward_drop["py/set"].join("\n")
                            }
                        }

                        var inputAccept = "-"
                        if (typeof node_firewall_config.input_accept !== "undefined") {
                            if ("py/set" in node_firewall_config.input_accept) {
                                inputAccept = node_firewall_config.input_accept["py/set"].join("\n")
                            }
                        }
                        var inputDrop = "-"
                        if (typeof node_firewall_config.input_drop !== "undefined") {
                            if ("py/set" in node_firewall_config.input_drop) {
                                inputDrop = node_firewall_config.input_drop["py/set"].join("\n")
                            }
                        }

                        var outputAccept = "-"
                        if (typeof node_firewall_config.output_accept !== "undefined") {
                            if ("py/set" in node_firewall_config.output_accept) {
                                outputAccept = node_firewall_config.output_accept["py/set"].join("\n")
                            }
                        }
                        var outputDrop = "-"
                        if (typeof node_firewall_config.output_drop !== "undefined") {
                            if ("py/set" in node_firewall_config.output_drop) {
                                outputDrop = node_firewall_config.output_drop["py/set"].join("\n")
                            }
                        }
                        return (
                            <tr key={index}>
                                <td>{node_firewall_config.ip}</td>
                                <td>{node_firewall_config.hostname}</td>
                                <td>{node_firewall_config.default_gw}</td>
                                <td>{node_firewall_config.default_forward}</td>
                                <td>{node_firewall_config.default_input}</td>
                                <td>{node_firewall_config.default_output}</td>
                                <td>{forwardAccept}</td>
                                <td>{forwardDrop}</td>
                                <td>{inputAccept}</td>
                                <td>{inputDrop}</td>
                                <td>{outputAccept}</td>
                                <td>{outputDrop}</td>
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
        <div className="FirewallConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> Firewall configurations </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>Container IP</th>
                                    <th>Hostname</th>
                                    <th>Default gateway</th>
                                    <th>Default forward</th>
                                    <th>Default input</th>
                                    <th>Default output</th>
                                    <th>Forward accept</th>
                                    <th>Forward drop</th>
                                    <th>Input accept</th>
                                    <th>Input drop</th>
                                    <th>Output accept</th>
                                    <th>Output drop</th>
                                </tr>
                                </thead>
                                <FirewallConfigTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

FirewallsConfig.propTypes = {};
FirewallsConfig.defaultProps = {};
export default FirewallsConfig;