import React, {useState, createRef, useCallback, useEffect} from 'react';
import './EmulationTraces.css';
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
import EmulationTrace from "./EmulationTrace/EmulationTrace";
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import TraceImg from './TracesLoop.png'
import {
    HTTP_PREFIX, HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    EMULATION_TRACES_RESOURCE,
    IDS_QUERY_PARAM
} from "../../../Common/constants";

/**
 * Component representing emulation traces on the page /traces-page
 */
const EmulationTraces = (props) => {
    const [showEmulationTracesInfoModal, setShowEmulationTracesInfoModal] = useState(false);
    const [selectedEmulationTraceId, setSelectedEmulationTraceId] = useState(null);
    const [selectedEmulationTrace, setSelectedEmulationTrace] = useState(null);
    const [emulationTracesIds, setEmulationTracesIds] = useState([]);
    const [loadingEmulationTraces, setLoadingEmulationTraces] = useState(true);
    const [loadingSelectedEmulationTrace, setLoadingSelectedEmulationTrace] = useState(true);
    const [filteredEmulationTracesIds, setFilteredEmulationTracesIds] = useState([]);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData
    const wrapper = createRef();

    const fetchEmulationTrace = useCallback((trace_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_TRACES_RESOURCE}/${trace_id.value}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
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
                setSelectedEmulationTrace(response)
                setLoadingSelectedEmulationTrace(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchEmulationTracesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_TRACES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const emulationTracesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, emulation: ${id_obj.emulation}`
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
    }, [alert, fetchEmulationTrace, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeEmulationTraceRequest = useCallback((emulation_trace_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_TRACES_RESOURCE}/${emulation_trace_id}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
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
                fetchEmulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchEmulationTracesIds, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeAllEmulationTracesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_TRACES_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
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
                fetchEmulationTracesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [fetchEmulationTracesIds, ip, navigate, port, alert, props.sessionData.token, setSessionData]);

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

    const searchEmulationTracesFilter = (emulationTraceIdLabel, searchVal) => {
        return (searchVal === "" || emulationTraceIdLabel.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchEmulationTracesChange = (event) => {
        var searchVal = event.target.value
        const filteredEmTracesIds = emulationTracesIds.filter(emulationTraceId => {
            return searchEmulationTracesFilter(emulationTraceId.label, searchVal)
        });
        setFilteredEmulationTracesIds(filteredEmTracesIds)
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

    const updateSelectedEmulationTraceId = (selectedId) => {
        setSelectedEmulationTraceId(selectedId)
        fetchEmulationTrace(selectedId)
        setLoadingSelectedEmulationTrace(true)
    }

    const DeleteAllEmulationTracesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllEmulationTracesTooltip}
                >
                    <Button variant="danger" onClick={removeAllEmulationTracesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about how emulation traces are collected
        </Tooltip>
    );

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
                            Emulation trace:
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
                        <Button className="infoButton5" variant="button" onClick={() => setShowEmulationTracesInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <EmulationTracesInfoModal
                        show={showEmulationTracesInfoModal}
                        onHide={() => setShowEmulationTracesInfoModal(false)}/>
                    <DeleteAllEmulationTracesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const EmulationTracesInfoModal = (props) => {
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
                        Emulation traces are collected from the emulation system. At every time-step of an emulation
                        episode, observations, actions, rewards, states and beliefs are measured or computed based on
                        data from the emulation.
                    </p>
                    <div className="text-center">
                        <img src={TraceImg} alt="Traces" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
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
                                        sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    useEffect(() => {
        setLoadingEmulationTraces(true)
        fetchEmulationTracesIds()
    }, [fetchEmulationTracesIds]);

    return (
        <div>
            <div className="row tracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">

                        <SelectEmulationTraceOrSpinner loadingEmulationTraces={loadingEmulationTraces}
                                                       emulationTracesIds={filteredEmulationTracesIds}
                                                       selectedEmulationTraceId={selectedEmulationTraceId}
                                                       sessionData={props.sessionData}
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
                                     sessionData={props.sessionData}
            />
        </div>
    )
}

EmulationTraces.propTypes = {};
EmulationTraces.defaultProps = {};
export default EmulationTraces;
