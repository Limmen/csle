import React, {useState, useCallback, createRef, useEffect} from 'react';
import './FnnWSoftmaxPolicies.css';
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
import FnnWSoftmaxPolicy from "./FnnWSoftmaxPolicy/FnnWSoftmaxPolicy";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import NeuralNetworkPolicies from './../NeuralNetworkPolicies.png'
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
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
    FNN_W_SOFTMAX_POLICIES_RESOURCE
} from "../../../Common/constants";

/**
 * Component representing a feed-forward neural network with softmax policy
 */
const FnnWSoftmaxPolicies = (props) => {
    const [showFNNPoliciesInfoModal, setShowFNNPoliciesInfoModal] = useState(false);
    const [fnnWSoftmaxPoliciesIds, setFnnWSoftmaxPoliciesIds] = useState([]);
    const [selectedFnnWSoftmaxPolicy, setSelectedFnnWSoftmaxPolicy] = useState(null);
    const [selectedFnnWSoftmaxPolicyId, setSelectedFnnWSoftmaxPolicyId] = useState(null);
    const [loadingFnnWSoftmaxPolicy, setLoadingFnnWSoftmaxPolicy] = useState(true);
    const [filteredFnnWSoftmaxPoliciesIds, setFilteredFnnWSoftmaxPoliciesIds] = useState([]);
    const [loadingFnnWSoftmaxPolicies, setLoadingFnnWSoftmaxPolicies] = useState(true);

    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchFnnWSoftmaxPolicy = useCallback((fnn_w_softmax_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${FNN_W_SOFTMAX_POLICIES_RESOURCE}/${fnn_w_softmax_policy_id.value}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedFnnWSoftmaxPolicy(response)
                setLoadingFnnWSoftmaxPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchFnnWSoftmaxPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${FNN_W_SOFTMAX_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const fnnWSoftmaxPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchFnnWSoftmaxPolicy]);

    const removeFnnWSoftmaxPoliciesRequest = useCallback((fnn_w_softmax_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${FNN_W_SOFTMAX_POLICIES_RESOURCE}/${fnn_w_softmax_policy_id}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                fetchFnnWSoftmaxPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchFnnWSoftmaxPoliciesIds]);

    const removeAllFnnWSoftmaxPoliciesRequest = useCallback(() => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${FNN_W_SOFTMAX_POLICIES_RESOURCE}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                fetchFnnWSoftmaxPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchFnnWSoftmaxPoliciesIds]);

    const removeFnnWSoftmaxPolicy = (fnnWSoftmaxPolicy) => {
        setLoadingFnnWSoftmaxPolicies(true)
        removeFnnWSoftmaxPoliciesRequest(fnnWSoftmaxPolicy.id)
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

    const removeAllFnnWSoftmaxPolicies = () => {
        setLoadingFnnWSoftmaxPolicies(true)
        removeAllFnnWSoftmaxPoliciesRequest()
    }

    const refreshFnnWSoftmaxPolicies = () => {
        setLoadingFnnWSoftmaxPolicies(true)
        fetchFnnWSoftmaxPoliciesIds()
    }

    const renderRemoveAllFnnWSoftmaxPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Feed-forward neural network with softmax output policies.
        </Tooltip>
    );

    const renderFnnWSoftmaxRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload feed-forward neural network policies with softmax outputs from the backend
        </Tooltip>
    );

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
                            Feed-forward neural network policy:
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

    const searchFnnWSoftmaxPoliciesFilter = (fnnWSoftmaxPolicyId, searchVal) => {
        return (searchVal === "" || fnnWSoftmaxPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchFnnWSoftmaxPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = fnnWSoftmaxPoliciesIds.filter(policy => {
            return searchFnnWSoftmaxPoliciesFilter(policy, searchVal)
        });
        setFilteredFnnWSoftmaxPoliciesIds(fPoliciesIds)

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
            setSelectedFnnWSoftmaxPolicy(null)
        }
    }

    const searchFnnWSoftmaxPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchFnnWSoftmaxPolicyChange(event)
        },
        350
    );

    const updateSelectedFnnWSoftmaxPolicyId = (selectedId) => {
        setSelectedFnnWSoftmaxPolicyId(selectedId)
        fetchFnnWSoftmaxPolicy(selectedId)
        setLoadingFnnWSoftmaxPolicy(true)
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned feed-forward neural network with softmax policies.
        </Tooltip>
    );

    useEffect(() => {
        setLoadingFnnWSoftmaxPolicies(true)
        fetchFnnWSoftmaxPoliciesIds()
    }, [fetchFnnWSoftmaxPoliciesIds]);

    return (
        <div>
            <div className="row ppoPolicies simulationTracesHeader">
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
        </div>
    )
}

FnnWSoftmaxPolicies.propTypes = {};
FnnWSoftmaxPolicies.defaultProps = {};
export default FnnWSoftmaxPolicies;
