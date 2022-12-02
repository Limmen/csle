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
    STOP_ALL_PROPERTY, FILEBEAT_SUBRESOURCE, PACKETBEAT_SUBRESOURCE, METRICBEAT_SUBRESOURCE,
    HEARTBEAT_SUBRESOURCE
} from "../../../../Common/constants";

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
                        <div className="aggregateActionsContainer beatsAllActions">
                            <span className="aggregateActions">Stop all filebeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${FILEBEAT_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                                running={true} entity={FILEBEAT_SUBRESOURCE}
                                name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                            <span className="aggregateActions">Start all filebeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${FILEBEAT_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                                running={false} entity={FILEBEAT_SUBRESOURCE}
                                name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />

                            <span className="aggregateActions">Stop all packetbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${PACKETBEAT_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                                running={true} entity={PACKETBEAT_SUBRESOURCE}
                                name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                            <span className="aggregateActions">Start all packetbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${PACKETBEAT_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                                running={false} entity={PACKETBEAT_SUBRESOURCE}
                                name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                        </div>
                        <div className="aggregateActionsContainer beatsAllActions">
                            <span className="aggregateActions">Stop all metricbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${METRICBEAT_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                                running={true} entity={METRICBEAT_SUBRESOURCE}
                                name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                            <span className="aggregateActions">Start all metricbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${METRICBEAT_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                                running={false} entity={METRICBEAT_SUBRESOURCE}
                                name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                            <span className="aggregateActions">Stop all heartbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${HEARTBEAT_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                                running={true} entity={HEARTBEAT_SUBRESOURCE}
                                name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                            <span className="aggregateActions">Start all heartbeats:</span>
                            <SpinnerOrButton
                                loading={props.loadingEntities.includes(
                                    `${HEARTBEAT_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                                running={false} entity={HEARTBEAT_SUBRESOURCE}
                                name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                                startOrStop={props.startOrStop}
                            />
                        </div>
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
                                <tr key={`${HOST_MANAGER_SUBRESOURCE}-${index}`}>
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
                                    {props.activeStatus(status.monitor_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${HOST_MONITOR_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.monitor_running}
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
                            {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                <tr key={`${FILEBEAT_SUBRESOURCE}-${index}`}>
                                    <td>Filebeat</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.filebeat_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${FILEBEAT_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.filebeat_running}
                                            entity={FILEBEAT_SUBRESOURCE}
                                            name={FILEBEAT_SUBRESOURCE}
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
                                <tr key={`${PACKETBEAT_SUBRESOURCE}-${index}`}>
                                    <td>Packetbeat</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.packetbeat_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${PACKETBEAT_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.packetbeat_running}
                                            entity={PACKETBEAT_SUBRESOURCE}
                                            name={PACKETBEAT_SUBRESOURCE}
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
                                <tr key={`${METRICBEAT_SUBRESOURCE}-${index}`}>
                                    <td>Metricbeat</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.metricbeat_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${METRICBEAT_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.metricbeat_running}
                                            entity={METRICBEAT_SUBRESOURCE}
                                            name={METRICBEAT_SUBRESOURCE}
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
                                <tr key={`${HEARTBEAT_SUBRESOURCE}-${index}`}>
                                    <td>Heartbeat</td>
                                    <td>{props.hostManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.heartbeat_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${HEARTBEAT_SUBRESOURCE}-`
                                                + `${props.hostManagersInfo.ips[index]}`)}
                                            running={status.heartbeat_running}
                                            entity={HEARTBEAT_SUBRESOURCE}
                                            name={HEARTBEAT_SUBRESOURCE}
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
    )
        ;
}

HostManagersInfo.propTypes = {};
HostManagersInfo.defaultProps = {};
export default HostManagersInfo;
