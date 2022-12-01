import React from 'react';
import './HostManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import {
    HOST_MONITOR_SUBRESOURCE,
    HOST_MANAGER_SUBRESOURCE,
    START_ALL_PROPERTY,
    STOP_ALL_PROPERTY} from "../../../../Common/constants";

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
                    <h5 className="semiTitle"> Host managers
                        <i className="fa fa-server headerIcon" aria-hidden="true"></i>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.hostManagersOpen}>
                <div id="hostManagersOpen" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${HOST_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={HOST_MANAGER_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${HOST_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={HOST_MANAGER_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${HOST_MONITOR_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={HOST_MONITOR_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${HOST_MONITOR_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={HOST_MONITOR_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
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
                                <tr key={`${HOST_MONITOR_SUBRESOURCE}-${index}`}>
                                    <td>Host Manager</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td>{props.hostManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.hostManagersInfo.host_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${HOST_MANAGER_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={props.hostManagersInfo.host_managers_running[index]}
                                            entity={HOST_MANAGER_SUBRESOURCE} name={HOST_MANAGER_SUBRESOURCE}
                                            ip={props.hostManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.hostManagersInfo.ips[index]}
                                                    entity={HOST_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                <tr key={`${HOST_MONITOR_SUBRESOURCE}-${index}`}>
                                    <td>Host monitor thread</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${HOST_MONITOR_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.running}
                                            entity={HOST_MONITOR_SUBRESOURCE}
                                            name={HOST_MONITOR_SUBRESOURCE}
                                            ip={props.hostManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.hostManagersInfo.ips[index]}
                                                    entity={HOST_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
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
