import React, {useState, useEffect, useCallback} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './SystemModels.css';
import SystemIdentification from './SystemId.png'
import Collapse from 'react-bootstrap/Collapse'
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'

const SystemModels = () => {
    const [systemModels, setSystemModels] = useState([]);
    const [selectedSystemModel, setSelectedSystemModel] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(0);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const resetState = () => {
        setSystemModels([])
        setSelectedSystemModel(null)
        setConditionals([])
        setSelectedConditionals(null)
        setMetrics([])
        setSelectedMetric(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload system models from the backend
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        resetState()
        fetchSystemModels()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the system models
        </Tooltip>
    );

    const renderRemoveModelTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove the selected system model.
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
                        Emulation statistics
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>System identification: estimating system models</h4>
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

    const updateSystemModel = (dynModel) => {
        setSelectedSystemModel(dynModel)
    }
    const updateSelectedConditionals = (selected) => {
        setSelectedConditionals(selected)
    }

    const updateMetric = (metricName) => {
        setSelectedMetric(metricName)
    }

    const getMetricForSelectedConditional = (conditionalOptions, selectedConds) => {
        var metrics = []
        for (let i = 0; i < conditionalOptions.length; i++) {
            var match = false
            for (let j = 0; j < selectedConds.length; j++) {
                if(conditionalOptions[i].label === selectedConds[j].label) {
                    match = true
                }
            }
            if (match) {
                metrics.push(conditionalOptions[i].value.metric_name)
            }
        }
        const uniqueMetrics = [...new Set(metrics)];
        return uniqueMetrics
    }

    const getFirstTwoConditionals = () => {
        if (selectedConditionals.length >= 2) {
            return [selectedConditionals[0], selectedConditionals[1]]
        } else {
            return selectedConditionals
        }
    }

    const fetchSystemModels = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemmodelsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                console.log(response)
                const modelOptions = response.map((model, index) => {
                    return {
                        value: model,
                        label: model.id + "-" + model.emulation_env_name
                    }
                })
                setSystemModels(modelOptions)
                setLoading(false)
                if (response.length > 0) {
                    setSelectedSystemModel(modelOptions[0])
                    var conditionalOptions = []
                    for (let i = 0; i < modelOptions[0].value.conditional_metric_distributions.length; i++) {
                        for (let j = 0; j < modelOptions[0].value.conditional_metric_distributions[i].length; j++) {
                            conditionalOptions.push(
                                {
                                    value: modelOptions[0].value.conditional_metric_distributions[i][j],
                                    label: modelOptions[0].value.conditional_metric_distributions[i][j].conditional_name
                                }
                            )
                        }
                    }
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = getMetricForSelectedConditional(conditionalOptions,[conditionalOptions[0]]).map((metricName, index) => {
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
        fetchSystemModels()
    }, [fetchSystemModels]);


    const removeModelRequest = useCallback((model_id) => {
        fetch(
            `http://` + ip + ':7777/systemmodelsdata/remove/' + model_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSystemModels()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeModel = (model) => {
        setLoading(true)
        resetState()
        removeModelRequest(model.id)
    }

    const SelectSystemModelDropdownOrSpinner = (props) => {
        if (!props.loading && props.systemModels.length === 0) {
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
                <div className="inline-block">
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
                        <Button variant="danger" className="removeButton"
                                onClick={() => removeModel(selectedSystemModel.value)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Model:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "400px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSystemModel}
                                defaultValue={props.selectedSystemModel}
                                options={props.systemModels}
                                onChange={updateSystemModel}
                                placeholder="Select model"
                            />
                        </div>
                    </div>

                    <SelectConditionalDistributionDropdownOrSpinner conditionals={conditionals}
                                                                    selectedConditionals={selectedConditionals}
                                                                    loading={loading}/>
                    <SelectMetricDistributionDropdownOrSpinner metrics={metrics}
                                                               selectedMetric={selectedMetric}
                                                               loading={loading}/>
                </div>
            )
        }
    }

    const ModelDescriptionOrSpinner = (props) => {
        if (!props.loading && props.systemModels.length === 0) {
            return (<span> </span>)
        }
        if (props.loading || props.selectedSystemModel === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="statisticDescription">
                        Model description: {props.selectedSystemModel.value.descr}
                        <span className="numSamples">
                            Statistic id: {props.selectedSystemModel.value.emulation_statistic_id}
                    </span>
                        <span className="numSamples">
                            Emulation: {props.selectedSystemModel.value.emulation_env_name}
                    </span>
                    </p>
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


    const ConditionalChartsOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <p className="statisticDescription"></p>
            )
        }
        if (!props.loading && props.selectedConditionals !== null && props.selectedConditionals !== undefined &&
            props.selectedConditionals.length === 0) {
            return (
                <p className="statisticDescription">Select a conditional distribution from the dropdown list.</p>
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
                                    onClick={() => setDeltaProbsOpen(!deltaProbsOpen)}
                                    aria-controls="deltaProbsBody"
                                    aria-expanded={deltaProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Conditional Distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaProbsOpen}>
                                <div id="deltaProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedSystemModel.value}
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
                                                        <td>Conditional: {conditional.label}, num mixture components</td>
                                                        <td>{conditional.value.mixture_weights.length}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>Conditional: {conditional.label}, mixture means</td>
                                                        <td>{conditional.value.mixture_means.join(", ")}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>Conditional: {conditional.label}, mixture weights</td>
                                                        <td>{conditional.value.mixture_weights.join(", ")}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (conditional.value.mixtures_covariance_matrix.map((cov_row, index) => {
                                                    return (
                                                        <tr key={conditional.label + "-" + index}>
                                                            <td>Conditional: {conditional.label}, mixture component: {index}, covariance</td>
                                                            <td>{cov_row.join(", ")}</td>
                                                        </tr>
                                                    )
                                                }))
                                            })}

                                            {conditionalPairs().map((conditionalPair, index) => {
                                                return (
                                                    <tr key={conditionalPair.conditional_1 + "-" +
                                                        conditionalPair.conditional_2 + "-" + index}>
                                                        <td>Kullback-Leibler divergence between conditional
                                                            "{conditionalPair.conditional_1}" and
                                                            "{conditionalPair.conditional_2}"
                                                        </td>
                                                        <td>{props.selectedSystemModel.value.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedSystemModel.value), "data.json")}>
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
        <div className="systemModels">
            <h5 className="text-center inline-block emulationsHeader">
                <SelectSystemModelDropdownOrSpinner systemModels={systemModels}
                                                    selectedSystemModel={selectedSystemModel}
                                                    loading={loading}
                />
            </h5>
            <ModelDescriptionOrSpinner systemModels={systemModels}
                                           selectedSystemModel={selectedSystemModel}
                                           loading={loading}/>

            <ConditionalChartsOrSpinner key={animationDuration}
                                        selectedSystemModel={selectedSystemModel}
                                        selectedConditionals={selectedConditionals}
                                        animationDurationFactor={animationDurationFactor}
                                        animationDuration={animationDuration}
                                        conditionals={conditionals} systemModels={systemModels}
                                        selectedMetric={selectedMetric}
                                        metrics={metrics}
                                        loading={loading}
            />
        </div>
    );
}
SystemModels.propTypes = {};
SystemModels.defaultProps = {};
export default SystemModels;
