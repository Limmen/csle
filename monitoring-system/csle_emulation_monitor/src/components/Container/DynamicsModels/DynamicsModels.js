import React, {useState, useEffect, useCallback} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './DynamicsModels.css';
import SystemIdentification from './SystemId.png'
import Collapse from 'react-bootstrap/Collapse'
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'

const DynamicsModels = () => {
    const [dynamicsModels, setDynamicsModels] = useState([]);
    const [selectedDynamicsModel, setSelectedDynamicsModel] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaCountsOpen, setDeltaCountsOpen] = useState(false);
    const [initialCountsOpen, setInitialCountsOpen] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [initialProbsOpen, setInitialProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const resetState = () => {
        setDynamicsModels([])
        setSelectedDynamicsModel(null)
        setConditionals([])
        setSelectedConditionals(null)
        setMetrics([])
        setSelectedMetric(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload dynamics models from the backend
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        resetState()
        fetchDynamicsModels()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the dynamics models
        </Tooltip>
    );

    const renderRemoveModelTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove the selected dynamics model.
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Dynamics Models
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>System identification: estimating dynamics models</h4>
                    <p className="modalText">
                        System identification (model learning) is the process of
                        building mathematical models of of dynamical systems from
                        observed input-output signals. In our case, a model refers
                        to a Markov decision process or a stochastic game
                        and model-learning refers to the process of estimating the
                        transition probabilities (dynamics) of the decision process or game.
                        To estimate these probabilities, we use measurements from the emulated infrastructures.
                        After learning the model, we use it to simulate the system.
                    </p>
                    <div className="text-center">
                        <img src={SystemIdentification} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const updateDynamicsModel = (dynModel) => {
        setSelectedDynamicsModel(dynModel)
        const conditionalOptions = Object.keys(dynModel.value.conditionals_counts).map((conditionalName, index) => {
            return {
                value: conditionalName,
                label: conditionalName
            }
        })
        setConditionals(conditionalOptions)
        setSelectedConditionals([conditionalOptions[0]])
        const metricOptions = Object.keys(dynModel.value.conditionals_counts[
            Object.keys(dynModel.value.conditionals_counts)[0]]).map((metricName, index) => {
            return {
                value: metricName,
                label: metricName
            }
        })
        setMetrics(metricOptions)
        setSelectedMetric(metricOptions[0])
    }
    const updateSelectedConditionals = (selected) => {
        setSelectedConditionals(selected)
    }

    const updateMetric = (metricName) => {
        setSelectedMetric(metricName)
    }

    const getFirstTwoConditionals = () => {
        if (selectedConditionals.length >= 2) {
            return [selectedConditionals[0], selectedConditionals[1]]
        } else {
            return selectedConditionals
        }
    }

    const getNumSamples = (model) => {
        var num_samples = 0
        for (let i = 0; i < Object.keys(model.conditionals_counts).length; i++) {
            var metric = Object.keys(model.conditionals_counts[Object.keys(model.conditionals_counts)[i]])[0]
            for (let j = 0; j < Object.keys(model.conditionals_counts[Object.keys(model.conditionals_counts)[i]][metric]).length; j++) {
                var value = Object.keys(model.conditionals_counts[Object.keys(model.conditionals_counts)[i]][metric])[j]
                num_samples = num_samples + model.conditionals_counts[Object.keys(model.conditionals_counts)[i]][metric][value]
            }
        }
        return num_samples
    }

    const fetchDynamicsModels = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/dynamicsmodelsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const modelOptions = response.map((model, index) => {
                    return {
                        value: model,
                        label: model.id + "-" + model.emulation_name
                    }
                })
                setDynamicsModels(modelOptions)
                setLoading(false)
                if (response.length > 0) {
                    setSelectedDynamicsModel(modelOptions[0])
                    const conditionalOptions = Object.keys(response[0].conditionals_counts).map((conditionalName, index) => {
                        return {
                            value: conditionalName,
                            label: conditionalName
                        }
                    })
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = Object.keys(response[0].conditionals_counts[Object.keys(
                        response[0].conditionals_counts)[0]]).map((metricName, index) => {
                        return {
                            value: metricName,
                            label: metricName
                        }
                    })
                    setMetrics(metricOptions)
                    setSelectedMetric(metricOptions[0])
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchDynamicsModels()
    }, [fetchDynamicsModels]);


    const removeModelRequest = useCallback((model_id) => {
        fetch(
            `http://` + ip + ':7777/dynamicsmodelsdata/remove/' + model_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchDynamicsModels()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeModel = (model) => {
        setLoading(true)
        resetState()
        removeModelRequest(model.id)
    }

    const SelectDynamicsModelDropdownOrSpinner = (props) => {
        if (!props.loading && props.dynamicsModels.length === 0) {
            return (
                <span className="emptyText">No models are available</span>
            )
        }
        if (props.loading) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Model:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedDynamicsModel}
                            defaultValue={props.selectedDynamicsModel}
                            options={props.dynamicsModels}
                            onChange={updateDynamicsModel}
                            placeholder="Select model"
                        />
                    </div>
                </div>
            )
        }
    }

    const SelectConditionalDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedConditional === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Conditionals:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedConditionals}
                            isMulti={true}
                            defaultValue={props.selectedConditionals}
                            options={props.conditionals}
                            onChange={updateSelectedConditionals}
                            placeholder="Select conditional distributions"
                        />
                    </div>
                </div>
            )
        }
    }

    const SelectMetricDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.metrics.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block metricLabel">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Metric:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedMetric}
                            defaultValue={props.selectedMetric}
                            options={props.metrics}
                            onChange={updateMetric}
                            placeholder="Select metric"
                        />
                    </div>
                </div>
            )
        }
    }

    const conditionalPairs = () => {
        if (selectedConditionals.length < 2) {
            return []
        } else {
            var conditionalPairs = []
            for (let i = 0; i < selectedConditionals.length; i++) {
                for (let j = 0; j < selectedConditionals.length; j++) {
                    if (selectedConditionals[i] !== selectedConditionals[j]) {
                        conditionalPairs.push({
                            "conditional_1": selectedConditionals[i].label,
                            "conditional_2": selectedConditionals[j].label
                        })
                    }
                }
            }
            return conditionalPairs
        }
    }

    const ModelDescriptionOrSpinner = (props) => {
        if (!props.loading && props.dynamicsModels.length === 0) {
            return (<span> </span>)
        }
        if (props.loading || props.selectedDynamicsModel === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="modelDescription">
                        Model description: {props.selectedDynamicsModel.value.descr}
                        <span className="numSamples">
                        Number of samples: {getNumSamples(props.selectedDynamicsModel.value)}
                    </span>
                    </p>
                </div>
            )
        }
    }

    const ConditionalChartsOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <span></span>
            )
        }
        if (props.loading || props.selectedConditionals === null || props.selectedConditionals.length === 0
            || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <div className="row chartsRow">
                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaCountsOpen(!deltaCountsOpen)}
                                    aria-controls="deltaCountsBody"
                                    aria-expanded={deltaCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaCountsOpen}>
                                <div id="deltaCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedDynamicsModel.value.conditionals_counts}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta counts: " + props.selectedMetric.value}
                                            title2={"Delta counts: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialCountsOpen(!initialCountsOpen)}
                                    aria-controls="initialCountsBody"
                                    aria-expanded={initialCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Initial value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialCountsOpen}>
                                <div id="initialCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedDynamicsModel.value.initial_distributions_counts}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaProbsOpen(!deltaProbsOpen)}
                                    aria-controls="deltaProbsBody"
                                    aria-expanded={deltaProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value probability distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaProbsOpen}>
                                <div id="deltaProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedDynamicsModel.value.conditionals_probs}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta probabilities: " + props.selectedMetric.value}
                                            title2={"Delta probabilities: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialProbsOpen(!initialProbsOpen)}
                                    aria-controls="initialProbsBody"
                                    aria-expanded={initialProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Initial value probability distributions
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialProbsOpen}>
                                <div id="initialProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedDynamicsModel.value.initial_distributions_probs}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDescriptiveStatsOpen(!descriptiveStatsOpen)}
                                    aria-controls="descriptiveStatsBody"
                                    aria-expanded={descriptiveStatsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Descriptive statistics
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={descriptiveStatsOpen}>
                                <div id="descriptiveStatsBody" className="cardBodyHidden">
                                    <div className="table-responsive">
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Attribute</th>
                                                <th> Value</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} mean</td>
                                                        <td>{props.selectedDynamicsModel.value.means[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} standard deviation</td>
                                                        <td>{props.selectedDynamicsModel.value.stds[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} minimum value</td>
                                                        <td>{props.selectedDynamicsModel.value.mins[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} maximum value</td>
                                                        <td>{props.selectedDynamicsModel.value.maxs[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Initial value mean</td>
                                                <td>{props.selectedDynamicsModel.value.initial_means[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial value standard deviation</td>
                                                <td>{props.selectedDynamicsModel.value.initial_stds[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial minimum value</td>
                                                <td>{props.selectedDynamicsModel.value.initial_mins[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial maximum value</td>
                                                <td>{props.selectedDynamicsModel.value.initial_maxs[props.selectedMetric.label]}</td>
                                            </tr>
                                            {conditionalPairs().map((conditionalPair, index) => {
                                                return (
                                                    <tr key={conditionalPair.conditional_1 + "-" +
                                                        conditionalPair.conditional_2 + "-" + index}>
                                                        <td>Kullback-Leibler divergence between conditional
                                                            "{conditionalPair.conditional_1}" and
                                                            "{conditionalPair.conditional_2}"
                                                        </td>
                                                        <td>{props.selectedDynamicsModel.value.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedDynamicsModel.value), "config.json")}>
                                                        data.json
                                                    </Button>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </Table>
                                    </div>
                                </div>
                            </Collapse>
                        </Card>
                    </div>
                </div>
            )
        }
    }


    return (
        <div className="dynamicsModels">

            <h5 className="text-center inline-block emulationsHeader">
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRefreshTooltip}
                >
                    <Button variant="button" onClick={refresh}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)}>
                        <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    className="removeButton"
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveModelTooltip}
                >
                    <Button variant="outline-dark" className="removeButton"
                            onClick={() => removeModel(selectedDynamicsModel.value)}>
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                <SelectDynamicsModelDropdownOrSpinner dynamicsModels={dynamicsModels}
                                                      selectedDynamicsModel={selectedDynamicsModel}
                                                      loading={loading}
                />
                <SelectConditionalDistributionDropdownOrSpinner conditionals={conditionals}
                                                                selectedConditionals={selectedConditionals}
                                                                loading={loading}/>
                <SelectMetricDistributionDropdownOrSpinner metrics={metrics}
                                                           selectedMetric={selectedMetric}
                                                           loading={loading}/>
            </h5>
            <ModelDescriptionOrSpinner dynamicsModels={dynamicsModels}
                                       selectedDynamicsModel={selectedDynamicsModel}
                                       loading={loading}/>

            <ConditionalChartsOrSpinner key={animationDuration}
                                        selectedDynamicsModel={selectedDynamicsModel}
                                        selectedConditionals={selectedConditionals}
                                        animationDurationFactor={animationDurationFactor}
                                        animationDuration={animationDuration}
                                        conditionals={conditionals} dynamicsModels={dynamicsModels}
                                        selectedMetric={selectedMetric}
                                        metrics={metrics}
                                        loading={loading}
            />

        </div>
    );
}
DynamicsModels.propTypes = {};
DynamicsModels.defaultProps = {};
export default DynamicsModels;
