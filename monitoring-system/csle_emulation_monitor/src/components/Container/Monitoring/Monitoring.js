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
    const [runningEmulations, setRunningEmulations] = useState([]);
    const [selectedEmulation, setSelectedEmulation] = useState(null);
    const [windowLength, setWindowLength] = useState(10);
    const [selectedContainer, setSelectedContainer] = useState(null);
    const [monitoringData, setMonitoringData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const ip = "localhost"
    const [grafanaStatus, setGrafanaStatus] = useState(null);
    const [cAdvisorStatus, setCAdvisorStatus] = useState(null);
    const [prometheusStatus, setPrometheusStatus] = useState(null);
    const [nodeExporterStatus, setNodeExporterStatus] = useState(null);
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
            return monitoringData.docker_host_stats[selectedContainer]
        } else {
            return null
        }
    }

    const getHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.host_metrics[selectedContainer]
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
        setSelectedEmulation(emulation_name)
        for (let i = 0; i < runningEmulations.length; i++) {
            if(runningEmulations[i].name === emulation_name) {
                var c = runningEmulations[i].containers_config.containers[0]
                setSelectedContainer(c.full_name_str)
            }
        }
        setLoading(true)
        fetchMonitoringData(windowLength, emulation_name)
    }

    const updateHost = (container_name) => {
        setSelectedContainer(container_name)
    }

    const refresh = () => {
        setLoading(true)
        fetchGrafanaStatus()
        fetchPrometheusStatus()
        fetchCadvisorStatus()
        fetchNodeExporterStatus()
        fetchEmulations()
    }

    const getSelectedEmulationConfig = (emulation_name) => {
        for (let i = 0; i < runningEmulations.length; i++) {
            if (emulation_name === runningEmulations[i].name) {
                return runningEmulations[i]
            }
        }
        return null
    }

    const startOrStopGrafanaRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/grafana',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setGrafanaStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopcAdvisorRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/cadvisor',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setCAdvisorStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopNodeExporterRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/node_exporter',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setNodeExporterStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopPrometheusRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/prometheus',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setPrometheusStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchEmulations = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulations',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                var rEmulations = response.filter(em => em.running)
                setRunningEmulations(rEmulations);
                if (rEmulations.length >= 0) {
                    if(selectedEmulation === null) {
                        setSelectedEmulation(rEmulations[0].name)
                    }
                    var c = rEmulations[0].containers_config.containers[0]
                    setSelectedContainer(c.full_name_str)
                    fetchMonitoringData(windowLength, rEmulations[0].name)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchMonitoringData = useCallback((len, emulation) => fetch(
        `http://` + ip + ':7777/monitor/' + emulation + "/" + len,
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
            setSelectedEmulation(emulation)
            setLoading(false)
        })
        .catch(error => console.log("error:" + error)), []);


    useEffect(() => {
        setLoading(true)
        fetchEmulations();
    }, []);


    const fetchGrafanaStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/grafana',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setGrafanaStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchGrafanaStatus()
    }, []);


    const fetchCadvisorStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/cadvisor',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setCAdvisorStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchCadvisorStatus()
    }, []);

    const fetchPrometheusStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/prometheus',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setPrometheusStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchPrometheusStatus()
    }, []);

    const fetchNodeExporterStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/nodeexporter',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setNodeExporterStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchNodeExporterStatus()
    }, []);


    const startOrStopGrafana = () => {
        startOrStopGrafanaRequest()
    }

    const startOrStopPrometheus = () => {
        startOrStopPrometheusRequest()
    }

    const startOrStopcAdvisor = () => {
        startOrStopcAdvisorRequest()
    }

    const startOrStopNodeExporter = () => {
        startOrStopNodeExporterRequest()
    }

    const SelectEmulationDropdownOrSpinner = (props) => {
        if (props.loading || props.selectedEmulation === null || props.runningEmulations.length === 0) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Dropdown className="d-inline mx-2 inline-block">
                    <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="md" className="dropdownText">
                        {props.selectedEmulation}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {props.runningEmulations.map((emulation, index) =>
                            <Dropdown.Item key={emulation.name + "-" + index}
                                           onClick={() => updateEmulation(emulation.name)}>
                                {emulation.name}
                            </Dropdown.Item>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
            )
        }
    }

    const SelectHostDropdownOrSpinner = (props) => {
        if (props.loading || props.selectedEmulation === null || props.selectedHost === null) {
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
                        {props.selectedEmulation.containers_config.containers.map((container, index) =>
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


    const MonitoringDataOrEmpty = (props) => {
        if (runningEmulations.length === 0 && !loading) {
            return (
                <div>
                    <h3>No running emulations</h3>
                    <p className="emptyEmulations">
                        Start an emulation to enable monitoring.
                    </p>
                </div>
            )
        } else {
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
                            <SelectEmulationDropdownOrSpinner loading={loading} selectedEmulation={selectedEmulation}
                                                              runningEmulations={runningEmulations}/>
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
                            <SelectHostDropdownOrSpinner loading={loading}
                                                         selectedEmulation={getSelectedEmulationConfig(selectedEmulation)}
                                                         selectedHost={selectedContainer}/>
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
            )
        }
    }

    const renderStartTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start service
        </Tooltip>
    );

    const renderStopTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop service
        </Tooltip>
    );


    const GrafanaLink = (props) => {
        if (props.grafanaStatus == null || props.grafanaStatus.running === false) {
            return (
                    <span className="grafanaStatus">Grafana status: stopped
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 250, hide: 400}}
                        overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopGrafana()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    </span>)
        } else {
            return (
                    <a className="grafanaStatus" href={props.grafanaStatus.url}>Grafana (running)
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 250, hide: 400}}
                            overlay={renderStopTooltip()}>
                            <Button variant="outline-dark" className="startButton"
                                    onClick={() => startOrStopGrafana()}>
                                <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </a>
            )
        }
    }

    const PrometheusLink = (props) => {
        if (props.prometheusStatus == null || props.prometheusStatus.running === false) {
            return (
                <span className="grafanaStatus">Prometheus status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopPrometheus()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.prometheusStatus.url}>Prometheus (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 250, hide: 400}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopPrometheus()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const NodeExporterLink = (props) => {
        if (props.nodeExporterStatus == null || props.nodeExporterStatus.running === false) {
            return (
                <span className="grafanaStatus">Node exporter status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopNodeExporter()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.nodeExporterStatus.url}>Node exporter (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 250, hide: 400}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopNodeExporter()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const CadvisorLink = (props) => {
        if (props.cAdvisorStatus == null || props.cAdvisorStatus.running === false) {
            return (
                <span className="grafanaStatus">cAdvisor status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopcAdvisor()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.cAdvisorStatus.url}>cAdvisor (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 250, hide: 400}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startOrStopcAdvisor()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    return (
        <div className="container-fluid">
            <MonitoringDataOrEmpty/>
            <div className="row">
                <div className="col-sm-12">
                    <GrafanaLink className="grafanaStatus" grafanaStatus={grafanaStatus}/>
                    <PrometheusLink className="grafanaStatus" prometheusStatus={prometheusStatus}/>
                    <NodeExporterLink className="grafanaStatus" nodeExporterStatus={nodeExporterStatus}/>
                    <CadvisorLink className="grafanaStatus" cAdvisorStatus={cAdvisorStatus}/>
                </div>
            </div>
        </div>
    );
}

Monitoring.propTypes = {};
Monitoring.defaultProps = {};
export default Monitoring;
