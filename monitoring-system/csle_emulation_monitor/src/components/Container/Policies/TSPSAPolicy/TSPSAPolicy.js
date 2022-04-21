import React from 'react';
import './TSPSAPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

const TSPSAPolicy = (props) => {

    const renderRemoveTSPSAPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove T-SPSA policy
        </Tooltip>
    );

    return (<Card key={props.policy.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.policy.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.policy.id}, Simulation: {props.policy.simulation_name}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.policy.id}>
            <Card.Body>
                <h5 className="semiTitle">
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
                    General Information about the policy:
                </h5>
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
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

TSPSAPolicy.propTypes = {};
TSPSAPolicy.defaultProps = {};
export default TSPSAPolicy;
