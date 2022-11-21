import React, {useState, useCallback} from 'react';
import {useNavigate} from "react-router-dom";
import './ExecutionControlPlane.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'
import getIps from "../../../Common/getIps";
import getTopicsString from "../../../Common/getTopicsString";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Modal from 'react-bootstrap/Modal'
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import parseLogs from "../../../Common/parseLogs";
import KibanaImg from './Kibana.png'

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
    const [showContainerLogsModal, setShowContainerLogsModal] = useState(false);
    const [containerToGetLogsFor, setContainerToGetLogsFor] = useState(null);
    const [loadingContainerLogs, setLoadingContainerLogs] = useState(false);
    const [containerLogs, setContainerLogs] = useState([]);
    const [showClientManagerLogsModal, setShowClientManagerLogsModal] = useState(false);
    const [loadingClientManagerLogs, setLoadingClientManagerLogs] = useState(false);
    const [clientManagerLogs, setClientManagerLogs] = useState([]);
    const [clientManagerToGetLogsFor, setClientManagerToGetLogsFor] = useState(null);
    const [showSnortManagerLogsModal, setShowSnortManagerLogsModal] = useState(false);
    const [loadingSnortManagerLogs, setLoadingSnortManagerLogs] = useState(false);
    const [snortManagerLogs, setSnortManagerLogs] = useState([]);
    const [snortManagerToGetLogsFor, setSnortManagerToGetLogsFor] = useState(null);
    const [showKafkaManagerLogsModal, setShowKafkaManagerLogsModal] = useState(false);
    const [loadingKafkaManagerLogs, setLoadingKafkaManagerLogs] = useState(false);
    const [kafkaManagerLogs, setKafkaManagerLogs] = useState([]);
    const [kafkaManagerToGetLogsFor, setKafkaManagerToGetLogsFor] = useState(null);
    const [showOssecIDSManagerLogsModal, setShowOssecIDSManagerLogsModal] = useState(false);
    const [loadingOssecIDSManagerLogs, setLoadingOssecIDSManagerLogs] = useState(false);
    const [ossecIDSManagerLogs, setOssecIDSManagerLogs] = useState([]);
    const [ossecIDSManagerToGetLogsFor, setOssecIDSManagerToGetLogsFor] = useState(null);
    const [showTrafficManagerLogsModal, setShowTrafficManagerLogsModal] = useState(false);
    const [loadingTrafficManagerLogs, setLoadingTrafficManagerLogs] = useState(false);
    const [trafficManagerLogs, setTrafficManagerLogs] = useState([]);
    const [trafficManagerToGetLogsFor, setTrafficManagerToGetLogsFor] = useState(null);
    const [showHostManagerLogsModal, setShowHostManagerLogsModal] = useState(false);
    const [loadingHostManagerLogs, setLoadingHostManagerLogs] = useState(false);
    const [hostManagerLogs, setHostManagerLogs] = useState([]);
    const [hostManagerToGetLogsFor, setHostManagerToGetLogsFor] = useState(null);
    const [showElkManagerLogsModal, setShowElkManagerLogsModal] = useState(false);
    const [loadingElkManagerLogs, setLoadingElkManagerLogs] = useState(false);
    const [elkManagerLogs, setElkManagerLogs] = useState([]);
    const [elkManagerToGetLogsFor, setELkManagerToGetLogsFor] = useState(null);
    const [showDockerStatsManagerLogsModal, setShowDockerStatsManagerLogsModal] = useState(false);
    const [loadingDockerStatsManagerLogs, setLoadingDockerStatsManagerLogs] = useState(false);
    const [dockerStatsManagerLogs, setDockerStatsManagerLogs] = useState([]);
    const [dockerStatsManagerToGetLogsFor, setDockerStatsManagerToGetLogsFor] = useState(null);
    const ip = serverIp;
    const port = serverPort;
    const navigate = useNavigate();

    const fetchContainerLogs = useCallback((containerName) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/container' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({name: containerName})
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
                setLoadingContainerLogs(false)
                setContainerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchStatsManagerLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/logs/docker-stats-manager' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                setLoadingDockerStatsManagerLogs(false)
                setDockerStatsManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchClientManagerLogs = useCallback((emulation, client_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/client-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: client_manager_ip})
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
                setLoadingClientManagerLogs(false)
                setClientManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchKafkaManagerLogs = useCallback((emulation, kafka_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/kafka-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: kafka_manager_ip})
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
                setLoadingKafkaManagerLogs(false)
                setKafkaManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSnortIdsManagerLogs = useCallback((emulation, snort_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/snort-ids-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: snort_manager_ip})
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
                setLoadingSnortManagerLogs(false)
                setSnortManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchOssecIdsManagerLogs = useCallback((emulation, ossec_ids_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/ossec-ids-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: ossec_ids_manager_ip})
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
                setLoadingOssecIDSManagerLogs(false)
                setOssecIDSManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchHostManagerLogs = useCallback((emulation, host_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/host-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: host_manager_ip})
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
                setLoadingHostManagerLogs(false)
                setHostManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchElkManagerLogs = useCallback((emulation, elk_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/elk-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: elk_manager_ip})
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
                setLoadingElkManagerLogs(false)
                setElkManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTrafficManagerLogs = useCallback((emulation, traffic_manager_ip) => {
        fetch(
            `http://` + ip + ":" + port + '/logs/traffic-manager' + "?token=" + props.sessionData.token
            + "&emulation=" + emulation + "&executionid=" + props.execution.ip_first_octet,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: traffic_manager_ip})
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
                setLoadingTrafficManagerLogs(false)
                setTrafficManagerLogs(parseLogs(response.logs))
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

    const renderStopTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop
        </Tooltip>)
    }

    const renderLogsTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View logs
        </Tooltip>)
    }

    const renderShellTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Open SSH shell
        </Tooltip>)
    }

    const renderKibanaTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View Kibana
        </Tooltip>)
    }

    const renderStartTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start
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

    const getContainerLogs = (containerName) => {
        setShowContainerLogsModal(true)
        setContainerToGetLogsFor(containerName)
        setLoadingContainerLogs(true)
        fetchContainerLogs(containerName)
    }

    const getClientManagerLogs = (ip) => {
        setShowClientManagerLogsModal(true)
        setLoadingClientManagerLogs(true)
        setClientManagerToGetLogsFor(ip)
        fetchClientManagerLogs(props.execution.emulation_name, ip)
    }

    const getKafkaManagerLogs = (ip) => {
        setShowKafkaManagerLogsModal(true)
        setLoadingKafkaManagerLogs(true)
        setKafkaManagerToGetLogsFor(ip)
        fetchKafkaManagerLogs(props.execution.emulation_name, ip)
    }

    const getSnortManagerLogs = (ip) => {
        setShowSnortManagerLogsModal(true)
        setLoadingSnortManagerLogs(true)
        setSnortManagerToGetLogsFor(ip)
        fetchSnortIdsManagerLogs(props.execution.emulation_name, ip)
    }

    const getTrafficManagerLogs = (ip) => {
        setShowTrafficManagerLogsModal(true)
        setLoadingTrafficManagerLogs(true)
        setTrafficManagerToGetLogsFor(ip)
        fetchTrafficManagerLogs(props.execution.emulation_name, ip)
    }

    const getHostManagerLogs = (ip) => {
        setShowHostManagerLogsModal(true)
        setLoadingHostManagerLogs(true)
        setHostManagerToGetLogsFor(ip)
        fetchHostManagerLogs(props.execution.emulation_name, ip)
    }

    const getElkManagerLogs = (ip) => {
        setShowElkManagerLogsModal(true)
        setLoadingElkManagerLogs(true)
        setELkManagerToGetLogsFor(ip)
        fetchElkManagerLogs(props.execution.emulation_name, ip)
    }

    const getDockerStatsManagerLogs = (ip) => {
        setShowDockerStatsManagerLogsModal(true)
        setLoadingDockerStatsManagerLogs(true)
        setDockerStatsManagerToGetLogsFor(ip)
        fetchStatsManagerLogs()
    }

    const getOssecIDSManagerLogs = (ip) => {
        setShowOssecIDSManagerLogsModal(true)
        setLoadingOssecIDSManagerLogs(true)
        setOssecIDSManagerToGetLogsFor(ip)
        fetchOssecIdsManagerLogs(props.execution.emulation_name, ip)
    }

    const startOrStop = (start, stop, entity, name, ip) => {
        addLoadingEntity(entity + "-" + ip)
        props.startOrStopEntity(props.execution.ip_first_octet, props.execution.emulation_name,
            start, stop, entity, name, ip)
    }

    const SpinnerOrLogs = (props) => {
        if (props.loadingLogs || props.logs === null || props.logs === undefined) {
            return (
                <div>
                    <span className="logsLabel">Fetching logs...</span>
                    <Spinner
                        as="span"
                        animation="grow"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                    />
                </div>
            )
        } else {
            return (
                <div className="table-responsive">
                    <Table striped bordered hover>
                        <thead>
                        <tr>
                            <th>Line number</th>
                            <th>Log</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.logs.map((logLine, index) => {
                            return <tr key={logLine.index + "-" + index}>
                                <td>{logLine.index}</td>
                                <td>{logLine.content}</td>
                            </tr>
                        })}
                        </tbody>
                    </Table>
                </div>
            )
        }
    }

    const ContainerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for container: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const ClientManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for client manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const KafkaManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for Kafka manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SnortIdsManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for Snort IDS manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const OssecIDSManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for OSSEC IDS manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const TrafficManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for traffic manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const HostManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for host manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const ElkManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for ELK manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const DockerStatsManagerLogsModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs for Docker stats manager: {props.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="logsModalBody">
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const ContainerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getContainerLogs(props.name)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const ClientManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getClientManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const SnortManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getSnortManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const KafkaManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getKafkaManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const OssecIDSManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getOssecIDSManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const TrafficManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getTrafficManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const HostManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getHostManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const ElkManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getElkManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const DockerStatsManagerLogsButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderLogsTooltip}
            >
                <Button variant="info" className="startButton" size="sm"
                        onClick={() => getDockerStatsManagerLogs(props.ip)}>
                    <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
    }

    const ShellButton = (props) => {
        return (
            <OverlayTrigger
                placement="right"
                delay={{show: 0, hide: 0}}
                overlay={renderShellTooltip}
            >
                <Button variant="secondary" className="startButton" size="sm"
                        onClick={() => getContainerLogs(props.name)}>
                    <i className="fa fa-terminal startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>
        )
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

    const SpinnerOrButton = (props) => {
        if (props.loading) {
            return (<Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
            />)
        } else {
            if (props.running) {
                return (
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip}
                    >
                        <Button variant="warning" className="startButton" size="sm"
                                onClick={() => startOrStop(false, true, props.entity, props.name, props.ip)}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            } else {
                return (
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStartTooltip}
                    >
                        <Button variant="success" className="startButton" size="sm"
                                onClick={() => startOrStop(true, false, props.entity, props.name, props.ip)}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            }
        }
    };

    return (<Card key={props.execution.name} ref={props.wrapper}>
        <ContainerLogsModal show={showContainerLogsModal} onHide={() => setShowContainerLogsModal(false)} name={containerToGetLogsFor}
                   loading={loadingContainerLogs} logs={containerLogs}/>
        <ClientManagerLogsModal show={showClientManagerLogsModal} onHide={() => setShowClientManagerLogsModal(false)}
                            loading={loadingClientManagerLogs} logs={clientManagerLogs} name={clientManagerToGetLogsFor}/>
        <KafkaManagerLogsModal show={showKafkaManagerLogsModal} onHide={() => setShowKafkaManagerLogsModal(false)}
                                loading={loadingKafkaManagerLogs} logs={kafkaManagerLogs} name={kafkaManagerToGetLogsFor}/>
        <SnortIdsManagerLogsModal show={showSnortManagerLogsModal} onHide={() => setShowSnortManagerLogsModal(false)}
                               loading={loadingSnortManagerLogs} logs={snortManagerLogs} name={snortManagerToGetLogsFor}/>
        <OssecIDSManagerLogsModal show={showOssecIDSManagerLogsModal} onHide={() => setShowOssecIDSManagerLogsModal(false)}
                                  loading={loadingOssecIDSManagerLogs} logs={ossecIDSManagerLogs} name={ossecIDSManagerToGetLogsFor}/>
        <TrafficManagerLogsModal show={showTrafficManagerLogsModal} onHide={() => setShowTrafficManagerLogsModal(false)}
                                  loading={loadingTrafficManagerLogs} logs={trafficManagerLogs} name={trafficManagerToGetLogsFor}/>
        <HostManagerLogsModal show={showHostManagerLogsModal} onHide={() => setShowHostManagerLogsModal(false)}
                                 loading={loadingHostManagerLogs} logs={hostManagerLogs} name={hostManagerToGetLogsFor}/>
        <ElkManagerLogsModal show={showElkManagerLogsModal} onHide={() => setShowElkManagerLogsModal(false)}
                              loading={loadingElkManagerLogs} logs={elkManagerLogs} name={elkManagerToGetLogsFor}/>
        <DockerStatsManagerLogsModal show={showDockerStatsManagerLogsModal} onHide={() => setShowDockerStatsManagerLogsModal(false)}
                             loading={loadingDockerStatsManagerLogs} logs={dockerStatsManagerLogs} name={dockerStatsManagerToGetLogsFor}/>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.execution.emulation_name + "_"
                + props.execution.ip_first_octet} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.execution.ip_first_octet}, name: {props.execution.emulation_name}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.execution.emulation_name + "_" + props.execution.ip_first_octet}>
            <Card.Body>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setRunningContainersOpen(!runningContainersOpen)}
                            aria-controls="runningContainersBody"
                            aria-expanded={runningContainersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Docker container statuses
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={runningContainersOpen}>
                        <div id="activeNetworksBody" className="cardBodyHidden">
                            <div className="aggregateActionsContainer">
                                <span className="aggregateActions">Stop all containers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("container-stop-all")}
                                    running={true} entity="container"
                                    name="stop-all" ip="stop-all"
                                />
                                <span className="aggregateActions">Start all containers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("container-start-all")}
                                    running={false} entity="container"
                                    name="start-all" ip="start-all"
                                />
                            </div>
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Image</th>
                                        <th>Os</th>
                                        <th>IPs</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.info.running_containers.map((container, index) =>
                                        <tr key={container.full_name_str + "-" + index}>
                                            <td>{container.full_name_str}</td>
                                            <td>{container.name}</td>
                                            <td>{container.os}</td>
                                            <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                            <td className="containerRunningStatus"> Running</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("container-"
                                                        + container.full_name_str)}
                                                    running={true} entity="container"
                                                    name={container.full_name_str} ip={container.full_name_str}
                                                />
                                                <ContainerLogsButton
                                                    loading={loadingEntities.includes("container-" +
                                                        container.full_name_str + "-logs")}
                                                    name={container.full_name_str}/>
                                                <ShellButton
                                                    loading={loadingEntities.includes("container-" +
                                                        container.full_name_str + "-shell")}
                                                    name={container.full_name_str}/>
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.stopped_containers.map((container, index) =>
                                        <tr key={container.full_name_str + "-" + index}>
                                            <td>{container.full_name_str}</td>
                                            <td>{container.name}</td>
                                            <td>{container.os}</td>
                                            <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                            <td className="containerStoppedStatus">Stopped</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("container-" +
                                                        container.full_name_str)}
                                                    running={false} entity="container"
                                                    name={container.full_name_str} ip={container.full_name_str}/>
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
                                    {props.info.active_networks.map((network, index) =>
                                        <tr key={network.name + "-" + index}>
                                            <td>{network.name}</td>
                                            <td>{network.subnet_mask}</td>
                                            <td>{network.bitmask}</td>
                                            <td className="containerRunningStatus">Active</td>
                                        </tr>
                                    )}
                                    {props.info.inactive_networks.map((network, index) =>
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
                                    {props.info.client_managers_info.client_managers_statuses.map((status, index) =>
                                        <tr key={"client-manager-" + index}>
                                            <td>Client manager</td>
                                            <td>{props.info.client_managers_info.ips[index]}</td>
                                            <td>{props.info.client_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.client_managers_info.client_managers_running[index])}
                                            <td></td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-manager-" +
                                                        props.info.client_managers_info.ips[index])}
                                                    running={props.info.client_managers_info.client_managers_running[index]}
                                                    entity={"client-manager"} name={"client-manager"}
                                                    ip={props.info.client_managers_info.ips[index]}
                                                />
                                                <ClientManagerLogsButton
                                                    loading={loadingEntities.includes("client-manager-" +
                                                        props.info.client_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.client_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.client_managers_info.client_managers_statuses.map((status, index) =>
                                        <tr key={"client-population-" + index}>
                                            <td>Client process</td>
                                            <td>{props.info.client_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.client_process_active)}
                                            <td>{status.num_clients}</td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-population-" +
                                                        props.info.client_managers_info.ips[index])}
                                                    running={status.client_process_active}
                                                    entity={"client-population"} name={"client-population"}
                                                    ip={props.info.client_managers_info.ips[index]}
                                                />
                                                <ClientManagerLogsButton
                                                    loading={loadingEntities.includes("client-manager-" +
                                                        props.info.client_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.client_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.client_managers_info.client_managers_statuses.map((status, index) =>
                                        <tr key={"client-producer-" + index}>
                                            <td>Producer process</td>
                                            <td>{props.info.client_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.producer_active)}
                                            <td></td>
                                            <td>{status.clients_time_step_len_seconds}</td>
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("client-producer-" +
                                                        props.info.client_managers_info.ips[index])}
                                                    running={status.producer_active}
                                                    entity={"client-producer"} name={"client-producer"}
                                                    ip={props.info.client_managers_info.ips[index]}
                                                />
                                                <ClientManagerLogsButton
                                                    loading={loadingEntities.includes("client-manager-" +
                                                        props.info.client_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.client_managers_info.ips[index]}
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
                                    {props.info.docker_stats_managers_info.docker_stats_managers_statuses.map((status, index) =>
                                        <tr key={"docker-stats-manager-" + index}>
                                            <td>Docker Statistics Manager</td>
                                            <td>{props.info.docker_stats_managers_info.ips[index]}</td>
                                            <td>{props.info.docker_stats_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.docker_stats_managers_info.docker_stats_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("docker-stats-manager-" +
                                                        props.info.docker_stats_managers_info.ips[index])}
                                                    running={props.info.docker_stats_managers_info.docker_stats_managers_running[index]}
                                                    entity={"docker-stats-manager"} name={"docker-stats-manager"}
                                                    ip={props.info.docker_stats_managers_info.ips[index]}
                                                />
                                                <DockerStatsManagerLogsButton
                                                    loading={loadingEntities.includes("docker-stats-manager-" +
                                                        props.info.docker_stats_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.docker_stats_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.docker_stats_managers_info.docker_stats_managers_statuses.map((status, index) =>
                                        <tr key={"docker-stats-monitor-" + index}>
                                            <td>Docker Statistics Monitor Thread</td>
                                            <td>{props.info.docker_stats_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.num_monitors > 0)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("docker-stats-monitor-" +
                                                        props.info.docker_stats_managers_info.ips[index])}
                                                    running={status.num_monitors > 0}
                                                    entity={"docker-stats-monitor"} name={"docker-stats-monitor"}
                                                    ip={props.info.docker_stats_managers_info.ips[index]}
                                                />
                                                <DockerStatsManagerLogsButton
                                                    loading={loadingEntities.includes("docker-stats-manager-" +
                                                        props.info.docker_stats_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.docker_stats_managers_info.ips[index]}
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
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-manager-start-all")}
                                    running={false} entity="host-manager"
                                    name="start-all" ip="start-all"
                                />
                                <span className="aggregateActions">Stop all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-monitor-stop-all")}
                                    running={true} entity="host-monitor"
                                    name="stop-all" ip="stop-all"
                                />
                                <span className="aggregateActions">Start all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("host-monitor-start-all")}
                                    running={false} entity="host-monitor"
                                    name="start-all" ip="start-all"
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
                                    {props.info.host_managers_info.host_managers_statuses.map((status, index) =>
                                        <tr key={"host-monitor-" + index}>
                                            <td>Host Manager</td>
                                            <td>{props.info.host_managers_info.ips[index]}</td>
                                            <td>{props.info.host_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.host_managers_info.host_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("host-manager-" +
                                                        props.info.host_managers_info.ips[index])}
                                                    running={props.info.host_managers_info.host_managers_running[index]}
                                                    entity={"host-manager"} name={"host-manager"}
                                                    ip={props.info.host_managers_info.ips[index]}
                                                />
                                                <HostManagerLogsButton
                                                    loading={loadingEntities.includes("host-manager-" +
                                                        props.info.host_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.host_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.host_managers_info.host_managers_statuses.map((status, index) =>
                                        <tr key={"host-monitor-" + index}>
                                            <td>Host monitor thread</td>
                                            <td>{props.info.host_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("host-monitor-" +
                                                        props.info.host_managers_info.ips[index])}
                                                    running={status.running}
                                                    entity={"host-monitor"} name={"host-monitor"}
                                                    ip={props.info.host_managers_info.ips[index]}
                                                />
                                                <HostManagerLogsButton
                                                    loading={loadingEntities.includes("host-manager-" +
                                                        props.info.host_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.host_managers_info.ips[index]}
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
                                    {props.info.kafka_managers_info.kafka_managers_statuses.map((status, index) =>
                                        <tr key={"kafka-manager-" + index}>
                                            <td>Kafka Manager</td>
                                            <td>{props.info.kafka_managers_info.ips[index]}</td>
                                            <td>{props.info.kafka_managers_info.ports[index]}</td>
                                            <td></td>
                                            {activeStatus(props.info.kafka_managers_info.kafka_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kafka-manager-" +
                                                        props.info.kafka_managers_info.ips[index])}
                                                    running={props.info.kafka_managers_info.kafka_managers_running[index]}
                                                    entity={"kafka-manager"} name={"kafka-manager"}
                                                    ip={props.info.kafka_managers_info.ips[index]}
                                                />
                                                <KafkaManagerLogsButton
                                                    loading={loadingEntities.includes("kafka-manager-" +
                                                        props.info.kafka_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.kafka_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.kafka_managers_info.kafka_managers_statuses.map((status, index) =>
                                        <tr key={"kafka-" + index}>
                                            <td>Kafka
                                            </td>
                                            <td>{props.info.kafka_managers_info.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.kafka_config.kafka_port}</td>
                                            <td>{getTopicsString(status.topics)}</td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kafka-" +
                                                        props.info.kafka_managers_info.ips[index])}
                                                    running={status.running}
                                                    entity={"kafka"} name={"kafka"}
                                                    ip={props.info.kafka_managers_info.ips[index]}
                                                />
                                                <KafkaManagerLogsButton
                                                    loading={loadingEntities.includes("kafka-manager-" +
                                                        props.info.kafka_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.kafka_managers_info.ips[index]}
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
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-manager-start-all")}
                                    running={false} entity="ossec-ids-manager"
                                    name="start-all" ip="start-all"
                                />
                                <span className="aggregateActions">Stop all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-monitor-stop-all")}
                                    running={true} entity="ossec-ids-monitor"
                                    name="stop-all" ip="stop-all"
                                />
                                <span className="aggregateActions">Start all monitors:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-monitor-start-all")}
                                    running={false} entity="ossec-ids-monitor"
                                    name="start-all" ip="start-all"
                                />
                                <span className="aggregateActions">Stop all IDSes:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-stop-all")}
                                    running={true} entity="ossec-ids"
                                    name="stop-all" ip="stop-all"
                                />
                                <span className="aggregateActions">Start all IDSes:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("ossec-ids-start-all")}
                                    running={false} entity="ossec-ids"
                                    name="start-all" ip="start-all"
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
                                    {props.info.ossec_ids_managers_info.ossec_ids_managers_statuses.map((status, index) =>
                                        <tr key={"ossec-ids-manager" + index}>
                                            <td>OSSEC IDS Manager</td>
                                            <td>{props.info.ossec_ids_managers_info.ips[index]}</td>
                                            <td>{props.info.ossec_ids_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.ossec_ids_managers_info.ossec_ids_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-manager-" +
                                                        props.info.ossec_ids_managers_info.ips[index])}
                                                    running={props.info.ossec_ids_managers_info.ossec_ids_managers_running[index]}
                                                    entity={"ossec-ids-manager"} name={"ossec-ids-manager"}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
                                                />
                                                <OssecIDSManagerLogsButton
                                                    loading={loadingEntities.includes("ossec-ids-manager-" +
                                                        props.info.ossec_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.ossec_ids_managers_info.ossec_ids_managers_statuses.map((status, index) =>
                                        <tr key={"ossec-ids-monitor-" + index}>
                                            <td>OSSEC IDS Monitor</td>
                                            <td>{props.info.ossec_ids_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.monitor_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-monitor-" +
                                                        props.info.ossec_ids_managers_info.ips[index])}
                                                    running={status.monitor_running}
                                                    entity={"ossec-ids-monitor"} name={"ossec-ids-monitor"}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
                                                />
                                                <OssecIDSManagerLogsButton
                                                    loading={loadingEntities.includes("ossec-ids-manager-" +
                                                        props.info.ossec_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.ossec_ids_managers_info.ossec_ids_managers_statuses.map((status, index) =>
                                        <tr key={"ossec-ids-" + index}>
                                            <td>OSSEC IDS
                                            </td>
                                            <td>{props.info.ossec_ids_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.ossec_ids_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("ossec-ids-" +
                                                        props.info.ossec_ids_managers_info.ips[index])}
                                                    running={status.ossec_ids_running}
                                                    entity={"ossec-ids"} name={"ossec-ids"}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
                                                />
                                                <OssecIDSManagerLogsButton
                                                    loading={loadingEntities.includes("ossec-ids-manager-" +
                                                        props.info.ossec_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.ossec_ids_managers_info.ips[index]}
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
                                    {props.info.snort_ids_managers_info.snort_ids_managers_statuses.map((status, index) =>
                                        <tr key={"snort-ids-manager-" + index}>
                                            <td>Snort IDS Manager</td>
                                            <td>{props.info.snort_ids_managers_info.ips[index]}</td>
                                            <td>{props.info.snort_ids_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.snort_ids_managers_info.snort_ids_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-manager-" +
                                                        props.info.snort_ids_managers_info.ips[index])}
                                                    running={props.info.snort_ids_managers_info.snort_ids_managers_running[index]}
                                                    entity={"snort-ids-manager"} name={"snort-ids-manager"}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
                                                />
                                                <SnortManagerLogsButton
                                                    loading={loadingEntities.includes("snort-manager-" +
                                                        props.info.snort_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.snort_ids_managers_info.snort_ids_managers_statuses.map((status, index) =>
                                        <tr key={"snort-ids-monitor-" + index}>
                                            <td>Snort IDS Monitor</td>
                                            <td>{props.info.snort_ids_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.monitor_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-monitor-" +
                                                        props.info.snort_ids_managers_info.ips[index])}
                                                    running={status.monitor_running}
                                                    entity={"snort-ids-monitor"} name={"snort-ids-monitor"}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
                                                />
                                                <SnortManagerLogsButton
                                                    loading={loadingEntities.includes("snort-manager-" +
                                                        props.info.snort_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.snort_ids_managers_info.snort_ids_managers_statuses.map((status, index) =>
                                        <tr key={"snort-ids-" + index}>
                                            <td>Snort IDS
                                            </td>
                                            <td>{props.info.snort_ids_managers_info.ips[index]}</td>
                                            <td></td>
                                            {activeStatus(status.snort_ids_running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("snort-ids-" + props.info.snort_ids_managers_info.ips[index])}
                                                    running={status.snort_ids_running}
                                                    entity={"snort-ids"} name={"snort-ids"}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
                                                />
                                                <SnortManagerLogsButton
                                                    loading={loadingEntities.includes("snort-manager-" +
                                                        props.info.snort_ids_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.snort_ids_managers_info.ips[index]}
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
                                    {props.info.elk_managers_info.elk_managers_statuses.map((status, index) =>
                                        <tr key={"elk-manager-" + index}>
                                            <td>ELK manager</td>
                                            <td>{props.info.elk_managers_info.ips[index]}</td>
                                            <td>{props.info.elk_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.elk_managers_info.elk_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    running={props.info.elk_managers_info.elk_managers_running[index]}
                                                    entity={"elk-manager"} name={"elk-manager"}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                                <ElkManagerLogsButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.elk_managers_info.elk_managers_statuses.map((status, index) =>
                                        <tr key={"elk-stack-" + index}>
                                            <td>ELK stack</td>
                                            <td>{props.info.elk_managers_info.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.elk_config.elastic_port},
                                                {props.execution.emulation_env_config.elk_config.logstash_port},
                                                {props.execution.emulation_env_config.elk_config.kibana_port}
                                            </td>
                                            {activeStatus((status.elasticRunning & status.kibanaRunning
                                                & status.logstashRunning))}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elk-stack-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    running={(status.elasticRunning & status.kibanaRunning
                                                        & status.logstashRunning)}
                                                    entity={"elk-stack"} name={"elk-stack"}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                                <ElkManagerLogsButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.elk_managers_info.elk_managers_statuses.map((status, index) =>
                                        <tr key={"elastic-" + index}>
                                            <td>Elasticsearch
                                            </td>
                                            <td>{props.info.elk_managers_info.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.elk_config.elastic_port}</td>
                                            {activeStatus(status.elasticRunning)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("elastic-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    running={status.elasticRunning}
                                                    entity={"elastic"} name={"elastic"}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                                <ElkManagerLogsButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.elk_managers_info.elk_managers_statuses.map((status, index) =>
                                        <tr key={"elk_manager_status-" + index}>
                                            <td>Logstash
                                            </td>
                                            <td>{props.info.elk_managers_info.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.elk_config.logstash_port}</td>
                                            {activeStatus(status.logstashRunning)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("logstash-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    running={status.logstashRunning}
                                                    entity={"logstash"} name={"logstash"}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                                <ElkManagerLogsButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}

                                    {props.info.elk_managers_info.elk_managers_statuses.map((status, index) =>
                                        <tr key={"kibana-" + index}>
                                            <td>Kibana
                                            </td>
                                            <td>{props.info.elk_managers_info.ips[index]}</td>
                                            <td>{props.execution.emulation_env_config.elk_config.kibana_port}</td>
                                            {activeStatus(status.kibanaRunning)}
                                            <td>
                                                <KibanaButton
                                                    loading={loadingEntities.includes("kibana-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    name={props.info.elk_managers_info.ips[index]}
                                                    port={props.info.elk_managers_info.local_kibana_port}
                                                />
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("kibana-" +
                                                        props.info.elk_managers_info.ips[index])}
                                                    running={status.kibanaRunning}
                                                    entity={"kibana"} name={"kibana"}
                                                    ip={props.info.elk_managers_info.ips[index]}
                                                />
                                                <ElkManagerLogsButton
                                                    loading={loadingEntities.includes("elk-manager-" +
                                                        props.info.elk_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.elk_managers_info.ips[index]}
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
                                />
                                <span className="aggregateActions">Start all managers:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-manager-start-all")}
                                    running={false} entity="traffic-manager"
                                    name="start-all" ip="start-all"
                                />
                                <span className="aggregateActions">Stop all generators:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-generator-stop-all")}
                                    running={true} entity="traffic-generator"
                                    name="stop-all" ip="stop-all"
                                />
                                <span className="aggregateActions">Start all generators:</span>
                                <SpinnerOrButton
                                    loading={loadingEntities.includes("traffic-generator-start-all")}
                                    running={false} entity="traffic-generator"
                                    name="start-all" ip="start-all"
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
                                    {props.info.traffic_managers_info.traffic_managers_statuses.map((status, index) =>
                                        <tr key={"traffic-manager-" + index}>
                                            <td>Traffic Manager</td>
                                            <td>{props.info.traffic_managers_info.ips[index]}</td>
                                            <td>{props.info.traffic_managers_info.ports[index]}</td>
                                            {activeStatus(props.info.traffic_managers_info.traffic_managers_running[index])}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("traffic-manager-" +
                                                        props.info.traffic_managers_info.ips[index])}
                                                    running={props.info.traffic_managers_info.traffic_managers_running[index]}
                                                    entity={"traffic-manager"} name={"traffic-manager"}
                                                    ip={props.info.traffic_managers_info.ips[index]}
                                                />
                                                <TrafficManagerLogsButton
                                                    loading={loadingEntities.includes("traffic-manager-" +
                                                        props.info.traffic_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.traffic_managers_info.ips[index]}
                                                />
                                            </td>
                                        </tr>
                                    )}
                                    {props.info.traffic_managers_info.traffic_managers_statuses.map((status, index) =>
                                        <tr key={"traffic-generator-" + index}>
                                            <td>Traffic Generator</td>
                                            <td>{props.info.traffic_managers_info.ips[index]}</td>
                                            <td>-</td>
                                            {activeStatus(status.running)}
                                            <td>
                                                <SpinnerOrButton
                                                    loading={loadingEntities.includes("traffic-generator-" +
                                                        props.info.traffic_managers_info.ips[index])}
                                                    running={status.running}
                                                    entity={"traffic-generator"} name={"traffic-generator"}
                                                    ip={props.info.traffic_managers_info.ips[index]}
                                                />
                                                <TrafficManagerLogsButton
                                                    loading={loadingEntities.includes("traffic-manager-" +
                                                        props.info.traffic_managers_info.ips[index] + "-logs")}
                                                    ip={props.info.traffic_managers_info.ips[index]}
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

            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

ExecutionControlPlane.propTypes = {};
ExecutionControlPlane.defaultProps = {};
export default ExecutionControlPlane;
