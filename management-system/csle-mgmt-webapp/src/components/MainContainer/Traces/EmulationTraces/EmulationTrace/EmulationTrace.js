import React, {useState} from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import './EmulationTrace.css';
import Collapse from 'react-bootstrap/Collapse'
import Select from 'react-select'
import convertListToCommaSeparatedString from "../../../../Common/convertListToCommaSeparatedString";

/**
 * Component representing the /emulation-traces/id resource
 */
const EmulationTrace = (props) => {
    const defMachines = props.emulationTrace.initial_defender_observation_state.machines.map((machine, index) => {
        return {
            value: machine,
            label: `IPs: ${machine.ips.join(', ')}`
        }
    })

    const [attackerActionsOpen, setAttackerActionsOpen] = useState(false);
    const [defenderActionsOpen, setDefenderActionsOpen] = useState(false);
    const [attackerObservationsOpen, setAttackerObservationsOpen] = useState(false);
    const [defenderObservationsOpen, setDefenderObservationsOpen] = useState(false);
    const [selectedDefenderMachine, setSelectedDefenderMachine] = useState(defMachines[0]);
    const [defenderMachines, setDefenderMachines] = useState(defMachines);

    const updateSelectedDefenderMachine = (selectedDefMachine) => {
        setSelectedDefenderMachine(selectedDefMachine)
    }

    const getDefenderMachineObs = (defenderObsState) => {
        for (let i = 0; i < defenderObsState.machines.length; i++) {
            if (defenderObsState.machines[i].ips.includes(selectedDefenderMachine.value.ips[0])) {
                return defenderObsState.machines[i]
            }
        }
    }

    const SelectDefenderMachine = (props) => {
        return (
            <div className="inline-block">
                <div className="conditionalDist inline-block">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Machine:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "300px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedDefenderMachine}
                            defaultValue={props.selectedDefenderMachine}
                            options={props.defenderMachines}
                            onChange={updateSelectedDefenderMachine}
                            placeholder="Select machine"
                        />
                    </div>
                </div>
            </div>
        )
    }

    const renderRemoveEmulationTraceTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove emulation trace
        </Tooltip>
    );

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
            if (attacker_machines[i].shell_access) {
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
        return convertListToCommaSeparatedString(ips)
    }

    const getCompromisedNodesIps = (attacker_machines) => {
        var ips = []
        for (let i = 0; i < attacker_machines.length; i++) {
            if (attacker_machines[i].shell_access) {
                for (let j = 0; j < attacker_machines[i].ips.length; j++) {
                    ips.push(attacker_machines[i].ips[j])
                }
            }
        }
        return convertListToCommaSeparatedString(ips)
    }

    const RenderActions = (props) => {
        if (props.sessionData === null || props.sessionData === undefined || !props.sessionData.admin) {
            return (<></>)
        }
        return (
            <h5 className="semiTitle">
                Actions:
                <OverlayTrigger
                    className="removeButton"
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveEmulationTraceTooltip}
                >
                    <Button variant="danger" className="removeButton" size="sm"
                            onClick={() => props.removeEmulationTrace(props.emulationTrace)}>
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            </h5>
        )
    }

    return (<Card key={props.emulationTrace.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.emulationTrace.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.emulationTrace.id},</span> Emulation: {props.emulationTrace.emulation_name}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.emulationTrace.id}>
            <Card.Body>
                <RenderActions sessionData={props.sessionData} removeEmulationTrace={props.removeEmulationTrace}
                               emulationTrace={props.emulationTrace}/>
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setAttackerActionsOpen(!attackerActionsOpen)}
                            aria-controls="attackerActionsBody"
                            aria-expanded={attackerActionsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Attacker actions
                                <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={attackerActionsOpen}>
                        <div id="attackerActionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>t</th>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Commands</th>
                                        <th>Description</th>
                                        <th>Execution time (s)</th>
                                        <th>IPs</th>
                                        <th>Index</th>
                                        <th>Action outcome</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulationTrace.attacker_actions.map((a_action, index) =>
                                        <tr key={a_action.id + "-" + index}>
                                            <td>{index + 1}</td>
                                            <td>{a_action.id}</td>
                                            <td>{a_action.name}</td>
                                            <td>{a_action.cmds}</td>
                                            <td>{a_action.descr}</td>
                                            <td>{a_action.execution_time}</td>
                                            <td>{convertListToCommaSeparatedString(a_action.ips)}</td>
                                            <td>{a_action.index}</td>
                                            <td>{getAttackerActionOutcome(a_action.action_outcome)}</td>
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
                            onClick={() => setDefenderActionsOpen(!defenderActionsOpen)}
                            aria-controls="defenderActionsBody"
                            aria-expanded={defenderActionsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Defender actions
                                <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={defenderActionsOpen}>
                        <div id="defenderActionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>t</th>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Commands</th>
                                        <th>Description</th>
                                        <th>Execution time (s)</th>
                                        <th>IPs</th>
                                        <th>Index</th>
                                        <th>Action outcome</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulationTrace.defender_actions.map((a_action, index) =>
                                        <tr key={a_action.id + "-" + index}>
                                            <td>{index + 1}</td>
                                            <td>{a_action.id}</td>
                                            <td>{a_action.name}</td>
                                            <td>{a_action.cmds}</td>
                                            <td>{a_action.descr}</td>
                                            <td>{a_action.execution_time}</td>
                                            <td>{convertListToCommaSeparatedString(a_action.ips)}</td>
                                            <td>{a_action.index}</td>
                                            <td>{getDefenderActionOutcome(a_action.action_outcome)}</td>
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
                            onClick={() => setAttackerObservationsOpen(!attackerObservationsOpen)}
                            aria-controls="attackerObservationsBody"
                            aria-expanded={attackerObservationsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Attacker observations
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={attackerObservationsOpen}>
                        <div id="attackerObservationsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>t</th>
                                        <th># Found nodes</th>
                                        <th># Catched flags</th>
                                        <th># Compromised nodes</th>
                                        <th>IPs of found nodes</th>
                                        <th>IPs of compromised nodes</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulationTrace.attacker_observation_states.map((obs_state, index) =>
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
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setDefenderObservationsOpen(!defenderObservationsOpen)}
                            aria-controls="defenderActionsBody"
                            aria-expanded={defenderObservationsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Defender observations
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={defenderObservationsOpen}>
                        <div id="defenderActionsBody" className="cardBodyHidden">
                            <h3> Aggregate observations </h3>
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>t</th>
                                        <th># Clients</th>
                                        <th># Failed logins</th>
                                        <th># Logged in users</th>
                                        <th># Successful logins</th>
                                        <th># Open TCP connections</th>
                                        <th># User sessions</th>
                                        <th># Blocks read</th>
                                        <th># Blocks written</th>
                                        <th># CPU utilization %</th>
                                        <th># Memory utilization %</th>
                                        <th># Received MBs</th>
                                        <th># Transmitted MBs</th>
                                        <th># PIDs</th>
                                        <th>Snort Alerts weighted by priority</th>
                                        <th># Snort Severe alerts</th>
                                        <th># Snort Warning alerts</th>
                                        <th>OSSEC Alerts weighted by level</th>
                                        <th># OSSEC Severe alerts</th>
                                        <th># OSSEC Warning alerts</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulationTrace.defender_observation_states.map((obs_state, index) =>
                                        <tr key={index}>
                                            <td>{index + 1}</td>
                                            <td>{obs_state.avg_client_population_metrics.num_clients}</td>
                                            <td>{obs_state.avg_aggregated_host_metrics.num_failed_login_attempts}</td>
                                            <td>{obs_state.avg_aggregated_host_metrics.num_logged_in_users}</td>
                                            <td>{obs_state.avg_aggregated_host_metrics.num_login_events}</td>
                                            <td>{obs_state.avg_aggregated_host_metrics.num_open_connections}</td>
                                            <td>{obs_state.avg_aggregated_host_metrics.num_users}</td>
                                            <td>{obs_state.avg_docker_stats.blk_read}</td>
                                            <td>{obs_state.avg_docker_stats.blk_write}</td>
                                            <td>{obs_state.avg_docker_stats.cpu_percent}</td>
                                            <td>{obs_state.avg_docker_stats.mem_percent}</td>
                                            <td>{obs_state.avg_docker_stats.net_rx}</td>
                                            <td>{obs_state.avg_docker_stats.net_tx}</td>
                                            <td>{obs_state.avg_docker_stats.pids}</td>
                                            <td>{obs_state.avg_snort_ids_alert_counters.alerts_weighted_by_priority}</td>
                                            <td>{obs_state.avg_snort_ids_alert_counters.severe_alerts}</td>
                                            <td>{obs_state.avg_snort_ids_alert_counters.warning_alerts}</td>
                                            <td>{obs_state.avg_ossec_ids_alert_counters.alerts_weighted_by_level}</td>
                                            <td>{obs_state.avg_ossec_ids_alert_counters.severe_alerts}</td>
                                            <td>{obs_state.avg_ossec_ids_alert_counters.warning_alerts}</td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </div>
                            <h3>Machine observations</h3>
                            <SelectDefenderMachine selectedDefenderMachine={selectedDefenderMachine}
                                                   defenderMachines={defenderMachines}
                            />

                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>t</th>
                                        <th># Failed logins</th>
                                        <th># Logged in users</th>
                                        <th># Successful logins</th>
                                        <th># Open TCP connections</th>
                                        <th># User sessions</th>
                                        <th># Block read</th>
                                        <th># Block written</th>
                                        <th># CPU utilization %</th>
                                        <th># Memory utilization %</th>
                                        <th># Received MB</th>
                                        <th># Transmitted MB</th>
                                        <th># PIDs</th>
                                        <th>Snort Alerts weighted by priority</th>
                                        <th># Snort Severe alerts</th>
                                        <th># Snort Warning alerts</th>
                                        <th>OSSEC Alerts weighted by level</th>
                                        <th># OSSEC Severe alerts</th>
                                        <th># OSSEC Warning alerts</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.emulationTrace.defender_observation_states.map((obs_state, index) => {
                                            var machineObs = getDefenderMachineObs(obs_state)
                                            return (<tr key={index}>
                                                <td>{index + 1}</td>
                                                <td>{machineObs.host_metrics.num_failed_login_attempts}</td>
                                                <td>{machineObs.host_metrics.num_logged_in_users}</td>
                                                <td>{machineObs.host_metrics.num_login_events}</td>
                                                <td>{machineObs.host_metrics.num_open_connections}</td>
                                                <td>{machineObs.host_metrics.num_users}</td>
                                                <td>{machineObs.docker_stats.blk_read}</td>
                                                <td>{machineObs.docker_stats.blk_write}</td>
                                                <td>{machineObs.docker_stats.cpu_percent}</td>
                                                <td>{machineObs.docker_stats.mem_percent}</td>
                                                <td>{machineObs.docker_stats.net_rx}</td>
                                                <td>{machineObs.docker_stats.net_tx}</td>
                                                <td>{machineObs.docker_stats.pids}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.alerts_weighted_by_priority}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.severe_alerts}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.warning_alerts}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.alerts_weighted_by_level}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.severe_alerts}</td>
                                                <td>{machineObs.snort_ids_ip_alert_counters.warning_alerts}</td>
                                            </tr>)
                                        }
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

EmulationTrace.propTypes = {};
EmulationTrace.defaultProps = {};
export default EmulationTrace;
