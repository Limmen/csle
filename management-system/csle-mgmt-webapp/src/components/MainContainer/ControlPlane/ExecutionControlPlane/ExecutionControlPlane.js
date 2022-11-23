import React, {useState, useCallback} from 'react';
import {useNavigate} from "react-router-dom";
import './ExecutionControlPlane.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'
import getTopicsString from "../../../Common/getTopicsString";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import parseLogs from "../../../Common/parseLogs";
import KibanaImg from './Kibana.png'
import LogsButton from "./LogsButton/LogsButton";
import SpinnerOrButton from "./SpinnerOrButton/SpinnerOrButton";
import LogsModal from "./LogsModal/LogsModal";

/**
 * Component representing the /emulation-executions/<id>/control resource
 */
const ExecutionControlPlane = (props) => {
    const [runningContainersOpen, setRunningContainersOpen] = useState(false);
    const [activeNetworksOpen, setActiveNetworksOpen] = useState(false);
    const [clientManagersOpen, setClientManagersOpen] = useState(false);
    const [dockerStatsManagersOpen, setDockerStatsManagersOpen] = useState(false);
    const [hostManagersOpen, setHostManagersOpen] = useState(false);
    const [kafkaManagersOpen, setKafkaManagersOpen] = useState(false);
    const [ossecIdsManagersOpen, setOssecIdsManagersOpen] = useState(false);
    const [snortManagersOpen, setSnortManagersOpen] = useState(false);
    const [elkManagersOpen, setElkManagersOpen] = useState(false);
    const [trafficManagersOpen, setTrafficManagersOpen] = useState(false);
    const [loadingEntities, setLoadingEntities] = useState([]);
    const [showLogsModal, setShowLogsModal] = useState(false);
    const [nameToGetLogsFor, setNameToGetLogsFor] = useState(null);
    const [entityToGetLogsFor, setEntityToGetLogsFor] = useState(null);
    const [loadingLogs, setLoadingLogs] = useState(false);
    const [logs, setLogs] = useState([]);
    const ip = serverIp;
    const port = serverPort;
    const navigate = useNavigate();

    const fetchLogs = useCallback((name, entity) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/' + entity + "?token=" + props.sessionData.token +
            "&emulation=" + props.execution.emulation_name + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({name: name})
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                setLoadingLogs(false)
                setLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const activeStatus = (active) => {
        if (active) {
            return (<td className="containerRunningStatus">Active</td>)
        } else {
            return (<td className="containerStoppedStatus">Inactive</td>)
        }
    }

    const renderKibanaTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View Kibana
        </Tooltip>)
    }

    const addLoadingEntity = (entity) => {
        var newLoadingEntities = []
        for (let i = 0; i < loadingEntities.length; i++) {
            newLoadingEntities.push(loadingEntities[i])
        }
        newLoadingEntities.push(entity)
        setLoadingEntities(newLoadingEntities)
    }

    const removeLoadingEntity = (entity) => {
        var newLoadingEntities = []
        for (let i = 0; i < loadingEntities.length; i++) {
            if (loadingEntities[i] !== entity) {
                newLoadingEntities.push(loadingEntities[i])
            }
        }
        setLoadingEntities(newLoadingEntities)
    }

    const getLogs = (ipOrName, entity) => {
        setShowLogsModal(true)
        setNameToGetLogsFor(ipOrName)
        setEntityToGetLogsFor(entity)
        setLoadingLogs(true)
        fetchLogs(ipOrName, entity)
    }

    const startOrStop = (start, stop, entity, name, ip) => {
        addLoadingEntity(entity + "-" + ip)
        props.startOrStopEntity(props.execution.ip_first_octet, props.execution.emulation_name,
            start, stop, entity, name, ip)
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

    return (<Card key={props.execution.name} ref={props.wrapper}>
        <LogsModal show={showLogsModal} onHide={() => setShowLogsModal(false)} name={nameToGetLogsFor}
                   loading={loadingLogs} logs={logs} entity={entityToGetLogsFor}/>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.execution.emulation_name + "_"
                + props.execution.ip_first_octet} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.execution.ip_first_octet}, name: {props.execution.emulation_name}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.execution.emulation_name + "_" + props.execution.ip_first_octet}>
            <Card.Body>

                {/*<ContainersInfo*/}
                {/*    setRunningContainersOpen={setRunningContainersOpen}*/}
                {/*    runningContainersOpen={runningContainersOpen}*/}
                {/*    loadingEntities={loadingEntities}*/}
                {/*    runningContainers={props.runningContainers}*/}
                {/*    stoppedContainers={props.stoppedContainers}*/}
                {/*/>*/}

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setActiveNetworksOpen(!activeNetworksOpen)}
                            aria-controls="activeNetworksBody"
                            aria-expanded={activeNetworksOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Active networks </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={activeNetworksOpen}>
                        <div id="activeNetworksBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Network name</th>
                                        <th>Subnet mask</th>
                                        <th>Bitmask</th>
                                        <th>Status</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.activeNetworks.map((network, index) =>
                                        <tr key={network.name + "-" + index}>
                                            <td>{network.name}</td>
                                            <td>{network.subnet_mask}</td>
                                            <td>{network.bitmask}</td>
                                            <td className="containerRunningStatus">Active</td>
                                        </tr>
                                    )}
                                    {props.inactiveNetworks.map((network, index) =>
                                        <tr key={network.name + "-" + index}>
                                            <td>{network.name}</td>
                                            <td>{network.subnet_mask}</td>
                                            <td>{network.bitmask}</td>
                                            <td className="containerStoppedStatus">Inactive</td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setClientManagersOpen(!clientManagersOpen)}
                            aria-controls="clientManagersBody"
                            aria-expanded={clientManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Client managers</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={clientManagersOpen}>
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
                                        <tr key={"client-manager-" + index}>
                                            <td>Client manager</td>
                                            <td>{props.clientManagersInfo.ips[index]}</td>
                                            <td>{props.clientManagersInfo.ports[index]}</td>
                                            {activeStatus(props.clientManagersInfo.client_managers_running[index])}
                                            <td></td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-manager-" +
                                                        props.clientManagersInfo.ips[index])}
                                                    running={props.clientManagersInfo.client_managers_running[index]}
                                                    entity={"client-manager"} name={"client-manager"}
                                                    ip={props.clientManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.clientManagersInfo.ips[index]}
                                                            entity="client-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.clientManagersInfo.client_managers_statuses.map((status, index) =>
                                        <tr key={"client-population-" + index}>
                                            <td>Client process</td>
                                            <td>{props.clientManagersInfo.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.client_process_active)}
                                            <td>{status.num_clients}</td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-population-" +
                                                        props.clientManagersInfo.ips[index])}
                                                    running={status.client_process_active}
                                                    entity={"client-population"} name={"client-population"}
                                                    ip={props.clientManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.clientManagersInfo.ips[index]}
                                                            entity="client-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.clientManagersInfo.client_managers_statuses.map((status, index) =>
                                        <tr key={"client-producer-" + index}>
                                            <td>Producer process</td>
                                            <td>{props.clientManagersInfo.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.producer_active)}
                                            <td></td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-producer-" +
                                                        props.clientManagersInfo.ips[index])}
                                                    running={status.producer_active}
                                                    entity={"client-producer"} name={"client-producer"}
                                                    ip={props.clientManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.clientManagersInfo.ips[index]}
                                                            entity="client-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setDockerStatsManagersOpen(!dockerStatsManagersOpen)}
                            aria-controls="dockerStatsManagersBody"
                            aria-expanded={dockerStatsManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Docker Statistics Managers
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={dockerStatsManagersOpen}>
                        <div id="dockerStatsManagersBody" className="cardBodyHidden">
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
                                    {props.dockerStatsManagersInfo.docker_stats_managers_statuses.map((status, index) =>
                                        <tr key={"docker-stats-manager-" + index}>
                                            <td>Docker Statistics Manager</td>
                                            <td>{props.dockerStatsManagersInfo.ips[index]}</td>
                                            <td>{props.dockerStatsManagersInfo.ports[index]}</td>
                                            {activeStatus(props.dockerStatsManagersInfo.docker_stats_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("docker-stats-manager-" +
                                                        props.dockerStatsManagersInfo.ips[index])}
                                                    running={props.dockerStatsManagersInfo.docker_stats_managers_running[index]}
                                                    entity={"docker-stats-manager"} name={"docker-stats-manager"}
                                                    ip={props.dockerStatsManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.dockerStatsManagersInfo.ips[index]}
                                                            entity="docker-stats-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.dockerStatsManagersInfo.docker_stats_managers_statuses.map((status, index) =>
                                        <tr key={"docker-stats-monitor-" + index}>
                                            <td>Docker Statistics Monitor Thread</td>
                                            <td>{props.dockerStatsManagersInfo.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.num_monitors > 0)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("docker-stats-monitor-" +
                                                        props.dockerStatsManagersInfo.ips[index])}
                                                    running={status.num_monitors > 0}
                                                    entity={"docker-stats-monitor"} name={"docker-stats-monitor"}
                                                    ip={props.dockerStatsManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.dockerStatsManagersInfo.ips[index]}
                                                            entity="docker-stats-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setHostManagersOpen(!hostManagersOpen)}
                            aria-controls="hostManagersBody"
                            aria-expanded={hostManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Host managers </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={hostManagersOpen}>
                        <div id="hostManagersOpen" className="cardBodyHidden">
                            <div className="aggregateActionsContainer">
                                <span className="aggregateActions">Stop all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-manager-stop-all")}
                                    running={true} entity="host-manager"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-manager-start-all")}
                                    running={false} entity="host-manager"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Stop all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-monitor-stop-all")}
                                    running={true} entity="host-monitor"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-monitor-start-all")}
                                    running={false} entity="host-monitor"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
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
                                    {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                        <tr key={"host-monitor-" + index}>
                                            <td>Host Manager</td>
                                            <td>{props.hostManagersInfo.ips[index]}</td>
                                            <td>{props.hostManagersInfo.ports[index]}</td>
                                            {activeStatus(props.hostManagersInfo.host_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("host-manager-" +
                                                        props.hostManagersInfo.ips[index])}
                                                    running={props.hostManagersInfo.host_managers_running[index]}
                                                    entity={"host-manager"} name={"host-manager"}
                                                    ip={props.hostManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.hostManagersInfo.ips[index]}
                                                            entity="host-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.hostManagersInfo.host_managers_statuses.map((status, index) =>
                                        <tr key={"host-monitor-" + index}>
                                            <td>Host monitor thread</td>
                                            <td>{props.hostManagersInfo.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("host-monitor-" +
                                                        props.hostManagersInfo.ips[index])}
                                                    running={status.running}
                                                    entity={"host-monitor"} name={"host-monitor"}
                                                    ip={props.hostManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.hostManagersInfo.ips[index]}
                                                            entity="host-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setKafkaManagersOpen(!kafkaManagersOpen)}
                            aria-controls="kafkaManagersBody"
                            aria-expanded={kafkaManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Kafka managers
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={kafkaManagersOpen}>
                        <div id="kafkaManagersBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Service</th>
                                        <th>IP</th>
                                        <th>Port</th>
                                        <th>Topics</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.kafkaManagersInfo.kafka_managers_statuses.map((status, index) =>
                                        <tr key={"kafka-manager-" + index}>
                                            <td>Kafka Manager</td>
                                            <td>{props.kafkaManagersInfo.ips[index]}</td>
                                            <td>{props.kafkaManagersInfo.ports[index]}</td>
                                            <td></td>
                                            {activeStatus(props.kafkaManagersInfo.kafka_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kafka-manager-" +
                                                        props.kafkaManagersInfo.ips[index])}
                                                    running={props.kafkaManagersInfo.kafka_managers_running[index]}
                                                    entity={"kafka-manager"} name={"kafka-manager"}
                                                    ip={props.kafkaManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.kafkaManagersInfo.ips[index]}
                                                            entity="kafka-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.kafkaManagersInfo.kafka_managers_statuses.map((status, index) =>
                                        <tr key={"kafka-" + index}>
                                            <td>Kafka
                                            </td>
                                            <td>{props.kafkaManagersInfo.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.kafka_config.kafka_port}</td>
                                            <td>{getTopicsString(status.topics)}</td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kafka-" +
                                                        props.kafkaManagersInfo.ips[index])}
                                                    running={status.running}
                                                    entity={"kafka"} name={"kafka"}
                                                    ip={props.kafkaManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.kafkaManagersInfo.ips[index]}
                                                            entity="kafka"/>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setOssecIdsManagersOpen(!ossecIdsManagersOpen)}
                            aria-controls="ossecIdsManagersBody"
                            aria-expanded={ossecIdsManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> OSSEC IDS Managers
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={ossecIdsManagersOpen}>
                        <div id="ossecIdsManagersBody" className="cardBodyHidden">
                            <div className="aggregateActionsContainer">
                                <span className="aggregateActions">Stop all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-manager-stop-all")}
                                    running={true} entity="ossec-ids-manager"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-manager-start-all")}
                                    running={false} entity="ossec-ids-manager"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Stop all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-monitor-stop-all")}
                                    running={true} entity="ossec-ids-monitor"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-monitor-start-all")}
                                    running={false} entity="ossec-ids-monitor"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Stop all IDSes:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-stop-all")}
                                    running={true} entity="ossec-ids"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all IDSes:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-start-all")}
                                    running={false} entity="ossec-ids"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
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
                                            {activeStatus(props.ossecIDSManagersInfo.ossec_ids_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-manager-" +
                                                        props.ossecIDSManagersInfo.ips[index])}
                                                    running={props.ossecIDSManagersInfo.ossec_ids_managers_running[index]}
                                                    entity={"ossec-ids-manager"} name={"ossec-ids-manager"}
                                                    ip={props.ossecIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            {activeStatus(status.monitor_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-monitor-" +
                                                        props.ossecIDSManagersInfo.ips[index])}
                                                    running={status.monitor_running}
                                                    entity={"ossec-ids-monitor"} name={"ossec-ids-monitor"}
                                                    ip={props.ossecIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            {activeStatus(status.ossec_ids_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-" +
                                                        props.ossecIDSManagersInfo.ips[index])}
                                                    running={status.ossec_ids_running}
                                                    entity={"ossec-ids"} name={"ossec-ids"}
                                                    ip={props.ossecIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setSnortManagersOpen(!snortManagersOpen)}
                            aria-controls="snortManagersBody "
                            aria-expanded={snortManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Snort IDS Managers
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={snortManagersOpen}>
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
                                            {activeStatus(props.snortIDSManagersInfo.snort_ids_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-manager-" +
                                                        props.snortIDSManagersInfo.ips[index])}
                                                    running={props.snortIDSManagersInfo.snort_ids_managers_running[index]}
                                                    entity={"snort-ids-manager"} name={"snort-ids-manager"}
                                                    ip={props.snortIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            {activeStatus(status.monitor_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-monitor-" +
                                                        props.snortIDSManagersInfo.ips[index])}
                                                    running={status.monitor_running}
                                                    entity={"snort-ids-monitor"} name={"snort-ids-monitor"}
                                                    ip={props.snortIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            {activeStatus(status.snort_ids_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-" + props.snortIDSManagersInfo.ips[index])}
                                                    running={status.snort_ids_running}
                                                    entity={"snort-ids"} name={"snort-ids"}
                                                    ip={props.snortIDSManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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


                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setElkManagersOpen(!elkManagersOpen)}
                            aria-controls="elkManagersBody "
                            aria-expanded={elkManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> ELK Managers
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={elkManagersOpen}>
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
                                            {activeStatus(props.elkManagersInfo.elk_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    running={props.elkManagersInfo.elk_managers_running[index]}
                                                    entity={"elk-manager"} name={"elk-manager"}
                                                    ip={props.elkManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            <td>{props.execution.emulation_env_config.elk_config.elastic_port},
                                                {props.execution.emulation_env_config.elk_config.logstash_port},
                                                {props.execution.emulation_env_config.elk_config.kibana_port}
                                            </td>
                                            {activeStatus((status.elasticRunning & status.kibanaRunning
                                                & status.logstashRunning))}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elk-stack-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    running={(status.elasticRunning & status.kibanaRunning
                                                        & status.logstashRunning)}
                                                    entity={"elk-stack"} name={"elk-stack"}
                                                    ip={props.elkManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            <td>{props.execution.emulation_env_config.elk_config.elastic_port}</td>
                                            {activeStatus(status.elasticRunning)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elastic-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    running={status.elasticRunning}
                                                    entity={"elastic"} name={"elastic"}
                                                    ip={props.elkManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            <td>{props.execution.emulation_env_config.elk_config.logstash_port}</td>
                                            {activeStatus(status.logstashRunning)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("logstash-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    running={status.logstashRunning}
                                                    entity={"logstash"} name={"logstash"}
                                                    ip={props.elkManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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
                                            <td>{props.execution.emulation_env_config.elk_config.kibana_port}</td>
                                            {activeStatus(status.kibanaRunning)}
                                            <td>
                                                <KibanaButton
                                                    loading={loadingEntities.includes("kibana-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    name={props.elkManagersInfo.ips[index]}
                                                    port={props.elkManagersInfo.local_kibana_port}
                                                />
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kibana-" +
                                                        props.elkManagersInfo.ips[index])}
                                                    running={status.kibanaRunning}
                                                    entity={"kibana"} name={"kibana"}
                                                    ip={props.elkManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
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

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setTrafficManagersOpen(!trafficManagersOpen)}
                            aria-controls="trafficManagersBody"
                            aria-expanded={trafficManagersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Traffic managers </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={trafficManagersOpen}>
                        <div id="trafficManagersBody" className="cardBodyHidden">
                            <div className="aggregateActionsContainer">
                                <span className="aggregateActions">Stop all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-manager-stop-all")}
                                    running={true} entity="traffic-manager"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-manager-start-all")}
                                    running={false} entity="traffic-manager"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Stop all generators:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-generator-stop-all")}
                                    running={true} entity="traffic-generator"
                                    name="stop-all" ip="stop-all"
                                    startOrStop={startOrStop}
                                />
                                <span className="aggregateActions">Start all generators:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-generator-start-all")}
                                    running={false} entity="traffic-generator"
                                    name="start-all" ip="start-all"
                                    startOrStop={startOrStop}
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
                                        <tr key={"traffic-manager-" + index}>
                                            <td>Traffic Manager</td>
                                            <td>{props.trafficManagersInfo.ips[index]}</td>
                                            <td>{props.trafficManagersInfo.ports[index]}</td>
                                            {activeStatus(props.trafficManagersInfo.traffic_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("traffic-manager-" +
                                                        props.trafficManagersInfo.ips[index])}
                                                    running={props.trafficManagersInfo.traffic_managers_running[index]}
                                                    entity={"traffic-manager"} name={"traffic-manager"}
                                                    ip={props.trafficManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                            entity="traffic-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.trafficManagersInfo.traffic_managers_statuses.map((status, index) =>
                                        <tr key={"traffic-generator-" + index}>
                                            <td>Traffic Generator</td>
                                            <td>{props.trafficManagersInfo.ips[index]}</td>
                                            <td>-</td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("traffic-generator-" +
                                                        props.trafficManagersInfo.ips[index])}
                                                    running={status.running}
                                                    entity={"traffic-generator"} name={"traffic-generator"}
                                                    ip={props.trafficManagersInfo.ips[index]}
                                                    startOrStop={startOrStop}
                                                />
                                                <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                            entity="traffic-manager"/>
                                            </td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

ExecutionControlPlane.propTypes = {};
ExecutionControlPlane.defaultProps = {};
export default ExecutionControlPlane;
