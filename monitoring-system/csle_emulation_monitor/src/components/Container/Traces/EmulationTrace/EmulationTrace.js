import React from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import './EmulationTrace.css';

const EmulationTrace = (props) => {
    return (<Card key={props.emulationTrace.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.emulationTrace.id} className="mgHeader">
                <span className="subnetTitle">ID: {props.emulationTrace.id}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.emulationTrace.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information
                </h5>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

EmulationTrace.propTypes = {};

EmulationTrace.defaultProps = {};

export default EmulationTrace;
