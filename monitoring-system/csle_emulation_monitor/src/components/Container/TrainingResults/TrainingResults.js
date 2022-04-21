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

const TrainingResults = () => {
    const [experiments, setExperiments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
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
                setExperiments(response);
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
            <TrainingRunAccordions loading={loading} experiments={experiments}/>
        </div>
    );
}

TrainingResults.propTypes = {};
TrainingResults.defaultProps = {};
export default TrainingResults;
