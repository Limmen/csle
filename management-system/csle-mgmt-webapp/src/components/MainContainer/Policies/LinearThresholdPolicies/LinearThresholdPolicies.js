import React, {useState, useCallback, createRef, useEffect} from 'react';
import './LinearThresholdPolicies.css';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import LinearThresholdPolicy from "./LinearThresholdPolicy/LinearThresholdPolicy";
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
    LINEAR_THRESHOLD_POLICIES_RESOURCE,
} from "../../../Common/constants";

/**
 * Component representing Linear threshold policies
 */
const LinearThresholdPolicies = (props) => {
    const [showLinearThresholdPoliciesInfoModal, setShowLinearThresholdPoliciesInfoModal] = useState(false);
    const [linearThresholdPoliciesIds, setLinearThresholdPoliciesIds] = useState([]);
    const [filteredLinearThresholdPoliciesIds, setFilteredLinearThresholdPoliciesIds] = useState([]);
    const [selectedLinearThresholdPolicy, setSelectedLinearThresholdPolicy] = useState(null);
    const [selectedLinearThresholdPolicyId, setSelectedLinearThresholdPolicyId] = useState(null);
    const [loadingLinearThresholdPolicy, setLoadingLinearThresholdPolicy] = useState(true);
    const [loadingLinearThresholdPolicies, setLoadingLinearThresholdPolicies] = useState(true);

    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchLinearThresholdPolicy = useCallback((linear_threshold_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${LINEAR_THRESHOLD_POLICIES_RESOURCE}/${linear_threshold_policy_id.value}` +
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
                setSelectedLinearThresholdPolicy(response)
                setLoadingLinearThresholdPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchLinearThresholdPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LINEAR_THRESHOLD_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const linearThresholdPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
                    }
                })
                setLinearThresholdPoliciesIds(linearThresholdPoliciesIds)
                setFilteredLinearThresholdPoliciesIds(linearThresholdPoliciesIds)
                setLoadingLinearThresholdPolicies(false)
                if (linearThresholdPoliciesIds.length > 0) {
                    setSelectedLinearThresholdPolicyId(linearThresholdPoliciesIds[0])
                    fetchLinearThresholdPolicy(linearThresholdPoliciesIds[0])
                    setLoadingLinearThresholdPolicy(true)
                } else {
                    setLoadingLinearThresholdPolicy(false)
                    setSelectedLinearThresholdPolicy(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchLinearThresholdPolicy]);

    const removeLinearThresholdPoliciesRequest = useCallback((linear_threshold_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${LINEAR_THRESHOLD_POLICIES_RESOURCE}/${linear_threshold_policy_id}`
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
                fetchLinearThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchLinearThresholdPoliciesIds]);

    const removeAllLinearThresholdPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${LINEAR_THRESHOLD_POLICIES_RESOURCE}`
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
                fetchLinearThresholdPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchLinearThresholdPoliciesIds]);

    const removeLinearThresholdPolicy = (linearThresholdPolicy) => {
        setLoadingLinearThresholdPolicies(true)
        removeLinearThresholdPoliciesRequest(linearThresholdPolicy.id)
    }

    const removeAllLinearThresholdPolicies = () => {
        setLoadingLinearThresholdPolicies(true)
        removeAllLinearThresholdPoliciesRequest()
    }

    const removeAllLinearThresholdPoliciesConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all linear-threshold policies? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllLinearThresholdPolicies()
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
                                    Are you sure you want to delete all linear-threshold policies?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllLinearThresholdPolicies()
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

    const removeLinearThresholdPolicyConfirm = (linearThresholdPolicy) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the linear-threshold policy with ID: ' + linearThresholdPolicy.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeLinearThresholdPolicy(linearThresholdPolicy)
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
                                    Are you sure you want to delete the linear-threshold policy
                                    with ID {linearThresholdPolicy.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeLinearThresholdPolicy(linearThresholdPolicy)
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

    const refreshLinearThresholdPolicies = () => {
        setLoadingLinearThresholdPolicies(true)
        fetchLinearThresholdPoliciesIds()
    }

    const renderLinearThresholdPoliciesRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload linear-threshold policies from the backend
        </Tooltip>
    );

    const renderRemoveAllLinearThresholdPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all linear-threshold policies.
        </Tooltip>
    );

    const LinearThresholdPoliciesInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Linear-Threshold Policies
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

    const updateSelectedLinearThresholdPolicyId = (selectedId) => {
        setSelectedLinearThresholdPolicyId(selectedId)
        fetchLinearThresholdPolicy(selectedId)
        setLoadingLinearThresholdPolicy(true)
    }

    const DeleteAllLinearThresholdPoliciesOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllLinearThresholdPoliciesTooltip}
                >
                    <Button variant="danger" onClick={removeAllLinearThresholdPoliciesConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectLinearThresholdPolicyOrSpinner = (props) => {
        if (!props.loadingLinearThresholdPolicies && props.linearThresholdPoliciesIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No linear-threshold policies are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderLinearThresholdPoliciesRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshLinearThresholdPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loadingLinearThresholdPolicies) {
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
                            Linear-threshold policy:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedLinearThresholdPolicyId}
                                defaultValue={props.selectedLinearThresholdPolicyId}
                                options={props.linearThresholdPoliciesIds}
                                onChange={updateSelectedLinearThresholdPolicyId}
                                placeholder="Select policy"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderLinearThresholdPoliciesRefreshTooltip}
                    >
                        <Button variant="button" onClick={refreshLinearThresholdPolicies}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowLinearThresholdPoliciesInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <LinearThresholdPoliciesInfoModal show={showLinearThresholdPoliciesInfoModal} onHide={() => setShowLinearThresholdPoliciesInfoModal(false)}/>

                    <DeleteAllLinearThresholdPoliciesOrEmpty sessionData={props.sessionData}/>
                </div>
            )
        }
    }

    const LinearThresholdPolicyAccordion = (props) => {
        if (props.loadingLinearThresholdPolicy || props.selectedLinearThresholdPolicy === null ||
            props.selectedLinearThresholdPolicy === undefined) {
            if (props.loadingLinearThresholdPolicy) {
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
                        Configuration of the selected linear-threshold policy:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <LinearThresholdPolicy policy={selectedLinearThresholdPolicy} wrapper={wrapper}
                                               key={selectedLinearThresholdPolicy.id}
                                               removeLinearThresholdPolicy={removeLinearThresholdPolicyConfirm}
                                               sessionData={props.sessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const searchLinearThresholdPoliciesFilter = (linearThresholdPolicyId, searchVal) => {
        return (searchVal === "" || linearThresholdPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchLinearThresholdPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = linearThresholdPoliciesIds.filter(policyId => {
            return searchLinearThresholdPoliciesFilter(policyId, searchVal)
        });
        setFilteredLinearThresholdPoliciesIds(fPoliciesIds)

        var selectedPolicyRemoved = false
        if (!loadingLinearThresholdPolicy && fPoliciesIds.length > 0) {
            for (let i = 0; i < fPoliciesIds.length; i++) {
                if (selectedLinearThresholdPolicy !== null && selectedLinearThresholdPolicy !== undefined &&
                    selectedLinearThresholdPolicy.id === fPoliciesIds[i].value) {
                    selectedPolicyRemoved = true
                }
            }
            if (!selectedPolicyRemoved) {
                setSelectedLinearThresholdPolicyId(fPoliciesIds[0])
                fetchLinearThresholdPolicy(fPoliciesIds[0])
                setLoadingLinearThresholdPolicy(true)
            }
        } else {
            setSelectedLinearThresholdPolicy(null)
        }
    }

    const searchLinearThresholdPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchLinearThresholdPolicyChange(event)
        },
        350
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned Linear-threshold policies.
        </Tooltip>
    );

    useEffect(() => {
        setLoadingLinearThresholdPolicies(true)
        fetchLinearThresholdPoliciesIds()
    }, [fetchLinearThresholdPoliciesIds]);

    return (
        <div>
            <div className="row ppoPolicies simulationTracesHeader">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectLinearThresholdPolicyOrSpinner
                            loadingLinearThresholdPolicies={loadingLinearThresholdPolicies}
                            linearThresholdPoliciesIds={filteredLinearThresholdPoliciesIds}
                            selectedLinearThresholdPolicyId={selectedLinearThresholdPolicyId}
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
                                onChange={searchLinearThresholdPoliciesHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <LinearThresholdPolicyAccordion loadingLinearThresholdPolicy={loadingLinearThresholdPolicy}
                                           selectedLinearThresholdPolicy={selectedLinearThresholdPolicy}
                                           sessionData={props.sessionData}
            />
        </div>
    )
}

LinearThresholdPolicies.propTypes = {};
LinearThresholdPolicies.defaultProps = {};
export default LinearThresholdPolicies;
