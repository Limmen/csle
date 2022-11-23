import React from 'react';
import './SnortIDSManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

/**
 * Subcomponent of the /control-plane page that contains information about Snort IDS managers
 */
const SnortIDSManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setSnortManagersOpen(!props.snortManagersOpen)}
                    aria-controls="snortManagersBody "
                    aria-expanded={props.snortManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Snort IDS Managers
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.snortManagersOpen}>
                <div id="snortManagersBody" className="cardBodyHidden">
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
                            {props.snortIDSManagersInfo.snort_ids_managers_statuses.map((status, index) =>
                                <tr key={"snort-ids-manager-" + index}>
                                    <td>Snort IDS Manager</td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td>{props.snortIDSManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.snortIDSManagersInfo.snort_ids_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("snort-ids-manager-" +
                                                props.snortIDSManagersInfo.ips[index])}
                                            running={props.snortIDSManagersInfo.snort_ids_managers_running[index]}
                                            entity={"snort-ids-manager"} name={"snort-ids-manager"}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity="snort-ids-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.snortIDSManagersInfo.snort_ids_managers_statuses.map((status, index) =>
                                <tr key={"snort-ids-monitor-" + index}>
                                    <td>Snort IDS Monitor</td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.monitor_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("snort-ids-monitor-" +
                                                props.snortIDSManagersInfo.ips[index])}
                                            running={status.monitor_running}
                                            entity={"snort-ids-monitor"} name={"snort-ids-monitor"}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity="snort-ids-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.snortIDSManagersInfo.snort_ids_managers_statuses.map((status, index) =>
                                <tr key={"snort-ids-" + index}>
                                    <td>Snort IDS
                                    </td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.snort_ids_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                "snort-ids-" + props.snortIDSManagersInfo.ips[index])}
                                            running={status.snort_ids_running}
                                            entity={"snort-ids"} name={"snort-ids"}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity="snort-ids"/>
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

SnortIDSManagersInfo.propTypes = {};
SnortIDSManagersInfo.defaultProps = {};
export default SnortIDSManagersInfo;
