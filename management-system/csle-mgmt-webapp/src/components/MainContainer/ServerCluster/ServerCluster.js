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
import DockerImg from './Docker.png'
import FlaskImg from './Flask.png'
import NginxImg from './Nginx.png'
import PostgresImg from './Postgres.png'
import NodeExporterImg from './NodeExporter.png'
import {
    HTTP_PREFIX, HTTP_REST_GET, LOGIN_PAGE_RESOURCE, GRAFANA_RESOURCE, PGADMIN_RESOURCE,
    PROMETHEUS_RESOURCE, NODE_EXPORTER_RESOURCE, NGINX_RESOURCE, POSTGRESQL_RESOURCE, CLUSTER_STATUS_RESOURCE,
    FLASK_RESOURCE, DOCKER_RESOURCE,
    CADVISOR_RESOURCE, TOKEN_QUERY_PARAM, HTTP_REST_POST,
} from "../../Common/constants";

/**
 *  Component representing the /server-cluster-page
 */
const ServerCluster = (props) => {
    const [loadingServerCluster, setLoadingServerCluster] = useState(true);
    const [serverCluster, setServerCluster] = useState([]);
    const [filteredServerCluster, setFilteredServerCluster] = useState([]);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [loadingEntities, setLoadingEntities] = useState([]);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
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

    const addLoadingEntity = (entity) => {
        var newLoadingEntities = []
        for (let i = 0; i < loadingEntities.length; i++) {
            newLoadingEntities.push(loadingEntities[i])
        }
        newLoadingEntities.push(entity)
        setLoadingEntities(newLoadingEntities)
    }

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
                setLoadingServerCluster(false)
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const startOrStopGrafanaRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${GRAFANA_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-grafana")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);


    const startOrStopNginxRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${NGINX_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-nginx")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopDockerRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DOCKER_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-docker")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopPostgreSQLRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${POSTGRESQL_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-postgresql")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopFlaskRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${FLASK_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-flask")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopPgAdminRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PGADMIN_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-pgAdmin")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopcAdvisorRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CADVISOR_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-cAdvisor")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopNodeExporterRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${NODE_EXPORTER_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-nodeExporter")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopPrometheusRequest = useCallback((node_ip) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PROMETHEUS_RESOURCE}`
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
                if (response === null) {
                    return
                }
                removeLoadingEntity(node_ip + "-prometheus")
                setServerCluster(response)
                setFilteredServerCluster(response)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, removeLoadingEntity]);

    const startOrStopGrafana = (node_ip) => {
        addLoadingEntity(node_ip + "-grafana")
        startOrStopGrafanaRequest(node_ip)
    }

    const startOrStopPgAdmin = (node_ip) => {
        addLoadingEntity(node_ip + "-pgAdmin")
        startOrStopPgAdminRequest(node_ip)
    }

    const startOrStopPrometheus = (node_ip) => {
        addLoadingEntity(node_ip + "-prometheus")
        startOrStopPrometheusRequest(node_ip)
    }

    const startOrStopcAdvisor = (node_ip) => {
        addLoadingEntity(node_ip + "-cAdvisor")
        startOrStopcAdvisorRequest(node_ip)
    }

    const startOrStopNodeExporter = (node_ip) => {
        addLoadingEntity(node_ip + "-nodeExporter")
        startOrStopNodeExporterRequest(node_ip)
    }

    const startOrStopFlask = (node_ip) => {
        addLoadingEntity(node_ip + "-flask")
        startOrStopFlaskRequest(node_ip)
    }

    const startOrStopDocker = (node_ip) => {
        addLoadingEntity(node_ip + "-docker")
        startOrStopDockerRequest(node_ip)
    }

    const startOrStopNginx = (node_ip) => {
        addLoadingEntity(node_ip + "-nginx")
        startOrStopNginxRequest(node_ip)
    }

    const startOrStopPostgreSQL = (node_ip) => {
        addLoadingEntity(node_ip + "-postgresql")
        startOrStopPostgreSQLRequest(node_ip)
    }


    const refresh = () => {
        setLoadingServerCluster(true)
        fetchServerCluster()
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
                                    <GrafanaLink className="grafanaStatus" node={node}
                                                 sessionData={props.sessionData} ip={node.ip}
                                                 loading={loadingEntities.includes(`${node.ip}-grafana`)}
                                    />
                                    <PrometheusLink className="grafanaStatus" node={node}
                                                    sessionData={props.sessionData} ip={node.ip}
                                                    loading={loadingEntities.includes(`${node.ip}-prometheus`)}
                                    />
                                    <NodeExporterLink className="grafanaStatus" node={node}
                                                      sessionData={props.sessionData} ip={node.ip}
                                                      loading={loadingEntities.includes(`${node.ip}-nodeExporter`)}
                                    />
                                    <CadvisorLink className="grafanaStatus" node={node}
                                                  sessionData={props.sessionData} ip={node.ip}
                                                  loading={loadingEntities.includes(`${node.ip}-cAdvisor`)}
                                    />
                                    <PgAdminLink className="grafanaStatus" node={node}
                                                 sessionData={props.sessionData} ip={node.ip}
                                                 loading={loadingEntities.includes(`${node.ip}-pgAdmin`)}
                                    />
                                    <NginxLink className="grafanaStatus" node={node}
                                                 sessionData={props.sessionData} ip={node.ip}
                                                 loading={loadingEntities.includes(`${node.ip}-nginx`)}
                                    />
                                    <DockerLink className="grafanaStatus" node={node}
                                               sessionData={props.sessionData} ip={node.ip}
                                               loading={loadingEntities.includes(`${node.ip}-docker`)}
                                    />
                                    <PostgreSQLLink className="grafanaStatus" node={node}
                                               sessionData={props.sessionData} ip={node.ip}
                                               loading={loadingEntities.includes(`${node.ip}-postgresql`)}
                                    />
                                    <FlaskLink className="grafanaStatus" node={node}
                                               sessionData={props.sessionData} ip={node.ip}
                                               loading={loadingEntities.includes(`${node.ip}-flask`)}
                                    />
                                </td>
                                <td>
                                    <GrafanaAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-grafana`)}
                                    />
                                    <PrometheusAction className="grafanaStatus" node={node}
                                                      sessionData={props.sessionData} ip={node.ip}
                                                      loading={loadingEntities.includes(`${node.ip}-prometheus`)}
                                    />
                                    <NodeExporterAction className="grafanaStatus"
                                                        node={node} sessionData={props.sessionData} ip={node.ip}
                                                        loading={loadingEntities.includes(`${node.ip}-nodeExporter`)}
                                    />
                                    <CadvisorAction className="grafanaStatus" node={node}
                                                    sessionData={props.sessionData} ip={node.ip}
                                                    loading={loadingEntities.includes(`${node.ip}-cAdvisor`)}
                                    />
                                    <PgAdminAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-pgAdmin`)}
                                    />
                                    <NginxAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-nginx`)}
                                    />
                                    <DockerAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-docker`)}
                                    />
                                    <PostgreSQLAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-postrgresql`)}
                                    />
                                    <FlaskAction className="grafanaStatus" node={node}
                                                   sessionData={props.sessionData} ip={node.ip}
                                                   loading={loadingEntities.includes(`${node.ip}-flask`)}
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

    const renderNodeExporterTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Node exporter
        </Tooltip>
    );

    const renderDockerTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Docker engine
        </Tooltip>
    );

    const renderNginxTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Nginx
        </Tooltip>
    );

    const renderPostgreSQLTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            PostgreSQL
        </Tooltip>
    );

    const renderFlaskTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Flask REST API
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
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.grafanaRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.grafanaUrl}>
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
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.grafanaRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopGrafana(props.node.ip)}>
                    Start Grafana
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopGrafana(props.node.ip)}>
                    Stop Grafana
                </Button>
            )
        }
    }

    const NginxLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.nginxRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.nginxUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderNginxTooltip()}>
                        <img src={NginxImg} alt="Nginx" className="img-fluid grafanaImg" width="35px" height="35px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const NginxAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.nginxRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNginx(props.node.ip)}>
                    Start Nginx
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNginx(props.node.ip)}>
                    Stop Nginx
                </Button>
            )
        }
    }


    const PostgreSQLLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.postgreSQLRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.postgreSQLUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderPostgreSQLTooltip()}>
                        <img src={PostgresImg} alt="PostgreSQL" className="img-fluid grafanaImg" width="40px" height="40px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const PostgreSQLAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.postgreSQLRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPostgreSQL(props.node.ip)}>
                    Start PostgreSQL
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPostgreSQL(props.node.ip)}>
                    Stop PostgreSQL
                </Button>
            )
        }
    }

    const DockerLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.dockerRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.dockerUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderDockerTooltip()}>
                        <img src={DockerImg} alt="Docker Engine" className="img-fluid grafanaImg" width="40px" height="40px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const DockerAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.dockerRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopDocker(props.node.ip)}>
                    Start Docker engine
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopDocker(props.node.ip)}>
                    Stop Docker engine
                </Button>
            )
        }
    }

    const FlaskLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.flaskRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.flaskUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderFlaskTooltip()}>
                        <img src={FlaskImg} alt="Flask" className="img-fluid" width="30px" height="30px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const FlaskAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.flaskRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopFlask(props.node.ip)}>
                    Start Flask
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopFlask(props.node.ip)}>
                    Stop Flask
                </Button>
            )
        }
    }


    const PrometheusAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.prometheusRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPrometheus(props.node.ip)}>
                    Start Prometheus
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPrometheus(props.node.ip)}>
                    Stop Prometheus
                </Button>
            )
        }
    }

    const PrometheusLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.prometheusRunning === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={props.node.prometheusUrl}>
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
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.nodeExporterRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNodeExporter(props.node.ip)}>
                    Start Node exporter
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopNodeExporter(props.node.ip)}>
                    Stop Node exporter
                </Button>
            )
        }
    }

    const NodeExporterLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.nodeExporterRunning === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={props.node.nodeExporterUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderNodeExporterTooltip()}>
                        <img src={NodeExporterImg} alt="Prometheus" className="img-fluid" width="45px" height="45px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const CadvisorAction = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.cAdvisorRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopcAdvisor(props.node.ip)}>
                    Start cAdvisor
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopcAdvisor(props.node.ip)}>
                    Stop cAdvisor
                </Button>
            )
        }
    }

    const CadvisorLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.cAdvisorRunning === false) {
            return (
                <></>
            )
        } else {
            return (
                <a className="grafanaStatus" href={props.node.cAdvisorUrl}>
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
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.pgAdminRunning === false) {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPgAdmin(props.node.ip)}>
                    Start pgAdmin
                </Button>)
        } else {
            return (
                <Button variant="link" className="dataDownloadLink"
                        onClick={() => startOrStopPgAdmin(props.node.ip)}>
                    Stop pgAdmin
                </Button>
            )
        }
    }

    const PgAdminLink = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
        if (props.node == null || props.node.pgAdminRunning === false) {
            return (
                <></>)
        } else {
            return (
                <a className="grafanaStatus" href={props.node.pgAdminUrl}>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderPgAdminTooltip()}>
                        <img src={pgAdminImg} alt="Grafana" className="img-fluid grafanaImg" width="90px" height="90px"/>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    useEffect(() => {
        setLoadingServerCluster(true)
        fetchServerCluster()
    }, [fetchServerCluster]);

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