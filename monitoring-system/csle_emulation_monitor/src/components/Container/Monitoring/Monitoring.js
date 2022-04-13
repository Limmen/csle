import React, {useState, useEffect, useCallback} from 'react';
import "rc-slider/assets/index.css";
import './Monitoring.css';
import Select from 'react-select'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Modal from 'react-bootstrap/Modal'
import ContainerMetrics from "./ContainerMetrics/ContainerMetrics";
import AggregateMetrics from "./AggregateMetrics/AggregateMetrics";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import DataCollection from './MonitoringSetup.png'

const Monitoring = () => {
    const windowLengthOptions = [
        {
            value: 15,
            label: "15 min"
        },
        {
            value: 30,
            label: "30 min"
        },
        {
            value: 60,
            label: "1h"
        },
        {
            value: 120,
            label: "2h"
        },
        {
            value: 240,
            label: "4h"
        },
        {
            value: 480,
            label: "8h"
        },
        {
            value: 960,
            label: "16h"
        },
        {
            value: 1920,
            label: "32h"
        },
        {
            value: 3840,
            label: "64h"
        },
    ]
    const evolutionSpeedOptions = [
        {
            value: 0,
            label: "No animation"
        },
        {
            value: 1,
            label: "1%"
        },
        {
            value: 25,
            label: "25%"
        },
        {
            value: 50,
            label: "50%"
        },
        {
            value: 75,
            label: "75%"
        },
        {
            value: 100,
            label: "100%"
        }
    ]
    const [runningEmulations, setRunningEmulations] = useState([]);
    const [containerOptions, setContainerOptions] = useState([]);
    const [selectedEmulation, setSelectedEmulation] = useState(null);
    const [windowLength, setWindowLength] = useState(windowLengthOptions[0]);
    const [selectedContainer, setSelectedContainer] = useState(null);
    const [monitoringData, setMonitoringData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(evolutionSpeedOptions[0]);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const ip = "localhost"
    const [grafanaStatus, setGrafanaStatus] = useState(null);
    const [cAdvisorStatus, setCAdvisorStatus] = useState(null);
    const [prometheusStatus, setPrometheusStatus] = useState(null);
    const [nodeExporterStatus, setNodeExporterStatus] = useState(null);
    const [showInfoModal, setShowInfoModal] = useState(false);
    // const ip = "172.31.212.92"

    const animationDurationUpdate = (selectedObj) => {
        setAnimationDuration(selectedObj)
        if (selectedObj.value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const getDockerMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.docker_host_stats[selectedContainer.label]
        } else {
            return null
        }
    }

    const getHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.host_metrics[selectedContainer.label]
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

    const onChangeWindowLength = (windowLenSelection) => {
        if(windowLenSelection.value !== windowLength) {
            setWindowLength(windowLenSelection)
            setLoading(true)
            fetchMonitoringData(windowLength.value, selectedEmulation)
        }
    }

    const updateEmulation = (emulation) => {
        if(selectedEmulation === null || selectedEmulation === undefined ||
            emulation.value.name !== selectedEmulation.value.name) {
            setSelectedEmulation(emulation)
            const containerOptions = emulation.value.containers_config.containers.map((c, index) => {
                return {
                    value: c,
                    label: c.full_name_str
                }
            })
            setContainerOptions(containerOptions)
            setSelectedContainer(containerOptions[0])
            setLoading(true)
            fetchMonitoringData(windowLength.value, emulation)
        }
    }

    const updateHost = (container) => {
        setSelectedContainer(container)
    }

    const refresh = () => {
        setLoading(true)
        fetchGrafanaStatus()
        fetchPrometheusStatus()
        fetchCadvisorStatus()
        fetchNodeExporterStatus()
        fetchEmulations()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the monitoring setup
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
                        Real-time monitoring of emulated infrastructures
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Monitoring setup</h4>
                    <p className="modalText">
                        A simulation is defined as a Markov decision process or stochastic game, which models
                        how a discrete-time dynamical system is evolved and can be controlled.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
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
                const emulationOptions = rEmulations.map((em, index) => {
                    return {
                        value: em,
                        label: em.name
                    }
                })
                setRunningEmulations(emulationOptions)
                if (rEmulations.length >= 0) {
                    if (selectedEmulation === null) {
                        setSelectedEmulation(emulationOptions[0])
                    }
                    const containerOptions = rEmulations[0].containers_config.containers.map((c, index) => {
                        return {
                            value: c,
                            label: c.full_name_str
                        }
                    })
                    setContainerOptions(containerOptions)
                    setSelectedContainer(containerOptions[0])
                    setLoading(false)
                    fetchMonitoringData(windowLength.value, emulationOptions[0])
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchMonitoringData = useCallback((len, emulation) => fetch(
        `http://` + ip + ':7777/monitor/' + emulation.value.name + "/" + len,
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
            // setSelectedEmulation(emulation)
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
    }, [fetchGrafanaStatus]);


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
    }, [fetchCadvisorStatus]);

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
    }, [fetchPrometheusStatus]);

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
    }, [fetchNodeExporterStatus]);


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
                <div className="conditionalDist inline-block selectEmulation">
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedEmulation}
                            defaultValue={props.selectedDynamicsModel}
                            options={props.runningEmulations}
                            onChange={updateEmulation}
                            placeholder="Select a running emulation"
                        />
                    </div>
                    <div className="conditionalDist inline-block windowLengthDropdown">
                        Time-series window length:
                    </div>
                    <div className="conditionalDist inline-block windowLengthDropdown" style={{width: "250px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.windowLength}
                            defaultValue={props.windowLength}
                            options={windowLengthOptions}
                            onChange={onChangeWindowLength}
                            placeholder="Select a window length"
                        />
                    </div>
                    <div className="conditionalDist inline-block windowLengthDropdown">
                        Evolution speed:
                    </div>
                    <div className="conditionalDist inline-block windowLengthDropdown" style={{width: "250px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.animationDuration}
                            defaultValue={props.animationDuration}
                            options={evolutionSpeedOptions}
                            onChange={animationDurationUpdate}
                            placeholder="Set the evolution speed"
                        />
                    </div>
                </div>
            )
        }
    }

    const SelectHostDropdownOrSpinner = (props) => {
        if (props.loading || props.selectedEmulation === null || props.selectedContainer === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block selectEmulation">
                    <div className="conditionalDist inline-block" style={{width: "500px"}}>
                        <Select
                            style={{display: 'inline-block', width: "1000px"}}
                            value={props.selectedContainer}
                            defaultValue={props.selectedContainer}
                            options={props.containerOptions}
                            onChange={updateHost}
                            placeholder="Select a container from the emulation"
                        />
                    </div>
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
                        delay={{show: 0, hide: 0}}
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
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
                    delay={{show: 0, hide: 0}}
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
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="outline-dark" className="startButton btn-sm"
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
            <div className="Monitoring container-fluid">
                <div className="row">

                    <div className="col-sm-12">
                        <h5 className="text-center inline-block monitoringHeader">
                            <OverlayTrigger
                                placement="right"
                                delay={{show: 0, hide: 0}}
                                overlay={renderRefreshTooltip()}
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

                            Aggregated Metrics for Emulation:
                        <SelectEmulationDropdownOrSpinner className="selectEmulation" loading={loading}
                                                          selectedEmulation={selectedEmulation}
                                                          runningEmulations={runningEmulations}
                                                          windowLength={windowLength}
                                                          animationDuration={animationDuration}
                        />

                        </h5>
                    </div>
                </div>
                <hr/>
                <AggregateMetrics key={animationDuration.value}
                    loading={loading}
                    animation={animation} animationDuration={animationDuration.value}
                    animationDurationFactor={animationDurationFactor}
                    clientMetrics={getClientMetrics()} idsMetrics={getIdsMetrics()}
                    aggregatedHostMetrics={getAggregatedHostMetrics()}
                    aggregatedDockerStats={getAggregatedDockerStats()}
                />
                <div className="row hostMetricsDropdownRow">
                    <div className="col-sm-12">
                        <h5 className="text-center inline-block monitoringHeader"> Metrics for Container:
                            <SelectHostDropdownOrSpinner loading={loading}
                                                         selectedEmulation={selectedEmulation}
                                                         selectedContainer={selectedContainer}
                                                         containerOptions={containerOptions}
                            />
                        </h5>
                    </div>
                </div>
                <hr/>

                <ContainerMetrics key={'container' + '-' + animationDuration.value} loading={loading}
                                  hostMetrics={getHostMetrics()}
                                  dockerMetrics={getDockerMetrics()}
                                  animation={animation} animationDuration={animationDuration.value}
                                  animationDurationFactor={animationDurationFactor}/>
            </div>
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
