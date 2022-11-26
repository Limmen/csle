import React, {useState, useCallback, createRef, useEffect} from 'react';
import './DQNPolicies.css';
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
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import DQNPolicy from "./DQNPolicy/DQNPolicy";
import {
    HTTP_PREFIX,
    HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM, DQN_POLICIES_RESOURCE
} from "../../../Common/constants";

/**
 * Component representing a DQN policy
 */
const DQNPolicies = (props) => {
    const [showDQNPoliciesInfoModal, setShowDQNPoliciesInfoModal] = useState(false);
    const [dqnPoliciesIds, setDQNPoliciesIds] = useState([]);
    const [selectedDQNPolicy, setSelectedDQNPolicy] = useState(null);
    const [selectedDQNPolicyId, setSelectedDQNPolicyId] = useState(null);
    const [loadingDQNPolicy, setLoadingDQNPolicy] = useState(true);
    const [filteredDQNPoliciesIds, setFilteredDQNPoliciesIds] = useState([]);
    const [loadingDQNPolicies, setLoadingDQNPolicies] = useState(true);

    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchDQNPolicy = useCallback((dqn_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DQN_POLICIES_RESOURCE}/${dqn_policy_id.value}`
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
                setSelectedDQNPolicy(response)
                setLoadingDQNPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchDQNPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DQN_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const dqnPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, fetchDQNPolicy, ip, navigate, port, props.sessionData.token, setSessionData]);


    const removeDQNPoliciesRequest = useCallback((dqn_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DQN_POLICIES_RESOURCE}/${dqn_policy_id}`
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
                fetchDQNPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchDQNPoliciesIds]);

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

    const removeAllDQNPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${DQN_POLICIES_RESOURCE}`
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
                fetchDQNPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchDQNPoliciesIds]);

    const removeDQNPolicy = (dqnPolicy) => {
        setLoadingDQNPolicies(true)
        removeDQNPoliciesRequest(dqnPolicy.id)
    }

    const removeAllDQNPolicies = () => {
        setLoadingDQNPolicies(true)
        removeAllDQNPoliciesRequest()
    }

    const refreshDQNPolicies = () => {
        setLoadingDQNPolicies(true)
        fetchDQNPoliciesIds()
    }

    const renderRemoveAllDQNPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all DQN policies.
        </Tooltip>
    );

    const renderDQNRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload DQN policies from the backend
        </Tooltip>
    );

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
                            DQN policy:
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

    const searchDQNPoliciesFilter = (dqnPolicyId, searchVal) => {
        return (searchVal === "" || dqnPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchDQNPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = dqnPoliciesIds.filter(policy => {
            return searchDQNPoliciesFilter(policy, searchVal)
        });
        setFilteredDQNPoliciesIds(fPoliciesIds)

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

    const updateSelectedDQNPolicyId = (selectedId) => {
        setSelectedDQNPolicyId(selectedId)
        fetchDQNPolicy(selectedId)
        setLoadingDQNPolicy(true)
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the learned DQN policies.
        </Tooltip>
    );

    useEffect(() => {
        setLoadingDQNPolicies(true)
        fetchDQNPoliciesIds()
    }, [fetchDQNPoliciesIds]);

    return (
        <div>
            <div className="row ppoPolicies simulationTracesHeader">
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
        </div>
    )
}

DQNPolicies.propTypes = {};
DQNPolicies.defaultProps = {};
export default DQNPolicies;
