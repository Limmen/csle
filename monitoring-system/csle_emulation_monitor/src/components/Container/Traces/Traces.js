import React, {useState, useEffect, useCallback, createRef} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import Modal from 'react-bootstrap/Modal'
import EmulationTrace from "./EmulationTrace/EmulationTrace";
import SimulationTrace from "./SimulationTrace/SimulationTrace";
import TraceImg from './TracesLoop.png'
import './Traces.css';

const Traces = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [emulationTraces, setEmulationTraces] = useState([]);
    const [simulationTraces, setSimulationTraces] = useState([]);
    const [loadingEmulationTraces, setLoadingEmulationTraces] = useState(true);
    const [loadingSimulationTraces, setLoadingSimulationTraces] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const wrapper = createRef();

    const fetchEmulationTraces = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationtraces',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setEmulationTraces(response)
                setLoadingEmulationTraces(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSimulationTraces = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationtraces',
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
                setSimulationTraces(response)
                setLoadingSimulationTraces(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoadingEmulationTraces(true)
        setLoadingSimulationTraces(true)
        fetchEmulationTraces()
        fetchSimulationTraces()
    }, []);

    const refreshEmulationTraces = () => {
        setLoadingEmulationTraces(true)
        fetchEmulationTraces()
    }

    const refreshSimulationTraces = () => {
        setLoadingSimulationTraces(true)
        fetchSimulationTraces()
    }

    const renderRefreshEmulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulation traces from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about how traces are collected
        </Tooltip>
    );

    const renderRefreshSimulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulation traces from the backend
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
                        Traces
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Collection of emulation and simulation traces</h4>
                    <p className="modalText">
                        Simulation traces are collected from the simulation system. At every time-step of the simulation,
                        the simulated observations, player actions, rewards, states, and beliefs are recorded.
                        Emulation traces are collected from the emulation system. At every time-step of an emulation
                        episode, observations, actions, rewards, states and beliefs are measured or computed based on
                        data from the emulation.
                    </p>
                    <div className="text-center">
                        <img src={TraceImg} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const EmulationTracesAccordions = (props) => {
        if (props.loadingEmulationTraces) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.emulationTraces.map((emulationTrace, index) =>
                        <EmulationTrace emulationTrace={emulationTrace}
                                        wrapper={wrapper} key={emulationTrace.id + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }

    const SimulationTracesAccordions = (props) => {
        if (props.loadingSimulationTraces) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.simulationTraces.map((simulationTrace, index) =>
                        <SimulationTrace simulationTrace={simulationTrace}
                                         wrapper={wrapper} key={simulationTrace.id + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }

    return (
        <div className="Traces">
            <h3 className="text-center inline-block emulationsHeader"> Emulation Traces

                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRefreshEmulationTracesTooltip}
                >
                    <Button variant="button" onClick={refreshEmulationTraces}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)}>
                        <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

            </h3>
            <EmulationTracesAccordions loadingEmulationTraces={loadingEmulationTraces} emulationTraces={emulationTraces}/>

            <h3 className="text-center inline-block simulationTracesHeader"> Simulation Traces

                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRefreshSimulationTracesTooltip}
                >
                    <Button variant="button" onClick={refreshSimulationTraces}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)}>
                        <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
            </h3>
            <SimulationTracesAccordions loadingSimulationTraces={loadingSimulationTraces}
                                        simulationTraces={simulationTraces}/>
        </div>
    );
}

Traces.propTypes = {};
Traces.defaultProps = {};
export default Traces;
