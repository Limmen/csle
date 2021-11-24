import React from 'react';
import './VulnerabilitiesConfig.css';

const VulnerabilitiesConfig = (props) => {

    const VulnerabilitiesConfigTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].vulnerabilities_config.vulnerabilities.map((vuln, index) => {
                        var vulnTypeId = 0
                        if ("py/reduce" in vuln.vuln_type) {
                            vulnTypeId = vuln.vuln_type["py/reduce"][1]["py/tuple"][0]
                        } else {
                            if ("py/id" in vuln.vuln_type) {
                                vulnTypeId = vuln.vuln_type["py/id"]
                            }
                        }
                        var vulnType = "brute-force vulnerability"
                        if (vulnTypeId === 0) {
                            vulnType = "brute-force vulnerability"
                        }
                        if (vulnTypeId === 1) {
                            vulnType = "remote-code execution"
                        }
                        if (vulnTypeId === 2) {
                            vulnType = "sql-injection"
                        }
                        if (vulnTypeId === 3) {
                            vulnType = "privilige escalation"
                        }
                        var rootAccess = "No"
                        if (vuln.root) {
                            rootAccess = "Yes"
                        }
                        return (
                            <tr key={index}>
                                <td>{vuln.node_ip}</td>
                                <td>{vulnType}</td>
                                <td>{rootAccess}</td>
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
        <div className="VulnerabilitiesConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> Vulnerable Containers </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>IP</th>
                                    <th>Vulnerability type</th>
                                    <th>Root access</th>
                                </tr>
                                </thead>
                                <VulnerabilitiesConfigTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

VulnerabilitiesConfig.propTypes = {};
VulnerabilitiesConfig.defaultProps = {};
export default VulnerabilitiesConfig;