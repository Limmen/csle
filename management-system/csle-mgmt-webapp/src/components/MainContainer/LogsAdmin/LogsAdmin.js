import React, {useState, useEffect, useCallback} from 'react';
import './LogsAdmin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Tooltip from 'react-bootstrap/Tooltip';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Spinner from 'react-bootstrap/Spinner'
import Collapse from 'react-bootstrap/Collapse'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";

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
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();

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
                setLoadingStatsManagerLogs(false)
                setStatsManagerLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchPrometheusLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/logs/prometheus' + "?token=" + props.sessionData.token,
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
                setLoadingPrometheusLogs(false)
                setPrometheusLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchNodeExporterLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/logs/node-exporter' + "?token=" + props.sessionData.token,
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
                setLoadingNodeExporterLogs(false)
                setNodeExporterLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchCAdvisorLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/logs/cadvisor' + "?token=" + props.sessionData.token,
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
                setLoadingCAdvisorLogs(false)
                setCAdvisorLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchGrafanaLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/logs/grafana' + "?token=" + props.sessionData.token,
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
                setLoadingGrafanaLogs(false)
                setGrafanaLogs(parseLogs(response.logs))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const refresh = () => {
        setLoadingStatsManagerLogs(true)
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
        fetchStatsManagerLogs()
        fetchNodeExporterLogs()
        fetchPrometheusLogs()
        fetchCAdvisorLogs()
        fetchGrafanaLogs()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload logs from the backend
        </Tooltip>
    );

    const parseLogs = (lines) => {
        var data = lines.map((line, index) => {
            return {
                index: index,
                content: line
            }
        })
        return data
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
    }, [fetchStatsManagerLogs, fetchPrometheusLogs, fetchNodeExporterLogs, fetchCAdvisorLogs,
        fetchGrafanaLogs]);

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
        </div>
    );
}

LogsAdmin.propTypes = {};
LogsAdmin.defaultProps = {};
export default LogsAdmin;
