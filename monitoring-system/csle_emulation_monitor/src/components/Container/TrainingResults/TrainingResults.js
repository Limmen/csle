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
import debounce from 'lodash.debounce';

const TrainingResults = () => {
    const [experiments, setExperiments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredExperiments, setFilteredExperiments] = useState([]);
    const [searchString, setSearchString] = useState("");

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchExperiments = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/experimentsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                console.log(response)
                setExperiments(response);
                setFilteredExperiments(response)
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchExperiments()
    }, [fetchExperiments]);

    const removeExperimentRequest = useCallback((experiment_id) => {
        fetch(
            `http://` + ip + ':7777/experimentsdata/remove/' + experiment_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchExperiments()
            })
            .catch(error => console.log("error:" + error))
    }, []);

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

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training runs from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training runs
        </Tooltip>
    );

    const searchFilter = (experiment, searchVal) => {
        return (searchVal === "" ||
            experiment.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            experiment.descr.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            experiment.simulation_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fExp = experiments.filter(exp => {
            return searchFilter(exp, searchVal)
        });
        setFilteredExperiments(fExp)
        setSearchString(searchVal)
    }

    const searchHandler = useCallback(debounce(searchChange, 350), []);

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
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
                        <img src={TrainingEnv} alt="Emulated infrastructures"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TrainingRunAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.experiments.map((experiment, index) =>
                        <Experiment experiment={experiment} wrapper={wrapper} key={experiment.id + "-" + index}
                                    removeExperiment={removeExperiment}
                        />
                    )}
                </Accordion>
            )
        }
    }

    return (
        <div className="TrainingResults">
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3 className="text-center inline-block experimentsHeader"> Training runs

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
                    </h3>
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
                <div className="col-sm-2"></div>
            </div>
            <TrainingRunAccordions loading={loading} experiments={filteredExperiments}/>
        </div>
    );
}

TrainingResults.propTypes = {};
TrainingResults.defaultProps = {};
export default TrainingResults;
