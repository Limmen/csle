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
import { useDebouncedCallback } from 'use-debounce';

const Jobs = () => {
    const [showTrainingJobsInfoModal, setShowTrainingJobsInfoModal] = useState(false);
    const [trainingJobsLoading, setTrainingJobsLoading] = useState(false);
    const [trainingJobs, setTrainingJobs] = useState([]);
    const [filteredTrainingJobs, setFilteredTrainingJobs] = useState([]);
    const [showDataCollectionJobsInfoModal, setShowDataCollectionJobsInfoModal] = useState(false);
    const [dataCollectionJobsLoading, setDataCollectionJobsLoading] = useState(false);
    const [dataCollectionJobs, setDataCollectionJobs] = useState([]);
    const [showOnlyRunningTrainingJobs, setShowOnlyRunningTrainingJobs] = useState(false);
    const [filteredDataCollectionJobs, setFilteredDataCollectionJobs] = useState([]);
    const [showOnlyRunningDataCollectionJobs, setShowOnlyRunningDataCollectionJobs] = useState(false);
    const [trainingJobsSearchString, setTrainingJobsSearchString] = useState("");
    const [dataCollectionJobsSearchString, setDataCollectionJobsSearchString] = useState("");
    const [showSystemIdentificationJobsInfoModal, setShowSystemIdentificationJobsInfoModal] = useState(false);
    const [systemIdentificationJobsLoading, setSystemIdentificationJobsLoading] = useState(false);
    const [systemIdentificationJobs, setSystemIdentificationJobs] = useState([]);
    const [systemIdentificationJobsSearchString, setSystemIdentificationJobsSearchString] = useState("");
    const [filteredSystemIdentificationJobs, setFilteredSystemIdentificationJobs] = useState([]);
    const [showOnlyRunningSystemIdentificationJobs, setShowOnlyRunningSystemIdentificationJobs] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchTrainingJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/trainingjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobs(response);
                setFilteredTrainingJobs(response);
                setTrainingJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchDataCollectionJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobs(response);
                setFilteredDataCollectionJobs(response);
                setDataCollectionJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSystemIdentificationJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                console.log("got sysid jobs")
                console.log(response)
                setSystemIdentificationJobs(response);
                setFilteredSystemIdentificationJobs(response);
                setSystemIdentificationJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setTrainingJobsLoading(true)
        fetchTrainingJobs()
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobs()
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobs()
    }, [fetchTrainingJobs, fetchDataCollectionJobs]);

    const removeTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/remove/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllTrainingJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        removeTrainingJobRequest(job.id)
    }

    const removeAllTrainingJobs = () => {
        setTrainingJobsLoading(true)
        removeAllTrainingJobsRequest()
    }

    const removeSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/remove/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSystemIdentificationJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSystemIdentificationJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        removeSystemIdentificationJobRequest(job.id)
    }

    const removeAllSystemIdentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        removeAllSystemIdentificationJobsRequest()
    }

    const stopTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/stop/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        stopTrainingJobRequest(job.id)
    }

    const stopSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/stop/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        stopSystemIdentificationJobRequest(job.id)
    }

    const startTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/start/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        startTrainingJobRequest(job.id)
    }

    const startSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/start/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTrainingJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        startSystemIdentificationJobRequest(job.id)
    }

    const trainingJobSearchFilter = (job, searchVal) => {
        return (searchVal === "" ||
            job.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.simulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.emulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.experiment_config.title.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1
        );
    }

    const systemIdentificationJobSearchFilter = (job, searchVal) => {
        return (searchVal === "" ||
            job.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.emulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.system_identification_config.title.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1
        );
    }

    const searchTrainingJobChange = (event) => {
        var searchVal = event.target.value
        const filteredTrainingJobs = trainingJobs.filter(job => {
            return trainingJobSearchFilter(job, searchVal)
        });
        setFilteredTrainingJobs(filteredTrainingJobs)
        setTrainingJobsSearchString(trainingJobsSearchString)
    }

    const searchSystemIdentificationJobChange = (event) => {
        var searchVal = event.target.value
        const filteredSystemIdentificationJobs = systemIdentificationJobs.filter(job => {
            return systemIdentificationJobSearchFilter(job, searchVal)
        });
        setFilteredSystemIdentificationJobs(filteredSystemIdentificationJobs)
        setSystemIdentificationJobsSearchString(systemIdentificationJobsSearchString)
    }

    const runningTrainingJobsChange = (event) => {
        if(!showOnlyRunningTrainingJobs) {
            const filteredTrainJobs = filteredTrainingJobs.filter(job => {
                return job.running
            });
            setFilteredTrainingJobs(filteredTrainJobs)
        } else {
            const filteredTrainJobs = trainingJobs.filter(job => {
                return trainingJobSearchFilter(job, trainingJobsSearchString)
            });
            setFilteredTrainingJobs(filteredTrainJobs)
        }
        setShowOnlyRunningTrainingJobs(!showOnlyRunningTrainingJobs)
    }

    const runningDataCollectionJobsChange = (event) => {
        if (!showOnlyRunningDataCollectionJobs) {
            const filteredDataCollectionJobs = filteredDataCollectionJobs.filter(job => {
                return job.running
            });
            setFilteredDataCollectionJobs(filteredDataCollectionJobs)
        } else {
            const filteredDataCollectionJobs = dataCollectionJobs.filter(job => {
                return dataCollectionJobSearchFilter(job, dataCollectionJobsSearchString)
            });
            setFilteredDataCollectionJobs(filteredDataCollectionJobs)
        }
        setShowOnlyRunningDataCollectionJobs(!showOnlyRunningDataCollectionJobs)
    }

    const runningSystemIdentificationJobsChange = (event) => {
        if(!showOnlyRunningSystemIdentificationJobs) {
            const filteredSystemIdentificationJobs = filteredSystemIdentificationJobs.filter(job => {
                return job.running
            });
            setFilteredSystemIdentificationJobs(filteredSystemIdentificationJobs)
        } else {
            const filteredSystemIdentificationJobs = systemIdentificationJobs.filter(job => {
                return systemIdentificationJobSearchFilter(job, systemIdentificationJobsSearchString)
            });
            setFilteredSystemIdentificationJobs(filteredSystemIdentificationJobs)
        }
        setShowOnlyRunningSystemIdentificationJobs(!showOnlyRunningSystemIdentificationJobs)
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

    const dataCollectionJobSearchFilter = (job, searchVal) => {
        return (searchVal === "" ||
            job.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.descr.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.emulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.pid.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1
        );
    }

    const searchDataCollectionJobChange = (event) => {
        var searchVal = event.target.value
        const filteredDataCollectionJobs = dataCollectionJobs.filter(job => {
            return dataCollectionJobSearchFilter(job, searchVal)
        });
        setFilteredDataCollectionJobs(filteredDataCollectionJobs)
        setDataCollectionJobsSearchString(searchVal)
    }

    const searchDataCollectionJobHandler = useDebouncedCallback(
        (event) => {
            searchDataCollectionJobChange(event)
        },
        350
    );

    const removeDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/remove/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchDataCollectionJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllDataCollectionJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchDataCollectionJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        removeDataCollectionJobRequest(job.id)
    }

    const removeAllDataCollectionJobs = (job) => {
        setDataCollectionJobsLoading(true)
        removeAllDataCollectionJobsRequest()
    }

    const stopDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/stop/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchDataCollectionJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        stopDataCollectionJobRequest(job.id)
    }

    const startDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/start/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchDataCollectionJobs()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        startDataCollectionJobRequest(job.id)
    }

    const refreshTrainingJobs = () => {
        setTrainingJobsLoading(true)
        fetchTrainingJobs()
    }

    const refreshSystemidentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobs()
    }

    const refreshDataCollectionJobs = () => {
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobs()
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

    const TrainingJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Training jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Training jobs</h4>
                    <p className="modalText">
                        A training job represents an ongoing execution of training policies.
                        The list of training jobs enables real-time monitoring of jobs.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
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
                    <Modal.Title id="contained-modal-title-vcenter">
                        System identification jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>System identification jobs</h4>
                    <p className="modalText">
                        A system identification job represents an ongoing process for estimating a system model
                        for an emulation.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
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
                    <Modal.Title id="contained-modal-title-vcenter">
                        Data Collection Jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Data Collection jobs</h4>
                    <p className="modalText">
                        A data collection job represents an ongoing execution of data collection.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TrainingJobsAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.jobs.map((job, index) =>
                        <TrainingJob job={job} wrapper={wrapper} key={job.id + "-" + index}
                                     removeTrainingJob={removeTrainingJob} stopTrainingJob={stopTrainingJob}
                                     startTrainingJob={startTrainingJob}/>
                    )}
                </Accordion>
            )
        }
    }

    const SystemIdentificationJobsAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.jobs.map((job, index) =>
                        <SystemIdentificationJob job={job} wrapper={wrapper} key={job.id + "-" + index}
                                                 removeSystemIdentificationJob={removeSystemIdentificationJob}
                                                 stopSystemIdentificationJob={stopSystemIdentificationJob}
                                                 startSystemIdentificationJob={startSystemIdentificationJob}/>
                    )}
                </Accordion>
            )
        }
    }

    const DataCollectionJobsAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.jobs.map((job, index) =>
                        <DataCollectionJob job={job} wrapper={wrapper} key={job.id + "-" + index}
                                           removeDataCollectionJob={removeDataCollectionJob}
                                           stopDataCollectionJob={stopDataCollectionJob}
                                           startDataCollectionJob={startDataCollectionJob}
                        />
                    )}
                </Accordion>
            )
        }
    }

    return (
        <div className="policyExamination">
            <div className="row">
                <div className="col-sm-4"></div>
                <div className="col-sm-2">
                    <h3>
                        Training jobs

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
                            <Button variant="button" onClick={() => setShowTrainingJobsInfoModal(true)} className="infoButton2">
                                <i className="fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <TrainingJobsInfoModal show={showTrainingJobsInfoModal}
                                               onHide={() => setShowTrainingJobsInfoModal(false)}/>

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllTrainingJobsTooltip}
                        >
                            <Button variant="danger" onClick={removeAllTrainingJobs}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
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

            <TrainingJobsAccordions jobs={filteredTrainingJobs} loading={trainingJobsLoading}/>


            <div className="row systemIdentificationJobs">
                <div className="col-sm-3"></div>
                <div className="col-sm-3">
                    <h3> Data collection jobs

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

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllDataCollectionJobsTooltip}
                        >
                            <Button variant="danger" onClick={removeAllDataCollectionJobs}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
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
                            id="dataCollectionSwitch"
                            label="Show only running jobs"
                            className="runningCheck"
                            onChange={runningDataCollectionJobsChange}
                        />
                    </Form>
                </div>
            </div>
            <DataCollectionJobsAccordions jobs={filteredDataCollectionJobs}
                                                loading={dataCollectionJobsLoading}/>


            <div className="row systemIdentificationJobs">
                <div className="col-sm-3"></div>
                <div className="col-sm-3">
                    <h3>
                        System identification jobs

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
                            <Button variant="button" onClick={() => setShowSystemIdentificationJobsInfoModal(true)} className="infoButton2">
                                <i className="fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <SystemIdentificationJobsInfoModal show={showSystemIdentificationJobsInfoModal}
                                               onHide={() => setShowSystemIdentificationJobsInfoModal(false)}/>

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllSystemIdentificationJobsTooltip}
                        >
                            <Button variant="danger" onClick={removeAllSystemIdentificationJobs}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
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

            <SystemIdentificationJobsAccordions jobs={filteredSystemIdentificationJobs}
                                                loading={systemIdentificationJobsLoading}/>

        </div>
    );
}

Jobs.propTypes = {};
Jobs.defaultProps = {};
export default Jobs;
