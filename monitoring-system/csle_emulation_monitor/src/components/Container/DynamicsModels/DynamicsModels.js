import React, {useState, useEffect, useCallback, createRef} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './DynamicsModels.css';
import SystemIdentification from './SystemId.png'

const DynamicsModels = () => {
    const [dynamicsModels, setDynamicsModels] = useState([]);
    const [selectedDynamicsModel, setSelectedDynamicsModel] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload dynamics models from the backend
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        fetchDynamicsModels()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the dynamics models
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
        const conditionalOptions = Object.keys(dynModel.value.conditionals).map((conditionalName, index) => {
            return {
                value: conditionalName,
                label: conditionalName
            }
        })
        setConditionals(conditionalOptions)
        setSelectedConditionals([conditionalOptions[0]])
        const metricOptions = Object.keys(dynModel.value.conditionals[Object.keys(dynModel.value.conditionals)[0]]).map((metricName, index) => {
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
        if(selectedConditionals.length>=2) {
            return [selectedConditionals[0], selectedConditionals[1]]
        } else {
            return selectedConditionals
        }
    }

    const fetchDynamicsModels = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/dynamicsmodels',
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
                    const conditionalOptions = Object.keys(response[0].conditionals).map((conditionalName, index) => {
                        return {
                            value: conditionalName,
                            label: conditionalName
                        }
                    })
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = Object.keys(response[0].conditionals[Object.keys(response[0].conditionals)[0]]).map((metricName, index) => {
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
    }, []);

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
    // <Dropdown className="d-inline mx-2 inline-block">
    //     <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
    //         {props.selectedConditionals}
    //     </Dropdown.Toggle>
    //     <Dropdown.Menu>
    //         {props.conditionals.map((conditional, index) =>
    //             <Dropdown.Item className="dropdownText"
    //                            key={conditional}
    //                            onClick={() => updateConditional(conditional)}>
    //                 {conditional}
    //            </Dropdown.Item>*/}
    //        )}*/
    //    </Dropdown.Menu>*/}
    // </Dropdown>

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
                <p className="modelDescription">
                    Model description: {props.selectedDynamicsModel.value.descr}
                </p>
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
                        <div className="col-sm-12">
                            <ConditionalHistogramDistribution
                                data={props.selectedDynamicsModel.value.conditionals}
                                selectedConditionals={getFirstTwoConditionals()}
                                selectedMetric={props.selectedMetric}
                                title1={"Histogram of observed " + props.selectedMetric.value + " counts"}
                                title2={"Scatter plot of observed " + props.selectedMetric.value + " counts"}
                                animationDuration={props.animationDuration}
                                animationDurationFactor={props.animationDurationFactor}
                            />
                        </div>
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
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                <SelectDynamicsModelDropdownOrSpinner dynamicsModels={dynamicsModels}
                                                      selectedDynamicsModel={selectedDynamicsModel}/>
                <SelectConditionalDistributionDropdownOrSpinner conditionals={conditionals}
                                                                selectedConditionals={selectedConditionals}/>
                <SelectMetricDistributionDropdownOrSpinner metrics={metrics}
                                                           selectedMetric={selectedMetric}/>
            </h5>
            <ModelDescriptionOrSpinner dynamicsModels={dynamicsModels}
                                       selectedDynamicsModel={selectedDynamicsModel}/>

            <ConditionalChartsOrSpinner key={animationDuration}
                                        selectedDynamicsModel={selectedDynamicsModel}
                                        selectedConditionals={selectedConditionals}
                                        animationDurationFactor={animationDurationFactor}
                                        animationDuration={animationDuration}
                                        conditionals={conditionals} dynamicsModels={dynamicsModels}
                                        selectedMetric={selectedMetric}
                                        metrics={metrics}
            />

        </div>
    );
}
DynamicsModels.propTypes = {};
DynamicsModels.defaultProps = {};
export default DynamicsModels;
