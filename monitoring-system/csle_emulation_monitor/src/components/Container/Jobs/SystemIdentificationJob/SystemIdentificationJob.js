import React from 'react';
import './SystemIdentificationJob.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';

const SystemIdentificationJob = (props) => {

    return (<Card key={props.job.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.job.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.job.id}, Emulation: {props.job.emulation_env_name}</span>
                Progress: {props.job.progress_percentage}%
                <span className="greenCircle"><svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                                                   version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg></span>
                Collected steps: {props.job.num_collected_steps}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.job.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information about the sysem identification job
                </h5>

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
                        <td>{props.job.id}</td>
                    </tr>
                    <tr>
                        <td>PID</td>
                        <td>{props.job.pid}</td>
                    </tr>
                    </tbody>
                </Table>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

SystemIdentificationJob.propTypes = {};
SystemIdentificationJob.defaultProps = {};
export default SystemIdentificationJob;
