import React, {useState, createRef, useCallback, useEffect} from 'react';
import './TrainingJobs.css';
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
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import TrainingJob from "./TrainingJob/TrainingJob";
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import {
    HTTP_PREFIX, HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM,
    TRAINING_JOBS_RESOURCE, STOP_PROPERTY, HTTP_REST_POST
} from "../../../Common/constants";

/**
 * The component representing the training jobs on the /jobs-page page
 */
const TrainingJobs = (props) => {
    const [showTrainingJobsInfoModal, setShowTrainingJobsInfoModal] = useState(false);
    const [trainingJobsLoading, setTrainingJobsLoading] = useState(false);
    const [trainingJobsIds, setTrainingJobsIds] = useState([]);
    const [selectedTrainingJobId, setSelectedTrainingJobId] = useState(null);
    const [selectedTrainingJob, setSelectedTrainingJob] = useState(null);
    const [loadingSelectedTrainingJob, setLoadingSelectedTrainingJob] = useState(true);
    const [filteredTrainingJobsIds, setFilteredTrainingJobsIds] = useState([]);
    const [showOnlyRunningTrainingJobs, setShowOnlyRunningTrainingJobs] = useState(false);
    const [trainingJobsSearchString, setTrainingJobsSearchString] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData
    const wrapper = createRef();


    const fetchTrainingJob = useCallback((training_job_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}/${training_job_id.value}`
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
                setSelectedTrainingJob(response)
                setLoadingSelectedTrainingJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchTrainingJobsIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const trainingJobsIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (id_obj.running) {
                        lbl = `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
                            + `, emulation: ${id_obj.emulation} (running)`
                    } else {
                        lbl = `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
                            + `, emulation: ${id_obj.emulation}`
                    }
                    return {
                        value: id_obj.id,
                        label: lbl,
                        running: id_obj.running
                    }
                })
                setTrainingJobsIds(trainingJobsIds)
                setFilteredTrainingJobsIds(trainingJobsIds)
                setTrainingJobsLoading(false)
                if (trainingJobsIds.length > 0) {
                    setSelectedTrainingJobId(trainingJobsIds[0])
                    fetchTrainingJob(trainingJobsIds[0])
                    setLoadingSelectedTrainingJob(true)
                } else {
                    setLoadingSelectedTrainingJob(false)
                    setSelectedTrainingJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTrainingJob]);

    const removeTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}/${training_job_id}`
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTrainingJobsIds]);

    const removeAllTrainingJobsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}`
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTrainingJobsIds]);

    const removeTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        removeTrainingJobRequest(job.id)
        setSelectedTrainingJobId(null)
    }

    const removeAllTrainingJobs = () => {
        setTrainingJobsLoading(true)
        removeAllTrainingJobsRequest()
        setSelectedTrainingJob(null)
    }

    const removeAllTrainingJobsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all training jobs? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllTrainingJobs()
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
                                    Are you sure you want to delete all training jobs? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllTrainingJobs()
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

    const removeTrainingJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the training job with ID: ' + job.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeTrainingJob(job)
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
                                    Are you sure you want to delete the training job with ID {job.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeTrainingJob(job)
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

    const stopTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}/${training_job_id}`
                + `?${STOP_PROPERTY}=true&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_POST,
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTrainingJobsIds]);


    const stopTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        stopTrainingJobRequest(job.id)
        setSelectedTrainingJob(null)
    }

    const startTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRAINING_JOBS_RESOURCE}/${training_job_id}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_POST,
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
                setTrainingJobsLoading()
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTrainingJobsIds]);

    const startTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        startTrainingJobRequest(job.id)
    }

    const trainingJobSearchFilter = (job_id_obj, searchVal) => {
        return (searchVal === "" || job_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const searchTrainingJobChange = (event) => {
        var searchVal = event.target.value
        const filteredTJobIds = trainingJobsIds.filter(job => {
            return trainingJobSearchFilter(job, searchVal)
        });
        setFilteredTrainingJobsIds(filteredTJobIds)
        setTrainingJobsSearchString(trainingJobsSearchString)

        var selectedTrainingJobRemoved = false
        if (!loadingSelectedTrainingJob && filteredTJobIds.length > 0) {
            for (let i = 0; i < filteredTJobIds.length; i++) {
                if (selectedTrainingJob !== null && selectedTrainingJob !== undefined &&
                    selectedTrainingJob.id === filteredTJobIds[i].value) {
                    selectedTrainingJobRemoved = true
                }
            }
            if (!selectedTrainingJobRemoved) {
                setSelectedTrainingJobId(filteredTJobIds[0])
                fetchTrainingJob(filteredTJobIds[0])
                setLoadingSelectedTrainingJob(true)
            }
        } else {
            setSelectedTrainingJob(null)
        }
    }

    const runningTrainingJobsChange = (event) => {
        var filteredTJobIds = null
        if (!showOnlyRunningTrainingJobs) {
            filteredTJobIds = filteredTrainingJobsIds.filter(job => {
                return job.running
            });
            setFilteredTrainingJobsIds(filteredTJobIds)
        } else {
            filteredTJobIds = trainingJobsIds.filter(job => {
                return trainingJobSearchFilter(job, trainingJobsSearchString)
            });
            setFilteredTrainingJobsIds(filteredTJobIds)
        }
        setShowOnlyRunningTrainingJobs(!showOnlyRunningTrainingJobs)

        var selectedTrainingJobRemoved = false
        if (!loadingSelectedTrainingJob && filteredTJobIds.length > 0) {
            for (let i = 0; i < filteredTJobIds.length; i++) {
                if (selectedTrainingJob !== null && selectedTrainingJob !== undefined &&
                    selectedTrainingJob.id === filteredTJobIds[i].value) {
                    selectedTrainingJobRemoved = true
                }
            }
            if (!selectedTrainingJobRemoved) {
                setSelectedTrainingJobId(filteredTJobIds[0])
                fetchTrainingJob(filteredTJobIds[0])
                setLoadingSelectedTrainingJob(true)
            }
        } else {
            setSelectedTrainingJob(null)
        }
    }

    const searchTrainingJobHandler = useDebouncedCallback(
        (event) => {
            searchTrainingJobChange(event)
        },
        350
    );

    const refreshTrainingJobs = () => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
    }

    const startTrainingJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm starting',
            message: 'Are you sure you want to start the training job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => startTrainingJob(job)
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
                                    <h1>Confirm starting job</h1>
                                    Are you sure you want to start the training job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    startTrainingJob(job)
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
                );
            }
        })
    }

    const stopTrainingJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm stopping',
            message: 'Are you sure you want to stop the training job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => stopTrainingJob(job)
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
                                    <h1>Confirm stopping job</h1>
                                    Are you sure you want to stop the training job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    stopTrainingJob(job)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, stop it.</span>
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

    const renderTrainingJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training jobs
        </Tooltip>
    );

    const renderRemoveAllTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all training jobs.
        </Tooltip>
    );

    const renderRefreshTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training jobs from the backend
        </Tooltip>
    );

    const updateSelectedTrainingJobId = (selectedId) => {
        setSelectedTrainingJobId(selectedId)
        fetchTrainingJob(selectedId)
        setLoadingSelectedTrainingJob(true)
    }

    const DeleteAllTrainingJobsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllTrainingJobsTooltip}
                >
                    <Button variant="danger" onClick={removeAllTrainingJobsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectTrainingJobOrSpinner = (props) => {
        if (!props.trainingJobsLoading && props.trainingJobsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No training jobs are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTrainingJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshTrainingJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.trainingJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching training jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Training job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedTrainingJobId}
                                defaultValue={props.selectedTrainingJobId}
                                options={props.trainingJobsIds}
                                onChange={updateSelectedTrainingJobId}
                                placeholder="Select job"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTrainingJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshTrainingJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderTrainingJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowTrainingJobsInfoModal(true)}
                                className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <TrainingJobsInfoModal show={showTrainingJobsInfoModal}
                                           onHide={() => setShowTrainingJobsInfoModal(false)}/>

                    <DeleteAllTrainingJobsOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const TrainingJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Training jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        A training job represents an ongoing execution of training policies.
                        The list of training jobs enables real-time monitoring of jobs.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const TrainingJobAccordion = (props) => {
        if (props.loadingSelectedTrainingJob || props.selectedTrainingJob === null || props.selectedTrainingJob === undefined) {
            if (props.loadingSelectedTrainingJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected training job... </span>
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
                        Configuration of the selected training job:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <TrainingJob job={props.selectedTrainingJob} wrapper={wrapper}
                                     key={props.selectedTrainingJob.id}
                                     removeTrainingJob={removeTrainingJobConfirm}
                                     stopTrainingJob={stopTrainingJobConfirm}
                                     startTrainingJob={startTrainingJobConfirm}
                                     sessionData={props.sessionData}
                                     setSessionData={props.setSessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }


    useEffect(() => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
    }, [fetchTrainingJobsIds]);

    return (
        <div>
            <div className="row jobsContainer">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectTrainingJobOrSpinner trainingJobsLoading={trainingJobsLoading}
                                                    trainingJobsIds={filteredTrainingJobsIds}
                                                    selectedTrainingJobId={selectedTrainingJobId}
                                                    sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="trainingJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="trainingJobInput"
                                onChange={searchTrainingJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                    <Form>
                        <Form.Check
                            inline
                            type="switch"
                            id="trainingSwitch"
                            label="Show only running jobs"
                            className="runningCheck"
                            onChange={runningTrainingJobsChange}
                        />
                    </Form>
                </div>
            </div>

            <TrainingJobAccordion loadingSelectedTrainingJob={loadingSelectedTrainingJob}
                                  selectedTrainingJob={selectedTrainingJob}
                                  sessionData={props.sessionData}
                                  setSessionData={props.setSessionData}/>
        </div>
    )
}

TrainingJobs.propTypes = {};
TrainingJobs.defaultProps = {};
export default TrainingJobs;
