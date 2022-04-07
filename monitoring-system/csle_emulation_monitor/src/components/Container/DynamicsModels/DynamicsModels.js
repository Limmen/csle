import React, {useState, useEffect, useCallback, createRef} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import {Dropdown} from "react-bootstrap"
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './DynamicsModels.css';

const DynamicsModels = () => {
    const [dynamicsModels, setDynamicsModels] = useState([]);
    const [selectedDynamicsModel, setSelectedDynamicsModel] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditional, setSelectedConditional] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000

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

    const getSelectedDynamicsModel = (dynamicsModelId) => {
        for (let i = 0; i < dynamicsModels.length; i++) {
            if (dynamicsModels[i].id === parseInt(dynamicsModelId[0])) {
                return dynamicsModels[i]
            }
        }
        return null
    }

    const updateDynamicsModel = (dynamicsModelId) => {
        setSelectedDynamicsModel(dynamicsModelId)
        setConditionals(Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals))
        setSelectedConditional(Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals)[0])
        setMetrics(Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals[Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals)[0]]))
        setSelectedMetric(Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals[Object.keys(getSelectedDynamicsModel(dynamicsModelId).conditionals)[0]])[0])
    }
    const updateConditional = (conditionalName) => {
        setSelectedConditional(conditionalName)
    }

    const updateMetric = (metricName) => {
        setSelectedMetric(metricName)
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
                console.log(response)
                setDynamicsModels(response)
                setLoading(false)
                if (response.length > 0) {
                    setSelectedDynamicsModel(response[0].id + "-" + response[0].emulation_name)
                    setConditionals(Object.keys(response[0].conditionals))
                    setSelectedConditional(Object.keys(response[0].conditionals)[0])
                    setMetrics(Object.keys(response[0].conditionals[Object.keys(response[0].conditionals)[0]]))
                    setSelectedMetric(Object.keys(response[0].conditionals[Object.keys(response[0].conditionals)[0]])[0])
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
                <Dropdown className="d-inline mx-2 inline-block">
                    <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                        {props.selectedDynamicsModel}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {props.dynamicsModels.map((dynamicsModel, index) =>
                            <Dropdown.Item className="dropdownText"
                                           key={dynamicsModel.id + "-" + dynamicsModel.emulation_name}
                                           onClick={() =>
                                               updateDynamicsModel(dynamicsModel.id + "-" +
                                                   dynamicsModel.emulation_name)}>
                                ID: {dynamicsModel.id} Emulation: {dynamicsModel.emulation_name}
                            </Dropdown.Item>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
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
                <div className="conditionalDist">
                    Conditional distributions:
                    <Dropdown className="d-inline mx-2 inline-block">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                            {props.selectedConditional}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            {props.conditionals.map((conditional, index) =>
                                <Dropdown.Item className="dropdownText"
                                               key={conditional}
                                               onClick={() => updateConditional(conditional)}>
                                    {conditional}
                                </Dropdown.Item>
                            )}
                        </Dropdown.Menu>
                    </Dropdown>
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
                <div className="conditionalDist">
                    Metric:
                    <Dropdown className="d-inline mx-2 inline-block">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                            {props.selectedMetric}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            {props.metrics.map((metric, index) =>
                                <Dropdown.Item className="dropdownText" key={metric}
                                               onClick={() => updateMetric(metric)}>
                                    {metric}
                                </Dropdown.Item>
                            )}
                        </Dropdown.Menu>
                    </Dropdown>
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
                    Model description: {getSelectedDynamicsModel(props.selectedDynamicsModel).descr}
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
        if (props.loading || props.selectedConditional === null) {
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
                                stats={getSelectedDynamicsModel(props.selectedDynamicsModel).conditionals[props.selectedConditional][props.selectedMetric]}
                                title={"P(new " + props.selectedMetric + " | " + props.selectedConditional + ")"}
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

            <h3 className="text-center inline-block emulationsHeader">
                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderRefreshTooltip}
                >
                    <Button variant="button" onClick={refresh}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                Dynamics Model:
                <SelectDynamicsModelDropdownOrSpinner dynamicsModels={dynamicsModels}
                                                      selectedDynamicsModel={selectedDynamicsModel}/>
                <SelectConditionalDistributionDropdownOrSpinner conditionals={conditionals}
                                                                selectedConditional={selectedConditional}/>
                <SelectMetricDistributionDropdownOrSpinner metrics={metrics}
                                                           selectedMetric={selectedMetric}/>
            </h3>
            <ModelDescriptionOrSpinner dynamicsModels={dynamicsModels}
                                       selectedDynamicsModel={selectedDynamicsModel}/>
            <ConditionalChartsOrSpinner
                selectedDynamicsModel={selectedDynamicsModel} selectedConditional={selectedConditional}
                animationDurationFactor={animationDurationFactor} animationDuration={animationDuration}
                conditionals={conditionals} dynamicsModels={dynamicsModels} selectedMetric={selectedMetric}
                metrics={metrics}
            />
        </div>
    );
}

DynamicsModels.propTypes = {};
DynamicsModels.defaultProps = {};
export default DynamicsModels;
