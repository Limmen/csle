import React, {useState, useEffect, useCallback, createRef} from 'react';
import Modal from 'react-bootstrap/Modal'
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Experiment from "./Experiment/Experiment";
import './TrainingResults.css';
import TrainingEnv from './RL_training_env.png'
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
    LOGIN_PAGE_RESOURCE, TOKEN_QUERY_PARAM, EXPERIMENTS_RESOURCE, IDS_QUERY_PARAM} from "../../Common/constants";


/**
 * Component representing the /training-results-page
 */
const TrainingResults = (props) => {
    const [experimentsIds, setExperimentsIds] = useState([]);
    const [selectedExperimentId, setSelectedExperimentId] = useState(null);
    const [selectedExperiment, setSelectedExperiment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedExperiment, setLoadingSelectedExperiment] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredExperimentsIds, setFilteredExperimentsIds] = useState([]);

    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchExperiment = useCallback((experiment_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EXPERIMENTS_RESOURCE}/${experiment_id.value}`
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
                setSelectedExperiment(response)
                setLoadingSelectedExperiment(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);


    const fetchExperiments = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EXPERIMENTS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const experimentIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}, emulation: ${id_obj.emulation}`
                    }
                })
                setExperimentsIds(experimentIds)
                setFilteredExperimentsIds(experimentIds)
                setLoading(false)
                if (experimentIds.length > 0) {
                    setSelectedExperimentId(experimentIds[0])
                    fetchExperiment(experimentIds[0])
                    setLoadingSelectedExperiment(true)
                } else {
                    setLoadingSelectedExperiment(false)
                    setSelectedExperiment(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchExperiment, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeExperimentRequest = useCallback((experiment_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EXPERIMENTS_RESOURCE}/${experiment_id}`
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
                fetchExperiments()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchExperiments, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeAllExperimentsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EXPERIMENTS_RESOURCE}`
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
                fetchExperiments()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchExperiments, ip, navigate, port, props.sessionData.token, setSessionData]);

    const removeExperiment = (experiment) => {
        setLoading(true)
        removeExperimentRequest(experiment.id)
    }

    const refresh = () => {
        setLoading(true)
        fetchExperiments()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const removeAllExperiments = () => {
        setLoading(true)
        removeAllExperimentsRequest()
        setSelectedExperiment(null)
    }

    const updateSelectedExperimentId = (selectedId) => {
        setSelectedExperimentId(selectedId)
        fetchExperiment(selectedId)
        setLoadingSelectedExperiment(true)
    }

    useEffect(() => {
        setLoading(true)
        fetchExperiments()
    }, [fetchExperiments]);

    const removeAllExperimentsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all experiments? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllExperiments()
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
                                    Are you sure you want to delete all experiments? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllExperiments()
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

    const removeExperimentConfirm = (experiment) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the experiment with ID: ' + experiment.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeExperiment(experiment)
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
                                    Are you sure you want to delete the experiment with ID {experiment.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeExperiment(experiment)
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

    const DeleteAllExperimentsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllExperimentsTooltip}
                >
                    <Button variant="danger" onClick={removeAllExperimentsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectExperimentOrSpinner = (props) => {
        if (!props.loading && props.experimentIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No training runs are available</span>
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
                    <span className="spinnerLabel"> Fetching training runs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Training run:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedExperimentId}
                                defaultValue={props.selectedExperimentId}
                                options={props.experimentIds}
                                onChange={updateSelectedExperimentId}
                                placeholder="Select training run"
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

                    <DeleteAllExperimentsOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training runs from the backend
        </Tooltip>
    );

    const renderRemoveAllExperimentsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all training runs
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training runs
        </Tooltip>
    );

    const searchFilter = (experimentId, searchVal) => {
        return (searchVal === "" || experimentId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fExpIds = experimentsIds.filter(exp => {
            return searchFilter(exp, searchVal)
        });
        setFilteredExperimentsIds(fExpIds)

        var selectedExperimentRemoved = false
        if (!loadingSelectedExperiment && fExpIds.length > 0) {
            for (let i = 0; i < fExpIds.length; i++) {
                if (selectedExperiment !== null && selectedExperiment !== undefined &&
                    selectedExperiment.id === fExpIds[i].value) {
                    selectedExperimentRemoved = true
                }
            }
            if (!selectedExperimentRemoved) {
                setSelectedExperimentId(fExpIds[0])
                fetchExperiment(fExpIds[0])
                setLoadingSelectedExperiment(true)
            }
        } else {
            setSelectedExperiment(null)
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
                        Policy training
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Training policies using reinforcement learning</h4>
                    <p className="modalText">
                        Policies are trained through reinforcement learning in the simulation system.
                        Different reinforcement learning algorithms can be used, e.g. PPO, T-SPSA, DQN, etc.
                    </p>
                    <div className="text-center">
                        <img src={TrainingEnv} alt="TrainingEnv" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TrainingRunAccordion = (props) => {
        if (props.loadingSelectedExperiment || props.selectedExperiment === null || props.selectedExperiment === undefined) {
            if (props.loadingSelectedExperiment) {
                return (
                    <Spinner animation="border" role="status">
                        <span className="visually-hidden"></span>
                    </Spinner>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <h3 className="emulationConfigTitle">
                        Results of the selected training run:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <Experiment experiment={props.selectedExperiment} wrapper={wrapper}
                                    key={props.selectedExperiment.id}
                                    removeExperiment={removeExperimentConfirm}
                                    sessionData={props.sessionData}
                                    setSessionData={props.setSessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    return (
        <div className="TrainingResults">
            <h3 className="managementTitle"> Management of Training Results </h3>
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectExperimentOrSpinner loading={loading}
                                                   experimentIds={filteredExperimentsIds}
                                                   selectedExperimentId={selectedExperimentId}
                                                   sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
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
            <TrainingRunAccordion loadingSelectedExperiment={loadingSelectedExperiment}
                                  selectedExperiment={selectedExperiment}
                                  sessionData={props.sessionData}
                                  setSessionData={props.setSessionData}
            />
        </div>
    );
}

TrainingResults.propTypes = {};
TrainingResults.defaultProps = {};
export default TrainingResults;
