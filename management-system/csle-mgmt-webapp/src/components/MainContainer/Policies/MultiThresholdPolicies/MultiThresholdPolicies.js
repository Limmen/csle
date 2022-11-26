import React, {useState, useCallback, createRef, useEffect} from 'react';
import './MultiThresholdPolicies.css';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import MultiThresholdPolicy from "./MultiThresholdPolicy/MultiThresholdPolicy";
import Modal from 'react-bootstrap/Modal'
import ThresholdPolicyImg from './ThresholdPolicy.png'
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
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
    MULTI_THRESHOLD_POLICIES_RESOURCE,
} from "../../../Common/constants";

/**
 * Component representing a Multi threshold policy
 */
const MultiThesholdPolicies = (props) => {
    const [showMultiThresholdPoliciesInfoModal, setShowMultiThresholdPoliciesInfoModal] = useState(false);
    const [multiThresholdPoliciesIds, setMultiThresholdPoliciesIds] = useState([]);
    const [filteredMultiThresholdPoliciesIds, setFilteredMultiThresholdPoliciesIds] = useState([]);
    const [selectedMultiThresholdPolicy, setSelectedMultiThresholdPolicy] = useState(null);
    const [selectedMultiThresholdPolicyId, setSelectedMultiThresholdPolicyId] = useState(null);
    const [loadingMultiThresholdPolicy, setLoadingMultiThresholdPolicy] = useState(true);
    const [loadingMultiThresholdPolicies, setLoadingMultiThresholdPolicies] = useState(true);

    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchMultiThresholdPolicy = useCallback((multi_threshold_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${MULTI_THRESHOLD_POLICIES_RESOURCE}/${multi_threshold_policy_id.value}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedMultiThresholdPolicy(response)
                setLoadingMultiThresholdPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchMultiThresholdPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${MULTI_THRESHOLD_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const multiThresholdPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchMultiThresholdPolicy]);

    const removeMultiThresholdPoliciesRequest = useCallback((multi_threshold_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${MULTI_THRESHOLD_POLICIES_RESOURCE}/${multi_threshold_policy_id}`
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
                fetchMultiThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchMultiThresholdPoliciesIds]);

    const removeAllMultiThresholdPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${MULTI_THRESHOLD_POLICIES_RESOURCE}`
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
                fetchMultiThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchMultiThresholdPoliciesIds]);

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

    const refreshMultiThresholdPolicies = () => {
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPoliciesIds()
    }

    const renderMultiThresholdPoliciesRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload multi-threshold policies from the backend
        </Tooltip>
    );

    const renderRemoveAllMultiThresholdPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all multi-threshold policies.
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

    const updateSelectedMultiThresholdPolicyId = (selectedId) => {
        setSelectedMultiThresholdPolicyId(selectedId)
        fetchMultiThresholdPolicy(selectedId)
        setLoadingMultiThresholdPolicy(true)
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
                            Multi-threshold policy:
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

    const searchMultiThresholdPoliciesFilter = (multiThresholdPolicyId, searchVal) => {
        return (searchVal === "" || multiThresholdPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchMultiThresholdPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = multiThresholdPoliciesIds.filter(policyId => {
            return searchMultiThresholdPoliciesFilter(policyId, searchVal)
        });
        setFilteredMultiThresholdPoliciesIds(fPoliciesIds)

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

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned Multi-threshold policies.
        </Tooltip>
    );

    useEffect(() => {
        setLoadingMultiThresholdPolicies(true)
        fetchMultiThresholdPoliciesIds()
    }, [fetchMultiThresholdPoliciesIds]);

    return (
        <div>
            <div className="row ppoPolicies simulationTracesHeader">
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
        </div>
    )
}

MultiThesholdPolicies.propTypes = {};
MultiThesholdPolicies.defaultProps = {};
export default MultiThesholdPolicies;
