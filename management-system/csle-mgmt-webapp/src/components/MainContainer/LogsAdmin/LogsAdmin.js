import React, {useState, useEffect, useCallback} from 'react';
import './LogsAdmin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Tooltip from 'react-bootstrap/Tooltip';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
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
    const [statsManagerLogs, setStatsManagerLogs] = useState("");
    const [loadingGrafanaLogs, setLoadingGrafanaLogs] = useState(true);
    const [grafanaLogsOpen, setGrafanaLogsOpen] = useState(false);
    const [grafanaLogs, setGrafanaLogs] = useState("");
    const [loadingCAdvisorLogs, setLoadingCAdvisorLogs] = useState(true);
    const [cadvisorLogsOpen, setCAdvisorLogsOpen] = useState(false);
    const [cadvisorLogs, setCAdvisorLogs] = useState("");
    const [loadingPrometheusLogs, setLoadingPrometheusLogs] = useState(true);
    const [prometheusLogsOpen, setPrometheusLogsOpen] = useState(false);
    const [prometheusLogs, setPrometheusLogs] = useState("");
    const [loadingNodeExporterLogs, setLoadingNodeExporterLogs] = useState(true);
    const [nodeExporterLogsOpen, setNodeExporterLogsOpen] = useState(false);
    const [nodeExporterLogs, setNodeExporterLogs] = useState("");
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();

    const fetchStatsManagerLogs = useCallback(() => {
        fetch(
            `http://` + ip + ":" + port + '/file' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({path: props.experiment.log_file_path})
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
                setStatsManagerLogs(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const refresh = () => {
        setLoadingStatsManagerLogs(true)
        setLoadingCAdvisorLogs(true)
        setLoadingGrafanaLogs(true)
        setLoadingNodeExporterLogs(true)
        setLoadingPrometheusLogs(true)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload logs from the backend
        </Tooltip>
    );


    useEffect(() => {
        setLoadingStatsManagerLogs(true);
    }, []);

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
                        <div className="table-responsive">
                            <p> LOGS</p>
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
                        <div className="table-responsive">
                            <p> LOGS</p>
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
                        <div className="table-responsive">
                            <p> LOGS</p>
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
                        <div className="table-responsive">
                            <p> LOGS</p>
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
                        <div className="table-responsive">
                            <p> LOGS</p>
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
