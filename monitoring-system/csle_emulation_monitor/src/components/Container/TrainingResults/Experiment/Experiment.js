import React from 'react';
import './Experiment.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Accordion from 'react-bootstrap/Accordion';
import MetricPlot from "./MetricPlot/MetricPlot";

const Experiment = (props) => {

    const getDateStr = (ts) => {
        var date = new Date(ts * 1000);
        var year = date.getFullYear()
        var month = date.getMonth()
        var day = date.getDate()
        var hours = date.getHours();
        var minutes = "0" + date.getMinutes();
        var seconds = "0" + date.getSeconds();
        var formattedTime = year + "-" + month + "-" + day + " " + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
        return formattedTime
    }

    return (<Card key={props.experiment.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.experiment.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.experiment.id}, Simulation: {props.experiment.simulation_name}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.experiment.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information about the training run:
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
                        <td>{props.experiment.id}</td>
                    </tr>
                    <tr>
                        <td>Description</td>
                        <td>{props.experiment.descr}</td>
                    </tr>
                    <tr>
                        <td>Simulation</td>
                        <td>{props.experiment.simulation_name}</td>
                    </tr>
                    <tr>
                        <td>Emulation</td>
                        <td>{props.experiment.emulation_name}</td>
                    </tr>
                    <tr>
                        <td>Timestamp</td>
                        <td>{getDateStr(props.experiment.timestamp)}</td>
                    </tr>
                    <tr>
                        <td>Configuration</td>
                        <td>
                            <Button variant="link"
                                    onClick={() => fileDownload(JSON.stringify(props.experiment), "config.json")}>
                                training_run.json
                            </Button>
                        </td>
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
                    {Object.keys(props.experiment.config.hparams).map((hparamName, index) => {
                        return <tr key={hparamName + "-" + index}>
                            <td>{hparamName}</td>
                            <td>{props.experiment.config.hparams[hparamName].descr}</td>
                            <td>{props.experiment.config.hparams[hparamName].value}</td>
                        </tr>
                    })}
                    </tbody>
                </Table>
                <h5 className="semiTitle">
                    Random seeds and output directories
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Seed</th>
                        <th>Output directory</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.experiment.config.random_seeds.map((seed, index) => {
                        return <tr key={seed + "-" + index}>
                            <td>{seed}</td>
                            <td>{props.experiment.config.output_dir}</td>
                        </tr>
                    })}
                    </tbody>
                </Table>

                {props.experiment.result.plot_metrics.map((metric, index2) => {
                    return <MetricPlot key={index2} className="metricPlot" metricName={metric}
                                       data={props.experiment.result.avg_metrics[metric]}
                                       stds={props.experiment.result.std_metrics[metric]}/>
                })}


                {Object.keys(props.experiment.result.all_metrics).map((seed, index1) => {
                        return Object.keys(props.experiment.result.all_metrics[seed]).map((metric, index2) => {
                            return (
                                <div className="metricsTable" key={seed + "-" + metric + "-" + index1 + "-" + index2}>
                                    <h5 className="semiTitle">
                                        Metric: {metric}, seed: {seed}
                                    </h5>
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Training iteration</th>
                                            <th>{metric}</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {props.experiment.result.all_metrics[seed][metric].map((metricValue, index3) => {
                                            return <tr key={metricValue + "-" + index3}>
                                                <td>{index3}</td>
                                                <td>{metricValue}</td>
                                            </tr>
                                        })}
                                        </tbody>
                                    </Table>
                                </div>)
                        })
                    }
                )
                }
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Experiment.propTypes = {};
Experiment.defaultProps = {};
export default Experiment;
