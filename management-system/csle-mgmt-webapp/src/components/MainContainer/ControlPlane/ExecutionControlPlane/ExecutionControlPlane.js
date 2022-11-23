import React, {useState, useCallback} from 'react';
import {useNavigate} from "react-router-dom";
import './ExecutionControlPlane.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import parseLogs from "../../../Common/parseLogs";
import LogsModal from "./LogsModal/LogsModal";
import ContainersInfo from "./ContainersInfo/ContainersInfo";
import ActiveNetworksInfo from "./ActiveNetworksInfo/ActiveNetworksInfo";
import ClientManagersInfo from "./ClientManagersInfo/ClientManagersInfo";
import DockerStatsManagersInfo from "./DockerStatsManagersInfo/DockerStatsManagersInfo";
import HostManagersInfo from "./HostManagersInfo/HostManagersInfo";
import KafkaManagersInfo from "./KafkaManagersInfo/KafkaManagersInfo";
import OSSECIDSManagersInfo from "./OSSECIDSManagersInfo/OSSECIDSManagersInfo";
import SnortIDSManagersInfo from "./SnortIDSManagersInfo/SnortIDSManagersInfo";
import ElkManagersInfo from "./ElkManagersInfo/ElkManagersInfo";
import TrafficManagersInfo from "./TrafficManagersInfo/TrafficManagersInfo";

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
    const [activeNetworks, setActiveNetworks] = useState(props.info.active_networks);
    const [clientManagersInfo, setClientManagersInfo] = useState(props.info.client_managers_info);
    const [dockerStatsManagersInfo, setDockerStatsManagersInfo] = useState(props.info.docker_stats_managers_info);
    const [elkManagersInfo, setElkManagersInfo] = useState(props.info.elk_managers_info);
    const [hostManagersInfo, setHostManagersInfo] = useState(props.info.host_managers_info);
    const [inactiveNetworks, setInactiveNetworks] = useState(props.info.inactive_networks);
    const [kafkaManagersInfo, setkafkaManagersInfo] = useState(props.info.kafka_managers_info);
    const [ossecIDSManagersInfo, setOSSECIDSManagersInfo] = useState(props.info.ossec_ids_managers_info);
    const [snortIDSManagersInfo, setSnortIDSManagersInfo] = useState(props.info.snort_ids_managers_info);
    const [runningContainers, setRunningContainers] = useState(props.info.running_containers);
    const [stoppedContainers, setStoppedContainers] = useState(props.info.stopped_containers);
    const [trafficManagersInfo, setTrafficManagersInfo] = useState(props.info.traffic_managers_info);

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

    const startOrStopEntity = useCallback((id, emulation, start, stop, entity, name, node_ip) => {
        fetch(
            `http://` + ip + ':' + port + '/emulation-executions/' + id + "/" + entity + "?emulation="
            + emulation + "&token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({start: start, stop: stop, name: name, ip: node_ip})
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                updateStateAfterStartOrStop(entity, response)
                removeLoadingEntity(entity + "-" + node_ip)
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const updateStateAfterStartOrStop = (entity, response) => {
        if(entity === "client-manager" || entity === "client-manager" || entity === "client-producer"){
            setClientManagersInfo(response.client_managers_info)
        }
        if(entity === "kafka-manager" || entity === "kafka"){
            setkafkaManagersInfo(response.kafka_managers_info)
        }
        if(entity === "elk-manager" || entity === "elk-stack" || entity === "elastic" || entity === "kibana"
            || entity === "logstash"){
            setElkManagersInfo(response.elk_managers_info)
        }
        if(entity === "ossec-ids-manager" || entity === "ossec-ids" || entity === "ossec-ids-monitor"){
            setOSSECIDSManagersInfo(response.ossec_ids_managers_info)
        }
        if(entity === "snort-ids-manager" || entity === "snort-ids" || entity === "snort-ids-monitor"){
            setSnortIDSManagersInfo(response.snort_ids_managers_info)
        }
        if(entity === "host-manager" || entity === "host-monitor"){
            setHostManagersInfo(response.host_managers_info)
        }
        if(entity === "traffic-manager" || entity === "traffic-generator"){
            setTrafficManagersInfo(response.traffic_managers_info)
        }
        if(entity === "container"){
            setInactiveNetworks(response.inactive_networks)
            setRunningContainers(response.running_containers)
            setStoppedContainers(response.stopped_containers)
            setActiveNetworks(response.active_networks)
        }
        if(entity === "docker-stats-manager" || entity === "docker-stats-monitor"){
            setDockerStatsManagersInfo(response.docker_stats_managers_info)
        }
    }

    const activeStatus = (active) => {
        if (active) {
            return (<td className="containerRunningStatus">Active</td>)
        } else {
            return (<td className="containerStoppedStatus">Inactive</td>)
        }
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
        startOrStopEntity(props.execution.ip_first_octet, props.execution.emulation_name,
            start, stop, entity, name, ip)
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

                <ContainersInfo
                    setRunningContainersOpen={setRunningContainersOpen}
                    runningContainersOpen={runningContainersOpen}
                    loadingEntities={loadingEntities}
                    runningContainers={runningContainers}
                    stoppedContainers={stoppedContainers}
                    getLogs={getLogs}
                    startOrStop={startOrStop}
                />

                <ActiveNetworksInfo
                    setActiveNetworksOpen={setActiveNetworksOpen}
                    activeNetworksOpen={activeNetworksOpen}
                    loadingEntities={loadingEntities}
                    activeNetworks={activeNetworks}
                    inactiveNetworks={inactiveNetworks}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <ClientManagersInfo
                    setClientManagersOpen={setClientManagersOpen}
                    clientManagersOpen={clientManagersOpen}
                    loadingEntities={loadingEntities}
                    clientManagersInfo={clientManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <DockerStatsManagersInfo
                    setDockerStatsManagersOpen={setDockerStatsManagersOpen}
                    dockerStatsManagersOpen={dockerStatsManagersOpen}
                    loadingEntities={loadingEntities}
                    dockerStatsManagersInfo={dockerStatsManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <HostManagersInfo
                    setHostManagersOpen={setHostManagersOpen}
                    hostManagersOpen={hostManagersOpen}
                    loadingEntities={loadingEntities}
                    hostManagersInfo={hostManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <KafkaManagersInfo
                    setKafkaManagersOpen={setKafkaManagersOpen}
                    kafkaManagersOpen={kafkaManagersOpen}
                    loadingEntities={loadingEntities}
                    kafkaManagersInfo={kafkaManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    kafkaPort={props.execution.emulation_env_config.kafka_config.kafka_port}
                    startOrStop={startOrStop}
                />

                <OSSECIDSManagersInfo
                    setOssecIdsManagersOpen={setOssecIdsManagersOpen}
                    ossecIdsManagersOpen={ossecIdsManagersOpen}
                    loadingEntities={loadingEntities}
                    ossecIDSManagersInfo={ossecIDSManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <SnortIDSManagersInfo
                    setSnortManagersOpen={setSnortManagersOpen}
                    snortManagersOpen={snortManagersOpen}
                    loadingEntities={loadingEntities}
                    snortIDSManagersInfo={snortIDSManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />

                <ElkManagersInfo
                    setElkManagersOpen={setElkManagersOpen}
                    elkManagersOpen={elkManagersOpen}
                    loadingEntities={loadingEntities}
                    elkManagersInfo={elkManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    elasticPort={props.execution.emulation_env_config.elk_config.elastic_port}
                    logstashPort={props.execution.emulation_env_config.elk_config.logstash_port}
                    kibanaPort={props.execution.emulation_env_config.elk_config.kibana_port}
                    startOrStop={startOrStop}
                />

                <TrafficManagersInfo
                    setTrafficManagersOpen={setTrafficManagersOpen}
                    trafficManagersOpen={trafficManagersOpen}
                    loadingEntities={loadingEntities}
                    trafficManagersInfo={trafficManagersInfo}
                    getLogs={getLogs}
                    activeStatus={activeStatus}
                    startOrStop={startOrStop}
                />


            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

ExecutionControlPlane.propTypes = {};
ExecutionControlPlane.defaultProps = {};
export default ExecutionControlPlane;
