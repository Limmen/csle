import React, {useState} from 'react';
import './TabularPolicy.css';
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
 * Component representing the /policies/id page for a tabular policy
 */
const TabularPolicy = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [actionsOpen, setActionsOpen] = useState(false);
    const [policyOpen, setPolicyOpen] = useState(false);
    const [valueFunOpen, setValueFunOpen] = useState(false);

    const renderRemoveTabularPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove Tabular policy
        </Tooltip>
    );

    const PolicyRow = (props) => {
        return (
            props.row.map((entry, index) => {
                return (<td key={entry + "-" + index} >{entry}</td>)
            })
        )
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
                        overlay={renderRemoveTabularPolicy}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeTabularPolicy(props.policy)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>
            )
        } else {
            return (<></>)
        }
    }

    const ValueFunctionOrEmpty = (props) => {
        if(props.policy.value_function !== null && props.policy.value_function !== undefined) {
            return (
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setValueFunOpen(!valueFunOpen)}
                            aria-controls="valueFunBody"
                            aria-expanded={valueFunOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Value function </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={valueFunOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>State</th>
                                        <th>Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.value_function.map((row, index) => {
                                        return(
                                            <tr key={row + "-" + index}>
                                                <td>{index}</td>
                                                <td>{row}</td>
                                            </tr>)})}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>
            )
        } else {
            return <></>
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
                <Actions sessionData={props.sessionData} removeTabularPolicy={props.removeTabularPolicy}
                         policy={props.policy}/>

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

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setPolicyOpen(!policyOpen)}
                            aria-controls="policyBody"
                            aria-expanded={policyOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Policy
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={policyOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>  State</th>
                                        {props.policy.lookup_table[0].map((action, index) => {
                                            return (<th key={action + "-" + index}>Action {index}</th>)
                                        })}
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.lookup_table.map((row, index) => {
                                        return(
                                        <tr key={row + "-" + index}>
                                            <td>{index}</td>
                                            <PolicyRow row={row} idx={index}/>
                                        </tr>)})}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <ValueFunctionOrEmpty policy={props.policy}/>

            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

TabularPolicy.propTypes = {};
TabularPolicy.defaultProps = {};
export default TabularPolicy;
