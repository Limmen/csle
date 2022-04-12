import React from 'react';
import './PPOPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';

const PPOPolicy = (props) => {

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
                    General Information about the policy:
                </h5>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

PPOPolicy.propTypes = {};
PPOPolicy.defaultProps = {};
export default PPOPolicy;
