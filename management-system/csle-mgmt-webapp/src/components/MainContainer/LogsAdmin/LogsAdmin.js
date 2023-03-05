import React, {useState, useEffect, useCallback} from 'react';
import './LogsAdmin.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Tooltip from 'react-bootstrap/Tooltip';
import Select from 'react-select'
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Modal from 'react-bootstrap/Modal'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Spinner from 'react-bootstrap/Spinner'
import Collapse from 'react-bootstrap/Collapse'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {useDebouncedCallback} from 'use-debounce';
import parseLogs from "../../Common/parseLogs";
import ArchImg from './Arch.png'
import {
    HTTP_PREFIX,
    LOGIN_PAGE_RESOURCE, CLUSTER_STATUS_RESOURCE,
    DOCKER_STATS_MANAGER_SUBRESOURCE, HTTP_REST_POST, HTTP_REST_GET,
    LOGS_RESOURCE, TOKEN_QUERY_PARAM, FILE_RESOURCE, CADVISOR_RESOURCE, PGADMIN_RESOURCE,
    GRAFANA_RESOURCE, NODE_EXPORTER_RESOURCE, PROMETHEUS_RESOURCE, NGINX_RESOURCE, DOCKER_RESOURCE,
    POSTGRESQL_RESOURCE, FLASK_RESOURCE, CLUSTER_MANAGER_RESOURCE
} from "../../Common/constants";

/**
 * Component representing the /logs-admin-page
 */
