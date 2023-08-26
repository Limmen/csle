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
import RyuManagersInfo from "./RyuManagersInfo/RyuManagersInfo";
import TrafficManagersInfo from "./TrafficManagersInfo/TrafficManagersInfo";
import {
    HTTP_PREFIX,
    CLIENT_MANAGER_SUBRESOURCE,
    CLIENT_POPULATION_SUBRESOURCE,
    CLIENT_PRODUCER_SUBRESOURCE,
    CONTAINER_SUBRESOURCE,
    DOCKER_STATS_MANAGER_SUBRESOURCE,
    DOCKER_STATS_MONITOR_SUBRESOURCE,
    ELASTIC_SUBRESOURCE,
    ELK_MANAGER_SUBRESOURCE,
    ELK_STACK_SUBRESOURCE,
    HOST_MANAGER_SUBRESOURCE,
    HOST_MONITOR_SUBRESOURCE,
    KAFKA_MANAGER_SUBRESOURCE,
    KAFKA_SUBRESOURCE,
    KIBANA_SUBRESOURCE,
    LOGSTASH_SUBRESOURCE,
    OSSEC_IDS_MANAGER_SUBRESOURCE,
    OSSEC_IDS_MONITOR_SUBRESOURCE,
    OSSEC_IDS_SUBRESOURCE,
    SNORT_IDS_MANAGER_SUBRESOURCE,
    SNORT_IDS_MONITOR_SUBRESOURCE,
    SNORT_IDS_SUBRESOURCE,
    TRAFFIC_GENERATOR_SUBRESOURCE,
    TRAFFIC_MANAGER_SUBRESOURCE,
    LOGS_RESOURCE,
    TOKEN_QUERY_PARAM,
    EMULATION_QUERY_PARAM,
    EXECUTION_ID_QUERY_PARAM,
    LOGIN_PAGE_RESOURCE,
    EMULATION_EXECUTIONS_RESOURCE,
    HTTP_REST_POST,
    FILEBEAT_SUBRESOURCE,
    PACKETBEAT_SUBRESOURCE,
    METRICBEAT_SUBRESOURCE,
    HEARTBEAT_SUBRESOURCE,
    RYU_MANAGER_SUBRESOURCE,
    RYU_MONITOR_SUBRESOURCE,
    RYU_CONTROLLER_SUBRESOURCE
} from "../../../Common/constants";

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
    const [ryuManagersOpen, setRyuManagersOpen] = useState(false);
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
    const [ryuManagersInfo, setRyuManagersInfo] = useState(props.info.ryu_managers_info);
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
    const setSessionData = props.setSessionData

    const removeLoadingEntity = useCallback((entity) => {
        var newLoadingEntities = []
        for (let i = 0; i < loadingEntities.length; i++) {
            if (loadingEntities[i] !== entity) {
                newLoadingEntities.push(loadingEntities[i])
            }
        }
        setLoadingEntities(newLoadingEntities)
    }, [loadingEntities])

    const fetchLogs = useCallback((name, entity) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${entity}?${TOKEN_QUERY_PARAM}=`
            +`${props.sessionData.token}&${EMULATION_QUERY_PARAM}=${props.execution.emulation_name}&`
            +`${EXECUTION_ID_QUERY_PARAM}=${props.execution.ip_first_octet}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({name: name, ip: name})
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`)
                    return null
                }
                return res.json()
            })
            .then(response => {
                setLoadingLogs(false)
                setLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, props.execution.emulation_name, props.sessionData.token,
        props.execution.ip_first_octet, setSessionData]);

    const startOrStopEntity = useCallback((id, emulation, start, stop, entity, name, node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}/${id}/${entity}?`
            +`${EMULATION_QUERY_PARAM}=${emulation}&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({start: start, stop: stop, name: name, ip: node_ip})
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                updateStateAfterStartOrStop(entity, response)
                removeLoadingEntity(entity + "-" + node_ip)
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, props.sessionData.token, removeLoadingEntity, setSessionData]);


    const updateStateAfterStartOrStop = (entity, response) => {
        if(entity === CLIENT_MANAGER_SUBRESOURCE || entity === CLIENT_POPULATION_SUBRESOURCE ||
            entity === CLIENT_PRODUCER_SUBRESOURCE){
            setClientManagersInfo(response.client_managers_info)
        }
        if(entity === KAFKA_MANAGER_SUBRESOURCE || entity === KAFKA_SUBRESOURCE){
            setkafkaManagersInfo(response.kafka_managers_info)
        }
        if(entity === ELK_MANAGER_SUBRESOURCE || entity === ELK_STACK_SUBRESOURCE || entity === ELASTIC_SUBRESOURCE
            || entity === KIBANA_SUBRESOURCE || entity === LOGSTASH_SUBRESOURCE){
            setElkManagersInfo(response.elk_managers_info)
        }
        if(entity === OSSEC_IDS_MANAGER_SUBRESOURCE || entity === OSSEC_IDS_SUBRESOURCE ||
            entity === OSSEC_IDS_MONITOR_SUBRESOURCE){
            setOSSECIDSManagersInfo(response.ossec_ids_managers_info)
        }
        if(entity === SNORT_IDS_MANAGER_SUBRESOURCE || entity === SNORT_IDS_SUBRESOURCE ||
            entity === SNORT_IDS_MONITOR_SUBRESOURCE){
            setSnortIDSManagersInfo(response.snort_ids_managers_info)
        }
        if(entity === HOST_MANAGER_SUBRESOURCE || entity === HOST_MONITOR_SUBRESOURCE ||
            entity === FILEBEAT_SUBRESOURCE || entity === PACKETBEAT_SUBRESOURCE ||
            entity === METRICBEAT_SUBRESOURCE || entity === HEARTBEAT_SUBRESOURCE){
            setHostManagersInfo(response.host_managers_info)
        }
        if(entity === TRAFFIC_MANAGER_SUBRESOURCE || entity === TRAFFIC_GENERATOR_SUBRESOURCE){
            setTrafficManagersInfo(response.traffic_managers_info)
        }
        if(entity === CONTAINER_SUBRESOURCE){
            setInactiveNetworks(response.inactive_networks)
            setRunningContainers(response.running_containers)
            setStoppedContainers(response.stopped_containers)
            setActiveNetworks(response.active_networks)
        }
        if(entity === DOCKER_STATS_MANAGER_SUBRESOURCE || entity === DOCKER_STATS_MONITOR_SUBRESOURCE){
            setDockerStatsManagersInfo(response.docker_stats_managers_info)
        }
        if(entity === RYU_MANAGER_SUBRESOURCE || entity === RYU_MONITOR_SUBRESOURCE
            || entity === RYU_CONTROLLER_SUBRESOURCE){
            setRyuManagersInfo(response.ryu_managers_info)
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

    const RyuManagersInfoOrEmpty = (props) => {
        if (props.ryuManagersInfo !== null && props.ryuManagersInfo !== undefined) {
            return (
                <RyuManagersInfo
                    setRyuManagersOpen={props.setRyuManagersOpen}
                    ryuManagersOpen={props.ryuManagersOpen}
                    loadingEntities={props.loadingEntities}
                    ryuManagersInfo={props.ryuManagersInfo}
                    getLogs={props.getLogs}
                    activeStatus={props.activeStatus}
                    startOrStop={props.startOrStop}
                />
            )
        } else {
            return (<></>)
        }
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
                    executionId={props.execution.ip_first_octet}
                    emulation={props.execution.emulation_name}
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

                <RyuManagersInfoOrEmpty
                    setRyuManagersOpen={setRyuManagersOpen}
                    ryuManagersOpen={ryuManagersOpen}
                    loadingEntities={loadingEntities}
                    ryuManagersInfo={ryuManagersInfo}
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
