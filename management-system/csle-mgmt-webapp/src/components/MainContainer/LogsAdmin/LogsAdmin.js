import React, {useState, useEffect, useCallback} from 'react';
import './LogsAdmin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Tooltip from 'react-bootstrap/Tooltip';
import Select from 'react-select'
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Spinner from 'react-bootstrap/Spinner'
import Collapse from 'react-bootstrap/Collapse'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import parseLogs from "../../Common/parseLogs";
import {
    HTTP_PREFIX,
    LOGIN_PAGE_RESOURCE,
    DOCKER_STATS_MANAGER_SUBRESOURCE, HTTP_REST_POST, HTTP_REST_GET,
    LOGS_RESOURCE, TOKEN_QUERY_PARAM, FILE_RESOURCE, CADVISOR_RESOURCE,
    GRAFANA_RESOURCE, NODE_EXPORTER_RESOURCE, PROMETHEUS_RESOURCE
} from "../../Common/constants";

/**
 * Component representing the /logs-admin-page
 */
const LogsAdmin = (props) => {
    const [loadingStatsManagerLogs, setLoadingStatsManagerLogs] = useState(true);
    const [statsManagerLogsOpen, setStatsManagerLogsOpen] = useState(false);
    const [statsManagerLogs, setStatsManagerLogs] = useState([]);
    const [loadingGrafanaLogs, setLoadingGrafanaLogs] = useState(true);
    const [grafanaLogsOpen, setGrafanaLogsOpen] = useState(false);
    const [grafanaLogs, setGrafanaLogs] = useState([]);
    const [loadingCAdvisorLogs, setLoadingCAdvisorLogs] = useState(true);
    const [cadvisorLogsOpen, setCAdvisorLogsOpen] = useState(false);
    const [cadvisorLogs, setCAdvisorLogs] = useState([]);
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
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchLogFile = useCallback((path) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${FILE_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({path: path})
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
                setLoadingSelectedCsleLogFile(false)
                setSelectedCsleLogFileData(parseLogs(response.logs.split("\n")))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchStatsManagerLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${DOCKER_STATS_MANAGER_SUBRESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                setLoadingStatsManagerLogs(false)
                setStatsManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);


    const fetchCsleLogFiles = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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

    const fetchPrometheusLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${PROMETHEUS_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                setLoadingPrometheusLogs(false)
                setPrometheusLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchNodeExporterLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${NODE_EXPORTER_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                setLoadingNodeExporterLogs(false)
                setNodeExporterLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchCAdvisorLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${CADVISOR_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
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

    const fetchGrafanaLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LOGS_RESOURCE}/${GRAFANA_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                setLoadingGrafanaLogs(false)
                setGrafanaLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const refresh = () => {
        setLoadingStatsManagerLogs(true)
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        setLoadingCsleLogFiles(true)
        setLoadingSelectedCsleLogFile(true)
        fetchStatsManagerLogs()
        fetchNodeExporterLogs()
        fetchPrometheusLogs()
        fetchCAdvisorLogs()
        fetchGrafanaLogs()
        fetchCsleLogFiles()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload logs from the backend
        </Tooltip>
    );

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
                    Selected log file:
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


    useEffect(() => {
        setLoadingStatsManagerLogs(true);
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        fetchStatsManagerLogs()
        fetchPrometheusLogs()
        fetchNodeExporterLogs()
        fetchCAdvisorLogs()
        fetchGrafanaLogs()
        fetchCsleLogFiles()
    }, [fetchStatsManagerLogs, fetchPrometheusLogs, fetchNodeExporterLogs, fetchCAdvisorLogs,
        fetchGrafanaLogs, fetchCsleLogFiles]);

    return (
        <div className="Admin">
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
                        onClick={() => setStatsManagerLogsOpen(!statsManagerLogsOpen)}
                        aria-controls="statsManagerLogsBody"
                        aria-expanded={statsManagerLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> Docker stats manager logs </h5>
                    </Button>
                </Card.Header>
                <Collapse in={statsManagerLogsOpen}>
                    <div id="statsManagerLogsBody" className="cardBodyHidden">
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingStatsManagerLogs} logs={statsManagerLogs}/>
                        </div>
                    </div>
                </Collapse>
            </Card>

            <Card className="subCard">
                <Card.Header>
                    <Button
                        onClick={() => setGrafanaLogsOpen(!grafanaLogsOpen)}
                        aria-controls="grafanaLogsBody"
                        aria-expanded={grafanaLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> Grafana logs </h5>
                    </Button>
                </Card.Header>
                <Collapse in={grafanaLogsOpen}>
                    <div id="grafanaLogsBody" className="cardBodyHidden">
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingGrafanaLogs} logs={grafanaLogs}/>
                        </div>
                    </div>
                </Collapse>
            </Card>

            <Card className="subCard">
                <Card.Header>
                    <Button
                        onClick={() => setPrometheusLogsOpen(!prometheusLogsOpen)}
                        aria-controls="prometheusLogsBody"
                        aria-expanded={prometheusLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> Prometheus logs </h5>
                    </Button>
                </Card.Header>
                <Collapse in={prometheusLogsOpen}>
                    <div id="prometheusLogsBody" className="cardBodyHidden">
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingPrometheusLogs} logs={prometheusLogs}/>
                        </div>
                    </div>
                </Collapse>
            </Card>

            <Card className="subCard">
                <Card.Header>
                    <Button
                        onClick={() => setCAdvisorLogsOpen(!cadvisorLogsOpen)}
                        aria-controls="cAdvisorLogsBody"
                        aria-expanded={cadvisorLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> cAdvisor logs </h5>
                    </Button>
                </Card.Header>
                <Collapse in={cadvisorLogsOpen}>
                    <div id="cAdvisorLogsBody" className="cardBodyHidden">
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingCAdvisorLogs} logs={cadvisorLogs}/>
                        </div>
                    </div>
                </Collapse>
            </Card>

            <Card className="subCard">
                <Card.Header>
                    <Button
                        onClick={() => setNodeExporterLogsOpen(!nodeExporterLogsOpen)}
                        aria-controls="nodeExporterLogsBody"
                        aria-expanded={nodeExporterLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> Node exporter logs </h5>
                    </Button>
                </Card.Header>
                <Collapse in={nodeExporterLogsOpen}>
                    <div id="nodeExporterLogsBody" className="cardBodyHidden">
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingNodeExporterLogs} logs={nodeExporterLogs}/>
                        </div>
                    </div>
                </Collapse>
            </Card>

            <Card className="subCard">
                <Card.Header>
                    <Button
                        onClick={() => setCsleLogsOpen(!csleLogsOpen)}
                        aria-controls="csleLogsBody"
                        aria-expanded={csleLogsOpen}
                        variant="link"
                    >
                        <h5 className="semiTitle"> CSLE Log files </h5>
                    </Button>
                </Card.Header>
                <Collapse in={csleLogsOpen}>
                    <div id="csleLogsBody" className="cardBodyHidden">
                        <h4>
                            <SelectCsleLogFileDropdownOrSpinner
                                selectedCsleLogFile={selectedCsleLogFile} loadingCsleLogFiles={loadingCsleLogFiles}
                                csleLogFiles={csleLogFiles} loadingSelectedCsleLogFile={loadingSelectedCsleLogFile}
                            />
                        </h4>
                        <h4>
                            Last 100 log lines:
                        </h4>
                        <div className="table-responsive">
                            <SpinnerOrLogs loadingLogs={loadingSelectedCsleLogFile || loadingCsleLogFiles} logs={selectedCsleLogFileData}/>
                        </div>
                    </div>
                </Collapse>
            </Card>
        </div>
    );
}

LogsAdmin.propTypes = {};
LogsAdmin.defaultProps = {};
export default LogsAdmin;
