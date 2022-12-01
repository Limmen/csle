import React from 'react';
import './TrafficManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import {
    TRAFFIC_MANAGER_SUBRESOURCE,
    TRAFFIC_GENERATOR_SUBRESOURCE,
    START_ALL_PROPERTY,
    STOP_ALL_PROPERTY} from "../../../../Common/constants";

/**
 * Subcomponent of the /control-plane page that contains information about traffic managers
 */
const TrafficManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setTrafficManagersOpen(!props.trafficManagersOpen)}
                    aria-controls="trafficManagersBody"
                    aria-expanded={props.trafficManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Traffic managers
                        <i className="fa fa-chrome headerIcon" aria-hidden="true"></i>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.trafficManagersOpen}>
                <div id="trafficManagersBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${TRAFFIC_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={TRAFFIC_MANAGER_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${TRAFFIC_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={TRAFFIC_MANAGER_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all generators:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${TRAFFIC_GENERATOR_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={TRAFFIC_GENERATOR_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all generators:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${TRAFFIC_GENERATOR_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={TRAFFIC_GENERATOR_SUBRESOURCE}
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
                            {props.trafficManagersInfo.traffic_managers_statuses.map((status, index) =>
                                <tr key={`${TRAFFIC_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>Traffic Manager</td>
                                    <td>{props.trafficManagersInfo.ips[index]}</td>
                                    <td>{props.trafficManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.trafficManagersInfo.traffic_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${TRAFFIC_MANAGER_SUBRESOURCE}-`
                                                + `${props.trafficManagersInfo.ips[index]}`)}
                                            running={props.trafficManagersInfo.traffic_managers_running[index]}
                                            entity={TRAFFIC_MANAGER_SUBRESOURCE} name={TRAFFIC_MANAGER_SUBRESOURCE}
                                            ip={props.trafficManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                    entity={TRAFFIC_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.trafficManagersInfo.traffic_managers_statuses.map((status, index) =>
                                <tr key={`${TRAFFIC_GENERATOR_SUBRESOURCE}-${index}`}>
                                    <td>Traffic Generator</td>
                                    <td>{props.trafficManagersInfo.ips[index]}</td>
                                    <td>-</td>
                                    {props.activeStatus(status.running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${TRAFFIC_GENERATOR_SUBRESOURCE}-`
                                                + `${props.trafficManagersInfo.ips[index]}`)}
                                            running={status.running}
                                            entity={TRAFFIC_GENERATOR_SUBRESOURCE}
                                            name={TRAFFIC_GENERATOR_SUBRESOURCE}
                                            ip={props.trafficManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                    entity={TRAFFIC_MANAGER_SUBRESOURCE}
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

TrafficManagersInfo.propTypes = {};
TrafficManagersInfo.defaultProps = {};
export default TrafficManagersInfo;