const LogsAdmin = (props) => {
    const [loadingServerCluster, setLoadingServerCluster] = useState(true);
    const [serverCluster, setServerCluster] = useState([]);
    const [filteredServerCluster, setFilteredServerCluster] = useState([]);
    const [selectedPhysicalServerIp, setSelectedPhysicalServerIp] = useState(null);
    const [loadingStatsManagerLogs, setLoadingStatsManagerLogs] = useState(true);
    const [statsManagerLogsOpen, setStatsManagerLogsOpen] = useState(false);
    const [statsManagerLogs, setStatsManagerLogs] = useState([]);
    const [loadingGrafanaLogs, setLoadingGrafanaLogs] = useState(true);
    const [grafanaLogsOpen, setGrafanaLogsOpen] = useState(false);
    const [grafanaLogs, setGrafanaLogs] = useState([]);
    const [loadingCAdvisorLogs, setLoadingCAdvisorLogs] = useState(true);
    const [cadvisorLogsOpen, setCAdvisorLogsOpen] = useState(false);
    const [cadvisorLogs, setCAdvisorLogs] = useState([]);
    const [loadingPgAdminLogs, setLoadingPgAdminLogs] = useState(true);
    const [pgAdminLogsOpen, setPgAdminLogsOpen] = useState(false);
    const [pgAdminLogs, setPgAdminLogs] = useState([]);
    const [loadingNginxLogs, setLoadingNginxLogs] = useState(true);
    const [nginxLogsOpen, setNginxLogsOpen] = useState(false);
    const [nginxLogs, setNginxLogs] = useState([]);
    const [loadingPostgresqlLogs, setLoadingPostgresqlLogs] = useState(true);
    const [postgresqlLogsOpen, setPostgresqlLogsOpen] = useState(false);
    const [postgresqlLogs, setPostgresqlLogs] = useState([]);
    const [loadingDockerLogs, setLoadingDockerLogs] = useState(true);
    const [dockerLogsOpen, setDockerLogsOpen] = useState(false);
    const [dockerLogs, setDockerLogs] = useState([]);
    const [loadingFlaskLogs, setLoadingFlaskLogs] = useState(true);
    const [flaskLogsOpen, setFlaskLogsOpen] = useState(false);
    const [flaskLogs, setFlaskLogs] = useState([]);
    const [loadingClusterManagerLogs, setLoadingClusterManagerLogs] = useState(true);
    const [clusterManagerLogsOpen, setClusterManagerLogsOpen] = useState(false);
    const [clusterManagerLogs, setClusterManagerLogs] = useState([]);
    const [loadingPrometheusLogs, setLoadingPrometheusLogs] = useState(true);
    const [prometheusLogsOpen, setPrometheusLogsOpen] = useState(false);
    const [prometheusLogs, setPrometheusLogs] = useState([]);
    const [loadingNodeExporterLogs, setLoadingNodeExporterLogs] = useState(true);
    const [nodeExporterLogsOpen, setNodeExporterLogsOpen] = useState(false);
    const [nodeExporterLogs, setNodeExporterLogs] = useState([]);
    const [csleLogsOpen, setCsleLogsOpen] = useState(false);
    const [csleLogFiles, setCsleLogFiles] = useState([]);
    const [selectedCsleLogFile, setSelectedCsleLogFile] = useState(null);
    const [selectedCsleLogFileData, setSelectedCsleLogFileData] = useState(null);
    const [loadingCsleLogFiles, setLoadingCsleLogFiles] = useState(true);
    const [loadingSelectedCsleLogFile, setLoadingSelectedCsleLogFile] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchLogFile = useCallback((path, node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${FILE_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({path: path, ip: node_ip})
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
                setLoadingSelectedCsleLogFile(false)
                setSelectedCsleLogFileData(parseLogs(response.logs.split("\n")))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchStatsManagerLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${DOCKER_STATS_MANAGER_SUBRESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingStatsManagerLogs(false)
                setStatsManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);


    const fetchCsleLogFiles = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingCsleLogFiles(false)
                const csleLogFiles = response.logs.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: id_obj
                    }
                })
                setCsleLogFiles(csleLogFiles)
                if (csleLogFiles.length > 0) {
                    setSelectedCsleLogFile(csleLogFiles[0])
                    fetchLogFile(csleLogFiles[0].value)
                    setLoadingSelectedCsleLogFile(true)
                } else {
                    setLoadingSelectedCsleLogFile(false)
                    setSelectedCsleLogFile(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchLogFile]);

    const fetchPrometheusLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${PROMETHEUS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingPrometheusLogs(false)
                setPrometheusLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchNodeExporterLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${NODE_EXPORTER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingNodeExporterLogs(false)
                setNodeExporterLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchCAdvisorLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${CADVISOR_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingCAdvisorLogs(false)
                setCAdvisorLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchPgAdminLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${PGADMIN_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingPgAdminLogs(false)
                setPgAdminLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchGrafanaLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${GRAFANA_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingGrafanaLogs(false)
                setGrafanaLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);


    const fetchNginxLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${NGINX_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingNginxLogs(false)
                setNginxLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchPostgresqlLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${POSTGRESQL_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingPostgresqlLogs(false)
                setPostgresqlLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchFlaskLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${FLASK_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingFlaskLogs(false)
                setFlaskLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchClusterManagerLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${CLUSTER_MANAGER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingClusterManagerLogs(false)
                setClusterManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchDockerLogs = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${DOCKER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({ip: node_ip})
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
                setLoadingDockerLogs(false)
                setDockerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchServerCluster = useCallback((path) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CLUSTER_STATUS_RESOURCE}`
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
                const serverClusterIPIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: `IP:${id_obj.ip}`
                    }
                })
                setLoadingServerCluster(false)
                setServerCluster(serverClusterIPIds)
                setFilteredServerCluster(serverClusterIPIds)
                if (serverClusterIPIds.length > 0) {
                    setSelectedPhysicalServerIp(serverClusterIPIds[0])
                    setLoadingStatsManagerLogs(true)
                    setLoadingNodeExporterLogs(true)
                    setLoadingPrometheusLogs(true)
                    setLoadingCAdvisorLogs(true)
                    setLoadingPgAdminLogs(true)
                    setLoadingGrafanaLogs(true)
                    setLoadingCsleLogFiles(true)
                    setLoadingNginxLogs(true)
                    setLoadingDockerLogs(true)
                    setLoadingPostgresqlLogs(true)
                    setLoadingFlaskLogs(true)
                    setLoadingClusterManagerLogs(true)
                    fetchStatsManagerLogs(serverClusterIPIds[0].value.ip)
                    fetchNodeExporterLogs(serverClusterIPIds[0].value.ip)
                    fetchPrometheusLogs(serverClusterIPIds[0].value.ip)
                    fetchCAdvisorLogs(serverClusterIPIds[0].value.ip)
                    fetchPgAdminLogs(serverClusterIPIds[0].value.ip)
                    fetchGrafanaLogs(serverClusterIPIds[0].value.ip)
                    fetchCsleLogFiles(serverClusterIPIds[0].value.ip)
                    fetchNginxLogs(serverClusterIPIds[0].value.ip)
                    fetchFlaskLogs(serverClusterIPIds[0].value.ip)
                    fetchClusterManagerLogs(serverClusterIPIds[0].value.ip)
                    fetchPostgresqlLogs(serverClusterIPIds[0].value.ip)
                    fetchDockerLogs(serverClusterIPIds[0].value.ip)
                } else {
                    setSelectedPhysicalServerIp(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchStatsManagerLogs,
        fetchNodeExporterLogs, fetchPrometheusLogs, fetchCAdvisorLogs, fetchPgAdminLogs, fetchGrafanaLogs,
        fetchCsleLogFiles, fetchNginxLogs, fetchFlaskLogs, fetchPostgresqlLogs, fetchDockerLogs,
        fetchClusterManagerLogs]);

    const refresh = () => {
        setLoadingServerCluster(true)
        setLoadingStatsManagerLogs(true)
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        setLoadingCsleLogFiles(true)
        setLoadingSelectedCsleLogFile(true)
        setLoadingPgAdminLogs(true)
        setLoadingNginxLogs(true)
        setLoadingDockerLogs(true)
        setLoadingPostgresqlLogs(true)
        setLoadingFlaskLogs(true)
        setLoadingClusterManagerLogs(true)
        fetchServerCluster()
    }

    const updateSelectedPhysicalServerIp = (physicalServerIp) => {
        setSelectedPhysicalServerIp(physicalServerIp)
        setLoadingStatsManagerLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        setLoadingCAdvisorLogs(true)
        setLoadingPgAdminLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingCsleLogFiles(true)
        setLoadingNginxLogs(true)
        setLoadingDockerLogs(true)
        setLoadingPostgresqlLogs(true)
        setLoadingFlaskLogs(true)
        setLoadingClusterManagerLogs(true)
        fetchStatsManagerLogs(physicalServerIp.value.ip)
        fetchNodeExporterLogs(physicalServerIp.value.ip)
        fetchPrometheusLogs(physicalServerIp.value.ip)
        fetchCAdvisorLogs(physicalServerIp.value.ip)
        fetchPgAdminLogs(physicalServerIp.value.ip)
        fetchGrafanaLogs(physicalServerIp.value.ip)
        fetchCsleLogFiles(physicalServerIp.value.ip)
        fetchNginxLogs(physicalServerIp.value.ip)
        fetchFlaskLogs(physicalServerIp.value.ip)
        fetchClusterManagerLogs(physicalServerIp.value.ip)
        fetchPostgresqlLogs(physicalServerIp.value.ip)
        fetchDockerLogs(physicalServerIp.value.ip)
    }

    const searchFilter = (node, searchVal) => {
        return (searchVal === "" ||
            node.ip.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fServerCluster = serverCluster.filter(node => {
            return searchFilter(node.value, searchVal)
        });
        setFilteredServerCluster(fServerCluster)

        var selectedServerRemoved = false
        if (fServerCluster.length > 0) {
            for (let i = 0; i < fServerCluster.length; i++) {
                if (selectedPhysicalServerIp !== null && selectedPhysicalServerIp !== undefined &&
                    selectedPhysicalServerIp.value.ip === fServerCluster[i].value.ip) {
                    selectedServerRemoved = true
                }
            }
            if (!selectedServerRemoved) {
                setSelectedPhysicalServerIp(fServerCluster[0])
                setLoadingStatsManagerLogs(true)
                setLoadingNodeExporterLogs(true)
                setLoadingPrometheusLogs(true)
                setLoadingCAdvisorLogs(true)
                setLoadingPgAdminLogs(true)
                setLoadingGrafanaLogs(true)
                setLoadingCsleLogFiles(true)
                setLoadingNginxLogs(true)
                setLoadingDockerLogs(true)
                setLoadingPostgresqlLogs(true)
                setLoadingFlaskLogs(true)
                setLoadingClusterManagerLogs(true)
                fetchStatsManagerLogs(fServerCluster[0].value.ip)
                fetchNodeExporterLogs(fServerCluster[0].value.ip)
                fetchPrometheusLogs(fServerCluster[0].value.ip)
                fetchCAdvisorLogs(fServerCluster[0].value.ip)
                fetchPgAdminLogs(fServerCluster[0].value.ip)
                fetchGrafanaLogs(fServerCluster[0].value.ip)
                fetchCsleLogFiles(fServerCluster[0].value.ip)
                fetchNginxLogs(fServerCluster[0].value.ip)
                fetchFlaskLogs(fServerCluster[0].value.ip)
                fetchClusterManagerLogs(fServerCluster[0].value.ip)
                fetchPostgresqlLogs(fServerCluster[0].value.ip)
                fetchDockerLogs(fServerCluster[0].value.ip)
            }
        } else {
            setSelectedPhysicalServerIp(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload logs from the backend
        </Tooltip>
    );

    const renderServerRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about how logs are collected
        </Tooltip>
    );

    const SelectedServerView = (props) => {
        if (props.loading){
            return (<></>)
        }
        return (
            <div>
                <h3> Logs
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h3>
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setStatsManagerLogsOpen(!props.statsManagerLogsOpen)}
                            aria-controls="statsManagerLogsBody"
                            aria-expanded={props.statsManagerLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Docker stats manager logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.statsManagerLogsOpen}>
                        <div id="statsManagerLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingStatsManagerLogs}
                                               logs={props.statsManagerLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setGrafanaLogsOpen(!props.grafanaLogsOpen)}
                            aria-controls="grafanaLogsBody"
                            aria-expanded={props.grafanaLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Grafana logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.grafanaLogsOpen}>
                        <div id="grafanaLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingGrafanaLogs} logs={props.grafanaLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setPrometheusLogsOpen(!props.prometheusLogsOpen)}
                            aria-controls="prometheusLogsBody"
                            aria-expanded={props.prometheusLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Prometheus logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.prometheusLogsOpen}>
                        <div id="prometheusLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingPrometheusLogs}
                                               logs={props.prometheusLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setCAdvisorLogsOpen(!props.cadvisorLogsOpen)}
                            aria-controls="cAdvisorLogsBody"
                            aria-expanded={props.cadvisorLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> cAdvisor logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.cadvisorLogsOpen}>
                        <div id="cAdvisorLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingCAdvisorLogs}
                                               logs={props.cadvisorLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setPgAdminLogsOpen(!props.pgAdminLogsOpen)}
                            aria-controls="pgAdminLogsBody"
                            aria-expanded={props.pgAdminLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> pgAdmin logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.pgAdminLogsOpen}>
                        <div id="pgAdminLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingPgAdminLogs} logs={props.pgAdminLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setNodeExporterLogsOpen(!props.nodeExporterLogsOpen)}
                            aria-controls="nodeExporterLogsBody"
                            aria-expanded={props.nodeExporterLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Node exporter logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.nodeExporterLogsOpen}>
                        <div id="nodeExporterLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingNodeExporterLogs}
                                               logs={props.nodeExporterLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setCsleLogsOpen(!props.csleLogsOpen)}
                            aria-controls="csleLogsBody"
                            aria-expanded={props.csleLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> CSLE Log files
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.csleLogsOpen}>
                        <div id="csleLogsBody" className="cardBodyHidden">
                            <h4>
                                <SelectCsleLogFileDropdownOrSpinner
                                    selectedCsleLogFile={props.selectedCsleLogFile}
                                    loadingCsleLogFiles={props.loadingCsleLogFiles}
                                    csleLogFiles={props.csleLogFiles}
                                    loadingSelectedCsleLogFile={props.loadingSelectedCsleLogFile}
                                />
                            </h4>
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingSelectedCsleLogFile || props.loadingCsleLogFiles}
                                               logs={props.selectedCsleLogFileData}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setNginxLogsOpen(!props.nginxLogsOpen)}
                            aria-controls="nginxLogsBody"
                            aria-expanded={props.nginxLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Nginx logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.nginxLogsOpen}>
                        <div id="nginxLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingNginxLogs}
                                               logs={props.nginxLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setDockerLogsOpen(!props.dockerLogsOpen)}
                            aria-controls="dockerLogsBody"
                            aria-expanded={props.dockerLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Docker engine logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.dockerLogsOpen}>
                        <div id="dockerLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingDockerLogs}
                                               logs={props.dockerLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setFlaskLogsOpen(!props.flaskLogsOpen)}
                            aria-controls="flaskLogsBody"
                            aria-expanded={props.flaskLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Flask logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.flaskLogsOpen}>
                        <div id="flaskLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingFlaskLogs}
                                               logs={props.flaskLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setPostgresqlLogsOpen(!props.postgresqlLogsOpen)}
                            aria-controls="postgresqlLogsBody"
                            aria-expanded={props.postgresqlLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> PostgreSQL logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.postgresqlLogsOpen}>
                        <div id="postgresqlLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingPostgresqlLogs}
                                               logs={props.postgresqlLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => props.setClusterManagerLogsOpen(!props.clusterManagerLogsOpen)}
                            aria-controls="clusterManagerLogsBody"
                            aria-expanded={props.clusterManagerLogsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Cluster manager logs
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={props.clusterManagerLogsOpen}>
                        <div id="clusterManagerLogsBody" className="cardBodyHidden">
                            <h4>
                                Last 100 log lines:
                            </h4>
                            <div className="table-responsive">
                                <SpinnerOrLogs loadingLogs={props.loadingClusterManagerLogs}
                                               logs={props.clusterManagerLogs}/>
                            </div>
                        </div>
                    </Collapse>
                </Card>
            </div>
        )
    }

    const SpinnerOrLogs = (props) => {
        if (props.loadingLogs || props.logs === null || props.logs === undefined) {
            return (<Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
            />)
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

    const updateSelectedCsleLogFile = (logFile) => {
        setSelectedCsleLogFile(logFile)
        fetchLogFile(logFile.value)
        setLoadingSelectedCsleLogFile(true)
    }

    const SelectCsleLogFileDropdownOrSpinner = (props) => {
        if (!(props.loadingCsleLogFiles || props.loadingSelectedCsleLogFile) && props.csleLogFiles.length === 0) {
            return (
                <div>
                    <span className="emptyText">No CSLE log files are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        }
        if ((props.loadingCsleLogFiles || props.loadingSelectedCsleLogFile)) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching log files... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (<div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    Log file:
                    <div className="conditionalDist inline-block selectEmulation">
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedCsleLogFile}
                                defaultValue={props.selectedCsleLogFile}
                                options={props.csleLogFiles}
                                onChange={updateSelectedCsleLogFile}
                                placeholder="Select a log file"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Logs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        CSLE is a distributed system that consist of N ≥ 1 physical servers connected through an IP network.
                        This page allows to view log files of each server.
                    </p>
                    <div className="text-center">
                        <img src={ArchImg} alt="Architecture" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SelectPhysicalServerDropdownOrSpinner = (props) => {
        if (!props.loading && props.serverCluster.length === 0) {
            return (
                <div>
                    <span className="emptyText">No physical servers are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching servers... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (<div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderServerRefreshTooltip}
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    Server:
                    <div className="conditionalDist inline-block selectEmulation">
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedPhysicalServerIp}
                                defaultValue={props.selectedPhysicalServerIp}
                                options={props.serverCluster}
                                onChange={updateSelectedPhysicalServerIp}
                                placeholder="Select a server"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }


    useEffect(() => {
        setLoadingStatsManagerLogs(true);
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        setLoadingPgAdminLogs(true)
        setLoadingServerCluster(true)
        setLoadingNginxLogs(true)
        setLoadingDockerLogs(true)
        setLoadingPostgresqlLogs(true)
        setLoadingFlaskLogs(true)
        setLoadingClusterManagerLogs(true)
        fetchServerCluster()
    }, [fetchServerCluster]);

    return (
        <div className="container-fluid">
            <h3 className="managementTitle"> Log files </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectPhysicalServerDropdownOrSpinner
                            loading={loadingServerCluster} serverCluster={filteredServerCluster}
                            selectedPhysicalServerIp={selectedPhysicalServerIp}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                <div className="col-sm-1">
                </div>
            </div>
            <SelectedServerView loading={loadingServerCluster} statsManagerLogsOpen={statsManagerLogsOpen}
                                setStatsManagerLogsOpen={setStatsManagerLogsOpen}
                                loadingStatsManagerLogs={loadingStatsManagerLogs}
                                statsManagerLogs={statsManagerLogs}
                                setGrafanaLogsOpen={setGrafanaLogsOpen} grafanaLogsOpen={grafanaLogsOpen}
                                loadingGrafanaLogs={loadingGrafanaLogs} grafanaLogs={grafanaLogs}
                                setPrometheusLogsOpen={setPrometheusLogsOpen} prometheusLogsOpen={prometheusLogsOpen}
                                loadingPrometheusLogs={loadingPrometheusLogs} prometheusLogs={prometheusLogs}
                                setCAdvisorLogsOpen={setCAdvisorLogsOpen} cadvisorLogsOpen={cadvisorLogsOpen}
                                loadingCAdvisorLogs={loadingCAdvisorLogs} cadvisorLogs={cadvisorLogs}
                                setPgAdminLogsOpen={setPgAdminLogsOpen} pgAdminLogsOpen={pgAdminLogsOpen}
                                loadingPgAdminLogs={loadingPgAdminLogs} pgAdminLogs={pgAdminLogs}
                                setNodeExporterLogsOpen={setNodeExporterLogsOpen}
                                nodeExporterLogsOpen={nodeExporterLogsOpen}
                                loadingNodeExporterLogs={loadingNodeExporterLogs} nodeExporterLogs={nodeExporterLogs}
                                setCsleLogsOpen={setCsleLogsOpen} csleLogsOpen={csleLogsOpen}
                                selectedCsleLogFile={selectedCsleLogFile} loadingCsleLogFiles={loadingCsleLogFiles}
                                csleLogFiles={csleLogFiles} loadingSelectedCsleLogFile={loadingSelectedCsleLogFile}
                                selectedCsleLogFileData={selectedCsleLogFileData}
                                nginxLogsOpen={nginxLogsOpen} setNginxLogsOpen={setNginxLogsOpen}
                                loadingNginxLogs={loadingNginxLogs} nginxLogs={nginxLogs}
                                dockerLogsOpen={dockerLogsOpen} setDockerLogsOpen={setDockerLogsOpen}
                                loadingDockerLogs={loadingDockerLogs} dockerLogs={dockerLogs}
                                flaskLogsOpen={flaskLogsOpen} setFlaskLogsOpen={setFlaskLogsOpen}
                                loadingFlaskLogs={loadingFlaskLogs} flaskLogs={flaskLogs}
                                postgresqlLogsOpen={postgresqlLogsOpen} setPostgresqlLogsOpen={setPostgresqlLogsOpen}
                                loadingPostgresqlLogs={loadingPostgresqlLogs} postgresqlLogs={postgresqlLogs}
                                clusterManagerLogsOpen={clusterManagerLogsOpen}
                                setClusterManagerLogsOpen={setClusterManagerLogsOpen}
                                loadingClusterManagerLogs={loadingClusterManagerLogs}
                                clusterManagerLogs={clusterManagerLogs}
            />
        </div>
    );
}

LogsAdmin.propTypes = {};
LogsAdmin.defaultProps = {};
export default LogsAdmin;
