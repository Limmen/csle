import React, {useState} from 'react';
import './PolicyExamination.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import PolicyExaminationSystem from './Architecture.png'

const PolicyExamination = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the policy examination.
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
                        Interactive examination of learned security policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Examination of learned security policies</h4>
                    <p className="modalText">
                        The policy examination page allows a user to traverse episodes of
                        Markov decision processes in a controlled manner and to track
                        the actions triggered by security policies. Similar to a software
                        debugger, a user can continue or or halt an episode at any
                        time step and inspect parameters and probability distributions
                        of interest. The system enables insight into the structure of a
                        given policy and in the behavior of a policy in edge cases.
                    </p>
                    <div className="text-center">
                        <img src={PolicyExaminationSystem} alt="A system for interactive examination of
                        learned security policies"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }


    return (
        <div className="policyExamination">
            <h3> Policy Examination
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                    className="overLayInfo"
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)} className="infoButton2">
                        <i className="infoButton2 fa fa-info-circle" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
            </h3>
        </div>
    );
}

PolicyExamination.propTypes = {};
PolicyExamination.defaultProps = {};
export default PolicyExamination;
