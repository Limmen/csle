import React, {useState, useCallback, useEffect, createRef} from 'react';
import './Jobs.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import TrainingJob from "./TrainingJob/TrainingJob";
import SystemIdentificationJob from "./SystemIdentificationJob/SystemIdentificationJob";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import debounce from 'lodash.debounce';

const Jobs = () => {
    const [showTrainingJobsInfoModal, setShowTrainingJobsInfoModal] = useState(false);
    const [trainingJobsLoading, setTrainingJobsLoading] = useState(false);
    const [trainingJobs, setTrainingJobs] = useState([]);
    const [filteredTrainingJobs, setFilteredTrainingJobs] = useState([]);
    const [showSystemIdentificationJobsInfoModal, setShowSystemIdentificationJobsInfoModal] = useState(false);
    const [systemIdentificationJobsLoading, setSystemIdentificationJobsLoading] = useState(false);
    const [systemIdentificationJobs, setSystemIdentificationJobs] = useState([]);
    const [showOnlyRunningTrainingJobs, setShowOnlyRunningTrainingJobs] = useState(false);
    const [filteredSystemIdentificationJobs, setFilteredSystemIdentificationJobs] = useState([]);
    const [showOnlyRunningSystemIdJobs, setShowOnlyRunningSystemIdJobs] = useState(false);
    const [trainingJobsSearchString, setTrainingJobsSearchString] = useState("");
    const [systemIdJobsSearchString, setSystemIdJobsSearchString] = useState("");

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
                setSystemIdentificationJobs(response);
                setFilteredSystemIdentificationJobs(response);
                setSystemIdentificationJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setTrainingJobsLoading(true)
        fetchTrainingJobs()
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobs()
    }, [fetchTrainingJobs, fetchSystemIdentificationJobs]);

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

    const removeTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        removeTrainingJobRequest(job.id)
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

    const trainingJobSearchFilter = (job, searchVal) => {
        return (searchVal === "" ||
            job.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.simulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.emulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.experiment_config.title.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1
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

    const runningSystemIdJobsChange = (event) => {
        if (!showOnlyRunningSystemIdJobs) {
            const filteredSystemIdJobs = filteredSystemIdentificationJobs.filter(job => {
                return job.running
            });
            setFilteredSystemIdentificationJobs(filteredSystemIdJobs)
        } else {
            const filteredSystemIdJobs = systemIdentificationJobs.filter(job => {
                return systemIdentificationJobSearchFilter(job, systemIdJobsSearchString)
            });
            setFilteredSystemIdentificationJobs(filteredSystemIdJobs)
        }
        setShowOnlyRunningSystemIdJobs(!showOnlyRunningSystemIdJobs)
    }


    const searchTrainingJobHandler = useCallback(debounce(searchTrainingJobChange, 350), []);

    const systemIdentificationJobSearchFilter = (job, searchVal) => {
        return (searchVal === "" ||
            job.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.descr.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.emulation_env_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            job.pid.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1
        );
    }

    const searchSystemIdJobChange = (event) => {
        var searchVal = event.target.value
        const filteredSystemIdJobs = systemIdentificationJobs.filter(job => {
            return systemIdentificationJobSearchFilter(job, searchVal)
        });
        setFilteredSystemIdentificationJobs(filteredSystemIdJobs)
        setSystemIdJobsSearchString(searchVal)
    }

    const searchSystemIdJobHandler = useCallback(debounce(searchSystemIdJobChange, 350), []);

    const removeSystemIdJobRequest = useCallback((sys_id_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/remove/' + sys_id_job_id,
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
        removeSystemIdJobRequest(job.id)
    }

    const stopSystemIdentificationJobRequest = useCallback((sys_id_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/stop/' + sys_id_job_id,
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

    const stopSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        stopSystemIdentificationJobRequest(job.id)
    }

    const startSystemIdentificationJobRequest = useCallback((sys_id_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/start/' + sys_id_job_id,
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

    const startSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        startSystemIdentificationJobRequest(job.id)
    }

    const refreshTrainingJobs = () => {
        setTrainingJobsLoading(true)
        fetchTrainingJobs()
    }

    const refreshSystemIdentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobs()
    }

    const renderTrainingJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training jobs
        </Tooltip>
    );

    const renderRefreshTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training jobs from the backend
        </Tooltip>
    );

    const renderSystemIdentificationJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the system identification jobs
        </Tooltip>
    );

    const renderRefreshSystemIdentificationJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload System identification jobs from the backend
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
                        System Identification Jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>System identification jobs</h4>
                    <p className="modalText">
                        A system identification job represents an ongoing execution of system identification.
                        The list of system identification jobs enables real-time monitoring of jobs.
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
                                                 startSystemIdentificationJob={startSystemIdentificationJob}
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
                    <h3> System identification jobs

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshSystemIdentificationJobsTooltip}
                        >
                            <Button variant="button" onClick={refreshSystemIdentificationJobs}>
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
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="systemIdJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="systemIdJobInput"
                                onChange={searchSystemIdJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                    <Form>
                        <Form.Check
                            inline
                            type="switch"
                            id="systemIdSwitch"
                            label="Show only running jobs"
                            className="runningCheck"
                            onChange={runningSystemIdJobsChange}
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
