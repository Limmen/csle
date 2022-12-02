import React, {useState, useCallback} from 'react';
import './Experiment.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import MetricPlot from "./MetricPlot/MetricPlot";
import Collapse from 'react-bootstrap/Collapse'
import Spinner from 'react-bootstrap/Spinner'
import getAgentTypeStr from '../../../Common/getAgentTypeStr'
import getPlayerTypeStr from '../../../Common/getPlayerTypeStr'
import getDateStr from "../../../Common/getDateStr";
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import {HTTP_PREFIX, HTTP_REST_POST, LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM, FILE_RESOURCE} from "../../../Common/constants";

/**
 * Component representing the /training-results/id resource
 */
const Experiment = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [hyperparametersOpen, setHyperparametersOpen] = useState(false);
    const [randomSeedsAndOutputsOpen, setRandomSeedsAndOutputsOpen] = useState(false);
    const [metricTablesOpen, setMetricTablesOpen] = useState(false);
    const [metricPlotsOpen, setMetricPlotsOpen] = useState(false);
    const [policiesOpen, setPoliciesOpen] = useState(false);
    const [logsOpen, setLogsOpen] = useState(false);
    const [loadingLogs, setLoadingLogs] = useState(false);
    const [logs, setLogs] = useState(null);

    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData


    const fetchLogs = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${FILE_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({path: props.experiment.log_file_path})
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
                setLoadingLogs(false)
                setLogs(parseLogs(response))
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, props.experiment.log_file_path]);

    const renderRemoveExperimentTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove experiment execution
        </Tooltip>
    );

    const getThresholds = (thresholds) => {
        if (thresholds === null || thresholds === undefined) {
            return "-"
        } else {
            return thresholds.join(", ")
        }
    }

    const parseLogs = (logs) => {
        var lines = logs.logs.split("\n")
        var data = lines.map((line, index) => {
            var parts = line.split(/,(.*)/)
            var date = parts[0]
            var content = parts[1]
            return {
                date: date,
                content: content
            }
        })
        return data
    }

    const getLogs = () => {
        if (logsOpen) {
            setLogsOpen(false)
        } else {
            setLogsOpen(true)
            setLoadingLogs(true)
            fetchLogs()
        }
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
                            <th>Timestamp</th>
                            <th>Log line</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.logs.map((logLine, index) => {
                            return <tr key={logLine.date + "-" + index}>
                                <td>{logLine.date}</td>
                                <td>{logLine.content}</td>
                            </tr>
                        })}
                        </tbody>
                    </Table>
                </div>
            )
        }

    }

    const Actions = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <h5 className="semiTitle">
                    Actions:

                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveExperimentTooltip}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeExperiment(props.experiment)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>
            )
        } else {
            return (<></>)
        }
    }

    const Logs = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={getLogs}
                            aria-controls="logsOpenBody"
                            aria-expanded={logsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                Logs: {props.experiment.log_file_path}
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={logsOpen}>
                        <div id="logsOpenBody" className="cardBodyHidden">
                            <SpinnerOrLogs loadingLogs={loadingLogs} logs={logs}/>
                            <p className="extraMarginTop"></p>
                        </div>
                    </Collapse>
                </Card>
            )
        } else {
            return (<></>)
        }
    }


    return (<Card key={props.experiment.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.experiment.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.experiment.id}, Simulation: {props.experiment.simulation_name}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.experiment.id}>
            <Card.Body>
                <Actions sessionData={props.sessionData} removeExperiment={props.removeExperiment}
                         experiment={props.experiment}/>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                General information about the training run
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Attribute</th>
                                        <th> Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td>ID</td>
                                        <td>{props.experiment.id}</td>
                                    </tr>
                                    <tr>
                                        <td>Description</td>
                                        <td>{props.experiment.descr}</td>
                                    </tr>
                                    <tr>
                                        <td>Simulation</td>
                                        <td>{props.experiment.simulation_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Emulation</td>
                                        <td>{props.experiment.emulation_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Timestamp</td>
                                        <td>{getDateStr(props.experiment.timestamp)}</td>
                                    </tr>
                                    <tr>
                                        <td>Log file path</td>
                                        <td>{props.experiment.log_file_path}</td>
                                    </tr>
                                    <tr>
                                        <td>Configuration</td>
                                        <td>
                                            <Button variant="link" className="dataDownloadLink"
                                                    onClick={() => fileDownload(JSON.stringify(props.experiment), "config.json")}>
                                                training_run.json
                                            </Button>
                                        </td>
                                    </tr>
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setHyperparametersOpen(!hyperparametersOpen)}
                            aria-controls="hyperparametersBody"
                            aria-expanded={hyperparametersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                Hyperparameters
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={hyperparametersOpen}>
                        <div id="hyperparametersOpen" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Description</th>
                                        <th>Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {Object.keys(props.experiment.config.hparams).map((hparamName, index) => {
                                        return <tr key={hparamName + "-" + index}>
                                            <td>{hparamName}</td>
                                            <td>{props.experiment.config.hparams[hparamName].descr}</td>
                                            <td>{props.experiment.config.hparams[hparamName].value}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setRandomSeedsAndOutputsOpen(!randomSeedsAndOutputsOpen)}
                            aria-controls="randomSeedsAndOutputsBody"
                            aria-expanded={randomSeedsAndOutputsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Random seeds and output directories
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={randomSeedsAndOutputsOpen}>
                        <div id="randomSeedsAndOutputsOpen" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Seed</th>
                                        <th>Output directory</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.experiment.config.random_seeds.map((seed, index) => {
                                        return <tr key={seed + "-" + index}>
                                            <td>{seed}</td>
                                            <td>{props.experiment.config.output_dir}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setMetricPlotsOpen(!metricPlotsOpen)}
                            aria-controls="metricPlotsBody"
                            aria-expanded={metricPlotsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Metric plots
                                <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricPlotsOpen}>
                        <div id="metricPlotsBody" className="cardBodyHidden">
                            {props.experiment.result.plot_metrics.map((metric, index2) => {
                                return <MetricPlot key={"plot_metrics-" + metric + "-" + index2} className="metricPlot"
                                                   metricName={metric}
                                                   data={props.experiment.result.avg_metrics[metric]}
                                                   stds={props.experiment.result.std_metrics[metric]}/>
                            })}
                            {Object.keys(props.experiment.result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.experiment.result.all_metrics[seed]).map((metric, index2) => {
                                        if (props.experiment.result.all_metrics[seed][metric] !== undefined
                                            && props.experiment.result.all_metrics[seed][metric] !== null &&
                                            props.experiment.result.all_metrics[seed][metric].length > 0 &&
                                            !Array.isArray(props.experiment.result.all_metrics[seed][metric][0])) {
                                            return (
                                                <div className="metricsTable"
                                                     key={"metricPlot-" + seed + "-" + metric + "-" + index1 + "-" + index2}>
                                                    <h5 className="semiTitle semiTitle2">
                                                        Metric: {metric}, seed: {seed}
                                                    </h5>
                                                    <MetricPlot key={metric + "-" + seed + "-" + index1 + "-" + index2}
                                                                className="metricPlot" metricName={metric}
                                                                data={props.experiment.result.all_metrics[seed][metric]}
                                                                stds={null}/>
                                                </div>)
                                        } else {
                                            return (<span
                                                key={"metricPlot-" + seed + "-" + metric + "-" + index1 + "-" + index2}></span>)
                                        }
                                    })
                                }
                            )
                            }
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setMetricTablesOpen(!metricTablesOpen)}
                            aria-controls="metricTablesBody"
                            aria-expanded={metricTablesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Metric tables
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricTablesOpen}>
                        <div id="metricTablesBody" className="cardBodyHidden">
                            {Object.keys(props.experiment.result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.experiment.result.all_metrics[seed]).map((metric, index2) => {
                                        if (props.experiment.result.all_metrics[seed][metric].length > 0) {
                                            return (
                                                <div
                                                    key={seed + "-" + metric + "-" + index1 + "-" + index2}>
                                                    <h5 className="semiTitle">
                                                        Metric: {metric}, seed: {seed}
                                                    </h5>
                                                    <div className="table-responsive">
                                                        <Table striped bordered hover>
                                                            <thead>
                                                            <tr>
                                                                <th>Training iteration</th>
                                                                <th>{metric}</th>
                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            {props.experiment.result.all_metrics[seed][metric].map((metricValue, index3) => {
                                                                return <tr
                                                                    key={metricValue + "-" + index3 + "-" + index2 + "-" + index1}>
                                                                    <td>{index3}</td>
                                                                    <td>{metricValue}</td>
                                                                </tr>
                                                            })}
                                                            </tbody>
                                                        </Table>
                                                    </div>
                                                </div>)
                                        } else {
                                            return (<span key={seed + "-" + metric + "-" + index1 + "-" + index2}></span>)
                                        }
                                    })
                                }
                            )
                            }
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setPoliciesOpen(!policiesOpen)}
                            aria-controls="policiesOpenBody"
                            aria-expanded={policiesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                Learned policies
                                <i className="fa fa-list-ul headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={policiesOpen}>
                        <div id="policiesOpenBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Seed</th>
                                        <th>Policy ID</th>
                                        <th>Agent type</th>
                                        <th>Player type</th>
                                        <th>Thresholds</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {Object.keys(props.experiment.result.policies).map((seed, index1) => {
                                            return (<tr
                                                key={seed + "-" + index1}>
                                                <td>{seed}</td>
                                                <td>{props.experiment.result.policies[seed].id}</td>
                                                <td>{getAgentTypeStr(props.experiment.result.policies[seed].agent_type)}</td>
                                                <td>{getPlayerTypeStr(props.experiment.result.policies[seed].player_type)}</td>
                                                <td>{getThresholds(props.experiment.result.policies[seed].thresholds)}</td>
                                            </tr>)
                                        })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Logs sessionData={props.sessionData} experiment={props.experiment}/>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Experiment.propTypes = {};
Experiment.defaultProps = {};
export default Experiment;
