import React, {useState, useCallback, createRef, useEffect} from 'react';
import './TabularPolicies.css';
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
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import TabularPolicyImg from './TabularPolicyImg.png'
import TabularPolicy from "./TabularPolicy/TabularPolicy";
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
    TABULAR_POLICIES_RESOURCE
} from "../../../Common/constants";

/**
 * Component representing a Tabular policy
 */
const TabularPolicies = (props) => {
    const [showTabularPoliciesInfoModal, setShowTabularPoliciesInfoModal] = useState(false);
    const [tabularPoliciesIds, setTabularPoliciesIds] = useState([]);
    const [selectedTabularPolicy, setSelectedTabularPolicy] = useState(null);
    const [selectedTabularPolicyId, setSelectedTabularPolicyId] = useState(null);
    const [loadingTabularPolicy, setLoadingTabularPolicy] = useState(true);
    const [filteredTabulaPoliciesIds, setFilteredTabularPoliciesIds] = useState([]);
    const [loadingTabularPolicies, setLoadingTabularPolicies] = useState(true);

    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchTabularPolicy = useCallback((tabular_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${TABULAR_POLICIES_RESOURCE}/${tabular_policy_id.value}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedTabularPolicy(response)
                setLoadingTabularPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchTabularPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TABULAR_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const tabularPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchTabularPolicy]);


    const removeTabularPoliciesRequest = useCallback((tabular_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TABULAR_POLICIES_RESOURCE}/${tabular_policy_id}`
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
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchTabularPoliciesIds]);

    const removeAllTabularPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TABULAR_POLICIES_RESOURCE}`
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
                fetchTabularPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchTabularPoliciesIds]);

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

    const removeAllTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        removeAllTabularPoliciesRequest()
    }

    const refreshTabularPolicies = () => {
        setLoadingTabularPolicies(true)
        fetchTabularPoliciesIds()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned tabular policies.
        </Tooltip>
    );

    const renderRemoveAllTabularPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Tabular policies.
        </Tooltip>
    );

    const renderTabularRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Tabular policies from the backend
        </Tooltip>
    );

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

    const updateSelectedTabularPolicyId = (selectedId) => {
        setSelectedTabularPolicyId(selectedId)
        fetchTabularPolicy(selectedId)
        setLoadingTabularPolicy(true)
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
                            Tabular policy:
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

    const searchTabularPoliciesFilter = (tabularPolicyId, searchVal) => {
        return (searchVal === "" || tabularPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchTabularPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = tabularPoliciesIds.filter(policy => {
            return searchTabularPoliciesFilter(policy, searchVal)
        });
        setFilteredTabularPoliciesIds(fPoliciesIds)

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

    useEffect(() => {
        setLoadingTabularPolicies(true)
        fetchTabularPoliciesIds()
    }, [fetchTabularPoliciesIds]);

    return (
        <div>
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
        </div>
    )
}

TabularPolicies.propTypes = {};
TabularPolicies.defaultProps = {};
export default TabularPolicies;
