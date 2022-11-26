import React, {useState, useCallback, createRef, useEffect} from 'react';
import './VectorPolicies.css';
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";
import VectorPolicy from "./VectorPolicy/VectorPolicy";
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
    VECTOR_POLICIES_RESOURCE
} from "../../../Common/constants";

/**
 * Component representing a Vector policy
 */
const VectorPolicies = (props) => {
    const [showVectorPoliciesInfoModal, setShowVectorPoliciesInfoModal] = useState(false);
    const [vectorPoliciesIds, setVectorPoliciesIds] = useState([]);
    const [selectedVectorPolicy, setSelectedVectorPolicy] = useState(null);
    const [selectedVectorPolicyId, setSelectedVectorPolicyId] = useState(null);
    const [loadingVectorPolicy, setLoadingVectorPolicy] = useState(true);
    const [filteredVectorPoliciesIds, setFilteredVectorPoliciesIds] = useState([]);
    const [loadingVectorPolicies, setLoadingVectorPolicies] = useState(true);
    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchVectorPolicy = useCallback((vector_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${VECTOR_POLICIES_RESOURCE}/${vector_policy_id.value}`
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
                setSelectedVectorPolicy(response)
                setLoadingVectorPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchVectorPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${VECTOR_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const vectorPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchVectorPolicy]);

    const removeVectorPoliciesRequest = useCallback((vector_policy_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${VECTOR_POLICIES_RESOURCE}/${vector_policy_id}`
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
                fetchVectorPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchVectorPoliciesIds]);

    const removeAllVectorPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${VECTOR_POLICIES_RESOURCE}`
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
                fetchVectorPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port,  navigate, props.sessionData.token, setSessionData, fetchVectorPoliciesIds]);

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

    const renderVectorRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Vector policies from the backend
        </Tooltip>
    );

    const renderRemoveAllVectorPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Vector policies.
        </Tooltip>
    );

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

    const updateSelectedVectorPolicyId = (selectedId) => {
        setSelectedVectorPolicyId(selectedId)
        fetchVectorPolicy(selectedId)
        setLoadingVectorPolicy(true)
    }

    const refreshVectorPolicies = () => {
        setLoadingVectorPolicies(true)
        fetchVectorPoliciesIds()
    }

    const removeAllVectorPolicies = () => {
        setLoadingVectorPolicies(true)
        removeAllVectorPoliciesRequest()
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
                            Vector policy:
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

    const searchVectorPoliciesFilter = (vectorPolicyId, searchVal) => {
        return (searchVal === "" || vectorPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchVectorPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = vectorPoliciesIds.filter(policy => {
            return searchVectorPoliciesFilter(policy, searchVal)
        });
        setFilteredVectorPoliciesIds(fPoliciesIds)

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

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about learned vector policies.
        </Tooltip>
    );

    const searchVectorPoliciesHandler = useDebouncedCallback(
        (event) => {
            searchVectorPolicyChange(event)
        },
        350
    );


    useEffect(() => {
        setLoadingVectorPolicies(true)
        fetchVectorPoliciesIds()
    }, [fetchVectorPoliciesIds]);

    return (
        <div>
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
    )
}

VectorPolicies.propTypes = {};
VectorPolicies.defaultProps = {};
export default VectorPolicies;
