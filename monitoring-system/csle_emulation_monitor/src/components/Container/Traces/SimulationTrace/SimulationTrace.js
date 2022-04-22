import React from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import './SimulationTrace.css';

const SimulationTrace = (props) => {

    const renderRemoveSimulationTraceTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove simulation trace
        </Tooltip>
    );

    return (<Card key={props.simulationTrace.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.simulationTrace.id} className="mgHeader">
                <span className="subnetTitle">ID: {props.simulationTrace.id},</span> Gym env: {props.simulationTrace.simulation_env}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.simulationTrace.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveSimulationTraceTooltip}
                    >
                        <Button variant="outline-dark" className="removeButton"
                                onClick={() => props.removeSimulationTrace(props.simulationTrace)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    Trace
                </h5>
                <Table striped bordered hover className="table-responsive">
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
                    {props.simulationTrace.attacker_actions.map((a_action, index) =>
                        <tr key={a_action + "-" + index}>
                            <td>{index+1}</td>
                            <td>{a_action}</td>
                            <td>{props.simulationTrace.defender_actions[index]}</td>
                            <td>{props.simulationTrace.beliefs[index]}</td>
                            <td>{props.simulationTrace.infrastructure_metrics[index]}</td>
                            <td>{props.simulationTrace.defender_rewards[index]}</td>
                            <td>{props.simulationTrace.attacker_rewards[index]}</td>
                            <td>{props.simulationTrace.states[index]}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

SimulationTrace.propTypes = {};
SimulationTrace.defaultProps = {};
export default SimulationTrace;
