import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Policies.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Tooltip from 'react-bootstrap/Tooltip';
import MultiThresholdPolicy from "./MultiThresholdPolicy/MultiThresholdPolicy";
import NeuralNetworkPolicies from './NeuralNetworkPolicies.png'
import PPOPolicy from "./PPOPolicy/PPOPolicy";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import { useDebouncedCallback } from 'use-debounce';

const Policies = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [multiThresholdPolicies, setMultiThresholdPolicies] = useState([]);
    const [filteredMultiThresholdPolicies, setFilteredMultiThresholdPolicies] = useState([]);
    const [multiThresholdPoliciesSearchString, setMultiThresholdPoliciesSearchString] = useState("");
    const [ppoPolicies, setPPOPolicies] = useState([]);
    const [filteredPPOPolicies, setFilteredPPOPolicies] = useState([]);
    const [ppoPoliciesSearchString, setPpoPoliciesSearchString] = useState("");
    const [loadingMultiThresholdPolicies, setLoadingMultiThresholdPolicies] = useState(true);
    const [loadingPPOPoliies, setLoadingPPOPolicies] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchMultiThresholdPolicies = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/multithresholdpolicies',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setMultiThresholdPolicies(response);
                setFilteredMultiThresholdPolicies(response)
                setLoadingMultiThresholdPolicies(false)
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
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPolicies()
        setLoadingPPOPolicies(true)
        fetchPPOPolicies()
    }, [fetchMultiThresholdPolicies, fetchPPOPolicies]);

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

    const removeMultiThresholdPoliciesRequest = useCallback((multi_threshold_policy_id) => {
        fetch(
            `http://` + ip + ':7777/multithresholdpolicies/remove/' + multi_threshold_policy_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchMultiThresholdPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const removeAllMultiThresholdPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/multithresholdpolicies/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchMultiThresholdPolicies()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeMultiThresholdPolicy = (multiThresholdPolicy) => {
        setLoadingMultiThresholdPolicies(true)
        removeMultiThresholdPoliciesRequest(multiThresholdPolicy.id)
    }

    const removeAllMultiThresholdPolicies = () => {
        setLoadingMultiThresholdPolicies(true)
        removeAllMultiThresholdPoliciesRequest()
    }

    const removeAllPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        removeAllPpoPoliciesRequest()
    }

    const refreshMultiThresholdPolicies = () => {
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPolicies()
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

    const renderRemoveAllMultiThresholdPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all multi-threshold policies.
        </Tooltip>
    );

    const renderRemoveAllPPOPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all PPO policies.
        </Tooltip>
    );

    const renderMultiThresholdPoliciesRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload multi-threshold policies from the backend
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

    const MultiThresholdPoliciesAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.policies.map((policy, index) =>
                        <MultiThresholdPolicy policy={policy} wrapper={wrapper} key={policy.id + "-" + index}
                                              removeMultiThresholdPolicy={removeMultiThresholdPolicy}
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

    const searchMultiThresholdPoliciesFilter = (multiThresholdPolicy, searchVal) => {
        return (searchVal === "" ||
            multiThresholdPolicy.id.toString().indexOf(searchVal.toLowerCase()) !== -1 ||
            multiThresholdPolicy.simulation_name.indexOf(searchVal.toLowerCase()) !== -1
        )
    }

    const searchMultiThresholdPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPolicies = multiThresholdPolicies.filter(policy => {
            return searchMultiThresholdPoliciesFilter(policy, searchVal)
        });
        setFilteredMultiThresholdPolicies(fPolicies)
        setMultiThresholdPoliciesSearchString(searchVal)
    }

    const searchMultiThresholdPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchMultiThresholdPolicyChange(event)
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
                    <h3> Multi-threshold policies

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderMultiThresholdPoliciesRefreshTooltip}
                        >
                            <Button variant="button" onClick={refreshMultiThresholdPolicies}>
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
                            overlay={renderRemoveAllMultiThresholdPoliciesTooltip}
                        >
                            <Button variant="danger" onClick={removeAllMultiThresholdPolicies}>
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
                                onChange={searchMultiThresholdPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <MultiThresholdPoliciesAccordions loading={loadingMultiThresholdPolicies} policies={filteredMultiThresholdPolicies}/>
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
