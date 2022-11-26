import React, {useState, useCallback, useEffect, createRef} from 'react';
import './AlphaVecPolicies.css';
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
import 'react-confirm-alert/src/react-confirm-alert.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import AlphaVecPolicy from "./AlphaVecPolicy/AlphaVecPolicy";
import PWLCValueFun from './PWLCValueFun.png'
import {
    ALPHA_VEC_POLICIES_RESOURCE,
    HTTP_PREFIX,
    HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM
} from "../../../Common/constants";

/**
 * Component representing an alphavector policy
 */
const AlphaVecPolicies = (props) => {
    const [showAlphaVectorPoliciesInfoModal, setShowAlphaVectorPoliciesInfoModal] = useState(false);
    const [alphaVecPoliciesIds, setAlphaVecPoliciesIds] = useState([]);
    const [selectedAlphaVecPolicy, setSelectedAlphaVecPolicy] = useState(null);
    const [selectedAlphaVecPolicyId, setSelectedALphaVecPolicyId] = useState(null);
    const [loadingAlphaVecPolicy, setLoadingAlphaVecPolicy] = useState(true);
    const [filteredAlphaVecPoliciesIds, setFilteredAlphaVecPoliciesIds] = useState([]);
    const [loadingAlphaVecPolicies, setLoadingAlphaVecPolicies] = useState(true);
    const ip = serverIp
    const port = serverPort
    const setSessionData = props.setSessionData
    const alert = useAlert();
    const navigate = useNavigate();
    const wrapper = createRef();

    const fetchAlphaVecPolicy = useCallback((alpha_vec_policy_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${ALPHA_VEC_POLICIES_RESOURCE}/${alpha_vec_policy_id.value}`
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
                setSelectedAlphaVecPolicy(response)
                setLoadingAlphaVecPolicy(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);

    const fetchAlphaVecPoliciesIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${ALPHA_VEC_POLICIES_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const alphavecPoliciesIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID: ${id_obj.id}, simulation: ${id_obj.simulation}`
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
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData, fetchAlphaVecPolicy]);

    const removeAlphaVecPoliciesRequest = useCallback((alpha_vec_policies_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${ALPHA_VEC_POLICIES_RESOURCE}/${alpha_vec_policies_id}`
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
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchAlphaVecPoliciesIds]);

    const removeAllAlphaVecPoliciesRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${ALPHA_VEC_POLICIES_RESOURCE}`
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
                fetchAlphaVecPoliciesIds()
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchAlphaVecPoliciesIds]);

    const removeAlphaVecPolicy = (alphaVecPolicy) => {
        setLoadingAlphaVecPolicies(true)
        removeAlphaVecPoliciesRequest(alphaVecPolicy.id)
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the alpha vector policies.
        </Tooltip>
    );

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

    const removeAllAlphaVecPolicies = () => {
        setLoadingAlphaVecPolicies(true)
        removeAllAlphaVecPoliciesRequest()
    }

    const refreshAlphaVecPolicies = () => {
        setLoadingAlphaVecPolicies(true)
        fetchAlphaVecPoliciesIds()
    }

    const renderRemoveAllAlphaVecPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all Alpha-Vector policies.
        </Tooltip>
    );

    const renderAlphaVecRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload Alpha-Vector policies from the backend
        </Tooltip>
    );

    const updateSelectedAlphaVecPolicyId = (selectedId) => {
        setSelectedALphaVecPolicyId(selectedId)
        fetchAlphaVecPolicy(selectedId)
        setLoadingAlphaVecPolicy(true)
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
                            Alpha-vector policy:
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

    const searchAlphaVecPoliciesFilter = (alphaVecPolicyId, searchVal) => {
        return (searchVal === "" || alphaVecPolicyId.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchAlphaVecPolicyChange = (event) => {
        var searchVal = event.target.value
        const fPoliciesIds = alphaVecPoliciesIds.filter(policy => {
            return searchAlphaVecPoliciesFilter(policy, searchVal)
        });
        setFilteredAlphaVecPoliciesIds(fPoliciesIds)

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

    useEffect(() => {
        setLoadingAlphaVecPolicies(true)
        fetchAlphaVecPoliciesIds()
    }, [fetchAlphaVecPoliciesIds]);

    return (
        <div>
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
        </div>
    )
}

AlphaVecPolicies.propTypes = {};
AlphaVecPolicies.defaultProps = {};
export default AlphaVecPolicies;
