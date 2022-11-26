import React, {useState, createRef, useCallback, useEffect} from 'react';
import './DataCollectionJobs.css';
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
import DataCollectionJob from "./DataCollectionJob/DataCollectionJob";
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import {
    DATA_COLLECTION_JOBS_RESOURCE,
    HTTP_PREFIX, HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM, STOP_PROPERTY, HTTP_REST_POST
} from "../../../Common/constants";

/**
 * The component representing the data collection jobs on the /jobs-page page
 */
const DataCollectionJobs = (props) => {
    const [showDataCollectionJobsInfoModal, setShowDataCollectionJobsInfoModal] = useState(false);
    const [dataCollectionJobsLoading, setDataCollectionJobsLoading] = useState(false);
    const [dataCollectionJobsIds, setDataCollectionJobsIds] = useState([]);
    const [selectedDataCollectionJobId, setSelectedDataCollectionJobId] = useState(null);
    const [selectedDataCollectionJob, setSelectedDataCollectionJob] = useState(null);
    const [loadingSelectedDataCollectionJob, setLoadingSelectedDataCollectionJob] = useState(true);
    const [filteredDataCollectionJobsIds, setFilteredDataCollectionJobsIds] = useState([]);
    const [showOnlyRunningDataCollectionJobs, setShowOnlyRunningDataCollectionJobs] = useState(false);
    const [dataCollectionJobsSearchString, setDataCollectionJobsSearchString] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData
    const wrapper = createRef();

    const fetchDataCollectionJob = useCallback((data_collection_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}/${data_collection_job_id.value}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedDataCollectionJob(response)
                setLoadingSelectedDataCollectionJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);


    const fetchDataCollectionJobIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const dataCollectionJobIds = response.map((id_obj, index) => {
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
                setDataCollectionJobsIds(dataCollectionJobIds)
                setFilteredDataCollectionJobsIds(dataCollectionJobIds)
                setDataCollectionJobsLoading(false)
                if (dataCollectionJobIds.length > 0) {
                    setSelectedDataCollectionJobId(dataCollectionJobIds[0])
                    fetchDataCollectionJob(dataCollectionJobIds[0])
                    setLoadingSelectedDataCollectionJob(true)
                } else {
                    setLoadingSelectedDataCollectionJob(false)
                    setSelectedDataCollectionJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchDataCollectionJob]);

    const runningDataCollectionJobsChange = (event) => {
        var filteredDCJobsIds = null
        if (!showOnlyRunningDataCollectionJobs) {
            filteredDCJobsIds = filteredDataCollectionJobsIds.filter(job => {
                return job.running
            });
            setFilteredDataCollectionJobsIds(filteredDCJobsIds)
        } else {
            filteredDCJobsIds = dataCollectionJobsIds.filter(job => {
                return dataCollectionJobSearchFilter(job, dataCollectionJobsSearchString)
            });
            setFilteredDataCollectionJobsIds(filteredDCJobsIds)
        }
        setShowOnlyRunningDataCollectionJobs(!showOnlyRunningDataCollectionJobs)

        var selectedDataCollectionJobRemoved = false
        if (!loadingSelectedDataCollectionJob && filteredDCJobsIds.length > 0) {
            for (let i = 0; i < filteredDCJobsIds.length; i++) {
                if (selectedDataCollectionJob !== null && selectedDataCollectionJob !== undefined &&
                    selectedDataCollectionJob.id === filteredDCJobsIds[i].value) {
                    selectedDataCollectionJobRemoved = true
                }
            }
            if (!selectedDataCollectionJobRemoved) {
                setSelectedDataCollectionJobId(filteredDCJobsIds[0])
                fetchDataCollectionJob(filteredDCJobsIds[0])
                setLoadingSelectedDataCollectionJob(true)
            }
        } else {
            setSelectedDataCollectionJob(null)
        }
    }

    const dataCollectionJobSearchFilter = (job_id, searchVal) => {
        return (searchVal === "" || job_id.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const searchDataCollectionJobChange = (event) => {
        var searchVal = event.target.value
        const filteredDCJobsIds = dataCollectionJobsIds.filter(job_id => {
            return dataCollectionJobSearchFilter(job_id, searchVal)
        });
        setFilteredDataCollectionJobsIds(filteredDCJobsIds)
        setDataCollectionJobsSearchString(searchVal)

        var selectedDataCollectionJobRemoved = false
        if (!loadingSelectedDataCollectionJob && filteredDCJobsIds.length > 0) {
            for (let i = 0; i < filteredDCJobsIds.length; i++) {
                if (selectedDataCollectionJob !== null && selectedDataCollectionJob !== undefined &&
                    selectedDataCollectionJob.id === filteredDCJobsIds[i].value) {
                    selectedDataCollectionJobRemoved = true
                }
            }
            if (!selectedDataCollectionJobRemoved) {
                setSelectedDataCollectionJobId(filteredDCJobsIds[0])
                fetchDataCollectionJob(filteredDCJobsIds[0])
                setLoadingSelectedDataCollectionJob(true)
            }
        } else {
            setSelectedDataCollectionJob(null)
        }
    }

    const searchDataCollectionJobHandler = useDebouncedCallback(
        (event) => {
            searchDataCollectionJobChange(event)
        },
        350
    );

    const removeDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}/${data_collection_job_id}` +
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
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchDataCollectionJobIds]);

    const removeAllDataCollectionJobsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}`
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
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchDataCollectionJobIds]);

    const removeDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        removeDataCollectionJobRequest(job.id)
        setSelectedDataCollectionJob(null)
    }

    const removeAllDataCollectionJobs = () => {
        setDataCollectionJobsLoading(true)
        removeAllDataCollectionJobsRequest()
        setSelectedDataCollectionJob(null)
    }

    const removeAllDataCollectionJobsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all data collection jobs? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllDataCollectionJobs()
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
                                    Are you sure you want to delete all data collection jobs?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllDataCollectionJobs()
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

    const removeDataCollectionJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the data collection job with ID: ' + job.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeDataCollectionJob(job)
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
                                    Are you sure you want to delete the data collection job with ID {job.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeDataCollectionJob(job)
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

    const stopDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}/${data_collection_job_id}`
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
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchDataCollectionJobIds]);

    const stopDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        setSelectedDataCollectionJob(null)
        stopDataCollectionJobRequest(job.id)
    }

    const startDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${DATA_COLLECTION_JOBS_RESOURCE}/${data_collection_job_id}` +
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
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchDataCollectionJobIds]);

    const startDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        startDataCollectionJobRequest(job.id)
    }

    const refreshDataCollectionJobs = () => {
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
    }

    const startDataCollectionJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm starting',
            message: 'Are you sure you want to start the data collection job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => startDataCollectionJob(job)
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
                                    Are you sure you want to start the data collection job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    startDataCollectionJob(job)
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

    const stopDataCollectionJobConfirm = (job) => {
        confirmAlert({
            title: 'Confirm stopping',
            message: 'Are you sure you want to stop the data collection job with ID: ' + job.id +
                "?",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => stopDataCollectionJob(job)
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
                                    Are you sure you want to stop the data collection job with ID {job.id}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    stopDataCollectionJob(job)
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

    const renderRemoveAllDataCollectionJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all data collection jobs.
        </Tooltip>
    );

    const renderDataCollectionJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the data collection jobs
        </Tooltip>
    );

    const renderRefreshDataCollectionJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload data collection jobs from the backend
        </Tooltip>
    );

    const updateSelectedDataCollectionJobId = (selectedId) => {
        setSelectedDataCollectionJobId(selectedId)
        fetchDataCollectionJob(selectedId)
        setLoadingSelectedDataCollectionJob(true)
    }

    const DeleteAllDataCollectionJobsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllDataCollectionJobsTooltip}
                >
                    <Button variant="danger" onClick={removeAllDataCollectionJobsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectDataCollectionJobOrSpinner = (props) => {
        if (!props.dataCollectionJobsLoading && props.dataCollectionJobsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No data collection jobs are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshDataCollectionJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshDataCollectionJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.dataCollectionJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching data collection jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Data collection job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedDataCollectionJobId}
                                defaultValue={props.selectedDataCollectionJobId}
                                options={props.dataCollectionJobsIds}
                                onChange={updateSelectedDataCollectionJobId}
                                placeholder="Select job"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshDataCollectionJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshDataCollectionJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderDataCollectionJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowDataCollectionJobsInfoModal(true)}
                                className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <DataCollectionJobsInfoModal show={showDataCollectionJobsInfoModal}
                                                 onHide={() => setShowDataCollectionJobsInfoModal(false)}/>

                    <DeleteAllDataCollectionJobsOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DataCollectionJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Data Collection Jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        A data collection job represents an ongoing execution of data collection.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const DataCollectionJobAccordion = (props) => {
        if (props.loadingSelectedDataCollectionJob || props.selectedDataCollectionJob === null ||
            props.selectedDataCollectionJob === undefined) {
            if (props.loadingSelectedDataCollectionJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected data collection job... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>
                )
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected data collection job:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <DataCollectionJob job={props.selectedDataCollectionJob} wrapper={wrapper}
                                           key={props.selectedDataCollectionJob.id}
                                           removeDataCollectionJob={removeDataCollectionJobConfirm}
                                           stopDataCollectionJob={stopDataCollectionJobConfirm}
                                           startDataCollectionJob={startDataCollectionJobConfirm}
                                           sessionData={props.sessionData}
                                           setSessionData={props.setSessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    useEffect(() => {
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
    }, [fetchDataCollectionJobIds]);

    return (
        <div>
            <div className="row jobsContainer">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectDataCollectionJobOrSpinner dataCollectionJobsLoading={dataCollectionJobsLoading}
                                                          dataCollectionJobsIds={filteredDataCollectionJobsIds}
                                                          selectedDataCollectionJobId={selectedDataCollectionJobId}
                                                          sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="dataCollectionJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="dataCollectionJobInput"
                                onChange={searchDataCollectionJobHandler}
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
                            onChange={runningDataCollectionJobsChange}
                        />
                    </Form>
                </div>
            </div>
            <DataCollectionJobAccordion selectedDataCollectionJob={selectedDataCollectionJob}
                                        loadingSelectedDataCollectionJob={loadingSelectedDataCollectionJob}
                                        sessionData={props.sessionData}
                                        setSessionData={props.setSessionData}/>
        </div>
    )
}

DataCollectionJobs.propTypes = {};
DataCollectionJobs.defaultProps = {};
export default DataCollectionJobs;
