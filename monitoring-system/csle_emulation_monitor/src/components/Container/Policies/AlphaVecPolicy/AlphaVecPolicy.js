import React, {useState} from 'react';
import './AlphaVecPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'

const AlphaVecPolicy = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [actionsOpen, setActionsOpen] = useState(false);
    const [alphaVectorsOpen, setAlphaVectorsOpen] = useState(false);

    const getAgentTypeStr = (agentType) => {
        if(agentType === 0) {
            return "T-SPSA"
        }
        if(agentType === 1) {
            return "PPO"
        }
        if(agentType === 2) {
            return "T-FP"
        }
        if(agentType === 3) {
            return "DQN"
        }
        if(agentType === 4) {
            return "REINFORCE"
        }
        if(agentType === 5) {
            return "NFSP"
        }
        if(agentType === 6) {
            return "RANDOM"
        }
        if(agentType === 7) {
            return "NONE"
        }
        if(agentType === 8) {
            return "VALUE ITERATION"
        }
        if(agentType === 9) {
            return "HSVI"
        }
        if(agentType === 10) {
            return "SONDIK's VALUE ITERATION"
        }
        if(agentType === 11) {
            return "RANDOM SEARCH"
        }
        if(agentType === 12) {
            return "DIFFERENTIAL EVOLUTION"
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
        if(playerType === 3) {
            return "Self Play"
        }
        else {
            return "Unknown"
        }
    }

    const renderRemoveAlphaVecPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove Alpha-vector policy
        </Tooltip>
    );

    const PolicyRow = (props) => {
        return (
            props.row.map((entry, index) => {
                return (<td>{entry}</td>)
            })
        )
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
                        overlay={renderRemoveAlphaVecPolicy}
                    >
                        <Button variant="danger" className="removeButton"
                                onClick={() => props.removeAlphaVecPolicy(props.policy)}>
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
                            onClick={() => setAlphaVectorsOpen(!alphaVectorsOpen)}
                            aria-controls="alphaVectorsBody"
                            aria-expanded={alphaVectorsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Alpha Vectors </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={alphaVectorsOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Vector ID</th>
                                        <th>Vector Elements</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.alpha_vectors.map((vec, index) => {
                                        return <tr key={vec + "-" + index}>
                                            <td>{index}</td>
                                            <td>{vec}</td>
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

AlphaVecPolicy.propTypes = {};
AlphaVecPolicy.defaultProps = {};
export default AlphaVecPolicy;
