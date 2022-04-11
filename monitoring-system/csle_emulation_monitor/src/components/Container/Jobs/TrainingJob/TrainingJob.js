import React from 'react';
import './TrainingJob.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';

const TrainingJob = (props) => {

    return (<Card key={props.job.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.job.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.job.id}, Simulation: {props.job.simulation_env_name}</span>
                Progress: {props.job.progress_percentage}%
                <span className="greenCircle"><svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                           version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg></span>
                 Average reward: {props.job.average_r}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.job.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information about the training job
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
                    <tr>
                        <td>Title</td>
                        <td>{props.job.experiment_config.title}</td>
                    </tr>
                    <tr>
                        <td>Random seeds</td>
                        <td>{props.job.experiment_config.random_seeds}</td>
                    </tr>
                    <tr>
                        <td>Output directory</td>
                        <td>{props.job.experiment_config.output_dir}</td>
                    </tr>
                    <tr>
                        <td>Log frequency</td>
                        <td>{props.job.experiment_config.log_every}</td>
                    </tr>
                    </tbody>
                </Table>
                <h5 className="semiTitle">
                    Hyperparameters:
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    {Object.keys(props.job.experiment_config.hparams).map((hparamName, index) => {
                        return <tr key={hparamName + "-" + index}>
                            <td>{hparamName}</td>
                            <td>{props.job.experiment_config.hparams[hparamName].descr}</td>
                            <td>{props.job.experiment_config.hparams[hparamName].value}</td>
                        </tr>
                    })}
                    </tbody>
                </Table>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

TrainingJob.propTypes = {};
TrainingJob.defaultProps = {};
export default TrainingJob;
