import React, {useState, useEffect, createRef, useCallback} from 'react';
import './Emulations.css';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import Emulation from "./Emulation/Emulation";
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import ConfigSpace from './ConfigSpace.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    HTTP_PREFIX,
    LOGIN_PAGE_RESOURCE,
    IDS_QUERY_PARAM,
    EMULATIONS_RESOURCE,
    HTTP_REST_GET,
    TOKEN_QUERY_PARAM, HTTP_REST_DELETE, EXECUTIONS_SUBRESOURCE, HTTP_REST_POST
} from "../../Common/constants";

/**
 * Component representing the /emulations-page
 */
const Emulations = (props) => {
    const [emulationIds, setEmulationIds] = useState([]);
    const [selectedEmulationId, setSelectedEmulationId] = useState(null);
    const [selectedEmulation, setSelectedEmulation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulation, setLoadingSelectedEmulation] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredEmulationsIds, setFilteredEmulationsIds] = useState([]);
    const [showOnlyRunningEmulations, setShowOnlyRunningEmulations] = useState(false);
    const [searchString, setSearchString] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchEmulation = useCallback((emulation_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}/${emulation_id.value}`
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
                setSelectedEmulation(response)
                setLoadingSelectedEmulation(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchEmulationIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const emulationIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (!id_obj.running) {
                        lbl = "ID: " + id_obj.id + ", name: " + id_obj.emulation
                    } else {
                        lbl = "ID: " + id_obj.id + ", name: " + id_obj.emulation + " (running)"
                    }
                    return {
                        value: id_obj.id,
                        running: id_obj.running,
                        label: lbl
                    }
                })
                setEmulationIds(emulationIds)
                setFilteredEmulationsIds(emulationIds)
                setLoading(false)
                if (emulationIds.length > 0) {
                    setSelectedEmulationId(emulationIds[0])
                    fetchEmulation(emulationIds[0])
                    setLoadingSelectedEmulation(true)
                } else {
                    setLoadingSelectedEmulation(false)
                    setSelectedEmulation(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchEmulation, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeEmulationRequest = useCallback((emulationId) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}/`
                + `${emulationId}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview",
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Request-Method': 'GET, POST, DELETE, PUT, OPTIONS'
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
                fetchEmulationIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchEmulationIds]);

    const removeEmulationExecutionRequest = useCallback((emulation_id, execution_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}/${emulation_id}/${EXECUTIONS_SUBRESOURCE}/`
                    + `${execution_id}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setLoadingSelectedEmulation(true)
                var id_obj = {
                    value: emulation_id,
                    label: "-"
                }
                fetchEmulation(id_obj)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchEmulation]);

    const startOrStopEmulationRequest = useCallback((emulation_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}/${emulation_id}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
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
                setLoadingSelectedEmulation(true)
                var id_obj = {
                    value: emulation_id,
                    label: "-"
                }
                fetchEmulation(id_obj)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchEmulation]);

    const removeAllEmulationsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATIONS_RESOURCE}`
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
                fetchEmulationIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchEmulationIds]);

    const removeEmulation = (emulation) => {
        setLoading(true)
        removeEmulationRequest(emulation.id)
        setSelectedEmulation(null)
    }

    const removeExecution = (emulation, ip_first_octet) => {
        removeEmulationExecutionRequest(emulation.id, ip_first_octet)
    }

    const startOrStopEmulation = (emulation_id) => {
        startOrStopEmulationRequest(emulation_id)
    }

    useEffect(() => {
        setLoading(true)
        fetchEmulationIds();
    }, [fetchEmulationIds]);

    const updateSelectedEmulationId = (selectedId) => {
        setSelectedEmulationId(selectedId)
        fetchEmulation(selectedId)
        setLoadingSelectedEmulation(true)
    }

    const refresh = () => {
        setLoading(true)
        fetchEmulationIds()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const removeAllEmulations = () => {
        setLoading(true)
        removeAllEmulationsRequest()
        setSelectedEmulation(null)
    }

    const removeAllEmulationsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all emulations? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllEmulations()
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
                                    Are you sure you want to delete all emulations? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllEmulations()
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

    const startOrStopEmulationConfirm = (emulation) => {
        confirmAlert({
            title: 'Confirm start/stop emulation',
            message: 'Are you sure you want to start/stop the emulation with id: ' + emulation.id,
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => startOrStopEmulation(emulation.id)
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
                if (emulation.running) {
                    return (
                        <div id="react-confirm-alert" onClick={onClose}>
                            <div className="react-confirm-alert-overlay">
                                <div className="react-confirm-alert" onClick={onClose}>
                                    <div className="react-confirm-alert-body">
                                        <h1>Confirm starting</h1>
                                        Are you sure you want to start the emulation with id {emulation.id}?
                                        <div className="react-confirm-alert-button-group">
                                            <Button className="remove-confirm-button"
                                                    onClick={() => {
                                                        startOrStopEmulation(emulation.id)
                                                        onClose()
                                                    }}
                                            >
                                                <span className="remove-confirm-button-text">Yes, start it.</span>
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
                    )
                } else {
                    return (
                        <div id="react-confirm-alert" onClick={onClose}>
                            <div className="react-confirm-alert-overlay">
                                <div className="react-confirm-alert" onClick={onClose}>
                                    <div className="react-confirm-alert-body">
                                        <h1>Confirm starting</h1>
                                        Are you sure you want to stop the emulation with id {emulation.id}?
                                        This will stop and delete all executions of the emulation.
                                        <div className="react-confirm-alert-button-group">
                                            <Button className="remove-confirm-button"
                                                    onClick={() => {
                                                        startOrStopEmulation(emulation.id)
                                                        onClose()
                                                    }}
                                            >
                                                <span className="remove-confirm-button-text">Yes, stop it it.</span>
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
                    )
                }
            }
        })
    }

    const removeEmulationConfirm = (emulation) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the emulation with ID: ' + emulation.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeEmulation(emulation)
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
                                    Are you sure you want to delete the emulation with ID {emulation.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeEmulation(emulation)
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

    const removeExecutionConfirm = (emulation, execution_id) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the execution with ID: ' + execution_id.id +
                " and emulation ID: " + emulation.id + "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeExecution(emulation, execution_id)
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
                                    Are you sure you want to delete the execution with ID {execution_id.id}
                                    and emulation {emulation.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeExecution(emulation, execution_id)
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

    const searchFilter = (em_id_obj, searchVal) => {
        return (searchVal === "" || em_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmsIds = emulationIds.filter(em => {
            return searchFilter(em, searchVal)
        });
        setFilteredEmulationsIds(filteredEmsIds)
        setSearchString(searchVal)

        var selectedEmulationRemoved = false
        if (!loadingSelectedEmulation && filteredEmsIds.length > 0) {
            for (let i = 0; i < filteredEmsIds.length; i++) {
                if (selectedEmulation !== null && selectedEmulation !== undefined &&
                    selectedEmulation.id === filteredEmsIds[i].value) {
                    selectedEmulationRemoved = true
                }
            }
            if (!selectedEmulationRemoved) {
                setSelectedEmulationId(filteredEmsIds[0])
                fetchEmulation(filteredEmsIds[0])
                setLoadingSelectedEmulation(true)
            }
        } else {
            setSelectedEmulation(null)
        }
    }

    const runningEmulationsChange = (event) => {
        var filteredEmsIds = null
        if (!showOnlyRunningEmulations) {
            filteredEmsIds = filteredEmulationsIds.filter(emIdObj => {
                return emIdObj.running
            });
            setFilteredEmulationsIds(filteredEmsIds)
        } else {
            filteredEmsIds = emulationIds.filter(emIdObj => {
                return searchFilter(emIdObj, searchString)
            });
            setFilteredEmulationsIds(filteredEmsIds)
        }
        setShowOnlyRunningEmulations(!showOnlyRunningEmulations)

        var selectedEmulationRemoved = false
        if (!loadingSelectedEmulation && filteredEmsIds.length > 0) {
            for (let i = 0; i < filteredEmsIds.length; i++) {
                if (selectedEmulation !== null && selectedEmulation !== undefined &&
                    selectedEmulation.id === filteredEmsIds[i].value) {
                    selectedEmulationRemoved = true
                }
            }
            if (!selectedEmulationRemoved) {
                setSelectedEmulationId(filteredEmsIds[0])
                fetchEmulation(filteredEmsIds[0])
                setLoadingSelectedEmulation(true)
            }
        } else {
            setSelectedEmulation(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const GetExecutions = (props) => {
        if (props.executions.length > 0) {
            return (
                <div>
                    <h3 className="executionsTitle">
                        Executions:
                    </h3>
                    {props.executions.map((exec, index) =>
                        <Accordion defaultActiveKey="0" key={index + exec.ip_first_octet}>
                            <Emulation emulation={exec.emulation_env_config}
                                       wrapper={wrapper} key={exec.emulation_env_config.name + "_" + index}
                                       removeEmulation={removeEmulationConfirm} execution={true}
                                       removeExecution={removeExecutionConfirm}
                                       startOrStopEmulation={startOrStopEmulationConfirm}
                                       execution_ip_octet={exec.ip_first_octet}
                                       sessionData={props.sessionData}
                            />
                        </Accordion>
                    )
                    }
                </div>
            )
        } else {
            return <span></span>
        }
    }

    const EmulationAccordion = (props) => {
        if (props.loadingSelectedEmulation || props.selectedEmulation === null || props.selectedEmulation === undefined) {
            if (props.loadingSelectedEmulation) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching emulation... </span>
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
                        Configuration of selected emulation:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <Emulation emulation={props.selectedEmulation}
                                   wrapper={wrapper} key={props.selectedEmulation.name}
                                   removeEmulation={removeEmulationConfirm} execution={false}
                                   execution_ip_octet={-1} removeExecution={removeExecutionConfirm}
                                   startOrStopEmulation={startOrStopEmulationConfirm}
                                   sessionData={props.sessionData}
                        />
                    </Accordion>
                    <GetExecutions executions={props.selectedEmulation.executions} sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllEmulationsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveEmulationsTooltip}
                >
                    <Button variant="danger" onClick={removeAllEmulationsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectEmulationOrSpinner = (props) => {
        if (!props.loading && props.emulationIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No emulations are available</span>
                    <OverlayTrigger
                        placement="top"
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
                    <span className="spinnerLabel"> Fetching emulations... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Emulation:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationId}
                                defaultValue={props.selectedEmulationId}
                                options={props.emulationIds}
                                onChange={updateSelectedEmulationId}
                                placeholder="Select emulation"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={info}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <DeleteAllEmulationsOrEmpty sessionData={props.sessionData}/>
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
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Emulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        An emulated infrastructure consists of a a cluster of machines that
                        runs a virtualization layer provided by Docker containers
                        and virtual links. It implements network isolation and traffic
                        shaping on the containers using network namespaces and the
                        NetEm module in the Linux kernel. Resource constraints
                        of the containers, e.g. CPU and memory constraints, are
                        enforced using cgroups. The configuration of an emulated infrastructure includes
                        the topology, resource constraints, vulnerabilities, services, users, etc.
                    </p>
                    <div className="text-center">
                        <img src={ConfigSpace} alt="Emulated infrastructures" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulations from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the emulation environments
        </Tooltip>
    );

    const renderRemoveEmulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all emulations
        </Tooltip>
    );

    const wrapper = createRef();

    return (
        <div className="Emulations">
            <h3 className="managementTitle"> Management of Emulated Infrastructures </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationOrSpinner loading={loading}
                                                  emulationIds={filteredEmulationsIds}
                                                  selectedEmulationId={selectedEmulationId}
                                                  sessionData={props.sessionData}
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
                <div className="col-sm-2">
                    <Form>
                        <Form.Check
                            inline
                            type="switch"
                            id="runningEmulationsSwitch"
                            label="Show only running emulations"
                            className="runningCheck"
                            onChange={runningEmulationsChange}
                        />
                    </Form>
                </div>
            </div>
            <EmulationAccordion loadingSelectedEmulation={loadingSelectedEmulation}
                                selectedEmulation={selectedEmulation}
                                sessionData={props.sessionData}
            />
        </div>
    );
}

Emulations.propTypes = {};
Emulations.defaultProps = {};
export default Emulations;
