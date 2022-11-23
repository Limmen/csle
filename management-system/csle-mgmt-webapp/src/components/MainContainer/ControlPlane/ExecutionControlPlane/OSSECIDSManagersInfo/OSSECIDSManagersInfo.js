import React from 'react';
import './OSSECIDSManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

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
                    <h5 className="semiTitle"> OSSEC IDS Managers
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.ossecIdsManagersOpen}>
                <div id="ossecIdsManagersBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-manager-stop-all")}
                            running={true} entity="ossec-ids-manager"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-manager-start-all")}
                            running={false} entity="ossec-ids-manager"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-monitor-stop-all")}
                            running={true} entity="ossec-ids-monitor"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all monitors:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-monitor-start-all")}
                            running={false} entity="ossec-ids-monitor"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all IDSes:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-stop-all")}
                            running={true} entity="ossec-ids"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all IDSes:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("ossec-ids-start-all")}
                            running={false} entity="ossec-ids"
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
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={"ossec-ids-manager" + index}>
                                    <td>OSSEC IDS Manager</td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td>{props.ossecIDSManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.ossecIDSManagersInfo.ossec_ids_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("ossec-ids-manager-" +
                                                props.ossecIDSManagersInfo.ips[index])}
                                            running={props.ossecIDSManagersInfo.ossec_ids_managers_running[index]}
                                            entity={"ossec-ids-manager"} name={"ossec-ids-manager"}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity="ossec-ids-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={"ossec-ids-monitor-" + index}>
                                    <td>OSSEC IDS Monitor</td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.monitor_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("ossec-ids-monitor-" +
                                                props.ossecIDSManagersInfo.ips[index])}
                                            running={status.monitor_running}
                                            entity={"ossec-ids-monitor"} name={"ossec-ids-monitor"}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity="ossec-ids-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.ossecIDSManagersInfo.ossec_ids_managers_statuses.map((status, index) =>
                                <tr key={"ossec-ids-" + index}>
                                    <td>OSSEC IDS
                                    </td>
                                    <td>{props.ossecIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.ossec_ids_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("ossec-ids-" +
                                                props.ossecIDSManagersInfo.ips[index])}
                                            running={status.ossec_ids_running}
                                            entity={"ossec-ids"} name={"ossec-ids"}
                                            ip={props.ossecIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.ossecIDSManagersInfo.ips[index]}
                                                    entity="ossec-ids-manager"/>
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
