import React, {useState} from 'react';
import './Simulations.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import MarkovChain from './Markov.png'

const Simulations = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the emulation environments
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
                        Simulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Simulation of emulated infrastructures</h4>
                    <p className="modalText">
                        A simulation is defined as a Markov decision process or stochastic game, which models
                        how a discrete-time dynamical system is evolved and can be controlled.
                    </p>
                    <div className="text-center">
                        <img src={MarkovChain} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    return (
        <div className="Simulations">
            <h3> Simulations

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
        </div>
    );
}

Simulations.propTypes = {};
Simulations.defaultProps = {};
export default Simulations;
