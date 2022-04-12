import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Policies.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Tooltip from 'react-bootstrap/Tooltip';
import TSPSAPolicy from "./TSPSAPolicy/TSPSAPolicy";
import NeuralNetworkPolicies from './NeuralNetworkPolicies.png'
import PPOPolicy from "./PPOPolicy/PPOPolicy";

const Policies = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [tspsaPolicies, setTSPSAPolicies] = useState([]);
    const [ppoPolicies, setPPOPolicies] = useState([]);
    const [loadingspsaPolicies, setLoadingSpsaPolicies] = useState(true);
    const [loadingPPOPoliies, setLoadingPPOPolicies] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchTSPSAPolicies = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tspsapolicies',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTSPSAPolicies(response);
                setLoadingSpsaPolicies(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchPPOPolicies = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/ppopolicies',
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
                setPPOPolicies(response);
                setLoadingPPOPolicies(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoadingSpsaPolicies(true)
        fetchTSPSAPolicies()
        setLoadingPPOPolicies(true)
        fetchPPOPolicies()
    }, [fetchTSPSAPolicies, fetchPPOPolicies]);

    const refreshTSPSAPolicies = () => {
        setLoadingSpsaPolicies(true)
        fetchTSPSAPolicies()
    }

    const refreshPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        fetchPPOPolicies()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned policies.
        </Tooltip>
    );

    const renderTSPSARefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload T-SPSA policies from the backend
        </Tooltip>
    );

    const renderPPORefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload PPO policies from the backend
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
                        Trained policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Policies</h4>
                    <p className="modalText">
                        Trained policies are typically in the form of deep neural networks but can also be in tabular
                        representations or in special parameterizations such as Gaussian policies or threshold policies.
                    </p>
                    <div className="text-center">
                        <img src={NeuralNetworkPolicies} alt="neural network policies"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TSPSAPoliciesAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.policies.map((policy, index) =>
                        <TSPSAPolicy policy={policy} wrapper={wrapper} key={policy.id + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }

    const PPOPoliciesAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.policies.map((policy, index) =>
                        <PPOPolicy policy={policy} wrapper={wrapper} key={policy.id + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }


    return (
        <div className="policyExamination">
            <h3> T-SPSA policies

                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderTSPSARefreshTooltip}
                >
                    <Button variant="button" onClick={refreshTSPSAPolicies}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)} className="infoButton2">
                        <i className="fa fa-info-circle" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
            </h3>
            <TSPSAPoliciesAccordions loading={loadingspsaPolicies} policies={tspsaPolicies}/>

            <h3 className="ppoPolicies"> PPO policies

                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderPPORefreshTooltip}
                >
                    <Button variant="button" onClick={refreshPPOPolicies}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderInfoTooltip}
                >
                    <Button variant="button" onClick={() => setShowInfoModal(true)} className="infoButton2">
                        <i className="fa fa-info-circle" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
                <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
            </h3>
            <PPOPoliciesAccordions loading={loadingPPOPoliies} policies={ppoPolicies}/>
        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
