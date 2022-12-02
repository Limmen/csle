import React from 'react';
import './OSSECIDSManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import {
    OSSEC_IDS_SUBRESOURCE,
    OSSEC_IDS_MANAGER_SUBRESOURCE,
    OSSEC_IDS_MONITOR_SUBRESOURCE,
    STOP_ALL_PROPERTY,
    START_ALL_PROPERTY} from "../../../../Common/constants";
import OssecImg from "./../../../Emulations/Emulation/Ossec.png"

/**
 * Subcomponent of the /control-plane page that contains information about OSSEC IDS managers
 */
const OSSECIDSManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setOssecIdsManagersOpen(!props.ossecIdsManagersOpen)}
                    aria-controls="ossecIdsManagersBody"
                    aria-expanded={props.ossecIdsManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> OSSEC IDS managers
                        <img src={OssecImg} alt="OSSEC" className="img-fluid headerIcon kafka"/>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.ossecIdsManagersOpen}>
                <div id="ossecIdsManagersBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={OSSEC_IDS_MANAGER_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={OSSEC_IDS_MANAGER_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_MONITOR_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={OSSEC_IDS_MONITOR_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_MONITOR_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={OSSEC_IDS_MONITOR_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all IDSes:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={OSSEC_IDS_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all IDSes:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${OSSEC_IDS_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={OSSEC_IDS_SUBRESOURCE}
                            name={OSSEC_IDS_SUBRESOURCE} ip={OSSEC_IDS_SUBRESOURCE}
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
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={`${OSSEC_IDS_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>OSSEC IDS Manager</td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td>{props.ossecIDSManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.ossecIDSManagersInfo.ossec_ids_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${OSSEC_IDS_MANAGER_SUBRESOURCE}-`
                                                + `${props.ossecIDSManagersInfo.ips[index]}`)}
                                            running={props.ossecIDSManagersInfo.ossec_ids_managers_running[index]}
                                            entity={OSSEC_IDS_MANAGER_SUBRESOURCE} name={OSSEC_IDS_MANAGER_SUBRESOURCE}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity={OSSEC_IDS_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={`${OSSEC_IDS_MONITOR_SUBRESOURCE}-${index}`}>
                                    <td>OSSEC IDS Monitor</td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.monitor_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${OSSEC_IDS_MONITOR_SUBRESOURCE}-`
                                                + `${props.ossecIDSManagersInfo.ips[index]}`)}
                                            running={status.monitor_running}
                                            entity={OSSEC_IDS_MONITOR_SUBRESOURCE}
                                            name={OSSEC_IDS_MONITOR_SUBRESOURCE}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity={OSSEC_IDS_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={`${OSSEC_IDS_SUBRESOURCE}-${index}`}>
                                    <td>OSSEC IDS
                                    </td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.ossec_ids_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${OSSEC_IDS_SUBRESOURCE}-`
                                                + `${props.ossecIDSManagersInfo.ips[index]}`)}
                                            running={status.ossec_ids_running}
                                            entity={OSSEC_IDS_SUBRESOURCE} name={OSSEC_IDS_SUBRESOURCE}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity={OSSEC_IDS_MANAGER_SUBRESOURCE}
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

OSSECIDSManagersInfo.propTypes = {};
OSSECIDSManagersInfo.defaultProps = {};
export default OSSECIDSManagersInfo;
