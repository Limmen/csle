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
import {useDebouncedCallback} from 'use-debounce';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';

const SystemModels = () => {
    const [systemModelsIds, setSystemModelsIds] = useState([]);
    const [filteredSystemModelsIds, setFilteredSystemModelsIds] = useState([]);
    const [selectedSystemModel, setSelectedSystemModel] = useState(null);
    const [selectedSystemModelId, setSelectedSystemModelId] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedSystemModel, setLoadingSelectedSystemModel] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(0);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);
    const [searchString, setSearchString] = useState("");

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const resetState = () => {
        setSystemModelsIds([])
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
        fetchSystemModelsIds()
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

    const updateSystemModelId = (systemModelId) => {
        setSelectedSystemModelId(systemModelId)
        fetchModel(systemModelId)
        setLoadingSelectedSystemModel(true)
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
                if (conditionalOptions[i].label === selectedConds[j].label) {
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

    const fetchSystemModelsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/system-models?ids=true',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const modelIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation + ", statistic_id: " + id_obj.statistic_id
                    }
                })
                setSystemModelsIds(modelIds)
                setFilteredSystemModelsIds(modelIds)
                setLoading(false)
                if (modelIds.length > 0) {
                    setSelectedSystemModelId(modelIds[0])
                    fetchModel(modelIds[0])
                    setLoadingSelectedSystemModel(true)
                } else {
                    setLoadingSelectedSystemModel(false)
                    setSelectedSystemModel(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchSystemModelsIds()
    }, [fetchSystemModelsIds]);

    const fetchModel = useCallback((model_id) => {
        fetch(
            `http://` + ip + ':7777/system-models/' + model_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedSystemModel(response)
                setLoadingSelectedSystemModel(false)
                if (response !== null && response !== undefined && !(Object.keys(response).length === 0)) {
                    var conditionalOptions = []
                    for (let i = 0; i < response.conditional_metric_distributions.length; i++) {
                        for (let j = 0; j < response.conditional_metric_distributions[i].length; j++) {
                            conditionalOptions.push(
                                {
                                    value: response.conditional_metric_distributions[i][j],
                                    label: response.conditional_metric_distributions[i][j].conditional_name
                                }
                            )
                        }
                    }
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = getMetricForSelectedConditional(conditionalOptions, [conditionalOptions[0]]).map((metricName, index) => {
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

    const removeModelRequest = useCallback((model_id) => {
        fetch(
            `http://` + ip + ':7777/system-models/' + model_id,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSystemModelsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeModel = (model) => {
        setLoading(true)
        resetState()
        removeModelRequest(model.id)
        setSelectedSystemModel(null)
    }

    const searchFilter = (modelIdObj, searchVal) => {
        return (searchVal === "" || modelIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredMIds = systemModelsIds.filter(model_id_obj => {
            return searchFilter(model_id_obj, searchVal)
        });
        setFilteredSystemModelsIds(filteredMIds)
        setSearchString(searchVal)

        var selectedModelRemoved = false
        if (!loadingSelectedSystemModel && filteredMIds.length > 0) {
            for (let i = 0; i < filteredMIds.length; i++) {
                if (selectedSystemModel !== null && selectedSystemModel !== undefined &&
                    selectedSystemModel.id === filteredMIds[i].value) {
                    selectedModelRemoved = true
                }
            }
            if (!selectedModelRemoved) {
                setSelectedSystemModelId(filteredMIds[0])
                fetchModel(filteredMIds[0])
                setLoadingSelectedSystemModel(true)
            }
        } else {
            setSelectedSystemModel(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const SelectedSystemModelView = (props) => {
        if (props.loadingSelectedSystemModel || props.selectedSystemModel === null || props.selectedSystemModel === undefined) {
            if (props.loadingSelectedSystemModel) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching system model... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <SelectConditionalDistributionDropdownOrSpinner conditionals={props.conditionals}
                                                                    selectedConditionals={props.selectedConditionals}
                                                                    loading={props.loadingSelectedSystemModel}/>
                    <SelectMetricDistributionDropdownOrSpinner metrics={props.metrics}
                                                               selectedMetric={props.selectedMetric}
                                                               loading={props.loadingSelectedSystemModel}/>

                    <ModelDescriptionOrSpinner selectedSystemModel={props.selectedSystemModel}
                                               loading={props.loadingSelectedSystemModel}/>

                    <ConditionalChartsOrSpinner key={props.animationDuration}
                                                selectedSystemModel={props.selectedSystemModel}
                                                selectedConditionals={props.selectedConditionals}
                                                animationDurationFactor={props.animationDurationFactor}
                                                animationDuration={props.animationDuration}
                                                conditionals={props.conditionals}
                                                selectedMetric={props.selectedMetric}
                                                metrics={props.metrics}
                                                loading={props.loadingSelectedSystemModel}
                    />
                </div>
            )
        }
    }

    const SelectSystemModelDropdownOrSpinner = (props) => {
        if (!props.loading && props.systemModelsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No models are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching system models... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
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
                                onClick={() => removeModel(selectedSystemModel)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Model:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSystemModelId}
                                defaultValue={props.selectedSystemModelId}
                                options={props.systemModelsIds}
                                onChange={updateSystemModelId}
                                placeholder="Select model"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    const ModelDescriptionOrSpinner = (props) => {
        if (props.loading || props.selectedSystemModel === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="statisticDescription">
                        Model description: {props.selectedSystemModel.descr}
                        <span className="numSamples">
                            Statistic id: {props.selectedSystemModel.emulation_statistic_id}
                    </span>
                        <span className="numSamples">
                            Emulation: {props.selectedSystemModel.emulation_env_name}
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
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Conditionals:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "800px"}}>
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
                    </h4>
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
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Metric:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedMetric}
                                defaultValue={props.selectedMetric}
                                options={props.metrics}
                                onChange={updateMetric}
                                placeholder="Select metric"
                            />
                        </div>
                    </h4>
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
                                            data={props.selectedSystemModel}
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
                                                        <td>Conditional: {conditional.label}, num mixture components
                                                        </td>
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
                                                            <td>Conditional: {conditional.label}, mixture
                                                                component: {index}, covariance
                                                            </td>
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
                                                        <td>{props.selectedSystemModel.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedSystemModel), "data.json")}>
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
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectSystemModelDropdownOrSpinner systemModelsIds={filteredSystemModelsIds}
                                                            selectedSystemModelId={selectedSystemModelId}
                                                            loading={loading}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <SelectedSystemModelView loadingSelectedSystemModel={loadingSelectedSystemModel}
                                     selectedSystemModel={selectedSystemModel}
                                     conditionals={conditionals}
                                     selectedConditionals={selectedConditionals}
                                     metrics={metrics}
                                     selectedMetric={selectedMetric}
                                     animationDuration={animationDuration}
                                     animationDurationFactor={animationDurationFactor}

            />
        </div>
    );
}

SystemModels.propTypes = {};
SystemModels.defaultProps = {};
export default SystemModels;
