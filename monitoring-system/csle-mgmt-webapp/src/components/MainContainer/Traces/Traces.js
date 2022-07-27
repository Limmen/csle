import React, {useState, useEffect, useCallback, createRef} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import Modal from 'react-bootstrap/Modal'
import EmulationTrace from "./EmulationTrace/EmulationTrace";
import SimulationTrace from "./SimulationTrace/SimulationTrace";
import TraceImg from './TracesLoop.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form'
import Select from 'react-select'
import './Traces.css';
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";

const Traces = (props) => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [simulationTraces, setSimulationTraces] = useState([]);
    const [selectedEmulationTraceId, setSelectedEmulationTraceId] = useState(null);
    const [selectedSimulationTraceId, setSelectedSimulationTraceId] = useState(null);
    const [selectedEmulationTrace, setSelectedEmulationTrace] = useState(null);
    const [selectedSimulationTrace, setSelectedSimulationTrace] = useState(null);
    const [emulationTracesIds, setEmulationTracesIds] = useState([]);
    const [simulationTracesIds, setSimulationTracesIds] = useState([]);
    const [loadingEmulationTraces, setLoadingEmulationTraces] = useState(true);
    const [loadingSelectedEmulationTrace, setLoadingSelectedEmulationTrace] = useState(true);
    const [loadingSelectedSimulationTrace, setLoadingSelectedSimulationTrace] = useState(true);
    const [loadingSimulationTraces, setLoadingSimulationTraces] = useState(true);
    const [filteredEmulationTracesIds, setFilteredEmulationTracesIds] = useState([]);
    const [filteredSimulationTracesIds, setFilteredSimulationTracesIds] = useState([]);
    const [emulationTracesSearchString, setEmulationTracesSearchString] = useState([]);
    const [simulationTracesSearchString, setSimulationTracesSearchString] = useState([]);
    const ip = "localhost"
    const alert = useAlert();
    const navigate = useNavigate();
    // const ip = "172.31.212.92"

    const wrapper = createRef();

    const fetchEmulationTrace = useCallback((trace_id) => {
        fetch(
            `http://` + ip + ':7777/emulation-traces/' + trace_id.value + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedEmulationTrace(response)
                setLoadingSelectedEmulationTrace(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSimulationTrace = useCallback((trace_id) => {
        fetch(
            `http://` + ip + ':7777/simulation-traces/' + trace_id.value + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedSimulationTrace(response)
                setLoadingSelectedSimulationTrace(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchEmulationTracesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulation-traces?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const emulationTracesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setEmulationTracesIds(emulationTracesIds)
                setFilteredEmulationTracesIds(emulationTracesIds)
                setLoadingEmulationTraces(false)
                if (emulationTracesIds.length > 0) {
                    setSelectedEmulationTraceId(emulationTracesIds[0])
                    fetchEmulationTrace(emulationTracesIds[0])
                    setLoadingSelectedEmulationTrace(true)
                } else {
                    setLoadingSelectedEmulationTrace(false)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSimulationTracesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulation-traces?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const simulationTracesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setSimulationTracesIds(simulationTracesIds)
                setFilteredSimulationTracesIds(simulationTracesIds)
                setLoadingSimulationTraces(false)
                if (simulationTracesIds.length > 0) {
                    setSelectedSimulationTraceId(simulationTracesIds[0])
                    fetchSimulationTrace(simulationTracesIds[0])
                    setLoadingSelectedSimulationTrace(true)
                } else {
                    setLoadingSelectedSimulationTrace(false)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSimulationTraces = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulation-traces' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setFilteredSimulationTracesIds(response)
                setSimulationTraces(response)
                setLoadingSimulationTraces(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoadingEmulationTraces(true)
        setLoadingSimulationTraces(true)
        fetchEmulationTracesIds()
        fetchSimulationTracesIds()
    }, [fetchSimulationTracesIds, fetchEmulationTracesIds]);

    const removeSimulationTraceRequest = useCallback((simulation_trace_id) => {
        fetch(
            (`http://` + ip + ':7777/simulation-traces/' + simulation_trace_id + "?token="
                + props.sessionData.token),
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchSimulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeSimulationTrace = (simulationTrace) => {
        setLoadingSimulationTraces(true)
        setLoadingSelectedSimulationTrace(true)
        removeSimulationTraceRequest(simulationTrace.id)
        setSelectedSimulationTrace(null)
    }

    const removeEmulationTraceRequest = useCallback((emulation_trace_id) => {
        fetch(
            `http://` + ip + ':7777/emulation-traces/' + emulation_trace_id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchEmulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllEmulationTracesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulation-traces' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchEmulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSimulationTracesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulation-traces' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchSimulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeEmulationTrace = (emulationTrace) => {
        setLoadingEmulationTraces(true)
        setLoadingSelectedEmulationTrace(true)
        removeEmulationTraceRequest(emulationTrace.id)
        setSelectedEmulationTrace(null)
    }

    const refreshEmulationTraces = () => {
        setLoadingEmulationTraces(true)
        setLoadingSelectedEmulationTrace(true)
        fetchEmulationTracesIds()
    }

    const removeAllEmulationTraces = () => {
        setLoadingEmulationTraces(true)
        setLoadingSelectedEmulationTrace(true)
        removeAllEmulationTracesRequest()
        setSelectedEmulationTrace(null)
    }

    const removeAllSimulationTraces = () => {
        setLoadingSimulationTraces(true)
        setLoadingSelectedSimulationTrace(true)
        removeAllSimulationTracesRequest()
        setSelectedSimulationTrace(null)
    }

    const removeAllEmulationTracesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all emulation traces? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllEmulationTraces()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all emulation traces? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllEmulationTraces()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeEmulationTraceConfirm = (trace) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the emulation trace with ID: ' + trace.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeEmulationTrace(trace)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the emulation trace with ID {trace.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeEmulationTrace(trace)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeAllSimulationTracesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all simulation traces? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllSimulationTraces()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all simulation traces? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllSimulationTraces()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeSimulationTraceConfirm = (trace) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the simulation trace with ID: ' + trace.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeSimulationTrace(trace)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the simulation trace with ID {trace.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeSimulationTrace(trace)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const refreshSimulationTraces = () => {
        setLoadingSimulationTraces(true)
        setLoadingSelectedSimulationTrace(true)
        fetchSimulationTracesIds()
    }

    const renderRefreshEmulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulation traces from the backend
        </Tooltip>
    );

    const renderRemoveAllEmulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all emulation traces
        </Tooltip>
    );

    const renderRemoveAllSimulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all simulation traces
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about how traces are collected
        </Tooltip>
    );

    const renderRefreshSimulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulation traces from the backend
        </Tooltip>
    );

    const searchEmulationTracesFilter = (emulationTraceIdLabel, searchVal) => {
        return (searchVal === "" || emulationTraceIdLabel.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchEmulationTracesChange = (event) => {
        var searchVal = event.target.value
        const filteredEmTracesIds = emulationTracesIds.filter(emulationTraceId => {
            return searchEmulationTracesFilter(emulationTraceId.label, searchVal)
        });
        setFilteredEmulationTracesIds(filteredEmTracesIds)
        setEmulationTracesSearchString(searchVal)
        var selectedEmulationTraceRemoved = false
        if (!loadingSelectedEmulationTrace && filteredEmTracesIds.length > 0) {
            for (let i = 0; i < filteredEmTracesIds.length; i++) {
                if (selectedEmulationTrace !== null && selectedEmulationTrace !== undefined &&
                    selectedEmulationTrace.id === filteredEmTracesIds[i].value) {
                    selectedEmulationTraceRemoved = true
                }
            }
            if (!selectedEmulationTraceRemoved) {
                setSelectedEmulationTraceId(filteredEmTracesIds[0])
                fetchEmulationTrace(filteredEmTracesIds[0])
                setLoadingSelectedEmulationTrace(true)
            }
        }
    }

    const searchEmulationTracesHandler = useDebouncedCallback(
        (event) => {
            searchEmulationTracesChange(event)
        },
        350
    );

    const searchSimulationTracesFilter = (simulationTraceIdObj, searchVal) => {
        return (searchVal === "" || simulationTraceIdObj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchSimulationTracesChange = (event) => {
        var searchVal = event.target.value
        const filteredSimTracesIds = simulationTracesIds.filter(simTraceId => {
            return searchSimulationTracesFilter(simTraceId, searchVal)
        });
        setFilteredSimulationTracesIds(filteredSimTracesIds)
        setSimulationTracesSearchString(searchVal)

        var selectedSimulationTraceRemoved = false
        if (!loadingSelectedSimulationTrace && filteredSimTracesIds.length > 0) {
            for (let i = 0; i < filteredSimTracesIds.length; i++) {
                if (selectedSimulationTrace !== null && selectedSimulationTrace !== undefined &&
                    selectedSimulationTrace.id === filteredSimTracesIds[i].value) {
                    selectedSimulationTraceRemoved = true
                }
            }
            if (!selectedSimulationTraceRemoved) {
                setSelectedSimulationTraceId(filteredSimTracesIds[0])
                fetchSimulationTrace(filteredSimTracesIds[0])
                setLoadingSelectedSimulationTrace(true)
            }
        }
    }

    const searchSimulationTracesHandler = useDebouncedCallback(
        (event) => {
            searchSimulationTracesChange(event)
        },
        350
    );

    const updateSelectedEmulationTraceId = (selectedId) => {
        setSelectedEmulationTraceId(selectedId)
        fetchEmulationTrace(selectedId)
        setLoadingSelectedEmulationTrace(true)
    }

    const updateSelectedSimulationTraceId = (selectedId) => {
        setSelectedSimulationTraceId(selectedId)
        fetchSimulationTrace(selectedId)
        setLoadingSelectedSimulationTrace(true)
    }

    const SelectEmulationTraceOrSpinner = (props) => {
        if (!props.loadingEmulationTraces && props.emulationTracesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No emulation traces are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshEmulationTracesTooltip}
                    >
                        <Button variant="button" onClick={refreshEmulationTraces}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingEmulationTraces) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Selected emulation trace:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationTraceId}
                                defaultValue={props.selectedEmulationTraceId}
                                options={props.emulationTracesIds}
                                onChange={updateSelectedEmulationTraceId}
                                placeholder="Select emulation trace"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshEmulationTracesTooltip}
                    >
                        <Button variant="button" onClick={refreshEmulationTraces}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button className="infoButton5" variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllEmulationTracesTooltip}
                    >
                        <Button variant="danger" onClick={removeAllEmulationTracesConfirm} size="sm">
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }


    const SelectSimulationTraceOrSpinner = (props) => {
        if (!props.loadingSimulationTraces && props.simulationTracesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No simulation traces are available</span>
                </div>
            )
        }
        if (props.loadingSimulationTraces) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshSimulationTracesTooltip}
                    >
                        <Button variant="button" onClick={refreshSimulationTraces}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </Spinner>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Selected simulation trace:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSimulationTraceId}
                                defaultValue={props.selectedSimulationTraceId}
                                options={props.simulationTracesIds}
                                onChange={updateSelectedSimulationTraceId}
                                placeholder="Select simulation trace"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshSimulationTracesTooltip}
                    >
                        <Button variant="button" onClick={refreshSimulationTraces}>
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

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllSimulationTracesTooltip}
                    >
                        <Button variant="danger" onClick={removeAllSimulationTracesConfirm} size="sm">
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Traces
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Collection of emulation and simulation traces</h4>
                    <p className="modalText">
                        Simulation traces are collected from the simulation system. At every time-step of the
                        simulation,
                        the simulated observations, player actions, rewards, states, and beliefs are recorded.
                        Emulation traces are collected from the emulation system. At every time-step of an emulation
                        episode, observations, actions, rewards, states and beliefs are measured or computed based on
                        data from the emulation.
                    </p>
                    <div className="text-center">
                        <img src={TraceImg} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const EmulationTracesAccordions = (props) => {
        if (props.loadingEmulationTraces) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.emulationTraces.map((emulationTrace, index) =>
                        <EmulationTrace emulationTrace={emulationTrace}
                                        wrapper={wrapper} key={emulationTrace.id + "-" + index}
                                        removeEmulationTrace={removeEmulationTraceConfirm}
                        />
                    )}
                </Accordion>
            )
        }
    }

    const EmulationTraceAccordion = (props) => {
        if (props.loadingSelectedEmulationTrace || props.selectedEmulationTrace === null || props.selectedEmulationTrace === undefined) {
            if (props.loadingSelectedEmulationTrace) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching emulation trace... </span>
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
                    <h3 className="emulationConfigTitle">
                        Configuration of selected emulation trace:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <EmulationTrace emulationTrace={props.selectedEmulationTrace}
                                        wrapper={wrapper} key={props.selectedEmulationTrace.id}
                                        removeEmulationTrace={removeEmulationTraceConfirm}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const SimulationTraceAccordion = (props) => {
        if (props.loadingSelectedSimulationTrace || props.selectedSimulationTrace === null || props.selectedSimulationTrace === undefined) {
            if (props.loadingSelectedSimulationTrace) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching simulation trace... </span>
                        <Spinner animation="border" role="status" className="spinnerLabel">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>
                )
            } else {
                return (
                    <p>
                    </p>)
            }
        } else {
            return (
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of selected simulation trace:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <SimulationTrace simulationTrace={props.selectedSimulationTrace}
                                         wrapper={wrapper} key={props.selectedSimulationTrace.id}
                                         removeSimulationTrace={removeSimulationTraceConfirm}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    return (
        <div className="Traces">
            <h3 className="managementTitle"> Traces </h3>
            <div className="row emulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">

                        <SelectEmulationTraceOrSpinner loadingEmulationTraces={loadingEmulationTraces}
                                                       emulationTracesIds={filteredEmulationTracesIds}
                                                       selectedEmulationTraceId={selectedEmulationTraceId}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="emulationTracesInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="emulationTracesInput"
                                onChange={searchEmulationTracesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <EmulationTraceAccordion selectedEmulationTrace={selectedEmulationTrace}
                                     loadingSelectedEmulationTrace={loadingSelectedEmulationTrace}
            />
            <div className="row simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block">
                        <SelectSimulationTraceOrSpinner loadingSimulationTraces={loadingSimulationTraces}
                                                        simulationTracesIds={filteredSimulationTracesIds}
                                                        selectedSimulationTraceId={selectedSimulationTraceId}/>
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="simulationTracesInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="simulationTracesInput"
                                onChange={searchSimulationTracesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <SimulationTraceAccordion selectedSimulationTrace={selectedSimulationTrace}
                                      loadingSelectedSimulationTrace={loadingSelectedSimulationTrace}/>
        </div>
    );
}

Traces.propTypes = {};
Traces.defaultProps = {};
export default Traces;
