import React, {useState, useCallback, useEffect, createRef} from 'react';
import './Jobs.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import TrainingJob from "./TrainingJob/TrainingJob";
import DataCollectionJob from "./DataCollectionJob/DataCollectionJob";
import SystemIdentificationJob from "./SystemIdentificationJob/SystemIdentificationJob";
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

/**
 * The component representing the /jobs-page
 */
const Jobs = (props) => {
    const [showTrainingJobsInfoModal, setShowTrainingJobsInfoModal] = useState(false);
    const [trainingJobsLoading, setTrainingJobsLoading] = useState(false);
    const [trainingJobs, setTrainingJobs] = useState([]);
    const [trainingJobsIds, setTrainingJobsIds] = useState([]);
    const [selectedTrainingJobId, setSelectedTrainingJobId] = useState(null);
    const [selectedTrainingJob, setSelectedTrainingJob] = useState(null);
    const [loadingSelectedTrainingJob, setLoadingSelectedTrainingJob] = useState(true);
    const [filteredTrainingJobsIds, setFilteredTrainingJobsIds] = useState([]);
    const [showDataCollectionJobsInfoModal, setShowDataCollectionJobsInfoModal] = useState(false);
    const [dataCollectionJobsLoading, setDataCollectionJobsLoading] = useState(false);
    const [dataCollectionJobs, setDataCollectionJobs] = useState([]);
    const [dataCollectionJobsIds, setDataCollectionJobsIds] = useState([]);
    const [selectedDataCollectionJobId, setSelectedDataCollectionJobId] = useState(null);
    const [selectedDataCollectionJob, setSelectedDataCollectionJob] = useState(null);
    const [loadingSelectedDataCollectionJob, setLoadingSelectedDataCollectionJob] = useState(true);
    const [showOnlyRunningTrainingJobs, setShowOnlyRunningTrainingJobs] = useState(false);
    const [filteredDataCollectionJobsIds, setFilteredDataCollectionJobsIds] = useState([]);
    const [showOnlyRunningDataCollectionJobs, setShowOnlyRunningDataCollectionJobs] = useState(false);
    const [trainingJobsSearchString, setTrainingJobsSearchString] = useState("");
    const [dataCollectionJobsSearchString, setDataCollectionJobsSearchString] = useState("");
    const [showSystemIdentificationJobsInfoModal, setShowSystemIdentificationJobsInfoModal] = useState(false);
    const [systemIdentificationJobsLoading, setSystemIdentificationJobsLoading] = useState(false);
    const [systemIdentificationJobs, setSystemIdentificationJobs] = useState([]);
    const [systemIdentificationJobsIds, setSystemIdentificationJobsIds] = useState([]);
    const [selectedSystemIdentificationJobId, setSelectedSystemIdentificationJobId] = useState(null);
    const [selectedSystemIdentificationJob, setSelectedSystemIdentificationJob] = useState(null);
    const [loadingSelectedSystemIdentificationJob, setLoadingSelectedSystemIdentificationJob] = useState(true);
    const [systemIdentificationJobsSearchString, setSystemIdentificationJobsSearchString] = useState("");
    const [filteredSystemIdentificationJobsIds, setFilteredSystemIdentificationJobsIds] = useState([]);
    const [showOnlyRunningSystemIdentificationJobs, setShowOnlyRunningSystemIdentificationJobs] = useState(false);

    const ip = serverIp
    const alert = useAlert();
    const navigate = useNavigate();
    // const ip = "172.31.212.92"

    const fetchTrainingJobsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/training-jobs?ids=true' + "&token=" + props.sessionData.token,
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
                const trainingJobsIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (id_obj.running) {
                        lbl = "ID: " + id_obj.id + ", simulation: " + id_obj.simulation + ", emulation: " + id_obj.emulation + " (running)"
                    } else {
                        lbl = "ID: " + id_obj.id + ", simulation: " + id_obj.simulation + ", emulation: " + id_obj.emulation
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
    }, []);


    const fetchDataCollectionJobIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/data-collection-jobs?ids=true' + "&token=" + props.sessionData.token,
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
                const dataCollectionJobIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (id_obj.running) {
                        lbl = "ID: " + id_obj.id + ", emulation: " + id_obj.emulation + " (running)"
                    } else {
                        lbl = "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
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
    }, []);


    const fetchSystemIdentificationJobsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/system-identification-jobs?ids=true' + "&token=" + props.sessionData.token,
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
                const systemIdentificationJobsIds = response.map((id_obj, index) => {
                    var lbl = ""
                    if (id_obj.running) {
                        lbl = "ID: " + id_obj.id + ", emulation: " + id_obj.emulation + " (running)"
                    } else {
                        lbl = "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
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
    }, []);

    useEffect(() => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }, [fetchTrainingJobsIds, fetchDataCollectionJobIds, fetchSystemIdentificationJobsIds]);

    const removeTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/training-jobs/' + training_job_id + "?token=" + props.sessionData.token,
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllTrainingJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/training-jobs' + "?token=" + props.sessionData.token,
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

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

    const removeSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`http://` + ip + ':7777/system-identification-jobs/' + system_identification_job_id +
            "?token=" + props.sessionData.token),
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSystemIdentificationJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/system-identification-jobs' + "?token=" + props.sessionData.token,
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

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

    const stopTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            (`http://` + ip + ':7777/training-jobs/' + training_job_id + "?stop=true" + "&token="
                + props.sessionData.token),
            {
                method: "POST",
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
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTrainingJob = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/training-jobs/' + training_job_id.value + "?token=" + props.sessionData.token,
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
                setSelectedTrainingJob(response)
                setLoadingSelectedTrainingJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        stopTrainingJobRequest(job.id)
        setSelectedTrainingJob(null)
    }

    const stopSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`http://` + ip + ':7777/system-identification-jobs/' + system_identification_job_id + "?stop=true" +
                "&token=" + props.sessionData.token),
            {
                method: "POST",
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSystemIdentificationJob = useCallback((system_identification_job_id) => {
        fetch(
            (`http://` + ip + ':7777/system-identification-jobs/' + system_identification_job_id.value +
            "?token=" + props.sessionData.token),
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
                setSelectedSystemIdentificationJob(response)
                setLoadingSelectedSystemIdentificationJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        stopSystemIdentificationJobRequest(job.id)
        setSelectedSystemIdentificationJob(null)
    }

    const startTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/training-jobs/' + training_job_id + "?token=" + props.sessionData.token,
            {
                method: "POST",
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
                setTrainingJobsLoading()
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        startTrainingJobRequest(job.id)
    }

    const startSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            (`http://` + ip + ':7777/system-identification-jobs/' + system_identification_job_id +
                "?token=" + props.sessionData.token),
            {
                method: "POST",
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
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        startSystemIdentificationJobRequest(job.id)
    }

    const trainingJobSearchFilter = (job_id_obj, searchVal) => {
        return (searchVal === "" || job_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const systemIdentificationJobSearchFilter = (job_id_obj, searchVal) => {
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

    const searchTrainingJobHandler = useDebouncedCallback(
        (event) => {
            searchTrainingJobChange(event)
        },
        350
    );

    const searchSystemIdentificationJobHandler = useDebouncedCallback(
        (event) => {
            searchSystemIdentificationJobChange(event)
        },
        350
    );

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
            (`http://` + ip + ':7777/data-collection-jobs/' + data_collection_job_id +
            "?token=" + props.sessionData.token),
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
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllDataCollectionJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/data-collection-jobs' + "?token=" + props.sessionData.token,
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
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

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
            (`http://` + ip + ':7777/data-collection-jobs/' + data_collection_job_id + "?stop=true"
            + "&token=" + props.sessionData.token),
            {
                method: "POST",
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
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchDataCollectionJob = useCallback((data_collection_job_id) => {
        fetch(
            (`http://` + ip + ':7777/data-collection-jobs/' + data_collection_job_id.value +
            "?token=" + props.sessionData.token),
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
                setSelectedDataCollectionJob(response)
                setLoadingSelectedDataCollectionJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        setSelectedDataCollectionJob(null)
        stopDataCollectionJobRequest(job.id)
    }

    const startDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            (`http://` + ip + ':7777/data-collection-jobs/' + data_collection_job_id +
            "?token=" + props.sessionData.token),
            {
                method: "POST",
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
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        startDataCollectionJobRequest(job.id)
    }

    const refreshTrainingJobs = () => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
    }

    const refreshSystemidentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }

    const refreshDataCollectionJobs = () => {
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
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

    const renderRemoveAllDataCollectionJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all data collection jobs.
        </Tooltip>
    );

    const renderRefreshTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training jobs from the backend
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

    const updateSelectedTrainingJobId = (selectedId) => {
        setSelectedTrainingJobId(selectedId)
        fetchTrainingJob(selectedId)
        setLoadingSelectedTrainingJob(true)
    }

    const updateSelectedDataCollectionJobId = (selectedId) => {
        setSelectedDataCollectionJobId(selectedId)
        fetchDataCollectionJob(selectedId)
        setLoadingSelectedDataCollectionJob(true)
    }

    const updateSelectedSystemIdentificationJob = (selectedId) => {
        setSelectedSystemIdentificationJobId(selectedId)
        fetchSystemIdentificationJob(selectedId)
        setLoadingSelectedSystemIdentificationJob(true)
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
                            Selected training job:
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
                            Selected data collection job:
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
                            Selected system identification job:
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

    const wrapper = createRef();

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

    return (
        <div className="jobs">
            <h3 className="managementTitle"> Management of Jobs </h3>
            <div className="row">
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


            <div className="row systemIdentificationJobs">
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


            <div className="row systemIdentificationJobs">
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
    );
}

Jobs.propTypes = {};
Jobs.defaultProps = {};
export default Jobs;
