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
import ThresholdPolicyImg from './ThresholdPolicy.png'
import TabularPolicyImg from './TabularPolicyImg.png'
import PWLCValueFun from './PWLCValueFun.png'
import PPOPolicy from "./PPOPolicy/PPOPolicy";
import DQNPolicy from "./DQNPolicy/DQNPolicy";
import FnnWSoftmaxPolicy from "./FnnWSoftmaxPolicy/FnnWSoftmaxPolicy";
import TabularPolicy from "./TabularPolicy/TabularPolicy";
import VectorPolicy from "./VectorPolicy/VectorPolicy";
import AlphaVecPolicy from "./AlphaVecPolicy/AlphaVecPolicy";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../Common/serverIp";

/**
 * Component representing the /policies page
 */
const Policies = (props) => {
    const [showMultiThresholdPoliciesInfoModal, setShowMultiThresholdPoliciesInfoModal] = useState(false);
    const [showPPOPoliciesInfoModal, setShowPPOPoliciesInfoModal] = useState(false);
    const [showTabularPoliciesInfoModal, setShowTabularPoliciesInfoModal] = useState(false);
    const [showAlphaVectorPoliciesInfoModal, setShowAlphaVectorPoliciesInfoModal] = useState(false);
    const [showDQNPoliciesInfoModal, setShowDQNPoliciesInfoModal] = useState(false);
    const [showFNNPoliciesInfoModal, setShowFNNPoliciesInfoModal] = useState(false);
    const [showVectorPoliciesInfoModal, setShowVectorPoliciesInfoModal] = useState(false);
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
    const [dqnPoliciesIds, setDQNPoliciesIds] = useState([]);
    const [selectedDQNPolicy, setSelectedDQNPolicy] = useState(null);
    const [selectedDQNPolicyId, setSelectedDQNPolicyId] = useState(null);
    const [loadingDQNPolicy, setLoadingDQNPolicy] = useState(true);
    const [filteredDQNPoliciesIds, setFilteredDQNPoliciesIds] = useState([]);
    const [dqnPoliciesSearchString, setDQNPoliciesSearchString] = useState("");
    const [fnnWSoftmaxPoliciesIds, setFnnWSoftmaxPoliciesIds] = useState([]);
    const [selectedFnnWSoftmaxPolicy, setSelectedFnnWSoftmaxPolicy] = useState(null);
    const [selectedFnnWSoftmaxPolicyId, setSelectedFnnWSoftmaxPolicyId] = useState(null);
    const [loadingFnnWSoftmaxPolicy, setLoadingFnnWSoftmaxPolicy] = useState(true);
    const [filteredFnnWSoftmaxPoliciesIds, setFilteredFnnWSoftmaxPoliciesIds] = useState([]);
    const [fnnWSoftmaxPoliciesSearchString, setFnnWSoftmaxPoliciesSearchString] = useState("");
    const [vectorPoliciesIds, setVectorPoliciesIds] = useState([]);
    const [selectedVectorPolicy, setSelectedVectorPolicy] = useState(null);
    const [selectedVectorPolicyId, setSelectedVectorPolicyId] = useState(null);
    const [loadingVectorPolicy, setLoadingVectorPolicy] = useState(true);
    const [filteredVectorPoliciesIds, setFilteredVectorPoliciesIds] = useState([]);
    const [vectorPoliciesSearchString, setVectorPoliciesSearchString] = useState("");
    const [loadingMultiThresholdPolicies, setLoadingMultiThresholdPolicies] = useState(true);
    const [loadingPPOPolicies, setLoadingPPOPolicies] = useState(true);
    const [loadingDQNPolicies, setLoadingDQNPolicies] = useState(true);
    const [loadingTabularPolicies, setLoadingTabularPolicies] = useState(true);
    const [loadingVectorPolicies, setLoadingVectorPolicies] = useState(true);
    const [loadingAlphaVecPolicies, setLoadingAlphaVecPolicies] = useState(true);
    const [loadingFnnWSoftmaxPolicies, setLoadingFnnWSoftmaxPolicies] = useState(true);
    const ip = serverIp
    const alert = useAlert();
    const navigate = useNavigate();
    // const ip = "172.31.212.92"

    const fetchMultiThresholdPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/multi-threshold-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
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
            `http://` + ip + ':7777/ppo-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
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

    const fetchDQNPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/dqn-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const dqnPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setDQNPoliciesIds(dqnPoliciesIds)
                setFilteredDQNPoliciesIds(dqnPoliciesIds)
                setLoadingDQNPolicies(false)
                if (dqnPoliciesIds.length > 0) {
                    setSelectedDQNPolicyId(dqnPoliciesIds[0])
                    fetchDQNPolicy(dqnPoliciesIds[0])
                    setLoadingDQNPolicy(true)
                } else {
                    setLoadingDQNPolicy(false)
                    setSelectedDQNPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTabularPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tabular-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
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

    const fetchVectorPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/vector-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const vectorPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setVectorPoliciesIds(vectorPoliciesIds)
                setFilteredVectorPoliciesIds(vectorPoliciesIds)
                setLoadingVectorPolicies(false)
                if (vectorPoliciesIds.length > 0) {
                    setSelectedVectorPolicyId(vectorPoliciesIds[0])
                    fetchVectorPolicy(vectorPoliciesIds[0])
                    setLoadingVectorPolicy(true)
                } else {
                    setLoadingVectorPolicy(false)
                    setSelectedVectorPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchAlphaVecPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/alpha-vec-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
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

    const fetchFnnWSoftmaxPoliciesIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/fnn-w-softmax-policies?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const fnnWSoftmaxPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation
                    }
                })
                setFnnWSoftmaxPoliciesIds(fnnWSoftmaxPoliciesIds)
                setFilteredFnnWSoftmaxPoliciesIds(fnnWSoftmaxPoliciesIds)
                setLoadingFnnWSoftmaxPolicies(false)
                if (fnnWSoftmaxPoliciesIds.length > 0) {
                    setSelectedFnnWSoftmaxPolicyId(fnnWSoftmaxPoliciesIds[0])
                    fetchFnnWSoftmaxPolicy(fnnWSoftmaxPoliciesIds[0])
                    setLoadingFnnWSoftmaxPolicy(true)
                } else {
                    setLoadingFnnWSoftmaxPolicy(false)
                    setSelectedFnnWSoftmaxPolicy(null)
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
        setLoadingDQNPolicies(true)
        fetchDQNPoliciesIds()
        setLoadingFnnWSoftmaxPolicies(true)
        fetchFnnWSoftmaxPoliciesIds()
        setLoadingVectorPolicies(true)
        fetchVectorPoliciesIds()
    }, [fetchMultiThresholdPoliciesIds, fetchPPOPoliciesIds, fetchDQNPoliciesIds, fetchTabularPoliciesIds,
        fetchAlphaVecPoliciesIds, fetchFnnWSoftmaxPoliciesIds, fetchVectorPoliciesIds]);

    const removePpoPoliciesRequest = useCallback((ppo_policy_id) => {
        fetch(
            `http://` + ip + ':7777/ppo-policies/' + ppo_policy_id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchPPOPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchPpoPolicy = useCallback((ppo_policy_id) => {
        fetch(
            `http://` + ip + ':7777/ppo-policies/' + ppo_policy_id.value + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedPpoPolicy(response)
                setLoadingPpoPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllPpoPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/ppo-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchPPOPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removePPOPolicy = (ppoPolicy) => {
        setLoadingPPOPolicies(true)
        removePpoPoliciesRequest(ppoPolicy.id)
    }

    const removeAllPPOPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all PPO policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllPPOPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all PPO policies? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllPPOPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removePPOPolicyConfirm = (ppoPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the PPO policy with ID: ' + ppoPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removePPOPolicy(ppoPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the PPO policy with ID {ppoPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removePPOPolicy(ppoPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeFnnWSoftmaxPoliciesRequest = useCallback((fnn_w_softmax_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/fnn-w-softmax-policies/' + fnn_w_softmax_policy_id +
            "?token=" + props.sessionData.token),
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchFnnWSoftmaxPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchFnnWSoftmaxPolicy = useCallback((fnn_w_softmax_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/fnn-w-softmax-policies/' + fnn_w_softmax_policy_id.value +
            "?token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedFnnWSoftmaxPolicy(response)
                setLoadingFnnWSoftmaxPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllFnnWSoftmaxPoliciesRequest = useCallback(() => {
        fetch(
            (`http://` + ip + ':7777/fnn-w-softmax-policies' + "?token=" + props.sessionData.token),
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchFnnWSoftmaxPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeFnnWSoftmaxPolicy = (fnnWSoftmaxPolicy) => {
        setLoadingFnnWSoftmaxPolicies(true)
        removeFnnWSoftmaxPoliciesRequest(fnnWSoftmaxPolicy.id)
    }

    const removeDQNPoliciesRequest = useCallback((dqn_policy_id) => {
        fetch(
            `http://` + ip + ':7777/dqn-policies' + dqn_policy_id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchDQNPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllDQNPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all DQN policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllDQNPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all DQN policies? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllDQNPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeDQNPolicyConfirm = (dqnPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the DQN policy with ID: ' + dqnPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeDQNPolicy(dqnPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the DQN policy with ID {dqnPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeDQNPolicy(dqnPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeAllFnnWSoftmaxPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all FNN-with-softmax policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllFnnWSoftmaxPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all FNN-with-softmax policies?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllFnnWSoftmaxPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeFnnWSoftmaxPolicyConfirm = (fnnWSoftmaxPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the FNN-with-softmax policy with ID: ' + fnnWSoftmaxPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeFnnWSoftmaxPolicy(fnnWSoftmaxPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the FNN-with-softmax policy with
                                    ID {fnnWSoftmaxPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeFnnWSoftmaxPolicy(fnnWSoftmaxPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const fetchDQNPolicy = useCallback((dqn_policy_id) => {
        fetch(
            `http://` + ip + ':7777/dqn-policies/' + dqn_policy_id.value + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedDQNPolicy(response)
                setLoadingDQNPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllDQNPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/dqn-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchDQNPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeDQNPolicy = (dqnPolicy) => {
        setLoadingDQNPolicies(true)
        removeDQNPoliciesRequest(dqnPolicy.id)
    }

    const removeTabularPoliciesRequest = useCallback((tabular_policy_id) => {
        fetch(
            `http://` + ip + ':7777/tabular-policies/' + tabular_policy_id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTabularPolicy = useCallback((tabular_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/tabular-policies/' + tabular_policy_id.value
            + "?token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedTabularPolicy(response)
                setLoadingTabularPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllTabularPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/tabular-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeTabularPolicy = (tabularPolicy) => {
        setLoadingTabularPolicies(true)
        removeTabularPoliciesRequest(tabularPolicy.id)
    }

    const removeAllTabularPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all Tabular policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllTabularPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all tabular policies? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllTabularPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeTabularPolicyConfirm = (tabularPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the tabular policy with ID: ' + tabularPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeTabularPolicy(tabularPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the tabular policy with ID {tabularPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeTabularPolicy(tabularPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeVectorPoliciesRequest = useCallback((vector_policy_id) => {
        fetch(
            `http://` + ip + ':7777/vector-policies/' + vector_policy_id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchVectorPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchVectorPolicy = useCallback((vector_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/vector-policies/' + vector_policy_id.value
            + "?token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedVectorPolicy(response)
                setLoadingVectorPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllVectorPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/vector-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchVectorPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeVectorPolicy = (vectorPolicy) => {
        setLoadingVectorPolicies(true)
        removeVectorPoliciesRequest(vectorPolicy.id)
    }

    const removeAllVectorPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all vector policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllVectorPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all vector policies? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllVectorPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeVectorPolicyConfirm = (vectorPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the vector policy with ID: ' + vectorPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeVectorPolicy(vectorPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the vector policy with ID {vectorPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeVectorPolicy(vectorPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeAlphaVecPoliciesRequest = useCallback((alpha_vec_policies_id) => {
        fetch(
            (`http://` + ip + ':7777/alpha-vec-policies/' + alpha_vec_policies_id + "?token="
            + props.sessionData.token),
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchAlphaVecPolicy = useCallback((alpha_vec_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/alpha-vec-policies/' + alpha_vec_policy_id.value + "?token="
                + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedAlphaVecPolicy(response)
                setLoadingAlphaVecPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllAlphaVecPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/alpha-vec-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAlphaVecPolicy = (alphaVecPolicy) => {
        setLoadingAlphaVecPolicies(true)
        removeAlphaVecPoliciesRequest(alphaVecPolicy.id)
    }

    const removeAllAlphaVecPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all alpha-vector policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllAlphaVecPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all alpha-vector policies?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllAlphaVecPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeAlphaVecPolicyConfirm = (alphaVecPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the alpha-vector policy with ID: ' + alphaVecPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAlphaVecPolicy(alphaVecPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the alpha-vector policy with ID {alphaVecPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAlphaVecPolicy(alphaVecPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeMultiThresholdPoliciesRequest = useCallback((multi_threshold_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/multi-threshold-policies/' + multi_threshold_policy_id + "?token="
                + props.sessionData.token),
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                fetchMultiThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchMultiThresholdPolicy = useCallback((multi_threshold_policy_id) => {
        fetch(
            (`http://` + ip + ':7777/multi-threshold-policies/' + multi_threshold_policy_id.value +
                "?token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedMultiThresholdPolicy(response)
                setLoadingMultiThresholdPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllMultiThresholdPoliciesRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/multi-threshold-policies' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
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

    const removeAllMultiThresholdPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all multi-threshold policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllMultiThresholdPolicies()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all multi-threshold policies?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllMultiThresholdPolicies()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeMultiThresholdPolicyConfirm = (multiThresholdPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the multi-threshold policy with ID: ' + multiThresholdPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeMultiThresholdPolicy(multiThresholdPolicy)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the multi-threshold policy
                                    with ID {multiThresholdPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeMultiThresholdPolicy(multiThresholdPolicy)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeAllPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        removeAllPpoPoliciesRequest()
    }

    const removeAllFnnWSoftmaxPolicies = () => {
        setLoadingFnnWSoftmaxPolicies(true)
        removeAllFnnWSoftmaxPoliciesRequest()
    }

    const removeAllDQNPolicies = () => {
        setLoadingDQNPolicies(true)
        removeAllDQNPoliciesRequest()
    }

    const removeAllTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        removeAllTabularPoliciesRequest()
    }

    const removeAllVectorPolicies = () => {
        setLoadingVectorPolicies(true)
        removeAllVectorPoliciesRequest()
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

    const refreshFnnWSoftmaxPolicies = () => {
        setLoadingFnnWSoftmaxPolicies(true)
        fetchFnnWSoftmaxPoliciesIds()
    }

    const refreshDQNPolicies = () => {
        setLoadingDQNPolicies(true)
        fetchDQNPoliciesIds()
    }

    const refreshTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        fetchTabularPoliciesIds()
    }

    const refreshVectorPolicies = () => {
        setLoadingVectorPolicies(true)
        fetchVectorPoliciesIds()
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

    const renderRemoveAllFnnWSoftmaxPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Feed-forward neural network with softmax output policies.
        </Tooltip>
    );

    const renderRemoveAllDQNPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all DQN policies.
        </Tooltip>
    );

    const renderRemoveAllTabularPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Tabular policies.
        </Tooltip>
    );

    const renderRemoveAllVectorPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Vector policies.
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

    const renderFnnWSoftmaxRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload feed-forward neural network policies with softmax outputs from the backend
        </Tooltip>
    );

    const renderDQNRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload DQN policies from the backend
        </Tooltip>
    );

    const renderTabularRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Tabular policies from the backend
        </Tooltip>
    );

    const renderVectorRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Vector policies from the backend
        </Tooltip>
    );

    const renderAlphaVecRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Alpha-Vector policies from the backend
        </Tooltip>
    );

    const MultiThresholdPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Multi-Threshold Policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        A threshold policy is a polic parameterized by a set of thresholds that determine when
                        to take different actions. The thresholds can be based on the state of an MDP if the state is observed
                        or based on a belief state of a POMDP if the state is not observed.
                    </p>
                    <div className="text-center">
                        <img src={ThresholdPolicyImg} alt="threshold policy" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const PPOPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        PPO Policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Policies trained with PPO are neural network policies where the input to the network
                        is either a state or an observation and the output is either an action or a distribution
                        over actions.
                    </p>
                    <div className="text-center">
                        <img src={NeuralNetworkPolicies} alt="threshold policy" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const TabularPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Tabular policies.
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Tabular policies are produced by tabular reinforcement learning algorithms such as
                        Q-learning, Sarsa, and TD-learning. A tabular policy consists of a table of mappings between
                        states and actions.
                    </p>
                    <div className="text-center">
                        <img src={TabularPolicyImg} alt="tabular" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const AlphaVectorPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Alpha-vector policies.
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Alpha-vector policies are greedy policies with respect to piece-wise linear and convex value functions
                        for POMDPs.
                    </p>
                    <div className="text-center">
                        <img src={PWLCValueFun} alt="piece-wise linar and convex value function" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const DQNPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        DQN Policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Policies trained with DQN are neural network policies where the input to the network
                        is either a state or an observation and the output is either an action or a distribution
                        over actions.
                    </p>
                    <div className="text-center">
                        <img src={NeuralNetworkPolicies} alt="threshold policy" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const FNNPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        FNN Policies
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Feed-forward neural network policies are neural networks where the input to the network
                        is either a state or an observation and the output is either an action or a distribution
                        over actions.
                    </p>
                    <div className="text-center">
                        <img src={NeuralNetworkPolicies} alt="threshold policy" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const VectorPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Vector policies.
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Vector policies are policies in the form of a single vector, e.g. obtained
                        through linear programming methods.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
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

    const updateSelectedFnnWSoftmaxPolicyId = (selectedId) => {
        setSelectedFnnWSoftmaxPolicyId(selectedId)
        fetchFnnWSoftmaxPolicy(selectedId)
        setLoadingFnnWSoftmaxPolicy(true)
    }

    const updateSelectedDQNPolicyId = (selectedId) => {
        setSelectedDQNPolicyId(selectedId)
        fetchDQNPolicy(selectedId)
        setLoadingDQNPolicy(true)
    }

    const updateSelectedTabularPolicyId = (selectedId) => {
        setSelectedTabularPolicyId(selectedId)
        fetchTabularPolicy(selectedId)
        setLoadingTabularPolicy(true)
    }

    const updateSelectedVectorPolicyId = (selectedId) => {
        setSelectedVectorPolicyId(selectedId)
        fetchVectorPolicy(selectedId)
        setLoadingVectorPolicy(true)
    }

    const updateSelectedAlphaVecPolicyId = (selectedId) => {
        setSelectedALphaVecPolicyId(selectedId)
        fetchAlphaVecPolicy(selectedId)
        setLoadingAlphaVecPolicy(true)
    }

    const DeleteAllMultiThresholdPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllMultiThresholdPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllMultiThresholdPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
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
                            Selected multi-threshold policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
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
                        <Button variant="button" onClick={() => setShowMultiThresholdPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <MultiThresholdPoliciesInfoModal show={showMultiThresholdPoliciesInfoModal} onHide={() => setShowMultiThresholdPoliciesInfoModal(false)}/>

                    <DeleteAllMultiThresholdPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllPPOPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllPPOPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllPPOPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
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
                            Selected PPO policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
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
                        <Button variant="button" onClick={() => setShowPPOPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <PPOPoliciesInfoModal show={showPPOPoliciesInfoModal} onHide={() => setShowPPOPoliciesInfoModal(false)}/>

                    <DeleteAllPPOPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllFNNWSoftmaxPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllFnnWSoftmaxPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllFnnWSoftmaxPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectFnnWSoftmaxPolicyOrSpinner = (props) => {
        if (!props.loadingFnnWSoftmaxPolicies && props.fnnWSoftmaxPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No feed-forward neural network policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderFnnWSoftmaxRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshFnnWSoftmaxPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingFnnWSoftmaxPolicies) {
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
                            Selected feed-forward neural network policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedFnnWSoftmaxPolicyId}
                                defaultValue={props.selectedFnnWSoftmaxPolicyId}
                                options={props.fnnWSoftmaxPoliciesIds}
                                onChange={updateSelectedFnnWSoftmaxPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderFnnWSoftmaxRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshFnnWSoftmaxPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowFNNPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <FNNPoliciesInfoModal show={showFNNPoliciesInfoModal} onHide={() => setShowFNNPoliciesInfoModal(false)}/>

                    <DeleteAllFNNWSoftmaxPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllDQNPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllDQNPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllDQNPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectDQNPolicyOrSpinner = (props) => {
        if (!props.loadingDQNPolicies && props.dqnPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No DQN policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderDQNRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshDQNPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingDQNPolicies) {
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
                            Selected DQN policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedDQNPolicyId}
                                defaultValue={props.selectedDQNPolicyId}
                                options={props.dqnPoliciesIds}
                                onChange={updateSelectedDQNPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderDQNRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshDQNPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowDQNPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <DQNPoliciesInfoModal show={showDQNPoliciesInfoModal}
                                                     onHide={() => setShowDQNPoliciesInfoModal(false)}/>

                    <DeleteAllDQNPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllTabularPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllTabularPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllTabularPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
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
                            Selected tabular policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
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
                        <Button variant="button" onClick={() => setShowTabularPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <TabularPoliciesInfoModal
                        show={showTabularPoliciesInfoModal}
                        onHide={() => setShowTabularPoliciesInfoModal(false)}/>

                    <DeleteAllTabularPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllVectorPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllVectorPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllVectorPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectVectorPolicyOrSpinner = (props) => {
        if (!props.loadingVectorPolicies && props.vectorPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No vector policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderVectorRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshVectorPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingVectorPolicies) {
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
                            Selected vector policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedVectorPolicyId}
                                defaultValue={props.selectedVectorPolicyId}
                                options={props.vectorPoliciesIds}
                                onChange={updateSelectedVectorPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderVectorRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshVectorPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowVectorPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <VectorPoliciesInfoModal show={showVectorPoliciesInfoModal} onHide={() => setShowVectorPoliciesInfoModal(false)}/>

                    <DeleteAllVectorPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const DeleteAllAlphaVecPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllAlphaVecPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllAlphaVecPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
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
                            Selected alpha-vector policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
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
                        <Button variant="button" onClick={() => setShowAlphaVectorPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <AlphaVectorPoliciesInfoModal show={showAlphaVectorPoliciesInfoModal}
                                                     onHide={() => setShowAlphaVectorPoliciesInfoModal(false)}/>

                    <DeleteAllAlphaVecPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }


    const wrapper = createRef();

    const MultiThresholdPolicyAccordion = (props) => {
        if (props.loadingMultiThresholdPolicy || props.selectedMultiThresholdPolicy === null ||
            props.selectedMultiThresholdPolicy === undefined) {
            if (props.loadingMultiThresholdPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected multi-threshold policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <MultiThresholdPolicy policy={selectedMultiThresholdPolicy} wrapper={wrapper}
                                              key={selectedMultiThresholdPolicy.id}
                                              removeMultiThresholdPolicy={removeMultiThresholdPolicyConfirm}
                                              sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const PPOPolicyAccordion = (props) => {
        if (props.loadingPpoPolicy || props.selectedPpoPolicy === null || props.selectedPpoPolicy === undefined) {
            if (props.loadingPpoPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected PPO policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <PPOPolicy policy={selectedPpoPolicy} wrapper={wrapper} key={selectedPpoPolicy.id}
                                   removePPOPolicy={removePPOPolicyConfirm} sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const FnnWSoftmaxPolicyAccordion = (props) => {
        if (props.loadingFnnWSoftmaxPolicy || props.selectedFnnWSoftmaxPolicy === null || props.selectedFnnWSoftmaxPolicy === undefined) {
            if (props.loadingFnnWSoftmaxPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected feed-forward neural network policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <FnnWSoftmaxPolicy policy={props.selectedFnnWSoftmaxPolicy} wrapper={wrapper}
                                           key={props.selectedFnnWSoftmaxPolicy.id}
                                           removeFnnWSoftmaxPolicy={removeFnnWSoftmaxPolicyConfirm}
                                           sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const DQNPolicyAccordion = (props) => {
        if (props.loadingDQNPolicy || props.selectedDQNPolicy === null || props.selectedDQNPolicy === undefined) {
            if (props.loadingDQNPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected DQN policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <DQNPolicy policy={selectedDQNPolicy} wrapper={wrapper} key={selectedDQNPolicy.id}
                                   removeDQNPolicy={removeDQNPolicyConfirm}
                                   sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const TabularPolicyAccordion = (props) => {
        if (props.loadingTabularPolicy || props.selectedTabularPolicy === null || props.selectedTabularPolicy === undefined) {
            if (props.loadingTabularPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected tabular policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <TabularPolicy policy={selectedTabularPolicy} wrapper={wrapper} key={selectedTabularPolicy.id}
                                       removeTabularPolicy={removeTabularPolicyConfirm}
                                       sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const VectorPolicyAccordion = (props) => {
        if (props.loadingVectorPolicy || props.selectedVectorPolicy === null || props.selectedVectorPolicy === undefined) {
            if (props.loadingVectorPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected vector policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <VectorPolicy policy={selectedVectorPolicy} wrapper={wrapper} key={selectedVectorPolicy.id}
                                      removeVectorPolicy={removeVectorPolicyConfirm}
                                      sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const AlphaVecPolicyAccordion = (props) => {
        if (props.loadingAlphaVecPolicy || props.selectedAlphaVecPolicy === null || props.selectedAlphaVecPolicy === undefined) {
            if (props.loadingAlphaVecPolicy) {
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
                <div>
                    <h3 className="emulationConfigTitle">
                        Configuration of the selected alpha-vector policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <AlphaVecPolicy policy={selectedAlphaVecPolicy} wrapper={wrapper}
                                        key={selectedAlphaVecPolicy.id}
                                        removeAlphaVecPolicy={removeAlphaVecPolicyConfirm}
                                        sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const searchMultiThresholdPoliciesFilter = (multiThresholdPolicyId, searchVal) => {
        return (searchVal === "" || multiThresholdPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchMultiThresholdPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = multiThresholdPoliciesIds.filter(policyId => {
            return searchMultiThresholdPoliciesFilter(policyId, searchVal)
        });
        setFilteredMultiThresholdPoliciesIds(fPoliciesIds)
        setMultiThresholdPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingMultiThresholdPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedMultiThresholdPolicy !== null && selectedMultiThresholdPolicy !== undefined &&
                    selectedMultiThresholdPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
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
        if (!loadingPpoPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedPpoPolicy !== null && selectedPpoPolicy !== undefined &&
                    selectedPpoPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
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

    //fnn

    const searchFnnWSoftmaxPoliciesFilter = (fnnWSoftmaxPolicyId, searchVal) => {
        return (searchVal === "" || fnnWSoftmaxPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchFnnWSoftmaxPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = fnnWSoftmaxPoliciesIds.filter(policy => {
            return searchPPOPoliciesFilter(policy, searchVal)
        });
        setFilteredFnnWSoftmaxPoliciesIds(fPoliciesIds)
        setFnnWSoftmaxPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingFnnWSoftmaxPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedFnnWSoftmaxPolicy !== null && selectedFnnWSoftmaxPolicy !== undefined &&
                    selectedFnnWSoftmaxPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
                setSelectedFnnWSoftmaxPolicyId(fPoliciesIds[0])
                fetchFnnWSoftmaxPolicy(fPoliciesIds[0])
                setLoadingFnnWSoftmaxPolicy(true)
            }
        } else {
            setSelectedPpoPolicy(null)
        }
    }

    const searchFnnWSoftmaxPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchFnnWSoftmaxPolicyChange(event)
        },
        350
    );

    const searchDQNPoliciesFilter = (dqnPolicyId, searchVal) => {
        return (searchVal === "" || dqnPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchDQNPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = dqnPoliciesIds.filter(policy => {
            return searchDQNPoliciesFilter(policy, searchVal)
        });
        setFilteredDQNPoliciesIds(fPoliciesIds)
        setDQNPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingDQNPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedDQNPolicy !== null && selectedDQNPolicy !== undefined &&
                    selectedDQNPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
                setSelectedDQNPolicyId(fPoliciesIds[0])
                fetchDQNPolicy(fPoliciesIds[0])
                setLoadingDQNPolicy(true)
            }
        } else {
            setSelectedDQNPolicy(null)
        }
    }

    const searchDQNPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchDQNPolicyChange(event)
        },
        350
    );


    const searchTabularPoliciesFilter = (tabularPolicyId, searchVal) => {
        return (searchVal === "" || tabularPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchTabularPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = tabularPoliciesIds.filter(policy => {
            return searchTabularPoliciesFilter(policy, searchVal)
        });
        setFilteredTabularPoliciesIds(fPoliciesIds)
        setTabularPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingTabularPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedTabularPolicy !== null && selectedTabularPolicy !== undefined &&
                    selectedTabularPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
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

    const searchVectorPoliciesFilter = (vectorPolicyId, searchVal) => {
        return (searchVal === "" || vectorPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchVectorPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = vectorPoliciesIds.filter(policy => {
            return searchVectorPoliciesFilter(policy, searchVal)
        });
        setFilteredVectorPoliciesIds(fPoliciesIds)
        setVectorPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingVectorPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedVectorPolicy !== null && selectedVectorPolicy !== undefined &&
                    selectedVectorPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
                setSelectedVectorPolicyId(fPoliciesIds[0])
                fetchVectorPolicy(fPoliciesIds[0])
                setLoadingVectorPolicy(true)
            }
        } else {
            setSelectedVectorPolicy(null)
        }
    }

    const searchVectorPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchVectorPolicyChange(event)
        },
        350
    );

    const searchAlphaVecPoliciesFilter = (alphaVecPolicyId, searchVal) => {
        return (searchVal === "" || alphaVecPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchAlphaVecPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = alphaVecPoliciesIds.filter(policy => {
            return searchAlphaVecPoliciesFilter(policy, searchVal)
        });
        setFilteredAlphaVecPoliciesIds(fPoliciesIds)
        setAlphaVecPoliciesSearchString(searchVal)

        var selectedPolicyRemoved = false
        if (!loadingAlphaVecPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedAlphaVecPolicy !== null && selectedAlphaVecPolicy !== undefined &&
                    selectedAlphaVecPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
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
            <h3 className="managementTitle"> Management of Policies </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectMultiThresholdPolicyOrSpinner
                            loadingMultiThresholdPolicies={loadingMultiThresholdPolicies}
                            multiThresholdPoliciesIds={filteredMultiThresholdPoliciesIds}
                            selectedMultiThresholdPolicyId={selectedMultiThresholdPolicyId}
                            sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                                           selectedMultiThresholdPolicy={selectedMultiThresholdPolicy}
                                           sessionData={props.sessionData}
            />

            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectPpoPolicyOrSpinner loadingPPOPolicies={loadingPPOPolicies}
                                                  ppoPoliciesIds={filteredPPOPoliciesIds}
                                                  selectedPpoPolicyId={selectedPpoPolicyId}
                                                  sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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

            <PPOPolicyAccordion loadingPpoPolicy={loadingPpoPolicy} selectedPpoPolicy={selectedPpoPolicy}
                                sessionData={props.sessionData}
            />


            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectTabularPolicyOrSpinner loadingTabularPolicies={loadingTabularPolicies}
                                                      tabularPoliciesIds={filteredTabulaPoliciesIds}
                                                      selectedTabularPolicyId={selectedTabularPolicyId}
                                                      sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                                    selectedTabularPolicy={selectedTabularPolicy}
                                    sessionData={props.sessionData}/>


            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectAlphaVecPolicyOrSpinner loadingAlphaVecPolicies={loadingAlphaVecPolicies}
                                                       alphaVecPoliciesIds={filteredAlphaVecPoliciesIds}
                                                       selectedAlphaVecPolicyId={selectedAlphaVecPolicyId}
                                                       sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                                     selectedAlphaVecPolicy={selectedAlphaVecPolicy}
                                     sessionData={props.sessionData}
            />


            <div className="row dqnPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectDQNPolicyOrSpinner loadingDQNPolicies={loadingDQNPolicies}
                                                  dqnPoliciesIds={filteredDQNPoliciesIds}
                                                  selectedDQNPolicyId={selectedDQNPolicyId}
                                                  sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="dqnPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="dqnPoliciesSearchLabel"
                                aria-describedby="dqnPoliciesSearchField"
                                onChange={searchDQNPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <DQNPolicyAccordion loadingDQNPolicy={loadingDQNPolicy} selectedDQNPolicy={selectedDQNPolicy}
                                sessionData={props.sessionData}
            />

            <div className="row fnnWSoftmaxPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectFnnWSoftmaxPolicyOrSpinner loadingFnnWSoftmaxPolicies={loadingFnnWSoftmaxPolicies}
                                                          fnnWSoftmaxPoliciesIds={filteredFnnWSoftmaxPoliciesIds}
                                                          selectedFnnWSoftmaxPolicyId={selectedFnnWSoftmaxPolicyId}
                                                          sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="fnnWSoftmaxPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="fnnWSoftmaxPoliciesSearchLabel"
                                aria-describedby="fnnWSoftmaxPoliciesSearchField"
                                onChange={searchFnnWSoftmaxPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <FnnWSoftmaxPolicyAccordion loadingFnnWSoftmaxPolicy={loadingFnnWSoftmaxPolicy}
                                        selectedFnnWSoftmaxPolicy={selectedFnnWSoftmaxPolicy}
                                        sessionData={props.sessionData}/>


            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectVectorPolicyOrSpinner loadingVectorPolicies={loadingVectorPolicies}
                                                     vectorPoliciesIds={filteredVectorPoliciesIds}
                                                     selectedVectorPolicyId={selectedVectorPolicyId}
                                                     sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="vectorPoliciesSearchField" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="vectorPoliciesSearchLabel"
                                aria-describedby="vectorPoliciesSearchField"
                                onChange={searchVectorPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <VectorPolicyAccordion loadingVectorPolicy={loadingVectorPolicy}
                                   selectedVectorPolicy={selectedVectorPolicy}
                                   sessionData={props.sessionData}/>

        </div>
    );
}

Policies.propTypes = {};
Policies.defaultProps = {};
export default Policies;
