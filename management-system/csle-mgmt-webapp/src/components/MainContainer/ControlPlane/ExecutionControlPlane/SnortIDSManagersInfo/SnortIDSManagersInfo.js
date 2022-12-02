import React from 'react';
import './SnortIDSManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import {
    SNORT_IDS_MONITOR_SUBRESOURCE,
    SNORT_IDS_MANAGER_SUBRESOURCE,
    SNORT_IDS_SUBRESOURCE
} from "../../../../Common/constants";
import SnortImg from "./../../../Emulations/Emulation/Snort.png"

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
                    <h5 className="semiTitle"> Snort IDS managers
                        <img src={SnortImg} alt="Snort" className="img-fluid headerIcon elastic"/>
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
                                <tr key={`${SNORT_IDS_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>Snort IDS Manager</td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td>{props.snortIDSManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.snortIDSManagersInfo.snort_ids_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${SNORT_IDS_MANAGER_SUBRESOURCE}-`
                                                + `${props.snortIDSManagersInfo.ips[index]}`)}
                                            running={props.snortIDSManagersInfo.snort_ids_managers_running[index]}
                                            entity={SNORT_IDS_MANAGER_SUBRESOURCE} name={SNORT_IDS_MANAGER_SUBRESOURCE}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity={SNORT_IDS_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.snortIDSManagersInfo.snort_ids_managers_statuses.map((status, index) =>
                                <tr key={`${SNORT_IDS_MONITOR_SUBRESOURCE}-${index}`}>
                                    <td>Snort IDS Monitor</td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.monitor_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${SNORT_IDS_MONITOR_SUBRESOURCE}-`
                                                + `${props.snortIDSManagersInfo.ips[index]}`)}
                                            running={status.monitor_running}
                                            entity={SNORT_IDS_MONITOR_SUBRESOURCE}
                                            name={SNORT_IDS_MONITOR_SUBRESOURCE}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity={SNORT_IDS_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.snortIDSManagersInfo.snort_ids_managers_statuses.map((status, index) =>
                                <tr key={`${SNORT_IDS_SUBRESOURCE}-${index}`}>
                                    <td>Snort IDS
                                    </td>
                                    <td>{props.snortIDSManagersInfo.ips[index]}</td>
                                    <td></td>
                                    {props.activeStatus(status.snort_ids_running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${SNORT_IDS_SUBRESOURCE}-`
                                                + `${props.snortIDSManagersInfo.ips[index]}`)}
                                            running={status.snort_ids_running}
                                            entity={SNORT_IDS_SUBRESOURCE} name={SNORT_IDS_SUBRESOURCE}
                                            ip={props.snortIDSManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.snortIDSManagersInfo.ips[index]}
                                                    entity={SNORT_IDS_SUBRESOURCE}
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

SnortIDSManagersInfo.propTypes = {};
SnortIDSManagersInfo.defaultProps = {};
export default SnortIDSManagersInfo;
