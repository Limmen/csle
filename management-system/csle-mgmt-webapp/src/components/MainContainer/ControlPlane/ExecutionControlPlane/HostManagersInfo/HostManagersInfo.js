import React from 'react';
import './HostManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

/**
 * Subcomponent of the /control-plane page that contains information about host managers
 */
const HostManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setHostManagersOpen(!props.hostManagersOpen)}
                    aria-controls="hostManagersBody"
                    aria-expanded={props.hostManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Host managers </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.hostManagersOpen}>
                <div id="hostManagersOpen" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("host-manager-stop-all")}
                            running={true} entity="host-manager"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("host-manager-start-all")}
                            running={false} entity="host-manager"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("host-monitor-stop-all")}
                            running={true} entity="host-monitor"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("host-monitor-start-all")}
                            running={false} entity="host-monitor"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                    </div>
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
                            {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                <tr key={"host-monitor-" + index}>
                                    <td>Host Manager</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td>{props.hostManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.hostManagersInfo.host_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("host-manager-" +
                                                props.hostManagersInfo.ips[index])}
                                            running={props.hostManagersInfo.host_managers_running[index]}
                                            entity={"host-manager"} name={"host-manager"}
                                            ip={props.hostManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.hostManagersInfo.ips[index]}
                                                    entity="host-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                <tr key={"host-monitor-" + index}>
                                    <td>Host monitor thread</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("host-monitor-" +
                                                props.hostManagersInfo.ips[index])}
                                            running={status.running}
                                            entity={"host-monitor"} name={"host-monitor"}
                                            ip={props.hostManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.hostManagersInfo.ips[index]}
                                                    entity="host-manager"/>
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

HostManagersInfo.propTypes = {};
HostManagersInfo.defaultProps = {};
export default HostManagersInfo;
