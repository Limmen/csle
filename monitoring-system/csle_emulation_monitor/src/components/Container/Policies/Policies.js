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
import TabularPolicy from "./TabularPolicy/TabularPolicy";
import AlphaVecPolicy from "./AlphaVecPolicy/AlphaVecPolicy";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import { useDebouncedCallback } from 'use-debounce';

const Policies = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [multiThresholdPoliciesIds, setMultiThresholdPoliciesIds] = useState([]);
    const [filteredMultiThresholdPoliciesIds, setFilteredMultiThresholdPoliciesIds] = useState([]);
    const [multiThresholdPoliciesSearchString, setMultiThresholdPoliciesSearchString] = useState("");
    const [selectedMultiThresholdPolicy, setSelectedMultiThresholdPolicy] = useState(null);
    const [selectedMultiThresholdPolicyId, setSelectedMultiThresholdPolicyId] = useState(null);
    const [loadingMultiThresholdPolicy, setLoadingMultiThresholdPolicy] = useState(true);
    const [ppoPoliciesIds, setPpoPoliciesIds] = useState([]);
    const [selectedPpoPolicy, setSelectedPpoPolicy] = useState(null);
    const [selectedPpoPolicyId, setSelectedPpoPolicyId] = useState(null);
    const [loadingPpoPolicy, setLoadingPpoPolicy] = useState(true);
    const [filteredPPOPoliciesIds, setFilteredPPOPoliciesIds] = useState([]);
    const [ppoPoliciesSearchString, setPpoPoliciesSearchString] = useState("");
    const [tabularPoliciesIds, setTabularPoliciesIds] = useState([]);
    const [selectedTabularPolicy, setSelectedTabularPolicy] = useState(null);
    const [selectedTabularPolicyId, setSelectedTabularPolicyId] = useState(null);
    const [loadingTabularPolicy, setLoadingTabularPolicy] = useState(true);
    const [filteredTabulaPoliciesIds, setFilteredTabularPoliciesIds] = useState([]);
    const [tabularPoliciesSearchString, setTabularPoliciesSearchString] = useState("");
    const [alphaVecPoliciesIds, setAlphaVecPoliciesIds] = useState([]);
    const [selectedAlphaVecPolicy, setSelectedAlphaVecPolicy] = useState(null);
    const [selectedAlphaVecPolicyId, setSelectedALphaVecPolicyId] = useState(null);
    const [loadingAlphaVecPolicy, setLoadingAlphaVecPolicy] = useState(true);
    const [filteredAlphaVecPoliciesIds, setFilteredAlphaVecPoliciesIds] = useState([]);
    const [alphaVecPoliciesSearchString, setAlphaVecPoliciesSearchString] = useState("");
    const [loadingMultiThresholdPolicies, setLoadingMultiThresholdPolicies] = useState(true);
    const [loadingPPOPolicies, setLoadingPPOPolicies] = useState(true);
    const [loadingTabularPolicies, setLoadingTabularPolicies] = useState(true);
    const [loadingAlphaVecPolicies, setLoadingAlphaVecPolicies] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchMultiThresholdPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/multithresholdpoliciesids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const multiThresholdPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setMultiThresholdPoliciesIds(multiThresholdPoliciesIds)
                setFilteredMultiThresholdPoliciesIds(multiThresholdPoliciesIds)
                setLoadingMultiThresholdPolicies(false)
                if (multiThresholdPoliciesIds.length > 0) {
                    setSelectedMultiThresholdPolicyId(multiThresholdPoliciesIds[0])
                    fetchMultiThresholdPolicy(multiThresholdPoliciesIds[0])
                    setLoadingMultiThresholdPolicy(true)
                } else {
                    setLoadingMultiThresholdPolicy(false)
                    setSelectedMultiThresholdPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchPPOPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/ppopoliciesids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const ppoPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setPpoPoliciesIds(ppoPoliciesIds)
                setFilteredPPOPoliciesIds(ppoPoliciesIds)
                setLoadingPPOPolicies(false)
                if (ppoPoliciesIds.length > 0) {
                    setSelectedPpoPolicyId(ppoPoliciesIds[0])
                    fetchPpoPolicy(ppoPoliciesIds[0])
                    setLoadingPpoPolicy(true)
                } else {
                    setLoadingPpoPolicy(false)
                    setSelectedPpoPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTabularPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tabularpoliciesids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const tabularPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setTabularPoliciesIds(tabularPoliciesIds)
                setFilteredTabularPoliciesIds(tabularPoliciesIds)
                setLoadingTabularPolicies(false)
                if (tabularPoliciesIds.length > 0) {
                    setSelectedTabularPolicyId(tabularPoliciesIds[0])
                    fetchTabularPolicy(tabularPoliciesIds[0])
                    setLoadingTabularPolicy(true)
                } else {
                    setLoadingTabularPolicy(false)
                    setSelectedTabularPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchAlphaVecPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/alphavecpoliciesids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const alphavecPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setAlphaVecPoliciesIds(alphavecPoliciesIds)
                setFilteredAlphaVecPoliciesIds(alphavecPoliciesIds)
                setLoadingAlphaVecPolicies(false)
                if (alphavecPoliciesIds.length > 0) {
                    setSelectedALphaVecPolicyId(alphavecPoliciesIds[0])
                    fetchAlphaVecPolicy(alphavecPoliciesIds[0])
                    setLoadingAlphaVecPolicy(true)
                } else {
                    setLoadingAlphaVecPolicy(false)
                    setSelectedAlphaVecPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPoliciesIds()
        setLoadingPPOPolicies(true)
        fetchPPOPoliciesIds()
        setLoadingTabularPolicies(true)
        fetchTabularPoliciesIds()
        setLoadingAlphaVecPolicies(true)
        fetchAlphaVecPoliciesIds()
    }, [fetchMultiThresholdPoliciesIds, fetchPPOPoliciesIds]);

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
                fetchPPOPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchPpoPolicy = useCallback((ppo_policy_id) => {
        fetch(
            `http://` + ip + ':7777/ppopolicies/get/' + ppo_policy_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedPpoPolicy(response)
                setLoadingPpoPolicy(false)
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
                fetchPPOPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removePPOPolicy = (ppoPolicy) => {
        setLoadingPPOPolicies(true)
        removePpoPoliciesRequest(ppoPolicy.id)
    }

    const removeTabularPoliciesRequest = useCallback((tabular_policy_id) => {
        fetch(
            `http://` + ip + ':7777/tabularpolicies/remove/' + tabular_policy_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTabularPolicy = useCallback((tabular_policy_id) => {
        fetch(
            `http://` + ip + ':7777/tabularpolicies/get/' + tabular_policy_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedTabularPolicy(response)
                setLoadingTabularPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllTabularPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tabularpolicies/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeTabularPolicy = (tabularPolicy) => {
        setLoadingTabularPolicies(true)
        removeTabularPoliciesRequest(tabularPolicy.id)
    }

    const removeAlphaVecPoliciesRequest = useCallback((alpha_vec_policies_id) => {
        fetch(
            `http://` + ip + ':7777/alphavecpolicies/remove/' + alpha_vec_policies_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchAlphaVecPolicy = useCallback((alpha_vec_policy_id) => {
        fetch(
            `http://` + ip + ':7777/alphavecpolicies/get/' + alpha_vec_policy_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedAlphaVecPolicy(response)
                setLoadingAlphaVecPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllAlphaVecPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/alphavecpolicies/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAlphaVecPolicy = (tabularPolicy) => {
        setLoadingAlphaVecPolicies(true)
        removeAlphaVecPoliciesRequest(tabularPolicy.id)
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
                fetchMultiThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchMultiThresholdPolicy = useCallback((multi_threshold_policy_id) => {
        fetch(
            `http://` + ip + ':7777/multithresholdpolicies/get/' + multi_threshold_policy_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedMultiThresholdPolicy(response)
                setLoadingMultiThresholdPolicy(false)
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
                fetchMultiThresholdPoliciesIds()
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

    const removeAllTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        removeAllTabularPoliciesRequest()
    }

    const removeAllAlphaVecPolicies = () => {
        setLoadingAlphaVecPolicies(true)
        removeAllAlphaVecPoliciesRequest()
    }

    const refreshMultiThresholdPolicies = () => {
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPoliciesIds()
    }

    const refreshPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        fetchPPOPoliciesIds()
    }

    const refreshTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        fetchTabularPoliciesIds()
    }

    const refreshAlphaVecPolicies = () => {
        setLoadingAlphaVecPolicies(true)
        fetchAlphaVecPoliciesIds()
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

    const renderRemoveAllTabularPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Tabular policies.
        </Tooltip>
    );

    const renderRemoveAllAlphaVecPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Alpha-Vector policies.
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

    const renderTabularRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Tabular policies from the backend
        </Tooltip>
    );

    const renderAlphaVecRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Alpha-Vector policies from the backend
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

    const updateSelectedMultiThresholdPolicyId = (selectedId) => {
        setSelectedMultiThresholdPolicyId(selectedId)
        fetchMultiThresholdPolicy(selectedId)
        setLoadingMultiThresholdPolicy(true)
    }

    const updateSelectedPpoPolicyId = (selectedId) => {
        setSelectedPpoPolicyId(selectedId)
        fetchPpoPolicy(selectedId)
        setLoadingPpoPolicy(true)
    }

    const updateSelectedTabularPolicyId = (selectedId) => {
        setSelectedTabularPolicyId(selectedId)
        fetchTabularPolicy(selectedId)
        setLoadingTabularPolicy(true)
    }

    const updateSelectedAlphaVecPolicyId = (selectedId) => {
        setSelectedALphaVecPolicyId(selectedId)
        fetchAlphaVecPolicy(selectedId)
        setLoadingAlphaVecPolicy(true)
    }

    const SelectMultiThresholdPolicyOrSpinner = (props) => {
        if (!props.loadingMultiThresholdPolicies && props.multiThresholdPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No multi-threshold policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderMultiThresholdPoliciesRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshMultiThresholdPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingMultiThresholdPolicies) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching policies... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Multi-threshold policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedMultiThresholdPolicyId}
                                defaultValue={props.selectedMultiThresholdPolicyId}
                                options={props.multiThresholdPoliciesIds}
                                onChange={updateSelectedMultiThresholdPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>
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
                </div>
            )
        }
    }


    const SelectPpoPolicyOrSpinner = (props) => {
        if (!props.loadingPPOPolicies && props.ppoPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No PPO policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderPPORefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshPPOPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingPPOPolicies) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching policies... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            PPO policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedPpoPolicyId}
                                defaultValue={props.selectedPpoPolicyId}
                                options={props.ppoPoliciesIds}
                                onChange={updateSelectedPpoPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

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
                </div>
            )
        }
    }

    const SelectTabularPolicyOrSpinner = (props) => {
        if (!props.loadingTabularPolicies && props.tabularPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No Tabular policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderTabularRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshTabularPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingTabularPolicies) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching policies... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Tabular policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedTabularPolicyId}
                                defaultValue={props.selectedTabularPolicyId}
                                options={props.tabularPoliciesIds}
                                onChange={updateSelectedTabularPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderTabularRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshTabularPolicies}>
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
                        overlay={renderRemoveAllTabularPoliciesTooltip}
                    >
                        <Button variant="danger" onClick={removeAllTabularPolicies}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }

    const SelectAlphaVecPolicyOrSpinner = (props) => {
        if (!props.loadingAlphaVecPolicies && props.alphaVecPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No alpha-vector policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderAlphaVecRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshAlphaVecPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingAlphaVecPolicies) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching policies... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Alpha-vector policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedAlphaVecPolicyId}
                                defaultValue={props.selectedAlphaVecPolicyId}
                                options={props.alphaVecPoliciesIds}
                                onChange={updateSelectedAlphaVecPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderAlphaVecRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshAlphaVecPolicies}>
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
                        overlay={renderRemoveAllAlphaVecPoliciesTooltip}
                    >
                        <Button variant="danger" onClick={removeAllAlphaVecPolicies}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }


    const wrapper = createRef();

    const MultiThresholdPolicyAccordion = (props) => {
        if (props.loadingMultiThresholdPolicy || props.selectedMultiThresholdPolicy === null ||
            props.selectedMultiThresholdPolicy === undefined) {
            if(props.loadingMultiThresholdPolicy) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching policy... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <MultiThresholdPolicy policy={selectedMultiThresholdPolicy} wrapper={wrapper} key={selectedMultiThresholdPolicy.id}
                                          removeMultiThresholdPolicy={removeMultiThresholdPolicy}
                    />
                </Accordion>
            )
        }
    }

    const PPOPolicyAccordion = (props) => {
        if (props.loadingPpoPolicy || props.selectedPpoPolicy === null || props.selectedPpoPolicy === undefined) {
            if(props.loadingPpoPolicy) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching policy... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <PPOPolicy policy={selectedPpoPolicy} wrapper={wrapper} key={selectedPpoPolicy.id}
                               removePPOPolicy={removePPOPolicy}
                    />
                </Accordion>
            )
        }
    }

    const TabularPolicyAccordion = (props) => {
        if (props.loadingTabularPolicy || props.selectedTabularPolicy === null || props.selectedTabularPolicy === undefined) {
            if(props.loadingTabularPolicy) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching policy... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <TabularPolicy policy={selectedTabularPolicy} wrapper={wrapper} key={selectedTabularPolicy.id}
                               removeTabularPolicy={removeTabularPolicy}
                    />
                </Accordion>
            )
        }
    }

    const AlphaVecPolicyAccordion = (props) => {
        if (props.loadingAlphaVecPolicy || props.selectedAlphaVecPolicy === null || props.selectedAlphaVecPolicy === undefined) {
            if(props.loadingAlphaVecPolicy) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching policy... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <AlphaVecPolicy policy={selectedAlphaVecPolicy} wrapper={wrapper}
                                   key={selectedAlphaVecPolicy.id}
                                   removeAlphaVecPolicy={removeAlphaVecPolicy}
                    />
                </Accordion>
            )
        }
    }

    const searchMultiThresholdPoliciesFilter = (multiThresholdPolicyId, searchVal) => {
        return (searchVal === "" ||  multiThresholdPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchMultiThresholdPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = multiThresholdPoliciesIds.filter(policyId => {
            return searchMultiThresholdPoliciesFilter(policyId, searchVal)
        });
        setFilteredMultiThresholdPoliciesIds(fPoliciesIds)
        setMultiThresholdPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if(!loadingMultiThresholdPolicy && fPoliciesIds.length > 0){
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if(selectedMultiThresholdPolicy !== null && selectedMultiThresholdPolicy !== undefined &&
                    selectedMultiThresholdPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if(!selectedPolicyRemoved) {
                setSelectedMultiThresholdPolicyId(fPoliciesIds[0])
                fetchMultiThresholdPolicy(fPoliciesIds[0])
                setLoadingMultiThresholdPolicy(true)
            }
        } else {
            setSelectedMultiThresholdPolicy(null)
        }
    }

    const searchMultiThresholdPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchMultiThresholdPolicyChange(event)
        },
        350
    );

    const searchPPOPoliciesFilter = (ppoPolicyId, searchVal) => {
        return (searchVal === "" || ppoPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchPPOPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = ppoPoliciesIds.filter(policy => {
            return searchPPOPoliciesFilter(policy, searchVal)
        });
        setFilteredPPOPoliciesIds(fPoliciesIds)
        setPpoPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if(!loadingPpoPolicy && fPoliciesIds.length > 0){
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if(selectedPpoPolicy !== null && selectedPpoPolicy !== undefined &&
                    selectedPpoPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if(!selectedPolicyRemoved) {
                setSelectedPpoPolicyId(fPoliciesIds[0])
                fetchPpoPolicy(fPoliciesIds[0])
                setLoadingPpoPolicy(true)
            }
        } else {
            setSelectedPpoPolicy(null)
        }
    }

    const searchPPOPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchPPOPolicyChange(event)
        },
        350
    );


    const searchTabularPoliciesFilter = (tabularPolicyId, searchVal) => {
        return (searchVal === "" || tabularPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchTabularPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = ppoPoliciesIds.filter(policy => {
            return searchTabularPoliciesFilter(policy, searchVal)
        });
        setFilteredTabularPoliciesIds(fPoliciesIds)
        setTabularPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if(!loadingTabularPolicy && fPoliciesIds.length > 0){
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if(selectedTabularPolicy !== null && selectedTabularPolicy !== undefined &&
                    selectedTabularPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if(!selectedPolicyRemoved) {
                setSelectedTabularPolicyId(fPoliciesIds[0])
                fetchTabularPolicy(fPoliciesIds[0])
                setLoadingTabularPolicy(true)
            }
        } else {
            setSelectedTabularPolicy(null)
        }
    }

    const searchTabularPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchTabularPolicyChange(event)
        },
        350
    );

    const searchAlphaVecPoliciesFilter = (alphaVecPolicyId, searchVal) => {
        return (searchVal === "" || alphaVecPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchAlphaVecPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = ppoPoliciesIds.filter(policy => {
            return searchAlphaVecPoliciesFilter(policy, searchVal)
        });
        setFilteredAlphaVecPoliciesIds(fPoliciesIds)
        setAlphaVecPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if(!loadingAlphaVecPolicy && fPoliciesIds.length > 0){
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if(selectedAlphaVecPolicy !== null && selectedAlphaVecPolicy !== undefined &&
                    selectedAlphaVecPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if(!selectedPolicyRemoved) {
                setSelectedALphaVecPolicyId(fPoliciesIds[0])
                fetchAlphaVecPolicy(fPoliciesIds[0])
                setLoadingAlphaVecPolicy(true)
            }
        } else {
            setSelectedAlphaVecPolicy(null)
        }
    }

    const searchAlphaVecPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchAlphaVecPolicyChange(event)
        },
        350
    );

    return (
        <div className="policyExamination">
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectMultiThresholdPolicyOrSpinner
                            loadingMultiThresholdPolicies={loadingMultiThresholdPolicies}
                            multiThresholdPoliciesIds={filteredMultiThresholdPoliciesIds}
                            selectedMultiThresholdPolicyId={selectedMultiThresholdPolicyId}
                        />
                    </h4>
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
                <div className="col-sm-2">
                </div>
            </div>
            <MultiThresholdPolicyAccordion loadingMultiThresholdPolicy={loadingMultiThresholdPolicy}
                                           selectedMultiThresholdPolicy={selectedMultiThresholdPolicy}/>

            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectPpoPolicyOrSpinner loadingPPOPolicies={loadingPPOPolicies}
                                                  ppoPoliciesIds={filteredPPOPoliciesIds}
                                                  selectedPpoPolicyId={selectedPpoPolicyId}
                        />
                    </h4>
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
                <div className="col-sm-2">
                </div>
            </div>

            <PPOPolicyAccordion loadingPpoPolicy={loadingPpoPolicy} selectedPpoPolicy={selectedPpoPolicy}/>


            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectTabularPolicyOrSpinner loadingTabularPolicies={loadingTabularPolicies}
                                                  tabularPoliciesIds={filteredTabulaPoliciesIds}
                                                  selectedTabularPolicyId={selectedTabularPolicyId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="tabularPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="tabularPoliciesSearchLabel"
                                aria-describedby="tabularPoliciesSearchField"
                                onChange={searchTabularPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <TabularPolicyAccordion loadingTabularPolicy={loadingTabularPolicy}
                                selectedTabularPolicy={selectedTabularPolicy}/>


            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectAlphaVecPolicyOrSpinner loadingAlphaVecPolicies={loadingAlphaVecPolicies}
                                                      alphaVecPoliciesIds={filteredAlphaVecPoliciesIds}
                                                      selectedAlphaVecPolicyId={selectedAlphaVecPolicyId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="alphaVecPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="alphaVecPoliciesSearchLabel"
                                aria-describedby="alphaVecPoliciesSearchField"
                                onChange={searchAlphaVecPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <AlphaVecPolicyAccordion loadingAlphaVecPolicy={loadingAlphaVecPolicy}
                                    selectedAlphaVecPolicy={selectedAlphaVecPolicy}/>
        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
