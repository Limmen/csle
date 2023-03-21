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
import {
    ELK_STACK_SUBRESOURCE,
    LOGSTASH_SUBRESOURCE,
    KIBANA_SUBRESOURCE,
    ELK_MANAGER_SUBRESOURCE,
    ELASTIC_SUBRESOURCE, HTTP_PREFIX
} from "../../../../Common/constants";
import ElasticImg from "./../../../Emulations/Emulation/Elastic.png"

/**
 * Subcomponent of the /control-plane page that contains information about ELK managers
 */
const ElkManagersInfo = (props) => {

    const renderKibanaTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View Kibana
        </Tooltip>)
    }

    const KibanaButton = (props) => {
        if (props.running && props.port !== -1 && !props.loading){
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderKibanaTooltip}
                >
                    <a href={`${HTTP_PREFIX}${props.ip}:${props.port}`} target="_blank" rel="noopener noreferrer">
                        <Button variant="light" className="startButton" size="sm">
                            <img src={KibanaImg} alt="Kibana" className="img-fluid"/>
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
                    onClick={() => props.setElkManagersOpen(!props.elkManagersOpen)}
                    aria-controls="elkManagersBody "
                    aria-expanded={props.elkManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> ELK managers
                        <img src={ElasticImg} alt="Elastic" className="img-fluid headerIcon elastic"/>
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
                                <tr key={`${ELK_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>ELK manager</td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.elkManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.elkManagersInfo.elk_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${ELK_MANAGER_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            running={props.elkManagersInfo.elk_managers_running[index]}
                                            entity={ELK_MANAGER_SUBRESOURCE} name={ELK_MANAGER_SUBRESOURCE}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity={ELK_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={`${ELK_STACK_SUBRESOURCE}-${index}`}>
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
                                            loading={props.loadingEntities.includes(
                                                `${ELK_STACK_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            running={(status.elasticRunning & status.kibanaRunning
                                                & status.logstashRunning)}
                                            entity={ELK_STACK_SUBRESOURCE} name={ELK_STACK_SUBRESOURCE}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity={ELK_STACK_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={`${ELASTIC_SUBRESOURCE}-${index}`}>
                                    <td>Elasticsearch
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.elasticPort}</td>
                                    {props.activeStatus(status.elasticRunning)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${ELASTIC_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            running={status.elasticRunning}
                                            entity={ELASTIC_SUBRESOURCE} name={ELASTIC_SUBRESOURCE}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity={ELK_STACK_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={`${LOGSTASH_SUBRESOURCE}-${index}`}>
                                    <td>Logstash
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.logstashPort}</td>
                                    {props.activeStatus(status.logstashRunning)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${LOGSTASH_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            running={status.logstashRunning}
                                            entity={LOGSTASH_SUBRESOURCE} name={LOGSTASH_SUBRESOURCE}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity={ELK_STACK_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}

                            {props.elkManagersInfo.elk_managers_statuses.map((status, index) =>
                                <tr key={`${KIBANA_SUBRESOURCE}-${index}`}>
                                    <td>Kibana
                                    </td>
                                    <td>{props.elkManagersInfo.ips[index]}</td>
                                    <td>{props.kibanaPort}</td>
                                    {props.activeStatus(status.kibanaRunning)}
                                    <td>
                                        <KibanaButton
                                            loading={props.loadingEntities.includes(
                                                `${KIBANA_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            name={props.elkManagersInfo.ips[index]}
                                            port={props.elkManagersInfo.local_kibana_port}
                                            running={status.kibanaRunning}
                                            ip={props.elkManagersInfo.physical_server_ip}
                                        />
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${KIBANA_SUBRESOURCE}-`
                                                + `${props.elkManagersInfo.ips[index]}`)}
                                            running={status.kibanaRunning}
                                            entity={KIBANA_SUBRESOURCE} name={KIBANA_SUBRESOURCE}
                                            ip={props.elkManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.elkManagersInfo.ips[index]}
                                                    entity={ELK_STACK_SUBRESOURCE}
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

ElkManagersInfo.propTypes = {};
ElkManagersInfo.defaultProps = {};
export default ElkManagersInfo;
