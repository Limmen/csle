import React, {useState, useEffect, useCallback} from 'react';
import "rc-slider/assets/index.css";
import './Monitoring.css';
import Select from 'react-select'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Modal from 'react-bootstrap/Modal'
import ContainerMetrics from "./ContainerMetrics/ContainerMetrics";
import AggregateMetrics from "./AggregateMetrics/AggregateMetrics";
import OpenFlowSwitchesStats from "./OpenFlowSwitchesStats/OpenFlowSwitchesStats";
import SnortMetrics from "./SnortMetrics/SnortMetrics";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import DataCollection from './MonitoringSetup.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    EMULATION_EXECUTIONS_RESOURCE, EMULATION_QUERY_PARAM, EMULATIONS_RESOURCE, EXECUTIONS_SUBRESOURCE,
    HTTP_PREFIX,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE, MONITOR_SUBRESOURCE,
    TOKEN_QUERY_PARAM, IDS_QUERY_PARAM
} from "../../Common/constants";

/**
 * Component containing various plots for monitoring a running execution of an emulation
 */
const Monitoring = (props) => {
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
    const [emulationExecutionIds, setEmulationExecutionIds] = useState([]);
    const [filteredEmulationExecutionIds, setFilteredEmulationExecutionIds] = useState([]);
    const [emulationExecutionContainerOptions, setEmulationExecutionContainerOptions] = useState([]);
    const [selectedEmulationExecutionId, setSelectedEmulationExecutionId] = useState(null);
    const [selectedEmulationExecution, setSelectedEmulationExecution] = useState(null);
    const [windowLength, setWindowLength] = useState(windowLengthOptions[0]);
    const [selectedContainer, setSelectedContainer] = useState(null);
    const [monitoringData, setMonitoringData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationExecution, setLoadingSelectedEmulationExecution] = useState(true);
    const [loadingMonitoringData, setLoadingMonitoringData] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(evolutionSpeedOptions[0]);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [openFlowSwitchesOptions, setOpenFlowSwitchesOptions] = useState([]);
    const [selectedOpenFlowSwitch, setSelectedOpenFlowSwitch] = useState(null);
    const [snortIdsOptions, setSnortIdsOptions] = useState([]);
    const [selectedSnortIds, setSelectedSnortIds] = useState(null);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData


    const fetchMonitoringData = useCallback((len, execution) => fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}/${execution.emulation_env_config.id}` +
                `/${EXECUTIONS_SUBRESOURCE}/${execution.ip_first_octet}/${MONITOR_SUBRESOURCE}/${len}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setMonitoringData(response)
                setLoadingMonitoringData(false)
                var openFlowSwitchesOptions = []
                openFlowSwitchesOptions = Object.keys(response.openflow_port_avg_metrics_per_switch).map((dpid, index) => {
                    return {
                        value: dpid,
                        label: dpid
                    }
                })
                setOpenFlowSwitchesOptions(openFlowSwitchesOptions)
                if (openFlowSwitchesOptions.length > 0) {
                    setSelectedOpenFlowSwitch(openFlowSwitchesOptions[0])
                }

                var snortIdsOptions = []
                snortIdsOptions = Object.keys(response.snort_alert_metrics_per_ids).map((snort_ids_ip, index) => {
                    return {
                        value: snort_ids_ip,
                        label: snort_ids_ip
                    }
                })
                setSnortIdsOptions(snortIdsOptions)
                if (snortIdsOptions.length > 0) {
                    setSelectedSnortIds(snortIdsOptions[0])
                }
            })
            .catch(error => console.log("error:" + error)),
        [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchSelectedExecution = useCallback((id_obj) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}/${id_obj.value.id}`
                + `?${EMULATION_QUERY_PARAM}=${id_obj.value.emulation}`
                + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedEmulationExecution(response)
                setLoadingSelectedEmulationExecution(false)
                if (response !== null && response !== undefined) {
                    const containerOptions = response.emulation_env_config.containers_config.containers.map(
                        (c, index) => {
                            return {
                                value: c,
                                label: c.full_name_str
                            }
                        })
                    setEmulationExecutionContainerOptions(containerOptions)
                    setSelectedContainer(containerOptions[0])
                    setLoadingMonitoringData(true)
                    fetchMonitoringData(windowLength.value, response)
                }

            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchMonitoringData,
        windowLength.value]);

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

    const getPortStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch != null) {
            return monitoringData.openflow_port_avg_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getAggFlowStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch != null) {
            return monitoringData.agg_openflow_flow_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getFlowStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch !== null) {
            return monitoringData.openflow_flow_avg_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getSnortIdsMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.agg_snort_ids_metrics
        } else {
            return null
        }
    }

    const getSpecificSnortIdsMetrics = () => {
        if (monitoringData !== null && selectedSnortIds !== null) {
            return monitoringData.snort_alert_metrics_per_ids[selectedSnortIds.label]
        } else {
            return null
        }
    }

    const getOSSECHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.ossec_host_alert_counters[selectedContainer.label]
        } else {
            return null
        }
    }

    const getSnortHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.snort_ids_ip_metrics[selectedContainer.label]
        } else {
            return null
        }
    }

    const getAggregatedOSSECHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_ossec_host_alert_counters
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
        if (windowLenSelection.value !== windowLength) {
            setWindowLength(windowLenSelection)
            setLoadingMonitoringData(true)
            fetchMonitoringData(windowLength.value, selectedEmulationExecution)
        }
    }

    const updateEmulationExecutionId = (emulationExecutionId) => {
        setSelectedEmulationExecutionId(emulationExecutionId)
        fetchSelectedExecution(emulationExecutionId)
        setLoadingSelectedEmulationExecution(true)
        setMonitoringData(null)
    }

    const updateHost = (container) => {
        setSelectedContainer(container)
    }

    const updateOpenFlowSwitch = (openFlowSwitch) => {
        setSelectedOpenFlowSwitch(openFlowSwitch)
    }

    const updateSnortIds = (snortIds) => {
        setSelectedSnortIds(snortIds)
    }

    const refresh = () => {
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setLoadingMonitoringData(true)
        setSelectedEmulationExecution(null)
        fetchEmulationExecutionIds()
    }

    const searchFilter = (executionIdObj, searchVal) => {
        return (searchVal === ""
            || executionIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEIds = emulationExecutionIds.filter(executionIdObj => {
            return searchFilter(executionIdObj, searchVal)
        });
        setFilteredEmulationExecutionIds(filteredEIds)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

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
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Real-time monitoring of emulated infrastructures
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Host and network metrics are collected at each emulated host and sent periodically to a
                        distributed Kafka queue.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Markov chain" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const fetchEmulationExecutionIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}?${IDS_QUERY_PARAM}=true`
            + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const emulationExecutionIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: `ID: ${id_obj.id}, emulation: ${id_obj.emulation}`
                    }
                })
                setEmulationExecutionIds(emulationExecutionIds)
                setFilteredEmulationExecutionIds(emulationExecutionIds)
                setLoading(false)
                if (emulationExecutionIds.length > 0) {
                    setSelectedEmulationExecutionId(emulationExecutionIds[0])
                    fetchSelectedExecution(emulationExecutionIds[0])
                    setLoadingSelectedEmulationExecution(true)
                    setLoadingMonitoringData(true)
                } else {
                    setLoadingSelectedEmulationExecution(false)
                    setLoadingMonitoringData(false)
                    setSelectedEmulationExecution(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSelectedExecution]);


    const SelectedExecutionView = (props) => {
        if (props.loadingSelectedEmulationExecution || props.loadingMonitoringData ||
            props.selectedEmulationExecution === null || props.selectedEmulationExecution === undefined) {
            if (props.loadingSelectedEmulationExecution || props.loadingMonitoringData) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching monitoring data... </span>
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
                    <div className="row">
                        <div className="col-sm-5">
                            <h4>
                                Time-series window length:
                                <div className="conditionalDist inline-block selectEmulation">
                                    <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                        <Select
                                            style={{display: 'inline-block'}}
                                            value={props.windowLength}
                                            defaultValue={props.windowLength}
                                            options={props.windowLengthOptions}
                                            onChange={onChangeWindowLength}
                                            placeholder="Select a window length"
                                        />
                                    </div>
                                </div>
                            </h4>
                        </div>
                        <div className="col-sm-5">
                            <h4>
                                Evolution speed:
                                <div className="conditionalDist inline-block selectEmulation">
                                    <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                        <Select
                                            style={{display: 'inline-block'}}
                                            value={props.animationDuration}
                                            defaultValue={props.animationDuration}
                                            options={props.evolutionSpeedOptions}
                                            onChange={animationDurationUpdate}
                                            placeholder="Set the evolution speed"
                                        />
                                    </div>
                                </div>
                            </h4>
                        </div>
                        <div className="col-sm-2">
                        </div>
                    </div>
                    <AggregateMetrics key={props.animationDuration.value}
                                      loading={props.loadingSelectedEmulationExecution}
                                      animation={props.animation}
                                      animationDuration={props.animationDuration.value}
                                      animationDurationFactor={props.animationDurationFactor}
                                      clientMetrics={getClientMetrics()} snortIdsMetrics={getSnortIdsMetrics()}
                                      aggregatedHostMetrics={getAggregatedHostMetrics()}
                                      aggregatedDockerStats={getAggregatedDockerStats()}
                                      aggregatedOSSECMetrics={getAggregatedOSSECHostMetrics()}
                    />
                    <div className="row hostMetricsDropdownRow">
                        <div className="col-sm-12">
                            <h5 className="text-center inline-block monitoringHeader">
                                <SelectHostDropdownOrSpinner
                                    loading={props.loadingSelectedEmulationExecution}
                                    selectedEmulation={props.selectedEmulationExecution.emulation_env_config}
                                    selectedContainer={props.selectedContainer}
                                    containerOptions={props.emulationExecutionContainerOptions}
                                />
                            </h5>
                        </div>
                    </div>
                    <hr/>

                    <ContainerMetrics key={`container-${props.animationDuration.value}`}
                                      loading={props.loadingSelectedEmulationExecution}
                                      hostMetrics={getHostMetrics()}
                                      dockerMetrics={getDockerMetrics()}
                                      ossecAlerts={getOSSECHostMetrics()}
                                      animation={props.animation} animationDuration={props.animationDuration.value}
                                      animationDurationFactor={props.animationDurationFactor}
                                      snortAlerts={getSnortHostMetrics()}
                    />

                    <div className="row hostMetricsDropdownRow">
                        <div className="col-sm-12">
                            <h5 className="text-center inline-block monitoringHeader">
                                <SelectOpenFlowSwitchDropdownOrSpinner
                                    loading={props.loadingSelectedEmulationExecution}
                                    selectedEmulation={props.selectedEmulationExecution.emulation_env_config}
                                    selectedSwitch={props.selectedSwitch}
                                    switchesOptions={props.switchesOptions}
                                />
                            </h5>
                        </div>
                    </div>
                    <hr/>
                    <OpenFlowSwitchesStats key={`switch-${props.animationDuration.value}`}
                                           loading={props.loadingSelectedEmulationExecution}
                                           portStats={getPortStats()}
                                           flowStats={getFlowStats()}
                                           aggFlowStats={getAggFlowStats()}
                                           animation={props.animation} animationDuration={props.animationDuration.value}
                                           animationDurationFactor={props.animationDurationFactor}/>

                    <div className="row hostMetricsDropdownRow">
                        <div className="col-sm-12">
                            <h5 className="text-center inline-block monitoringHeader">
                                <SelectSnortIdsDropdownOrSpinner
                                    loading={props.loadingSelectedEmulationExecution}
                                    selectedEmulation={props.selectedEmulationExecution.emulation_env_config}
                                    selectedIds={props.selectedIds}
                                    snortIdsOptions={props.snortIdsOptions}
                                />
                            </h5>
                        </div>
                    </div>
                    <hr/>
                    <SnortMetrics key={`snort-${props.animationDuration.value}`}
                                      loading={props.loadingSelectedEmulationExecution}
                                      animation={props.animation}
                                      animationDuration={props.animationDuration.value}
                                      animationDurationFactor={props.animationDurationFactor}
                                      snortIdsMetrics={getSpecificSnortIdsMetrics()}
                    />
                </div>
            )
        }
    }

    const SelectEmulationExecutionIdDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationExecutionIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No running executions are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching executions... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (<div>
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

                    Execution:
                    <div className="conditionalDist inline-block selectEmulation">
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationExecutionId}
                                defaultValue={props.selectedEmulationExecutionId}
                                options={props.emulationExecutionIds}
                                onChange={updateEmulationExecutionId}
                                placeholder="Select an emulation execution"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    const SelectHostDropdownOrSpinner = (props) => {
        if (!props.loading && props.selectedEmulation === null) {
            return (<></>)
        }
        if (props.loading || props.selectedEmulation === null || props.selectedContainer === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <h4>
                        Metrics for Container:
                        <div className="conditionalDist inline-block selectEmulation">
                            <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                <Select
                                    style={{display: 'inline-block', width: "300px"}}
                                    value={props.selectedContainer}
                                    defaultValue={props.selectedContainer}
                                    options={props.containerOptions}
                                    onChange={updateHost}
                                    placeholder="Select a container from the emulation"
                                />
                            </div>
                        </div>
                    </h4>
                </div>
            )
        }
    }


    const SelectOpenFlowSwitchDropdownOrSpinner = (props) => {
        if (!props.loading && (props.selectedEmulation === null || props.selectedSwitch === null)) {
            return (<></>)
        }
        if ((props.loading || props.selectedEmulation === null) || props.selectedSwitch === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <h4>
                        Metrics for OpenFlow switch with datapath ID:
                        <div className="conditionalDist inline-block selectEmulation">
                            <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                <Select
                                    style={{display: 'inline-block', width: "1000px"}}
                                    value={props.selectedSwitch}
                                    defaultValue={props.selectedSwitch}
                                    options={props.switchesOptions}
                                    onChange={updateOpenFlowSwitch}
                                    placeholder="Select an OpenFlow switch"
                                />
                            </div>
                        </div>
                    </h4>
                </div>
            )
        }
    }

    const SelectSnortIdsDropdownOrSpinner = (props) => {
        if (!props.loading && (props.selectedEmulation === null || props.selectedIds === null)) {
            return (<></>)
        }
        if ((props.loading || props.selectedEmulation === null) || props.selectedIds === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <h4>
                        IDS alerts from Snort IDS with IP:
                        <div className="conditionalDist inline-block selectEmulation">
                            <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                <Select
                                    style={{display: 'inline-block', width: "1000px"}}
                                    value={props.selectedIds}
                                    defaultValue={props.selectedIds}
                                    options={props.snortIdsOptions}
                                    onChange={updateSnortIds}
                                    placeholder="Select a Snort IDS"
                                />
                            </div>
                        </div>
                    </h4>
                </div>
            )
        }
    }


    useEffect(() => {
        setLoading(true)
        fetchEmulationExecutionIds()
    }, [fetchEmulationExecutionIds]);

    return (
        <div className="container-fluid">
            <h3 className="managementTitle"> Monitoring of Emulations </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationExecutionIdDropdownOrSpinner
                            loading={loading} emulationExecutionIds={filteredEmulationExecutionIds}
                            selectedEmulationExecutionId={selectedEmulationExecutionId}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                <div className="col-sm-1">
                </div>
            </div>
            <SelectedExecutionView loadingSelectedEmulationExecution={loadingSelectedEmulationExecution}
                                   selectedEmulationExecution={selectedEmulationExecution}
                                   windowLength={windowLength}
                                   windowLengthOptions={windowLengthOptions}
                                   animationDuration={animationDuration}
                                   evolutionSpeedOptions={evolutionSpeedOptions}
                                   selectedContainer={selectedContainer}
                                   emulationExecutionContainerOptions={emulationExecutionContainerOptions}
                                   animationDurationFactor={animationDurationFactor}
                                   animation={animation}
                                   selectedSwitch={selectedOpenFlowSwitch}
                                   switchesOptions={openFlowSwitchesOptions}
                                   loadingMonitoringData={loadingMonitoringData}
                                   snortIdsOptions={snortIdsOptions}
                                   selectedIds={selectedSnortIds}
            />
        </div>
    );
}

Monitoring.propTypes = {};
Monitoring.defaultProps = {};
export default Monitoring;
