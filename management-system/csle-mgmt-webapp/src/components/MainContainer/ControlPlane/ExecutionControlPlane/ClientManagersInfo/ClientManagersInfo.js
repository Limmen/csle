import React from 'react';
import './ClientManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import {
    CLIENT_PRODUCER_SUBRESOURCE,
    CLIENT_MANAGER_SUBRESOURCE,
    CLIENT_POPULATION_SUBRESOURCE} from "../../../../Common/constants";

/**
 * Subcomponent of the /control-plane page that contains information about client managers
 */
const ClientManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setClientManagersOpen(!props.clientManagersOpen)}
                    aria-controls="clientManagersBody"
                    aria-expanded={props.clientManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Client managers
                        <i className="fa fa-users headerIcon" aria-hidden="true"></i>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.clientManagersOpen}>
                <div id="clientManagersBody" className="cardBodyHidden">
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Service</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Status</th>
                                <th># Clients</th>
                                <th>Time-step length (s)</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.clientManagersInfo.client_managers_statuses.map((status, index) =>
                                <tr key={`${CLIENT_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>Client manager</td>
                                    <td>{props.clientManagersInfo.ips[index]}</td>
                                    <td>{props.clientManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.clientManagersInfo.client_managers_running[index])}
                                    <td></td>
                                    <td>{status.clients_time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(`
                                            ${CLIENT_MANAGER_SUBRESOURCE}-${props.clientManagersInfo.ips[index]}`)}
                                            running={props.clientManagersInfo.client_managers_running[index]}
                                            entity={CLIENT_MANAGER_SUBRESOURCE} name={CLIENT_MANAGER_SUBRESOURCE}
                                            ip={props.clientManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.clientManagersInfo.ips[index]}
                                                    entity={CLIENT_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.clientManagersInfo.client_managers_statuses.map((status, index) =>
                                <tr key={`${CLIENT_POPULATION_SUBRESOURCE}-${index}`}>
                                    <td>Client process</td>
                                    <td>{props.clientManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.client_process_active)}
                                    <td>{status.num_clients}</td>
                                    <td>{status.clients_time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${CLIENT_POPULATION_SUBRESOURCE}-`
                                                +`${props.clientManagersInfo.ips[index]}`)}
                                            running={status.client_process_active}
                                            entity={CLIENT_POPULATION_SUBRESOURCE} name={CLIENT_POPULATION_SUBRESOURCE}
                                            ip={props.clientManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.clientManagersInfo.ips[index]}
                                                    entity={CLIENT_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.clientManagersInfo.client_managers_statuses.map((status, index) =>
                                <tr key={`${CLIENT_PRODUCER_SUBRESOURCE}-${index}`}>
                                    <td>Producer process</td>
                                    <td>{props.clientManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.producer_active)}
                                    <td></td>
                                    <td>{status.clients_time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${CLIENT_PRODUCER_SUBRESOURCE}-`
                                                +`${props.clientManagersInfo.ips[index]}`)}
                                            running={status.producer_active}
                                            entity={CLIENT_PRODUCER_SUBRESOURCE} name={CLIENT_PRODUCER_SUBRESOURCE}
                                            ip={props.clientManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.clientManagersInfo.ips[index]}
                                                    entity={CLIENT_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}/>
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

ClientManagersInfo.propTypes = {};
ClientManagersInfo.defaultProps = {};
export default ClientManagersInfo;
