import React, {useState, useEffect, useCallback} from 'react';
import Slider from "rc-slider";
import "rc-slider/assets/index.css";
import './Monitoring.css';
import {Dropdown} from "react-bootstrap"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import ContainerMetrics from "./ContainerMetrics/ContainerMetrics";
import AggregateMetrics from "./AggregateMetrics/AggregateMetrics";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

const Monitoring = () => {
    const [runningEnvs, setRunningEnvs] = useState([]);
    const [selectedEnv, setSelectedEnv] = useState(null);
    const [windowLength, setWindowLength] = useState(60);
    const [selectedHost, setSelectedHost] = useState(null);
    const [monitoringData, setMonitoringData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const onSliderChange = (value) => {
        setAnimationDuration(value)
        if (value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const getDockerMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.docker_host_stats[selectedHost]
        } else {
            return null
        }
    }

    const getHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.host_metrics[selectedHost]
        } else {
            return null
        }
    }

    const getIdsMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.ids_metrics
        } else {
            return null
        }
    }

    const getClientMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.client_metrics
        } else {
            return null
        }
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulations and monitoring data from the backend
        </Tooltip>
    );

    const getAggregatedDockerStats = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_docker_stats
        } else {
            return null
        }
    }

    const getAggregatedHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_host_metrics
        } else {
            return null
        }
    }

    const onChangeWindowLength = (event) => {
        event.preventDefault();
        setWindowLength(event.target.value)
    }

    const updateEmulation = (emulation_name) => {
        setSelectedEnv(emulation_name)
    }

    const updateHost = (container_name) => {
        setSelectedHost(container_name)
    }

    const refresh = () => {
        setLoading(true)
        fetchEmulations()
        fetchMonitoringData(windowLength)
    }

    const getSelectedEnvConfig = (emulation_name) => {
        for (let i = 0; i < runningEnvs.length; i++) {
            if (emulation_name === runningEnvs[i].name) {
                return runningEnvs[i]
            }
        }
        return null
    }

    const getSelectedContainerConfig = (emulationConfig, containerName) => {
        if (emulationConfig !== null) {
            for (let i = 0; i < emulationConfig.containers_config.containers.length; i++) {
                var c = emulationConfig.containers_config.containers[i]
                if (containerName === c.full_name_str) {
                    return c
                }
            }
            return null
        }
        return null
    }

    const fetchEmulations = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/envs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                var rEnvs = response.filter(em => em.running)
                setRunningEnvs(rEnvs);
                if (rEnvs.length >= 0) {
                    setSelectedEnv(rEnvs[0].name)
                    var c = rEnvs[0].containers_config.containers[0]
                    setSelectedHost(c.full_name_str)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchEmulations();
    }, []);

    const fetchMonitoringData = useCallback((len) => fetch(
        `http://` + ip + ':7777/monitor/' + selectedEnv + "/" + len,
        {
            method: "GET",
            headers: new Headers({
                Accept: "application/vnd.github.cloak-preview"
            })
        }
    )
        .then(res => res.json())
        .then(response => {
            setMonitoringData(response)
            setLoading(false)
        })
        .catch(error => console.log("error:" + error)), [selectedEnv]);

    useEffect(() => {
        setLoading(true)
        fetchMonitoringData(windowLength)
    }, [fetchMonitoringData]);

    const SelectEmulationDropdownOrSpinner = (props) => {
        if (props.loading || props.selectedEnv === null || props.runningEnvs.length === 0) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Dropdown className="d-inline mx-2 inline-block">
                    <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                        {props.selectedEnv}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {props.runningEnvs.map((env, index) =>
                            <Dropdown.Item key={env.name + "-" + index} onClick={() => updateEmulation(env.name)}>
                                {env.name}
                            </Dropdown.Item>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
            )
        }
    }

    const SelectHostDropdownOrSpinner = (props) => {
        if (props.loading || props.selectedEnv === null || props.selectedHost === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Dropdown className="d-inline mx-2 inline-block">
                    <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                        {props.selectedHost}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {props.selectedEnv.containers_config.containers.map((container, index) =>
                            <Dropdown.Item key={container.full_name_str + "-" + index}
                                           onClick={() => updateHost(container.full_name_str)}>
                                {container.full_name_str}
                            </Dropdown.Item>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
            )
        }
    }

    return (
        <div className="Monitoring container-fluid">
            <div className="row">

                <div className="col-sm-6">
                    <h3 className="text-center inline-block monitoringHeader">
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 250, hide: 400}}
                            overlay={renderRefreshTooltip()}
                        >
                            <Button variant="button" onClick={refresh}>
                                <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>

                        Aggregated Metrics for Emulation:</h3>
                    <SelectEmulationDropdownOrSpinner loading={loading} selectedEnv={selectedEnv}
                                                      runningEnvs={runningEnvs}/>
                </div>

                <div className="col-sm-4">
                    <Form className="d-flex">
                        <Form.Group className="mb-3 d-flex" controlId="timeWindowLen">
                        <Form.Label className="formLabel">
                            Window length (min):
                        </Form.Label>
                        <Form.Control type="text" className="inline-block w-25 windowLengthInput"
                                      value={windowLength} onChange={onChangeWindowLength}
                                      placeholder=""/>
                        </Form.Group>
                    </Form>
                </div>

                <div className="col-sm-2">
                    <span className="evolutionTitle">Evolution speed:</span>
                    <Slider
                        className="defenderPolicyPlotSlider"
                        min={0}
                        max={100}
                        value={animationDuration}
                        onChange={onSliderChange}
                        marks={{
                            1: 1,
                            50: 50,
                            100: 100
                    }}
                    />
                </div>
            </div>
            <hr/>
            <AggregateMetrics loading={loading}
                              animation={animation} animationDuration={animationDuration}
                              animationDurationFactor={animationDurationFactor}
                              clientMetrics={getClientMetrics()} idsMetrics={getIdsMetrics()}
                              aggregatedHostMetrics={getAggregatedHostMetrics()}
                              aggregatedDockerStats={getAggregatedDockerStats()}
            />
            <div className="row hostMetricsDropdownRow">
                <div className="col-sm-6">
                    <h3 className="text-center inline-block monitoringHeader"> Metrics for Container: </h3>
                    <SelectHostDropdownOrSpinner loading={loading} selectedEnv={getSelectedEnvConfig(selectedEnv)}
                                                 selectedHost={selectedHost}/>
                </div>
                <div className="col-sm-6">
                </div>
            </div>
            <hr/>

            <ContainerMetrics loading={loading} hostMetrics={getHostMetrics()}
                              dockerMetrics={getDockerMetrics()}
                              animation={animation} animationDuration={animationDuration}
                              animationDurationFactor={animationDurationFactor}/>
        </div>
    );
}

Monitoring.propTypes = {};
Monitoring.defaultProps = {};
export default Monitoring;
