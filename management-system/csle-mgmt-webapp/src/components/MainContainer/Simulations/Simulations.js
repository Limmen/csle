import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Simulations.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import MarkovChain from './Markov.png'
import Simulation from "./Simulation/Simulation";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {HTTP_PREFIX, HTTP_REST_DELETE, HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE, TOKEN_QUERY_PARAM, SIMULATIONS_RESOURCE, IDS_QUERY_PARAM} from "../../Common/constants";


/**
 * Component representing the /simulations-page
 */
const Simulations = (props) => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [simulationIds, setSimulationIds] = useState([]);
    const [selectedSimulation, setSelectedSimulation] = useState(null);
    const [selectedSimulationId, setSelectedSimulationId] = useState(null);
    const [filteredSimulationIds, setFilteredSimulationsIds] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedSimulation, setLoadingSelectedSimulation] = useState(true);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchSimulation = useCallback((simulation_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATIONS_RESOURCE}/${simulation_id.value}`
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
                setSelectedSimulation(response)
                setLoadingSelectedSimulation(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchSimulationsIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATIONS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const simulationIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, name: ${id_obj.simulation}`
                    }
                })
                setSimulationIds(simulationIds)
                setFilteredSimulationsIds(simulationIds)
                setLoading(false)
                if (simulationIds.length > 0) {
                    setSelectedSimulationId(simulationIds[0])
                    fetchSimulation(simulationIds[0])
                    setLoadingSelectedSimulation(true)
                } else {
                    setLoadingSelectedSimulation(false)
                    setSelectedSimulation(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [ip, navigate, fetchSimulation, port, alert, props.sessionData.token, setSessionData]);

    const removeAllSimulationsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATIONS_RESOURCE}`
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
                fetchSimulationsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchSimulationsIds, ip, navigate, port, props.sessionData.token, setSessionData]);

    useEffect(() => {
        setLoading(true);
        fetchSimulationsIds();
    }, [fetchSimulationsIds]);


    const removeSimulationRequest = useCallback((simulation_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SIMULATIONS_RESOURCE}/${simulation_id}`
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
                fetchSimulationsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchSimulationsIds, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeSimulation = (simulation) => {
        setLoading(true)
        removeSimulationRequest(simulation.id)
        setSelectedSimulation(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulations from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the simulation environments
        </Tooltip>
    );

    const renderRemoveAllSimulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all simulations.
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        fetchSimulationsIds()
    }

    const removeAllSimulations = () => {
        setLoading(true)
        removeAllSimulationsRequest()
        setSelectedSimulation(null)
    }

    const removeAllSimulationsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all simulations? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllSimulations()
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
                                    Are you sure you want to delete all simulations? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllSimulations()
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

    const removeSimulationConfirm = (simulation) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the simulation with ID: ' + simulation.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeSimulation(simulation)
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
                                    Are you sure you want to delete the simulation with ID {simulation.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeSimulation(simulation)
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

    const searchFilter = (simIdObj, searchVal) => {
        return (searchVal === "" || simIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredSimsIds = simulationIds.filter(simulation_id_obj => {
            return searchFilter(simulation_id_obj, searchVal)
        });
        setFilteredSimulationsIds(filteredSimsIds)

        var selectedSimulationRemoved = false
        if (!loadingSelectedSimulation && filteredSimsIds.length > 0) {
            for (let i = 0; i < filteredSimsIds.length; i++) {
                if (selectedSimulation !== null && selectedSimulation !== undefined &&
                    selectedSimulation.id === filteredSimsIds[i].value) {
                    selectedSimulationRemoved = true
                }
            }
            if (!selectedSimulationRemoved) {
                setSelectedSimulationId(filteredSimsIds[0])
                fetchSimulation(filteredSimsIds[0])
                setLoadingSelectedSimulation(true)
            }
        } else {
            setSelectedSimulation(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

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
                        Simulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        A simulation is defined as a Markov decision process or stochastic game, which models
                        how a discrete-time dynamical system is evolved and can be controlled.
                    </p>
                    <div className="text-center">
                        <img src={MarkovChain} alt="Markov chain" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SimulationAccordion = (props) => {
        if (props.loadingSelectedSimulation || props.selectedSimulation === null || props.selectedSimulation === undefined) {
            if (props.loadingSelectedSimulation) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching simulation... </span>
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
                        Configuration of selected simulation:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <Simulation simulation={props.selectedSimulation} wrapper={wrapper}
                                    key={props.selectedSimulation.name}
                                    removeSimulation={removeSimulationConfirm}
                                    sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const updateSelectedSimulationId = (selectedId) => {
        setSelectedSimulationId(selectedId)
        fetchSimulation(selectedId)
        setLoadingSelectedSimulation(true)
    }

    const DeleteAllSimulationsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllSimulationsTooltip}
                >
                    <Button variant="danger" onClick={removeAllSimulationsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectSimulationOrSpinner = (props) => {
        if (!props.loading && props.simulationIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No simulations are available</span>
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
                    <span className="spinnerLabel"> Fetching simulations... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Simulation:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSimulationId}
                                defaultValue={props.selectedSimulationId}
                                options={props.simulationIds}
                                onChange={updateSelectedSimulationId}
                                placeholder="Select simulation"
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
                        <Button variant="button infoButton2" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    <DeleteAllSimulationsOrEmpty sessionData={props.sessionData}/>

                </div>
            )
        }
    }

    const wrapper = createRef();

    return (
        <div className="Simulations">
            <h3 className="managementTitle"> Management of Simulations </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectSimulationOrSpinner loading={loading}
                                                   simulationIds={filteredSimulationIds}
                                                   selectedSimulationId={selectedSimulationId}
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
                </div>
            </div>
            <SimulationAccordion loadingSelectedSimulation={loadingSelectedSimulation}
                                 selectedSimulation={selectedSimulation}
                                 sessionData={props.sessionData}
            />
        </div>
    );
}

Simulations.propTypes = {};
Simulations.defaultProps = {};
export default Simulations;
