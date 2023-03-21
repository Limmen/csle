import React from 'react';
import './RyuManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import RyuImg from './Ryu.png'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import {
    RYU_MONITOR_SUBRESOURCE,
    RYU_MANAGER_SUBRESOURCE,
    RYU_CONTROLLER_SUBRESOURCE, HTTP_PREFIX
} from "../../../../Common/constants";

/**
 * Subcomponent of the /control-plane page that contains information about Ryu managers
 */
const RyuManagersInfo = (props) => {

    const renderRyuTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View Ryu's web interface
        </Tooltip>)
    }

    const RyuWebButton = (props) => {
        if(props.running && props.port !== -1 && !props.loading) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRyuTooltip}
                >
                    <a href={`${HTTP_PREFIX}${props.ip}:${props.port}`} target="_blank" rel="noopener noreferrer">
                        <Button variant="light" className="startButton" size="sm">
                            <img src={RyuImg} alt="Ryu" className="img-fluid elastic"/>
                        </Button>
                    </a>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

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
                                    <td>{status.time_step_len}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_MANAGER_SUBRESOURCE}-${props.ryuManagersInfo.ips[index]}`)}
                                            running={props.ryuManagersInfo.ryu_managers_running[index]}
                                            entity={RYU_MANAGER_SUBRESOURCE}
                                            name={RYU_MANAGER_SUBRESOURCE}
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
                                    <td>{status.port}</td>
                                    {props.activeStatus(status.ryu_running)}
                                    <td>{status.time_step_len}</td>
                                    <td>
                                        <RyuWebButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_CONTROLLER_SUBRESOURCE}-`
                                                + `${props.ryuManagersInfo.ips[index]}`)}
                                            name={props.ryuManagersInfo.ips[index]}
                                            port={props.ryuManagersInfo.local_controller_web_port}
                                            running={status.ryu_running}
                                            ip={props.ryuManagersInfo.physical_server_ip}
                                        />
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_CONTROLLER_SUBRESOURCE}-`
                                                + `${props.ryuManagersInfo.ips[index]}`)}
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
                                    <td>{status.web_port}</td>
                                    {props.activeStatus(status.monitor_running)}
                                    <td>{status.time_step_len}</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${RYU_MONITOR_SUBRESOURCE}-`
                                                + `${props.ryuManagersInfo.ips[index]}`)}
                                            running={status.monitor_running}
                                            entity={RYU_MONITOR_SUBRESOURCE} name={RYU_MONITOR_SUBRESOURCE}
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
