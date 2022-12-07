import React from 'react';
import './RyuManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import RyuImg from './Ryu.png'
import {
    RYU_MONITOR_SUBRESOURCE,
    RYU_MANAGER_SUBRESOURCE,
    RYU_CONTROLLER_SUBRESOURCE
} from "../../../../Common/constants";
import ElasticImg from "../../../Emulations/Emulation/Elastic.png";

/**
 * Subcomponent of the /control-plane page that contains information about Ryu managers
 */
const RyuManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setRyuManagersOpen(!props.ryuManagersOpen)}
                    aria-controls="ryuManagersBody"
                    aria-expanded={props.ryuManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Ryu managers
                        <img src={RyuImg} alt="Ryu" className="img-fluid headerIcon elastic"/>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.ryuManagersOpen}>
                <div id="ryuManagersBody" className="cardBodyHidden">
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Service</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Status</th>
                                <th>Time-step length (s)</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.ryuManagersInfo.ryu_managers_statuses.map((status, index) =>
                                <tr key={`${RYU_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>Ryu manager</td>
                                    <td>{props.ryuManagersInfo.ips[index]}</td>
                                    <td>{props.ryuManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.ryuManagersInfo.ryu_managers_running[index])}
                                    <td>{status.time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(`
                                            ${RYU_MANAGER_SUBRESOURCE}-${props.ryuManagersInfo.ips[index]}`)}
                                            running={props.ryuManagersInfo.ryu_managers_running[index]}
                                            entity={RYU_MANAGER_SUBRESOURCE} name={RYU_MANAGER_SUBRESOURCE}
                                            ip={props.ryuManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ryuManagersInfo.ips[index]}
                                                    entity={RYU_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.ryuManagersInfo.ryu_managers_statuses.map((status, index) =>
                                <tr key={`${RYU_CONTROLLER_SUBRESOURCE}-${index}`}>
                                    <td>Ryu controller</td>
                                    <td>{props.ryuManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.ryu_running)}
                                    <td>{status.time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_CONTROLLER_SUBRESOURCE}-`
                                                +`${props.ryuManagersInfo.ips[index]}`)}
                                            running={status.ryu_running}
                                            entity={RYU_CONTROLLER_SUBRESOURCE}
                                            name={RYU_CONTROLLER_SUBRESOURCE}
                                            ip={props.ryuManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ryuManagersInfo.ips[index]}
                                                    entity={RYU_CONTROLLER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.ryuManagersInfo.ryu_managers_statuses.map((status, index) =>
                                <tr key={`${RYU_MONITOR_SUBRESOURCE}-${index}`}>
                                    <td>Controller monitor</td>
                                    <td>{props.ryuManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.producer_active)}
                                    <td></td>
                                    <td>{status.time_step_len_seconds}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_CONTROLLER_SUBRESOURCE}-`
                                                +`${props.ryuManagersInfo.ips[index]}`)}
                                            running={status.producer_active}
                                            entity={RYU_CONTROLLER_SUBRESOURCE} name={RYU_CONTROLLER_SUBRESOURCE}
                                            ip={props.ryuManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ryuManagersInfo.ips[index]}
                                                    entity={RYU_CONTROLLER_SUBRESOURCE}
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

RyuManagersInfo.propTypes = {};
RyuManagersInfo.defaultProps = {};
export default RyuManagersInfo;
