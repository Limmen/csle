import React, {useState, useCallback, createRef, useEffect} from 'react';
import './PPOPolicies.css';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Modal from 'react-bootstrap/Modal'
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import NeuralNetworkPolicies from './../NeuralNetworkPolicies.png'
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import PPOPolicy from "./PPOPolicy/PPOPolicy";
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import {
    HTTP_PREFIX,
    HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM,
    PPO_POLICIES_RESOURCE
} from "../../../Common/constants";

/**
 * Component representing a PPO policy
 */
const PPOPolicies = (props) => {
    const [showPPOPoliciesInfoModal, setShowPPOPoliciesInfoModal] = useState(false);
    const [ppoPoliciesIds, setPpoPoliciesIds] = useState([]);
    const [selectedPpoPolicy, setSelectedPpoPolicy] = useState(null);
    const [selectedPpoPolicyId, setSelectedPpoPolicyId] = useState(null);
    const [loadingPpoPolicy, setLoadingPpoPolicy] = useState(true);
    const [filteredPPOPoliciesIds, setFilteredPPOPoliciesIds] = useState([]);
    const [loadingPPOPolicies, setLoadingPPOPolicies] = useState(true);
    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchPpoPolicy = useCallback((ppo_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PPO_POLICIES_RESOURCE}/${ppo_policy_id.value}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept:
                        "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchPPOPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PPO_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
            + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchPpoPolicy]);

    const removePpoPoliciesRequest = useCallback((ppo_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PPO_POLICIES_RESOURCE}/${ppo_policy_id}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchPPOPoliciesIds]);

    const removeAllPpoPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${PPO_POLICIES_RESOURCE}` +
            `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchPPOPoliciesIds]);

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

    const removeAllPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        removeAllPpoPoliciesRequest()
    }

    const refreshPPOPolicies = () => {
        setLoadingPPOPolicies(true)
        fetchPPOPoliciesIds()
    }

    const renderRemoveAllPPOPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all PPO policies.
        </Tooltip>
    );

    const renderPPORefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload PPO policies from the backend
        </Tooltip>
    );

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

    const updateSelectedPpoPolicyId = (selectedId) => {
        setSelectedPpoPolicyId(selectedId)
        fetchPpoPolicy(selectedId)
        setLoadingPpoPolicy(true)
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
                            PPO policy:
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

    const searchPPOPoliciesFilter = (ppoPolicyId, searchVal) => {
        return (searchVal === "" || ppoPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchPPOPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = ppoPoliciesIds.filter(policy => {
            return searchPPOPoliciesFilter(policy, searchVal)
        });
        setFilteredPPOPoliciesIds(fPoliciesIds)

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

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned PPO policies.
        </Tooltip>
    );

    useEffect(() => {
        setLoadingPPOPolicies(true)
        fetchPPOPoliciesIds()
    }, [fetchPPOPoliciesIds]);

    return (
        <div>
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
        </div>
    )
}

PPOPolicies.propTypes = {};
PPOPolicies.defaultProps = {};
export default PPOPolicies;
