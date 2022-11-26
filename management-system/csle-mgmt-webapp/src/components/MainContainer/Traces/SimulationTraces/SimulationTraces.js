import React, {useState, createRef, useCallback, useEffect} from 'react';
import './SimulationTraces.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Modal from 'react-bootstrap/Modal'
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Select from 'react-select'
import SimulationTrace from "./SimulationTrace/SimulationTrace";
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import MarkovImg from './../../Simulations/Markov.png'
import {
    HTTP_PREFIX, HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    SIMULATION_TRACES_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM
} from "../../../Common/constants";

/**
 * Component representing simulation traces on the page /traces-page
 */
const SimulationTraces = (props) => {
    const [showSimulationTracesInfoModal, setShowSimulationTracesInfoModal] = useState(false);
    const [selectedSimulationTraceId, setSelectedSimulationTraceId] = useState(null);
    const [selectedSimulationTrace, setSelectedSimulationTrace] = useState(null);
    const [simulationTracesIds, setSimulationTracesIds] = useState([]);
    const [loadingSelectedSimulationTrace, setLoadingSelectedSimulationTrace] = useState(true);
    const [loadingSimulationTraces, setLoadingSimulationTraces] = useState(true);
    const [filteredSimulationTracesIds, setFilteredSimulationTracesIds] = useState([]);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData
    const wrapper = createRef();

    const fetchSimulationTrace = useCallback((trace_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATION_TRACES_RESOURCE}/${trace_id.value}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setSelectedSimulationTrace(response)
                setLoadingSelectedSimulationTrace(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchSimulationTracesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATION_TRACES_RESOURCE}?${IDS_QUERY_PARAM}=true`
            + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                const simulationTracesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, fetchSimulationTrace, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeSimulationTraceRequest = useCallback((simulation_trace_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${SIMULATION_TRACES_RESOURCE}/${simulation_trace_id}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchSimulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [fetchSimulationTracesIds, ip, navigate, port, alert, props.sessionData.token, setSessionData]);

    const removeSimulationTrace = (simulationTrace) => {
        setLoadingSimulationTraces(true)
        setLoadingSelectedSimulationTrace(true)
        removeSimulationTraceRequest(simulationTrace.id)
        setSelectedSimulationTrace(null)
    }

    const removeAllSimulationTracesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATION_TRACES_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchSimulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchSimulationTracesIds, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeAllSimulationTraces = () => {
        setLoadingSimulationTraces(true)
        setLoadingSelectedSimulationTrace(true)
        removeAllSimulationTracesRequest()
        setSelectedSimulationTrace(null)
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

    const renderRemoveAllSimulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all simulation traces
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about how simulation traces are collected
        </Tooltip>
    );

    const renderRefreshSimulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulation traces from the backend
        </Tooltip>
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

    const updateSelectedSimulationTraceId = (selectedId) => {
        setSelectedSimulationTraceId(selectedId)
        fetchSimulationTrace(selectedId)
        setLoadingSelectedSimulationTrace(true)
    }

    const DeleteAllSimulationTracesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllSimulationTracesTooltip}
                >
                    <Button variant="danger" onClick={removeAllSimulationTracesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
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
                            Simulation trace:
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
                        <Button variant="button" onClick={() => setShowSimulationTracesInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <SimulationTracesInfoModal show={showSimulationTracesInfoModal}
                                               onHide={() => setShowSimulationTracesInfoModal(false)}/>

                    <DeleteAllSimulationTracesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const SimulationTracesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Simulation Traces
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Simulation traces are collected from the simulation system. At every time-step of the
                        simulation,
                        the simulated observations, player actions, rewards, states, and beliefs are recorded.
                    </p>
                    <div className="text-center">
                        <img src={MarkovImg} alt="Traces" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
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
                                         sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }


    useEffect(() => {
        setLoadingSimulationTraces(true)
        fetchSimulationTracesIds()
    }, [fetchSimulationTracesIds]);

    return (
        <div>
            <div className="row tracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block">
                        <SelectSimulationTraceOrSpinner loadingSimulationTraces={loadingSimulationTraces}
                                                        simulationTracesIds={filteredSimulationTracesIds}
                                                        selectedSimulationTraceId={selectedSimulationTraceId}
                                                        sessionData={props.sessionData}
                        />
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
                                      loadingSelectedSimulationTrace={loadingSelectedSimulationTrace}
                                      sessionData={props.sessionData}
            />
        </div>
    )
}

SimulationTraces.propTypes = {};
SimulationTraces.defaultProps = {};
export default SimulationTraces;
