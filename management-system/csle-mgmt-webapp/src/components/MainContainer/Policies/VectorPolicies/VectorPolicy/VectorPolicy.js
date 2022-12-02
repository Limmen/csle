import React, {useState} from 'react';
import './VectorPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'
import getAgentTypeStr from '../../../../Common/getAgentTypeStr'
import getPlayerTypeStr from '../../../../Common/getPlayerTypeStr'

/**
 * Component representing the /policies/id page for a vector policy
 */
const VectorPolicy = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [actionsOpen, setActionsOpen] = useState(false);
    const [policyOpen, setPolicyOpen] = useState(false);

    const renderRemoveVectorPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove Vector policy
        </Tooltip>
    );

    const Actions = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <h5 className="semiTitle">
                    Actions:
                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveVectorPolicy}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeVectorPolicy(props.policy)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>
            )
        } else {
            return (<></>)
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
                <Actions sessionData={props.sessionData} policy={props.policy}
                         removeVectorPolicy={props.removeVectorPolicy}/>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> General Information about the policy
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

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setActionsOpen(!actionsOpen)}
                            aria-controls="actionsBody"
                            aria-expanded={actionsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">
                                Actions
                                <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                            </h5>
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
                                            <td>{action}</td>
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
                            onClick={() => setPolicyOpen(!policyOpen)}
                            aria-controls="policyBody"
                            aria-expanded={policyOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Policy
                                <i className="fa fa-list headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={policyOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Action</th>
                                        <th>Probability</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.policy_vector.map((action_prob, index) => {
                                        return(
                                        <tr key={action_prob + "-" + index}>
                                            <td>{index}</td>
                                            <td>{action_prob}</td>
                                        </tr>)})}
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

VectorPolicy.propTypes = {};
VectorPolicy.defaultProps = {};
export default VectorPolicy;
