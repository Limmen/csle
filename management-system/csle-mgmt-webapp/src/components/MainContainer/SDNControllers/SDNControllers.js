import React, {useState, useEffect, createRef, useCallback} from 'react';
import './SDNControllers.css';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import SDNController from "./SDNController/SDNController";
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    HTTP_PREFIX,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    SDN_CONTROLLERS_RESOURCE,
    EMULATION_EXECUTIONS_RESOURCE,
    EMULATION_QUERY_PARAM,
    IDS_QUERY_PARAM
} from "../../Common/constants";

/**
 * Component representing the /sdn-controllers-page
 */
const SDNControllers = (props) => {
    const [emulationExecutionsWithSdnControllersIds, setEmulationExecutionsWithSdnControllersIds] = useState(
        []);
    const [selectedEmulationExecutionWithSdnControllerId, setSelectedEmulationExecutionWithSdnControllerId] = useState(
        null);
    const [selectedEmulationExecutionWithSdnController, setSelectedEmulationExecutionWithSdnController] = useState(
        null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationExecution, setLoadingSelectedEmulationExecution] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredEmulationExecutionWithSdnControllerIds,
        setFilteredEmulationExecutionWithSdnControllerIds] = useState([]);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchEmulationExecutionWithSdnController = useCallback((id_obj) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}/${id_obj.value.id}`
                + `?${EMULATION_QUERY_PARAM}=${id_obj.value.emulation}`
                + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
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
                setSelectedEmulationExecutionWithSdnController(response)
                setLoadingSelectedEmulationExecution(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData.token, setSessionData]);

    const fetchEmulationExecutionsWithSdnControllersIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SDN_CONTROLLERS_RESOURCE}?${IDS_QUERY_PARAM}=true`
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
                const emulationExecutionIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: `ID: ${id_obj.id}, emulation: ${id_obj.emulation}`
                    }
                })
                setEmulationExecutionsWithSdnControllersIds(emulationExecutionIds)
                setFilteredEmulationExecutionWithSdnControllerIds(emulationExecutionIds)
                setLoading(false)
                if (emulationExecutionIds.length > 0) {
                    setSelectedEmulationExecutionWithSdnControllerId(emulationExecutionIds[0])
                    fetchEmulationExecutionWithSdnController(emulationExecutionIds[0])
                    setLoadingSelectedEmulationExecution(true)
                } else {
                    setLoadingSelectedEmulationExecution(false)
                    setSelectedEmulationExecutionWithSdnController(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, fetchEmulationExecutionWithSdnController, ip, navigate, port, props.sessionData.token, setSessionData]);

    useEffect(() => {
        setLoading(true)
        fetchEmulationExecutionsWithSdnControllersIds();
    }, [fetchEmulationExecutionsWithSdnControllersIds]);

    const updateSelectedEmulationExecutionWithSdnControllerId = (selectedId) => {
        setSelectedEmulationExecutionWithSdnControllerId(selectedId)
        fetchEmulationExecutionWithSdnController(selectedId)
        setLoadingSelectedEmulationExecution(true)
    }

    const refresh = () => {
        setLoading(true)
        fetchEmulationExecutionsWithSdnControllersIds()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const searchFilter = (em_id_obj, searchVal) => {
        return (searchVal === "" || em_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmsIds = emulationExecutionsWithSdnControllersIds.filter(em => {
            return searchFilter(em, searchVal)
        });
        setFilteredEmulationExecutionWithSdnControllerIds(filteredEmsIds)

        var selectedEmulationRemoved = false
        if (!loadingSelectedEmulationExecution && filteredEmsIds.length > 0) {
            for (let i = 0; i < filteredEmsIds.length; i++) {
                if (selectedEmulationExecutionWithSdnController !== null && selectedEmulationExecutionWithSdnController !== undefined &&
                    selectedEmulationExecutionWithSdnController.id === filteredEmsIds[i].value) {
                    selectedEmulationRemoved = true
                }
            }
            if (!selectedEmulationRemoved) {
                setSelectedEmulationExecutionWithSdnControllerId(filteredEmsIds[0])
                fetchEmulationExecutionWithSdnController(filteredEmsIds[0])
                setLoadingSelectedEmulationExecution(true)
            }
        } else {
            setSelectedEmulationExecutionWithSdnController(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const SDNControllerAccordion = (props) => {
        if (props.loadingSelectedEmulationExecution || props.selectedEmulationExecutionWithSdnController === null || props.selectedEmulationExecutionWithSdnController === undefined) {
            if (props.loadingSelectedEmulationExecution) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching SDN Controller information... </span>
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
                        SDN Controller Configuration:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <SDNController execution={props.selectedEmulationExecutionWithSdnController}
                                       wrapper={wrapper} key={props.selectedEmulationExecutionWithSdnController.name}
                                       sessionData={props.sessionData}
                                       setSessionData={props.setSessionData}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const SelectEmulationExecutionWithSdnControllerOrSpinner = (props) => {
        if (!props.loading && props.emulationExecutionWithSdnControllerIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No SDN controllers are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching SDN controllers... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Running SDN controller:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationExecutionWithSdnControllerId}
                                defaultValue={props.selectedEmulationExecutionWithSdnControllerId}
                                options={props.emulationExecutionWithSdnControllerIds}
                                onChange={updateSelectedEmulationExecutionWithSdnControllerId}
                                placeholder="Select emulation execution"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={info}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                </div>
            )
        }
    }

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        SDN Controllers
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        The SDN controller defines the control plane in a software-defined network (SDN) and provides
                        a southbound API to the data plane, which is defined by a set of programmable switches
                        (typically OpenFlow-enabled switches) as well as a northbound API for applications that
                        use the SDN.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload SDN controllers from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the SDN controllers
        </Tooltip>
    );

    const wrapper = createRef();

    return (
        <div className="SDNControllers">
            <h3 className="managementTitle"> Management of SDN Controllers </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationExecutionWithSdnControllerOrSpinner
                            loading={loading}
                            emulationExecutionWithSdnControllerIds={filteredEmulationExecutionWithSdnControllerIds}
                            selectedEmulationExecutionWithSdnControllerId={selectedEmulationExecutionWithSdnControllerId}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
            </div>
            <SDNControllerAccordion
                loadingSelectedEmulationExecution={loadingSelectedEmulationExecution}
                selectedEmulationExecutionWithSdnController={selectedEmulationExecutionWithSdnController}
                sessionData={props.sessionData}
                setSessionData={setSessionData}
            />
        </div>
    );
}

SDNControllers.propTypes = {};
SDNControllers.defaultProps = {};
export default SDNControllers;
