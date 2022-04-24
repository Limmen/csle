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
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import { useDebouncedCallback } from 'use-debounce';

const Policies = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [tspsaPolicies, setTSPSAPolicies] = useState([]);
    const [filteredTspsaPolicies, setFilteredTSPSAPolicies] = useState([]);
    const [tSPSAPoliciesSearchString, setTSPSAPoliciesSearchString] = useState("");
    const [ppoPolicies, setPPOPolicies] = useState([]);
    const [filteredPPOPolicies, setFilteredPPOPolicies] = useState([]);
    const [ppoPoliciesSearchString, setPpoPoliciesSearchString] = useState("");
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
                setFilteredTSPSAPolicies(response)
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
                setPPOPolicies(response);
                setFilteredPPOPolicies(response)
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

    const removePpoPoliciesRequest = useCallback((ppo_policy_id) => {
        fetch(
            `http://` + ip + ':7777/ppopolicies/remove/' + ppo_policy_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchPPOPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllPpoPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/ppopolicies/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchPPOPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removePPOPolicy = (ppoPolicy) => {
        setLoadingPPOPolicies(true)
        removePpoPoliciesRequest(ppoPolicy.id)
    }

    const removeTSPSAPoliciesRequest = useCallback((t_spsa_policy_id) => {
        fetch(
            `http://` + ip + ':7777/tspsapolicies/remove/' + t_spsa_policy_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTSPSAPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const removeAllTSPSAPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tspsapolicies/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTSPSAPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeTSPSAPolicy = (tspsaPolicy) => {
        setLoadingSpsaPolicies(true)
        removeTSPSAPoliciesRequest(tspsaPolicy.id)
    }

    const removeAllTSPSAPolicies = () => {
        setLoadingSpsaPolicies(true)
        removeAllTSPSAPoliciesRequest()
    }

    const removeAllPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        removeAllPpoPoliciesRequest()
    }

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

    const renderRemoveAllTSPSAPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all T-SPSA policies.
        </Tooltip>
    );

    const renderRemoveAllPPOPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all PPO policies.
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
                        <TSPSAPolicy policy={policy} wrapper={wrapper} key={policy.id + "-" + index}
                                     removeTSPSAPolicy={removeTSPSAPolicy}
                        />
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
                        <PPOPolicy policy={policy} wrapper={wrapper} key={policy.id + "-" + index}
                                   removePPOPolicy={removePPOPolicy}
                        />
                    )}
                </Accordion>
            )
        }
    }

    const searchTSPSAPoliciesFilter = (tSpsaPolicy, searchVal) => {
        return (searchVal === "" ||
            tSpsaPolicy.id.toString().indexOf(searchVal.toLowerCase()) !== -1 ||
            tSpsaPolicy.simulation_name.indexOf(searchVal.toLowerCase()) !== -1
        )
    }

    const searchTSPSAPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPolicies = tspsaPolicies.filter(policy => {
            return searchTSPSAPoliciesFilter(policy, searchVal)
        });
        setFilteredTSPSAPolicies(fPolicies)
        setTSPSAPoliciesSearchString(searchVal)
    }

    const searchTSPSAPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchTSPSAPolicyChange(event)
        },
        350
    );

    const searchPPOPoliciesFilter = (ppoPolicy, searchVal) => {
        return (searchVal === "" ||
            ppoPolicy.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            ppoPolicy.simulation_name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchPPOPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPolicies = ppoPolicies.filter(policy => {
            return searchPPOPoliciesFilter(policy, searchVal)
        });
        setFilteredPPOPolicies(fPolicies)
        setPpoPoliciesSearchString(searchVal)
    }

    const searchPPOPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchPPOPolicyChange(event)
        },
        350
    );

    return (
        <div className="policyExamination">
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
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

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllTSPSAPoliciesTooltip}
                        >
                            <Button variant="danger" onClick={removeAllTSPSAPolicies}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="tSpsaPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="tSpsaPoliciesSearchLabel"
                                aria-describedby="tSpsaPoliciesSearchField"
                                onChange={searchTSPSAPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <TSPSAPoliciesAccordions loading={loadingspsaPolicies} policies={filteredTspsaPolicies}/>
            <div className="row ppoPolicies">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> PPO policies

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

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllPPOPoliciesTooltip}
                        >
                            <Button variant="danger" onClick={removeAllPPOPolicies}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="ppoPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="ppoPoliciesSearchLabel"
                                aria-describedby="ppoPoliciesSearchField"
                                onChange={searchPPOPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <PPOPoliciesAccordions loading={loadingPPOPoliies} policies={filteredPPOPolicies}/>
        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
