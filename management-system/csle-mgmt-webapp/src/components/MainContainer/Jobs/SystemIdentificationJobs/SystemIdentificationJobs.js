import React, {useState, createRef, useCallback, useEffect} from 'react';
import './SystemIdentificationJobs.css';
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
import SystemIdentificationJob from "./SystemIdentificationJob/SystemIdentificationJob";
import 'react-confirm-alert/src/react-confirm-alert.css';
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
    SYSTEM_IDENTIFICATION_JOBS_RESOURCE, STOP_PROPERTY, HTTP_REST_POST
} from "../../../Common/constants";

/**
 * The component representing the system identification jobs on the /jobs-page page
 */
const SystemIdentificationJobs = (props) => {
    const [showSystemIdentificationJobsInfoModal, setShowSystemIdentificationJobsInfoModal] = useState(false);
    const [systemIdentificationJobsLoading, setSystemIdentificationJobsLoading] = useState(false);
    const [systemIdentificationJobsIds, setSystemIdentificationJobsIds] = useState([]);
    const [selectedSystemIdentificationJobId, setSelectedSystemIdentificationJobId] = useState(null);
    const [selectedSystemIdentificationJob, setSelectedSystemIdentificationJob] = useState(null);
    const [loadingSelectedSystemIdentificationJob, setLoadingSelectedSystemIdentificationJob] = useState(true);
    const [systemIdentificationJobsSearchString, setSystemIdentificationJobsSearchString] = useState("");
    const [filteredSystemIdentificationJobsIds, setFilteredSystemIdentificationJobsIds] = useState([]);
    const [showOnlyRunningSystemIdentificationJobs, setShowOnlyRunningSystemIdentificationJobs] = useState(false);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData
    const wrapper = createRef();

    const fetchSystemIdentificationJob = useCallback((system_identification_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}/` +
                `${system_identification_job_id.value}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedSystemIdentificationJob(response)
                setLoadingSelectedSystemIdentificationJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchSystemIdentificationJobsIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const systemIdentificationJobsIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (id_obj.running) {
                        lbl = `ID: ${id_obj.id}, emulation: ${id_obj.emulation} (running)`
                    } else {
                        lbl = `ID: ${id_obj.id}, emulation: ${id_obj.emulation}`
                    }
                    return {
                        value: id_obj.id,
                        label: lbl,
                        running: id_obj.running
                    }
                })
                setSystemIdentificationJobsIds(systemIdentificationJobsIds)
                setFilteredSystemIdentificationJobsIds(systemIdentificationJobsIds)
                setSystemIdentificationJobsLoading(false)
                if (systemIdentificationJobsIds.length > 0) {
                    setSelectedSystemIdentificationJobId(systemIdentificationJobsIds[0])
                    fetchSystemIdentificationJob(systemIdentificationJobsIds[0])
                    setLoadingSelectedSystemIdentificationJob(true)
                } else {
                    setLoadingSelectedSystemIdentificationJob(false)
                    setSelectedSystemIdentificationJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSystemIdentificationJob]);

    const removeSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}/${system_identification_job_id}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSystemIdentificationJobsIds]);

    const removeAllSystemIdentificationJobsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}`
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSystemIdentificationJobsIds]);

    const removeSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        removeSystemIdentificationJobRequest(job.id)
        setSelectedSystemIdentificationJob(null)
    }

    const removeAllSystemIdentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        removeAllSystemIdentificationJobsRequest()
        setSelectedSystemIdentificationJob(null)
    }

    const removeAllSystemIdentificationJobsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all system identification jobs? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllSystemIdentificationJobs()
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
                                    Are you sure you want to delete all system identification jobs?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllSystemIdentificationJobs()
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

    const removeSystemIdentificationJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the system identification job with ID: ' + job.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeSystemIdentificationJob(job)
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
                                    Are you sure you want to delete the system identification job with ID {job.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeSystemIdentificationJob(job)
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

    const stopSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}/${system_identification_job_id}`
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSystemIdentificationJobsIds]);

    const stopSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        stopSystemIdentificationJobRequest(job.id)
        setSelectedSystemIdentificationJob(null)
    }

    const startSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${SYSTEM_IDENTIFICATION_JOBS_RESOURCE}/${system_identification_job_id}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchSystemIdentificationJobsIds]);

    const startSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        startSystemIdentificationJobRequest(job.id)
    }

    const systemIdentificationJobSearchFilter = (job_id_obj, searchVal) => {
        return (searchVal === "" || job_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const searchSystemIdentificationJobChange = (event) => {
        var searchVal = event.target.value
        const filteredSIJobsIds = systemIdentificationJobsIds.filter(job => {
            return systemIdentificationJobSearchFilter(job, searchVal)
        });
        setFilteredSystemIdentificationJobsIds(filteredSIJobsIds)
        setSystemIdentificationJobsSearchString(systemIdentificationJobsSearchString)

        var selectedSystemIdentificationJobRemoved = false
        if (!loadingSelectedSystemIdentificationJob && filteredSIJobsIds.length > 0) {
            for (let i = 0; i < filteredSIJobsIds.length; i++) {
                if (selectedSystemIdentificationJob !== null && selectedSystemIdentificationJob !== undefined &&
                    selectedSystemIdentificationJob.id === filteredSIJobsIds[i].value) {
                    selectedSystemIdentificationJobRemoved = true
                }
            }
            if (!selectedSystemIdentificationJobRemoved) {
                setSelectedSystemIdentificationJobId(filteredSIJobsIds[0])
                fetchSystemIdentificationJob(filteredSIJobsIds[0])
                setLoadingSelectedSystemIdentificationJob(true)
            }
        } else {
            setSelectedSystemIdentificationJob(null)
        }
    }

    const runningSystemIdentificationJobsChange = (event) => {
        var filteredSIJobsIds = null
        if (!showOnlyRunningSystemIdentificationJobs) {
            filteredSIJobsIds = filteredSystemIdentificationJobsIds.filter(job => {
                return job.running
            });
            setFilteredSystemIdentificationJobsIds(filteredSIJobsIds)
        } else {
            filteredSIJobsIds = systemIdentificationJobsIds.filter(job => {
                return systemIdentificationJobSearchFilter(job, systemIdentificationJobsSearchString)
            });
            setFilteredSystemIdentificationJobsIds(filteredSIJobsIds)
        }
        setShowOnlyRunningSystemIdentificationJobs(!showOnlyRunningSystemIdentificationJobs)
        var selectedSystemIdentificationJobRemoved = false
        if (!loadingSelectedSystemIdentificationJob && filteredSIJobsIds.length > 0) {
            for (let i = 0; i < filteredSIJobsIds.length; i++) {
                if (selectedSystemIdentificationJob !== null && selectedSystemIdentificationJob !== undefined &&
                    selectedSystemIdentificationJob.id === filteredSIJobsIds[i].value) {
                    selectedSystemIdentificationJobRemoved = true
                }
            }
            if (!selectedSystemIdentificationJobRemoved) {
                setSelectedSystemIdentificationJobId(filteredSIJobsIds[0])
                fetchSystemIdentificationJob(filteredSIJobsIds[0])
                setLoadingSelectedSystemIdentificationJob(true)
            }
        } else {
            setSelectedSystemIdentificationJob(null)
        }
    }

    const searchSystemIdentificationJobHandler = useDebouncedCallback(
        (event) => {
            searchSystemIdentificationJobChange(event)
        },
        350
    );

    const refreshSystemidentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }

    const startSystemIdentificationJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm starting',
            message: 'Are you sure you want to start the system identification job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => startSystemIdentificationJob(job)
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
                                    Are you sure you want to start the system identification job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    startSystemIdentificationJob(job)
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

    const stopSystemIdentificationJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm stopping',
            message: 'Are you sure you want to stop the system identification job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => stopSystemIdentificationJob(job)
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
                                    Are you sure you want to stop the system identification job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    stopSystemIdentificationJob(job)
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
                );
            }
        })
    }

    const renderSystemIdentificationJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the system identification jobs
        </Tooltip>
    );

    const renderRemoveAllSystemIdentificationJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all system identification jobs.
        </Tooltip>
    );

    const renderRefreshSystemIdentificationJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload system identification jobs from the backend
        </Tooltip>
    );

    const updateSelectedSystemIdentificationJob = (selectedId) => {
        setSelectedSystemIdentificationJobId(selectedId)
        fetchSystemIdentificationJob(selectedId)
        setLoadingSelectedSystemIdentificationJob(true)
    }

    const DeleteAllSystemIdentificationJobsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllSystemIdentificationJobsTooltip}
                >
                    <Button variant="danger" onClick={removeAllSystemIdentificationJobsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }


    const SelectSystemIdentificationJobOrSpinner = (props) => {
        if (!props.systemIdentificationJobsLoading && props.systemIdentificationJobsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No system identification jobs are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshSystemIdentificationJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshSystemidentificationJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.systemIdentificationJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching system identification jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            System identification job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSystemIdentificationJobId}
                                defaultValue={props.selectedSystemIdentificationJobId}
                                options={props.systemIdentificationJobsIds}
                                onChange={updateSelectedSystemIdentificationJob}
                                placeholder="Select job"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshSystemIdentificationJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshSystemidentificationJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderSystemIdentificationJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowSystemIdentificationJobsInfoModal(true)}
                                className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <SystemIdentificationJobsInfoModal show={showSystemIdentificationJobsInfoModal}
                                                       onHide={() => setShowSystemIdentificationJobsInfoModal(false)}/>

                    <DeleteAllSystemIdentificationJobsOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const SystemIdentificationJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        System identification jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        A system identification job represents an ongoing process for estimating a system model
                        for an emulation.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SystemIdentificationJobAccordion = (props) => {
        if (props.loadingSelectedSystemIdentificationJob || props.selectedSystemIdentificationJob === null
            || props.selectedSystemIdentificationJob === undefined) {
            if (props.loadingSelectedSystemIdentificationJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected system identification job... </span>
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
                        Configuration of the selected system identification job:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <SystemIdentificationJob job={props.selectedSystemIdentificationJob} wrapper={wrapper}
                                                 key={props.selectedSystemIdentificationJob.id}
                                                 removeSystemIdentificationJob={removeSystemIdentificationJobConfirm}
                                                 stopSystemIdentificationJob={stopSystemIdentificationJobConfirm}
                                                 startSystemIdentificationJob={startSystemIdentificationJobConfirm}
                                                 sessionData={props.sessionData}
                                                 setSessionData={props.setSessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    useEffect(() => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }, [fetchSystemIdentificationJobsIds]);

    return (
        <div>
            <div className="row jobsContainer">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectSystemIdentificationJobOrSpinner
                            systemIdentificationJobsLoading={systemIdentificationJobsLoading}
                            systemIdentificationJobsIds={filteredSystemIdentificationJobsIds}
                            selectedSystemIdentificationJobId={selectedSystemIdentificationJobId}
                            sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="systemIdentificationJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="systemIdentificationJobInput"
                                onChange={searchSystemIdentificationJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                    <Form>
                        <Form.Check
                            inline
                            type="switch"
                            id="systemIdentificationJobSwitch"
                            label="Show only running jobs"
                            className="runningCheck"
                            onChange={runningSystemIdentificationJobsChange}
                        />
                    </Form>
                </div>
            </div>
            <SystemIdentificationJobAccordion selectedSystemIdentificationJob={selectedSystemIdentificationJob}
                                              loadingSelectedSystemIdentificationJob={loadingSelectedSystemIdentificationJob}
                                              sessionData={props.sessionData}
                                              setSessionData={props.setSessionData}/>
        </div>
    )
}

SystemIdentificationJobs.propTypes = {};
SystemIdentificationJobs.defaultProps = {};
export default SystemIdentificationJobs;
