import React, {useState} from 'react';
import './TSPSAPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'

const TSPSAPolicy = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [thresholdsOpen, setThresholdsOpen] = useState(false);
    const [actionsOpen, setActionsOpen] = useState(false);
    const [hParamsOpen, setHParamsOpen] = useState(false);

    const renderRemoveTSPSAPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove T-SPSA policy
        </Tooltip>
    );

    const getAgentTypeStr = (agentType) => {
        if(agentType === 0) {
            return "T-SPSA"
        }
        if(agentType === 1) {
            return "PPO"
        }
        else {
            return "Unknown"
        }
    }

    const getPlayerTypeStr = (playerType) => {
        if(playerType === 1) {
            return "Defender"
        }
        if(playerType === 2) {
            return "Attacker"
        }
        else {
            return "Unknown"
        }
    }

    return (<Card key={props.policy.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.policy.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.policy.id}, Simulation: {props.policy.simulation_name},
                    Average reward: {props.policy.avg_R}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.policy.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    Actions:
                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveTSPSAPolicy}
                    >
                        <Button variant="outline-dark" className="removeButton"
                                onClick={() => props.removeTSPSAPolicy(props.policy)}>
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
                            <h5 className="semiTitle"> General Information about the policy </h5>
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
                                        <td>{props.policy.id}</td>
                                    </tr>
                                    <tr>
                                        <td>Simulation name</td>
                                        <td>{props.policy.simulation_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Average reward</td>
                                        <td>{props.policy.avg_R}</td>
                                    </tr>
                                    <tr>
                                        <td>L</td>
                                        <td>{props.policy.L}</td>
                                    </tr>
                                    <tr>
                                        <td>Agent type</td>
                                        <td>{getAgentTypeStr(props.policy.agent_type)}</td>
                                    </tr>
                                    <tr>
                                        <td>Player type</td>
                                        <td>{getPlayerTypeStr(props.policy.player_type)}</td>
                                    </tr>
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setThresholdsOpen(!thresholdsOpen)}
                            aria-controls="thresholdsBody"
                            aria-expanded={thresholdsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Thresholds </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={thresholdsOpen}>
                        <div id="thresholdsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Threshold</th>
                                        <th> Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.thresholds.map((threshold, index) => {
                                        return <tr key={threshold + "-" + index}>
                                            <td>{index}</td>
                                            <td>{threshold}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setActionsOpen(!actionsOpen)}
                            aria-controls="actionsBody"
                            aria-expanded={actionsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Actions </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={actionsOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Action ID</th>
                                        <th> Description</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.actions.map((action, index) => {
                                        return <tr key={action + "-" + index}>
                                            <td>{action.id}</td>
                                            <td>{action.descr}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setHParamsOpen(!hParamsOpen)}
                            aria-controls="hyperparametersBody"
                            aria-expanded={hParamsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Hyperparameters </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={hParamsOpen}>
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
                                    {Object.keys(props.policy.experiment_config.hparams).map((hparamName, index) => {
                                        return <tr key={hparamName + "-" + index}>
                                            <td>{hparamName}</td>
                                            <td>{props.policy.experiment_config.hparams[hparamName].descr}</td>
                                            <td>{props.policy.experiment_config.hparams[hparamName].value}</td>
                                        </tr>
                                    })}
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

TSPSAPolicy.propTypes = {};
TSPSAPolicy.defaultProps = {};
export default TSPSAPolicy;
