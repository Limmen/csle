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
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Property</th>
                        <th> Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>Num hidden layers:</td>
                        <td>{props.policy.policy_kwargs.net_arch.length}</td>
                    </tr>
                    {props.policy.policy_kwargs.net_arch.map((layer, index) => {
                        return (<tr key={layer + "-" + index}>
                            <td>Num neurons for hidden layer: {index}</td>
                            <td>{layer}</td>
                        </tr>)
                    })}
                    </tbody>
                </Table>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

PPOPolicy.propTypes = {};
PPOPolicy.defaultProps = {};
export default PPOPolicy;
