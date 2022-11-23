import React from 'react';
import './ElkManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import KibanaImg from './Kibana.png'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import serverIp from "../../../../Common/serverIp";

/**
 * Subcomponent of the /control-plane page that contains information about ELK managers
 */
const ElkManagersInfo = (props) => {
    const ip = serverIp;

    const renderKibanaTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View Kibana
        </Tooltip>)
    }

    const KibanaButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderKibanaTooltip}
            >
                <a href={"http://" + ip + ":" + props.port} target="_blank" rel="noopener noreferrer">
                    <Button variant="light" className="startButton" size="sm">
                        <img src={KibanaImg} alt="Kibana" className="img-fluid"/>
                    </Button>
                </a>
            </OverlayTrigger>
        )
    }

    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setElkManagersOpen(!props.elkManagersOpen)}
                    aria-controls="elkManagersBody "
                    aria-expanded={props.elkManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> ELK Managers
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.elkManagersOpen}>
                <div id="elkManagersBody" className="cardBodyHidden">
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
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={"elk-manager-" + index}>
                                    <td>ELK manager</td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.elkManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.elkManagersInfo.elk_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                "elk-manager-" +
                                                props.elkManagersInfo.ips[index])}
                                            running={props.elkManagersInfo.elk_managers_running[index]}
                                            entity={"elk-manager"} name={"elk-manager"}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity="elk-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={"elk-stack-" + index}>
                                    <td>ELK stack</td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.elasticPort},
                                        {props.logstashPort},
                                        {props.kibanaPort}
                                    </td>
                                    {props.activeStatus((status.elasticRunning & status.kibanaRunning
                                        & status.logstashRunning))}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("elk-stack-" +
                                                props.elkManagersInfo.ips[index])}
                                            running={(status.elasticRunning & status.kibanaRunning
                                                & status.logstashRunning)}
                                            entity={"elk-stack"} name={"elk-stack"}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity="elk-stack"/>
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={"elastic-" + index}>
                                    <td>Elasticsearch
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.elasticPort}</td>
                                    {props.activeStatus(status.elasticRunning)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("elastic-" +
                                                props.elkManagersInfo.ips[index])}
                                            running={status.elasticRunning}
                                            entity={"elastic"} name={"elastic"}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity="elk-stack"/>
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={"elk_manager_status-" + index}>
                                    <td>Logstash
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.logstashPort}</td>
                                    {props.activeStatus(status.logstashRunning)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("logstash-" +
                                                props.elkManagersInfo.ips[index])}
                                            running={status.logstashRunning}
                                            entity={"logstash"} name={"logstash"}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity="elk-stack"/>
                                    </td>
                                </tr>
                            )}

                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={"kibana-" + index}>
                                    <td>Kibana
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.kibanaPort}</td>
                                    {props.activeStatus(status.kibanaRunning)}
                                    <td>
                                        <KibanaButton
                                            loading={props.loadingEntities.includes("kibana-" +
                                                props.elkManagersInfo.ips[index])}
                                            name={props.elkManagersInfo.ips[index]}
                                            port={props.elkManagersInfo.local_kibana_port}
                                        />
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("kibana-" +
                                                props.elkManagersInfo.ips[index])}
                                            running={status.kibanaRunning}
                                            entity={"kibana"} name={"kibana"}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity="elk-stack"/>
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

ElkManagersInfo.propTypes = {};
ElkManagersInfo.defaultProps = {};
export default ElkManagersInfo;
