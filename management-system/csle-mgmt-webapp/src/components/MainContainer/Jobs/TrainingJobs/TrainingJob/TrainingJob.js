import React, {useState, useCallback} from 'react';
import './TrainingJob.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import MetricPlot from "../../../TrainingResults/Experiment/MetricPlot/MetricPlot";
import Collapse from 'react-bootstrap/Collapse'
import Spinner from 'react-bootstrap/Spinner'
import getAgentTypeStr from '../../../../Common/getAgentTypeStr'
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../../../Common/serverIp";
import serverPort from "../../../../Common/serverPort";
import {
    HTTP_PREFIX,
    HTTP_REST_POST,
    LOGIN_PAGE_RESOURCE,
    FILE_RESOURCE,
    TOKEN_QUERY_PARAM} from "../../../../Common/constants";
/**
 * The component representing the /jobs/<id> resource for training jobs
 */
const TrainingJob = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [hyperparametersOpen, setHyperparametersOpen] = useState(false);
    const [metricTablesOpen, setMetricTablesOpen] = useState(false);
    const [metricPlotsOpen, setMetricPlotsOpen] = useState(false);
    const [simulationTracesOpen, setSimulationTracesOpen] = useState(false);
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
                body: JSON.stringify({path: props.job.log_file_path})
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
    }, [alert, ip, navigate, port, props.job.log_file_path, props.sessionData.token, setSessionData]);

    const renderRemoveTrainingJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove training job
        </Tooltip>
    );

    const renderStopTrainingJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop training job
        </Tooltip>
    );

    const renderStartTrainingJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start training job
        </Tooltip>
    );

    const getSeedReward = (experiment_result, seed, agentType) => {
        var len = 0
        if(agentType === 0 || agentType === 1){
            if (experiment_result.all_metrics[seed].average_reward !== null &&
                experiment_result.all_metrics[seed].average_reward !== undefined &&
                experiment_result.all_metrics[seed].average_reward.length > 0) {
                len = experiment_result.all_metrics[seed].average_reward.length
                return experiment_result.all_metrics[seed].average_reward[len - 1]
            } else {
                return -1
            }
        }
        if (agentType === 2) {
            if (experiment_result.all_metrics[seed].exploitability !== null &&
                experiment_result.all_metrics[seed].exploitability !== undefined &&
                experiment_result.all_metrics[seed].exploitability.length > 0) {
                len = experiment_result.all_metrics[seed].exploitability.length
                return experiment_result.all_metrics[seed].exploitability[len - 1]
            } else {
                return -1
            }
        }
        return -1
    }

    const getGreenOrRedCircle = () => {
        if (props.job.running) {
            return (
                <circle r="15" cx="15" cy="15" fill="green"></circle>
            )
        } else {
            return (
                <circle r="15" cx="15" cy="15" fill="red"></circle>
            )
        }
    }

    const getStatusText = () => {
        if (props.job.running) {
            return (
                "Running"
            )
        } else {
            return (
                "Stopped"
            )
        }
    }

    const getSeedRewardLabel = (agentType) => {
        if(agentType === 0 || agentType === 1) {
            return "(Seed, Avg_R):"
        }
        if (agentType === 2) {
            return "(Seed, Exp):"
        }
        return ":"
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

    const startOrStopButton = () => {
        if (props.job.running) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStopTrainingJobTooltip}
                >
                    <Button variant="warning" className="startButton" size="sm"
                            onClick={() => props.stopTrainingJob(props.job)}>
                        <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTrainingJobTooltip}
                >
                    <Button variant="success" className="startButton" size="sm"
                            onClick={() => props.startTrainingJob(props.job)}>
                        <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        }
    }

    const Actions = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <h5 className="semiTitle">
                    Actions:
                    {startOrStopButton()}

                    <OverlayTrigger
                        className="removeButton"
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveTrainingJobTooltip}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeTrainingJob(props.job)}>
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
                                Logs: {props.job.log_file_path}
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

    return (<Card key={props.job.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.job.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.job.id}, Simulation: {props.job.simulation_env_name},
                    Agent: {getAgentTypeStr(props.job.experiment_config.agent_type)}
                </span>
                Progress: {Math.round(100 * props.job.progress_percentage * 100) / 100}%
                Status: {getStatusText()}
                <span className="greenCircle">

                    <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                         version="1.1">
                    {getGreenOrRedCircle()}
                </svg></span>
                <span
                    className="subnetTitle">{getSeedRewardLabel(props.job.experiment_config.agent_type)}</span>
                {Object.keys(props.job.experiment_result.all_metrics).map((seed, index) => {
                    return <span key={seed + "-" + index} className="trainingJobSeedR">
                        ({seed}, <span className="seedRVal">
                        {Math.round(100 *
                            getSeedReward(props.job.experiment_result,
                                seed, props.job.experiment_config.agent_type)) / 100})
                        </span>
                    </span>
                })}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.job.id}>
            <Card.Body>
                <Actions sessionData={props.sessionData} job={props.job} removeTrainingJob={props.removeTrainingJob}/>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                General information about the training job
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
                                        <td>{props.job.id}</td>
                                    </tr>
                                    <tr>
                                        <td>Description</td>
                                        <td>{props.job.descr}</td>
                                    </tr>
                                    <tr>
                                        <td>PID</td>
                                        <td>{props.job.pid}</td>
                                    </tr>
                                    <tr>
                                        <td>Title</td>
                                        <td>{props.job.experiment_config.title}</td>
                                    </tr>
                                    <tr>
                                        <td>Random seeds</td>
                                        <td>{props.job.experiment_config.random_seeds.join(", ")}</td>
                                    </tr>
                                    <tr>
                                        <td>Output directory</td>
                                        <td>{props.job.experiment_config.output_dir}</td>
                                    </tr>
                                    <tr>
                                        <td>Log frequency</td>
                                        <td>{props.job.experiment_config.log_every}</td>
                                    </tr>
                                    <tr>
                                        <td>Emulation environment</td>
                                        <td>{props.job.emulation_env_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Simulation environment</td>
                                        <td>{props.job.simulation_env_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Number of saved simulation traces</td>
                                        <td>{props.job.num_cached_traces}</td>
                                    </tr>
                                    <tr>
                                        <td>Log file path</td>
                                        <td>{props.job.log_file_path}</td>
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
                        <div id="hyperparametersBody" className="cardBodyHidden">
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
                                    {Object.keys(props.job.experiment_config.hparams).map((hparamName, index) => {
                                        return <tr key={hparamName + "-" + index}>
                                            <td>{hparamName}</td>
                                            <td>{props.job.experiment_config.hparams[hparamName].descr}</td>
                                            <td>{props.job.experiment_config.hparams[hparamName].value}</td>
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
                            <h5 className="semiTitle">
                                Metric plots
                                <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricPlotsOpen}>
                        <div id="metricPlotsBody" className="cardBodyHidden">
                            {Object.keys(props.job.experiment_result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.job.experiment_result.all_metrics[seed]).map((metric, index2) => {
                                        if (props.job.experiment_result.all_metrics[seed][metric].length > 0 &&
                                            props.job.experiment_result.all_metrics[seed][metric].length !== undefined &&
                                            props.job.experiment_result.all_metrics[seed][metric].length !== null &&
                                            !Array.isArray(props.job.experiment_result.all_metrics[seed][metric][0])) {
                                            return (
                                                <div className="metricsTable"
                                                     key={seed + "-" + metric + "-" + index1 + "-" + index2}>
                                                    <h5 className="semiTitle semiTitle2">
                                                        Metric: {metric}, seed: {seed}
                                                    </h5>
                                                    <MetricPlot key={metric + "-" + seed + "-" + index1 + "-" + index2}
                                                                className="metricPlot" metricName={metric}
                                                                data={props.job.experiment_result.all_metrics[seed][metric]}
                                                                stds={null}/>
                                                </div>)
                                        } else {
                                            return <span key={seed + "-" + metric + "-" + index1 + "-" + index2}></span>
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
                            <h5 className="semiTitle">
                                Metric tables
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricTablesOpen}>
                        <div id="metricTablesBody" className="cardBodyHidden">
                            {Object.keys(props.job.experiment_result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.job.experiment_result.all_metrics[seed]).map((metric, index2) => {
                                        if (props.job.experiment_result.all_metrics[seed][metric].length > 0) {
                                            return (
                                                <div key={seed + "-" + metric + "-" + index1 + "-" + index2}>
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
                                                            {props.job.experiment_result.all_metrics[seed][metric].map((metricValue, index3) => {
                                                                return <tr key={metricValue + "-" + index3}>
                                                                    <td>{index3}</td>
                                                                    <td>{metricValue}</td>
                                                                </tr>
                                                            })}
                                                            </tbody>
                                                        </Table>
                                                    </div>
                                                </div>)
                                        } else {
                                            return <span key={seed + "-" + metric + "-" + index1 + "-" + index2}></span>
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
                            onClick={() => setSimulationTracesOpen(!simulationTracesOpen)}
                            aria-controls="simulationTracesBody"
                            aria-expanded={simulationTracesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                Last {props.job.num_cached_traces} simulation traces
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={simulationTracesOpen}>
                        <div id="simulationTracesBody" className="cardBodyHidden">
                            {props.job.simulation_traces.map((trace, index) => {
                                return (
                                    <div key={trace.id + "-" + index}>
                                        <h5> Trace index: {index} </h5>
                                        <div className="table-responsive">
                                            <Table striped bordered hover>
                                                <thead>
                                                <tr>
                                                    <th>t</th>
                                                    <th>Attacker action</th>
                                                    <th>Defender action</th>
                                                    <th>Belief</th>
                                                    <th>Observation</th>
                                                    <th>Defender reward</th>
                                                    <th>Attacker reward</th>
                                                    <th>State</th>
                                                </tr>
                                                </thead>
                                                <tbody>
                                                {trace.attacker_actions.map((a_action, index) =>
                                                    <tr key={a_action + "-" + index}>
                                                        <td>{index + 1}</td>
                                                        <td>{a_action}</td>
                                                        <td>{trace.defender_actions[index]}</td>
                                                        <td>{trace.beliefs[index]}</td>
                                                        <td>{trace.infrastructure_metrics[index]}</td>
                                                        <td>{trace.defender_rewards[index]}</td>
                                                        <td>{trace.attacker_rewards[index]}</td>
                                                        <td>{trace.states[index]}</td>
                                                    </tr>
                                                )}
                                                </tbody>
                                            </Table>
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                    </Collapse>
                </Card>

                <Logs sessionData={props.sessionData} job={props.job}/>

            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

TrainingJob.propTypes = {};
TrainingJob.defaultProps = {};
export default TrainingJob;
