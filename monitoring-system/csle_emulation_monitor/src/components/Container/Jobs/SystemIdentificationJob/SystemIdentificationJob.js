import React, {useState} from 'react';
import './SystemIdentificationJob.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'

const SystemIdentificationJob = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [attackerActionSequenceOpen, setAttackerActionSequenceOpen] = useState(false);
    const [defenderActionSequenceOpen, setDefenderActionSequenceOpen] = useState(false);
    const [tracesOpen, setTracesOpen] = useState(false);

    const renderRemoveSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove system identification job
        </Tooltip>);

    const renderStopSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop system identification job
        </Tooltip>);

    const renderStartSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start system identification job
        </Tooltip>);

    const getStatusText = () => {
        if (props.job.running) {
            return ("Running")
        } else {
            return ("Stopped")
        }
    }

    const getGreenOrRedCircle = () => {
        if (props.job.running) {
            return (<circle r="15" cx="15" cy="15" fill="green"></circle>)
        } else {
            return (<circle r="15" cx="15" cy="15" fill="red"></circle>)
        }
    }

    const getIpString = (ips) => {
        var ipsStr = ""
        for (let i = 0; i < ips.length; i++) {
            ipsStr = ipsStr + ips[i] + ","
        }
        return ipsStr
    }

    const getMaxSteps = () => {
        return (props.job.attacker_sequence.length)*props.job.repeat_times
    }

    const getAttackerActionOutcome = (actionOutcomeId) => {
        if (actionOutcomeId === 0) {
            return "Shell access"
        }
        if (actionOutcomeId === 1) {
            return "Information gathering"
        }
        if (actionOutcomeId === 2) {
            return "Login"
        }
        if (actionOutcomeId === 3) {
            return "Flag"
        }
        if (actionOutcomeId === 4) {
            return "Pivoting"
        }
        if (actionOutcomeId === 5) {
            return "Privilege escalation root"
        }
        if (actionOutcomeId === 6) {
            return "Game end"
        }
        if (actionOutcomeId === 7) {
            return "Continue"
        }
        return ""
    }

    const getDefenderActionOutcome = (actionOutcomeId) => {
        if (actionOutcomeId === 0) {
            return "Game end"
        }
        if (actionOutcomeId === 1) {
            return "Continue"
        }
        if (actionOutcomeId === 2) {
            return "State update"
        }
        if (actionOutcomeId === 3) {
            return "Add defensive mechanism"
        }
        return ""
    }

    const getNumCompromisedMachines = (attacker_machines) => {
        var numCompromised = 0
        for (let i = 0; i < attacker_machines.length; i++) {
            if(attacker_machines[i].shell_access) {
                numCompromised = numCompromised + 1
            }
        }
        return numCompromised
    }

    const getFoundNodesIps = (attacker_machines) => {
        var ips = []
        for (let i = 0; i < attacker_machines.length; i++) {
            for (let j = 0; j < attacker_machines[i].ips.length; j++) {
                ips.push(attacker_machines[i].ips[j])
            }
        }
        return getIpString(ips)
    }

    const getCompromisedNodesIps = (attacker_machines) => {
        var ips = []
        for (let i = 0; i < attacker_machines.length; i++) {
            if(attacker_machines[i].shell_access) {
                for (let j = 0; j < attacker_machines[i].ips.length; j++) {
                    ips.push(attacker_machines[i].ips[j])
                }
            }
        }
        return getIpString(ips)
    }

    const startOrStopButton = () => {
        if (props.job.running) {
            return (<OverlayTrigger
                placement="top"
                delay={{show: 0, hide: 0}}
                overlay={renderStopSystemIdentificationJobTooltip}
            >
                <Button variant="outline-dark" className="startButton"
                        onClick={() => props.stopSystemIdentificationJob(props.job)}>
                    <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>)
        } else {
            return (<OverlayTrigger
                placement="top"
                delay={{show: 0, hide: 0}}
                overlay={renderStartSystemIdentificationJobTooltip}
            >
                <Button variant="outline-dark" className="startButton"
                        onClick={() => props.startSystemIdentificationJob(props.job)}>
                    <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>)
        }
    }

    return (<Card key={props.job.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.job.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.job.id}, Emulation: {props.job.emulation_env_name}</span>
                Progress: {props.job.progress_percentage}%
                Status: {getStatusText()}
                <span className="greenCircle">

                    <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                         version="1.1">
                    {getGreenOrRedCircle()}
                </svg></span>
                Collected steps: {props.job.num_collected_steps}/{getMaxSteps()}
                <span className="seqCompleted">
                    Sequences completed: {props.job.num_sequences_completed}/{props.job.repeat_times}</span>
                <span className="seqCompleted">
                    Steps per sequence: {props.job.attacker_sequence.length}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.job.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    Actions:
                    {startOrStopButton()}
                    <OverlayTrigger
                        className="removeButton"
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveSystemIdentificationJobTooltip}
                    >
                        <Button variant="outline-dark" className="removeButton"
                                onClick={() => props.removeSystemIdentificationJob(props.job)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> General Information about the system identification job</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
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
                                    <td>PID</td>
                                    <td>{props.job.pid}</td>
                                </tr>
                                <tr>
                                    <td>Emulation</td>
                                    <td>{props.job.emulation_env_name}</td>
                                </tr>
                                <tr>
                                    <td>Repeat times</td>
                                    <td>{props.job.repeat_times}</td>
                                </tr>
                                <tr>
                                    <td>Description</td>
                                    <td>{props.job.descr}</td>
                                </tr>
                                <tr>
                                    <td>Sequences completed</td>
                                    <td>{props.job.num_sequences_completed}/{props.job.repeat_times}</td>
                                </tr>
                                <tr>
                                    <td>Steps collected</td>
                                    <td>{props.job.num_collected_steps}/{getMaxSteps()}</td>
                                </tr>
                                <tr>
                                    <td>Dynamics model ID</td>
                                    <td>{props.job.emulation_statistic_id}</td>
                                </tr>
                                </tbody>
                            </Table>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setAttackerActionSequenceOpen(!attackerActionSequenceOpen)}
                            aria-controls="attackerActionSequenceBody"
                            aria-expanded={attackerActionSequenceOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">Attacker action sequence</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={attackerActionSequenceOpen}>
                        <div id="attackerActionSequenceBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>t</th>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Commands</th>
                                    <th>Description</th>
                                    <th>Execution time</th>
                                    <th>IPs</th>
                                    <th>Index</th>
                                    <th>Action outcome</th>
                                </tr>
                                </thead>
                                <tbody>
                                {props.job.attacker_sequence.map((a_action, index) =>
                                    <tr key={a_action.id + "-" + index}>
                                        <td>{index + 1}</td>
                                        <td>{a_action.id}</td>
                                        <td>{a_action.name}</td>
                                        <td>{a_action.cmds}</td>
                                        <td>{a_action.descr}</td>
                                        <td>{a_action.execution_time}</td>
                                        <td>{getIpString(a_action.ips)}</td>
                                        <td>{a_action.index}</td>
                                        <td>{getAttackerActionOutcome(a_action.action_outcome)}</td>
                                    </tr>)}
                                </tbody>
                            </Table>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setDefenderActionSequenceOpen(!defenderActionSequenceOpen)}
                            aria-controls="defenderActionSequenceBody"
                            aria-expanded={defenderActionSequenceOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Defender action sequence</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={defenderActionSequenceOpen}>
                        <div id="defenderActionSequenceBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>t</th>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Commands</th>
                                    <th>Description</th>
                                    <th>Execution time</th>
                                    <th>IPs</th>
                                    <th>Index</th>
                                    <th>Action outcome</th>
                                </tr>
                                </thead>
                                <tbody>
                                {props.job.defender_sequence.map((a_action, index) =>
                                    <tr key={a_action.id + "-" + index}>
                                        <td>{index + 1}</td>
                                        <td>{a_action.id}</td>
                                        <td>{a_action.name}</td>
                                        <td>{a_action.cmds}</td>
                                        <td>{a_action.descr}</td>
                                        <td>{a_action.execution_time}</td>
                                        <td>{getIpString(a_action.ips)}</td>
                                        <td>{a_action.index}</td>
                                        <td>{getDefenderActionOutcome(a_action.action_outcome)}</td>
                                    </tr>)}
                                </tbody>
                            </Table>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setTracesOpen(!tracesOpen)}
                            aria-controls="tracesBody"
                            aria-expanded={tracesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Emulation traces </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={tracesOpen}>
                        <div id="tracesBody" className="cardBodyHidden">
                            {props.job.traces.map((trace, index) => {
                                return (
                                    <div key={trace.id + "-" + index}>
                                        <h4 className="semiTitle">
                                            Trace {index}
                                        </h4>
                                        <h5 className="semiTitle">
                                            Attacker observations
                                        </h5>
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>t</th>
                                                <th># Found nodes</th>
                                                <th># Catched flags</th>
                                                <th># Compromised nodes</th>
                                                <th>Found nodes ips</th>
                                                <th>Compromised nodes ips</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {trace.attacker_observation_states.map((obs_state, index) =>
                                                <tr key={index}>
                                                    <td>{index + 1}</td>
                                                    <td>{obs_state.machines.length}</td>
                                                    <td>{obs_state.catched_flags}</td>
                                                    <td>{getNumCompromisedMachines(obs_state.machines)}</td>
                                                    <td>{getFoundNodesIps(obs_state.machines)}</td>
                                                    <td>{getCompromisedNodesIps(obs_state.machines)}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                        <h5 className="semiTitle">
                                            Defender observations
                                        </h5>
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>t</th>
                                                <th># Clients</th>
                                                <th># Failed logins</th>
                                                <th># Logged in users </th>
                                                <th># Successful logins</th>
                                                <th># Open TCP connections </th>
                                                <th># Users</th>
                                                <th># Block read</th>
                                                <th># Block written</th>
                                                <th># CPU utilization %</th>
                                                <th># Memory utilization %</th>
                                                <th># Received MB</th>
                                                <th># Transmitted MB</th>
                                                <th># PIDs</th>
                                                <th>Alerts weighted by priority</th>
                                                <th># Severe alerts</th>
                                                <th># Warning alerts</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {trace.defender_observation_states.map((obs_state, index) =>
                                                <tr key={index}>
                                                    <td>{index+1}</td>
                                                    <td>{obs_state.client_population_metrics.num_clients}</td>
                                                    <td>{obs_state.aggregated_host_metrics.num_failed_login_attempts}</td>
                                                    <td>{obs_state.aggregated_host_metrics.num_logged_in_users}</td>
                                                    <td>{obs_state.aggregated_host_metrics.num_login_events}</td>
                                                    <td>{obs_state.aggregated_host_metrics.num_open_connections}</td>
                                                    <td>{obs_state.aggregated_host_metrics.num_users}</td>
                                                    <td>{obs_state.docker_stats.blk_read}</td>
                                                    <td>{obs_state.docker_stats.blk_write}</td>
                                                    <td>{obs_state.docker_stats.cpu_percent}</td>
                                                    <td>{obs_state.docker_stats.mem_percent}</td>
                                                    <td>{obs_state.docker_stats.net_rx}</td>
                                                    <td>{obs_state.docker_stats.net_tx}</td>
                                                    <td>{obs_state.docker_stats.pids}</td>
                                                    <td>{obs_state.ids_alert_counters.alerts_weighted_by_priority}</td>
                                                    <td>{obs_state.ids_alert_counters.severe_alerts}</td>
                                                    <td>{obs_state.ids_alert_counters.warning_alerts}</td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </Table>
                                    </div>
                                )
                            })}
                        </div>
                    </Collapse>
                </Card>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

SystemIdentificationJob.propTypes = {};
SystemIdentificationJob.defaultProps = {};
export default SystemIdentificationJob;
