import React, {useState, useEffect, useCallback} from 'react';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import './ServerCluster.css';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import getBoolStr from "../../Common/getBoolStr";
import SystemArch from './SystemArch.png'
import GrafanaImg from './Grafana.png'
import cAdvisorImg from './cAdvisor.png'
import pgAdminImg from './PGadmin.png'
import PrometheusImg from './Prometheus.png'
import NodeExporterImg from './NodeExporter.png'
import {
    HTTP_PREFIX, HTTP_REST_GET, LOGIN_PAGE_RESOURCE, GRAFANA_RESOURCE, PGADMIN_RESOURCE,
    PROMETHEUS_RESOURCE, NODE_EXPORTER_RESOURCE,
    CADVISOR_RESOURCE, TOKEN_QUERY_PARAM, SERVER_CLUSTER_RESOURCE, HTTP_REST_POST,
} from "../../Common/constants";

/**
 *  Component representing the /server-cluster-page
 */
const ServerCluster = (props) => {
    const [loadingServerCluster, setLoadingServerCluster] = useState(true);
    const [loadingGrafana, setLoadingGrafana] = useState(true);
    const [loadingCAdvisor, setLoadingCAdvisor] = useState(true);
    const [loadingPrometheus, setLoadingPrometheus] = useState(true);
    const [loadingNodeExporter, setLoadingNodeExporter] = useState(true);
    const [loadingPgAdmin, setLoadingPgAdmin] = useState(true);
    const [serverCluster, setServerCluster] = useState([]);
    const [filteredServerCluster, setFilteredServerCluster] = useState([]);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [grafanaStatus, setGrafanaStatus] = useState(null);
    const [cAdvisorStatus, setCAdvisorStatus] = useState(null);
    const [prometheusStatus, setPrometheusStatus] = useState(null);
    const [nodeExporterStatus, setNodeExporterStatus] = useState(null);
    const [pgAdminStatus, setPgAdminStatus] = useState(null);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchServerCluster = useCallback((path) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SERVER_CLUSTER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                setLoadingServerCluster(false)
                setServerCluster(response.cluster_nodes)
                setFilteredServerCluster(response.cluster_nodes)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const startOrStopGrafanaRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${GRAFANA_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setGrafanaStatus(response)
                setLoadingGrafana(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const startOrStopPgAdminRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PGADMIN_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setPgAdminStatus(response)
                setLoadingPgAdmin(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const startOrStopcAdvisorRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CADVISOR_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setCAdvisorStatus(response)
                setLoadingCAdvisor(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const startOrStopNodeExporterRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${NODE_EXPORTER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setNodeExporterStatus(response)
                setLoadingNodeExporter(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const startOrStopPrometheusRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PROMETHEUS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setPrometheusStatus(response)
                setLoadingPrometheus(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchGrafanaStatus = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${GRAFANA_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setGrafanaStatus(response)
                setLoadingGrafana(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchPgAdminStatus = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PGADMIN_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setPgAdminStatus(response)
                setLoadingPgAdmin(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchCadvisorStatus = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CADVISOR_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setCAdvisorStatus(response)
                setLoadingCAdvisor(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchPrometheusStatus = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PROMETHEUS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setPrometheusStatus(response)
                setLoadingPrometheus(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchNodeExporterStatus = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${NODE_EXPORTER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setNodeExporterStatus(response)
                setLoadingNodeExporter(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const startOrStopGrafana = () => {
        setLoadingGrafana(true)
        startOrStopGrafanaRequest()
    }

    const startOrStopPgAdmin = () => {
        setLoadingPgAdmin(true)
        startOrStopPgAdminRequest()
    }

    const startOrStopPrometheus = () => {
        setLoadingPrometheus(true)
        startOrStopPrometheusRequest()
    }

    const startOrStopcAdvisor = () => {
        setLoadingCAdvisor(true)
        startOrStopcAdvisorRequest()
    }

    const startOrStopNodeExporter = () => {
        setLoadingNodeExporter(true)
        startOrStopNodeExporterRequest()
    }


    const refresh = () => {
        setLoadingServerCluster(true)
        setLoadingGrafana(true)
        setLoadingCAdvisor(true)
        setLoadingPrometheus(true)
        setLoadingNodeExporter(true)
        setLoadingPgAdmin(true)
        fetchServerCluster()
        fetchGrafanaStatus()
        fetchPgAdminStatus()
        fetchPrometheusStatus()
        fetchCadvisorStatus()
        fetchNodeExporterStatus()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload server cluster configuration from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the server cluster.
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Server cluster of the CSLE installation
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        The management system of CSLE is a distributed system that consist of N >=1 physical servers
                        connected through an IP network.
                        One of the servers is designated to be the "leader" and the other servers are "workers"
                        Workers can perform local management actions but not actions that affect the overall system
                        state.
                        These actions are routed to the leader, which applies them sequentially to ensure
                        consistent updates to the system state.
                    </p>
                    <div className="text-center">
                        <img src={SystemArch} alt="ServerCluster" width="300" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SpinnerOrTable = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="table-responsive">
                    <Table bordered hover>
                        <thead>
                        <tr className="serverClusterTable">
                            <th>IP</th>
                            <th>CPUs (Cores)</th>
                            <th>GPUs</th>
                            <th>RAM (GB)</th>
                            <th>Leader</th>
                            <th>Links</th>
                            <th>Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.serverCluster.map((node, index) =>
                            <tr className="serverClusterTable" key={node.ip + "-" + index}>
                                <td>{node.ip}</td>
                                <td>{node.cpus}</td>
                                <td>{node.gpus}</td>
                                <td>{node.RAM}</td>
                                <td>{getBoolStr(node.leader)}</td>
                                <td>
                                    <GrafanaLink className="grafanaStatus" grafanaStatus={grafanaStatus}
                                                 sessionData={props.sessionData} ip={node.ip}
                                                 loading={loadingGrafana}
                                    />
                                    <PrometheusLink className="grafanaStatus" prometheusStatus={prometheusStatus}
                                                    sessionData={props.sessionData} ip={node.ip}
                                                    loading={loadingPrometheus}
                                    />
                                    <NodeExporterLink className="grafanaStatus" nodeExporterStatus={nodeExporterStatus}
                                                      sessionData={props.sessionData} ip={node.ip}
                                                      loading={loadingNodeExporter}
                                    />
                                    <CadvisorLink className="grafanaStatus" cAdvisorStatus={cAdvisorStatus}
                                                  sessionData={props.sessionData} ip={node.ip}
                                                  loading={loadingCAdvisor}
                                    />
                                    <PgAdminLink className="grafanaStatus" pgAdminStatus={pgAdminStatus}
                                                 sessionData={props.sessionData} ip={node.ip}
                                                 loading={loadingPgAdmin}
                                    />
                                </td>
                                <td>
                                    <GrafanaAction className="grafanaStatus" grafanaStatus={grafanaStatus}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingGrafana}
                                    />
                                    <PrometheusAction className="grafanaStatus" prometheusStatus={prometheusStatus}
                                                      sessionData={props.sessionData} ip={node.ip}
                                                      loading={loadingPrometheus}
                                    />
                                    <NodeExporterAction className="grafanaStatus"
                                                        nodeExporterStatus={nodeExporterStatus}
                                                        sessionData={props.sessionData} ip={node.ip}
                                                        loading={loadingNodeExporter}
                                    />
                                    <CadvisorAction className="grafanaStatus" cAdvisorStatus={cAdvisorStatus}
                                                    sessionData={props.sessionData} ip={node.ip}
                                                    loading={loadingCAdvisor}
                                    />
                                    <PgAdminAction className="grafanaStatus" pgAdminStatus={pgAdminStatus}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingPgAdmin}
                                    />
                                </td>
                            </tr>
                        )}
                        </tbody>
                    </Table>
                </div>
            )
        }
    }


    const renderGrafanaTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Grafana
        </Tooltip>
    );

    const renderPgAdminTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            pgAdmin
        </Tooltip>
    );

    const renderPrometheusTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Prometheus
        </Tooltip>
    );

    const rendercAdvisorTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            cAdvisor
        </Tooltip>
    );

    const rendernodeExporterTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Node exporter
        </Tooltip>
    );

    const searchFilter = (node, searchVal) => {
        return (searchVal === "" ||
            node.ip.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fServerCluster = serverCluster.filter(node => {
            return searchFilter(node, searchVal)
        });
        setFilteredServerCluster(fServerCluster)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const GrafanaLink = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.grafanaStatus !== null) {
            for (let i = 0; i < props.grafanaStatus.length; i++) {
                if(props.grafanaStatus[i].ip === props.ip) {
                    status = props.grafanaStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanfaStatus" href={status.url}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderGrafanaTooltip()}>
                        <img src={GrafanaImg} alt="Grafana" className="img-fluid" width="30px" height="30px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const GrafanaAction = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.grafanaStatus !== null) {
            for (let i = 0; i < props.grafanaStatus.length; i++) {
                if(props.grafanaStatus[i].ip === props.ip) {
                    status = props.grafanaStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopGrafana()}>
                    Start Grafana
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopGrafana()}>
                    Stop Grafana
                </Button>
            )
        }
    }

    const PrometheusAction = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.prometheusStatus !== null) {
            for (let i = 0; i < props.prometheusStatus.length; i++) {
                if(props.prometheusStatus[i].ip === props.ip) {
                    status = props.prometheusStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPrometheus()}>
                    Start Prometheus
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPrometheus()}>
                    Stop Prometheus
                </Button>
            )
        }
    }

    const PrometheusLink = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.prometheusStatus !== null) {
            for (let i = 0; i < props.prometheusStatus.length; i++) {
                if(props.prometheusStatus[i].ip === props.ip) {
                    status = props.prometheusStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={status.url}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderPrometheusTooltip()}>
                        <img src={PrometheusImg} alt="Prometheus" className="img-fluid" width="30px" height="30px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const NodeExporterAction = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.nodeExporterStatus !== null) {
            for (let i = 0; i < props.nodeExporterStatus.length; i++) {
                if(props.nodeExporterStatus[i].ip === props.ip) {
                    status = props.nodeExporterStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNodeExporter()}>
                    Start Node exporter
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNodeExporter()}>
                    Stop Node exporter
                </Button>
            )
        }
    }

    const NodeExporterLink = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.nodeExporterStatus !== null) {
            for (let i = 0; i < props.nodeExporterStatus.length; i++) {
                if(props.nodeExporterStatus[i].ip === props.ip) {
                    status = props.nodeExporterStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={status.url}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={rendernodeExporterTooltip()}>
                        <img src={NodeExporterImg} alt="Prometheus" className="img-fluid" width="45px" height="45px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const CadvisorAction = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.cAdvisorStatus !== null) {
            for (let i = 0; i < props.cAdvisorStatus.length; i++) {
                if(props.cAdvisorStatus[i].ip === props.ip) {
                    status = props.cAdvisorStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopcAdvisor()}>
                    Start cAdvisor
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopcAdvisor()}>
                    Stop cAdvisor
                </Button>
            )
        }
    }

    const CadvisorLink = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.cAdvisorStatus !== null) {
            for (let i = 0; i < props.cAdvisorStatus.length; i++) {
                if(props.cAdvisorStatus[i].ip === props.ip) {
                    status = props.cAdvisorStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={status.url}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={rendercAdvisorTooltip()}>
                        <img src={cAdvisorImg} alt="cAdvisor" className="img-fluid grafanaImg" width="30px"
                             height="30px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const PgAdminAction = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.pgAdminStatus !== null) {
            for (let i = 0; i < props.pgAdminStatus.length; i++) {
                if(props.pgAdminStatus[i].ip === props.ip) {
                    status = props.pgAdminStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPgAdmin()}>
                    Start pgAdmin
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPgAdmin()}>
                    Stop pgAdmin
                </Button>
            )
        }
    }

    const PgAdminLink = (props) => {
        if(props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>
            )
        }
        let status = null
        if (props.pgAdminStatus !== null) {
            for (let i = 0; i < props.pgAdminStatus.length; i++) {
                if(props.pgAdminStatus[i].ip === props.ip) {
                    status = props.pgAdminStatus[i]
                }
            }
        }
        if (status == null || status.running === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={status.url}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderPgAdminTooltip()}>
                        <img src={pgAdminImg} alt="Grafana" className="img-fluid" width="30px" height="30px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    useEffect(() => {
        setLoadingServerCluster(true)
        setLoadingGrafana(true)
        setLoadingCAdvisor(true)
        setLoadingPrometheus(true)
        setLoadingNodeExporter(true)
        setLoadingPgAdmin(true)
        fetchServerCluster()
        fetchGrafanaStatus()
        fetchCadvisorStatus()
        fetchPrometheusStatus()
        fetchNodeExporterStatus()
        fetchPgAdminStatus()
    }, [fetchServerCluster, fetchGrafanaStatus, fetchCadvisorStatus, fetchPrometheusStatus,
        fetchNodeExporterStatus, fetchPgAdminStatus]);

    return (
        <div className="ServerCluster">
            <h3 className="managementTitle"> Server Cluster Configuration </h3>
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Physical servers
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshTooltip}
                        >
                            <Button variant="button" onClick={refresh}>
                                <i className="fa fa-refresh refreshButton3" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderInfoTooltip}
                            className="overLayInfo"
                        >
                            <Button variant="button" onClick={() => setShowInfoModal(true)} className="infoButton3">
                                <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <SpinnerOrTable serverCluster={filteredServerCluster} loading={loadingServerCluster}
                            sessionData={props.sessionData}/>
        </div>
    );
}

ServerCluster.propTypes = {};
ServerCluster.defaultProps = {};
export default ServerCluster;