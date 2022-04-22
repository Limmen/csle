import React, {useState} from 'react';
import './Experiment.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import MetricPlot from "./MetricPlot/MetricPlot";
import Collapse from 'react-bootstrap/Collapse'

const Experiment = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [hyperparametersOpen, setHyperparametersOpen] = useState(false);
    const [randomSeedsAndOutputsOpen, setRandomSeedsAndOutputsOpen] = useState(false);
    const [metricTablesOpen, setMetricTablesOpen] = useState(false);
    const [metricPlotsOpen, setMetricPlotsOpen] = useState(false);

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

    const renderRemoveExperimentTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove experiment execution
        </Tooltip>
    );

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
                    Actions:

                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveExperimentTooltip}
                    >
                        <Button variant="outline-dark" className="removeButton"
                                onClick={() => props.removeExperiment(props.experiment)}>
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
                            <h5 className="semiTitle"> General information about the training run </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setHyperparametersOpen(!hyperparametersOpen)}
                            aria-controls="hyperparametersBody"
                            aria-expanded={hyperparametersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Hyperparameters </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={hyperparametersOpen}>
                        <div id="hyperparametersOpen" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setRandomSeedsAndOutputsOpen(!randomSeedsAndOutputsOpen)}
                            aria-controls="randomSeedsAndOutputsBody"
                            aria-expanded={randomSeedsAndOutputsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Random seeds and output directories </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={randomSeedsAndOutputsOpen}>
                        <div id="randomSeedsAndOutputsOpen" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setMetricPlotsOpen(!metricPlotsOpen)}
                            aria-controls="metricPlotsBody"
                            aria-expanded={metricPlotsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Metric plots </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricPlotsOpen}>
                        <div id="metricPlotsBody" className="cardBodyHidden">
                            {props.experiment.result.plot_metrics.map((metric, index2) => {
                                return <MetricPlot key={index2} className="metricPlot" metricName={metric}
                                                   data={props.experiment.result.avg_metrics[metric]}
                                                   stds={props.experiment.result.std_metrics[metric]}/>
                            })}
                            {Object.keys(props.experiment.result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.experiment.result.all_metrics[seed]).map((metric, index2) => {
                                        if(props.experiment.result.all_metrics[seed][metric] !== undefined
                                            && props.experiment.result.all_metrics[seed][metric] !== null &&
                                            props.experiment.result.all_metrics[seed][metric].length > 0 &&
                                            !Array.isArray(props.experiment.result.all_metrics[seed][metric][0])) {
                                            return (
                                                <div className="metricsTable" key={seed + "-" + metric + "-" + index1 + "-" + index2}>
                                                    <h5 className="semiTitle semiTitle2">
                                                        Metric: {metric}, seed: {seed}
                                                    </h5>
                                                    <MetricPlot key={metric + "-" + seed + "-" + index1 + "-" + index2}
                                                                className="metricPlot" metricName={metric}
                                                                data={props.experiment.result.all_metrics[seed][metric]}
                                                                stds={null}/>
                                                </div>)
                                        } else {
                                            return (<span></span>)
                                        }
                                    })
                                }
                            )
                            }
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setMetricTablesOpen(!metricTablesOpen)}
                            aria-controls="metricTablesBody"
                            aria-expanded={metricTablesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Metric tables </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={metricTablesOpen}>
                        <div id="metricTablesBody" className="cardBodyHidden">
                            {Object.keys(props.experiment.result.all_metrics).map((seed, index1) => {
                                    return Object.keys(props.experiment.result.all_metrics[seed]).map((metric, index2) => {
                                        if(props.experiment.result.all_metrics[seed][metric].length > 0) {
                                            return (
                                                <div className="metricsTable" key={seed + "-" + metric + "-" + index1 + "-" + index2}>
                                                    <h5 className="semiTitle semiTitle2">
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
                                        } else {
                                            return (<span></span>)
                                        }
                                    })
                                }
                            )
                            }
                        </div>
                    </Collapse>
                </Card>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Experiment.propTypes = {};
Experiment.defaultProps = {};
export default Experiment;
