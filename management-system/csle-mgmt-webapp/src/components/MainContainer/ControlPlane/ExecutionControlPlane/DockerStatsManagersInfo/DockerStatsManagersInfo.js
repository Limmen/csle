import React from 'react';
import './DockerStatsManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

/**
 * Subcomponent of the /control-plane page that contains information about Docker stats managers
 */
const DockerStatsManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setDockerStatsManagersOpen(!props.dockerStatsManagersOpen)}
                    aria-controls="dockerStatsManagersBody"
                    aria-expanded={props.dockerStatsManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Docker Statistics Managers
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.dockerStatsManagersOpen}>
                <div id="dockerStatsManagersBody" className="cardBodyHidden">
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Service</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.dockerStatsManagersInfo.docker_stats_managers_statuses.map((status, index) =>
                                <tr key={"docker-stats-manager-" + index}>
                                    <td>Docker Statistics Manager</td>
                                    <td>{props.dockerStatsManagersInfo.ips[index]}</td>
                                    <td>{props.dockerStatsManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.dockerStatsManagersInfo.docker_stats_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("docker-stats-manager-" +
                                                props.dockerStatsManagersInfo.ips[index])}
                                            running={props.dockerStatsManagersInfo.docker_stats_managers_running[index]}
                                            entity={"docker-stats-manager"} name={"docker-stats-manager"}
                                            ip={props.dockerStatsManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.dockerStatsManagersInfo.ips[index]}
                                                    entity="docker-stats-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.dockerStatsManagersInfo.docker_stats_managers_statuses.map((status, index) =>
                                <tr key={"docker-stats-monitor-" + index}>
                                    <td>Docker Statistics Monitor Thread</td>
                                    <td>{props.dockerStatsManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.num_monitors > 0)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("docker-stats-monitor-" +
                                                props.dockerStatsManagersInfo.ips[index])}
                                            running={status.num_monitors > 0}
                                            entity={"docker-stats-monitor"} name={"docker-stats-monitor"}
                                            ip={props.dockerStatsManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.dockerStatsManagersInfo.ips[index]}
                                                    entity="docker-stats-manager"/>
                                    </td>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </Collapse>
        </Card>
    );
}

DockerStatsManagersInfo.propTypes = {};
DockerStatsManagersInfo.defaultProps = {};
export default DockerStatsManagersInfo;
