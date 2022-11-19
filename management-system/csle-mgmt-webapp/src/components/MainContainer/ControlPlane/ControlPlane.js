import React, {useState, useEffect, useCallback, createRef} from 'react';
import "rc-slider/assets/index.css";
import './ControlPlane.css';
import Select from 'react-select'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import ControlPlaneImg from './ControlPlane.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import ExecutionControlPlane from "./ExecutionControlPlane/ExecutionControlPlane";
import Accordion from 'react-bootstrap/Accordion';
import {useDebouncedCallback} from 'use-debounce';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";

/**
 * Component with a user interface to the control plane of the emulations
 */
const ControlPlane = (props) => {
    const [emulationExecutionIds, setEmulationExecutionIds] = useState([]);
    const [filteredEmulationExecutionIds, setFilteredEmulationExecutionIds] = useState([]);
    const [emulationExecutionContainerOptions, setEmulationExecutionContainerOptions] = useState([]);
    const [selectedEmulationExecutionId, setSelectedEmulationExecutionId] = useState(null);
    const [selectedEmulationExecution, setSelectedEmulationExecution] = useState(null);
    const [selectedEmulationExecutionInfo, setSelectedEmulationExecutionInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationExecution, setLoadingSelectedEmulationExecution] = useState(true);
    const [loadingSelectedEmulationExecutionInfo, setLoadingSelectedEmulationExecutionInfo] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [searchString, setSearchString] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();

    // const ip = "172.31.212.92"

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload data about emulations from the backend
        </Tooltip>
    );

    const updateEmulationExecutionId = (emulationExecutionId) => {
        setSelectedEmulationExecutionId(emulationExecutionId)
        fetchSelectedExecution(emulationExecutionId)
        fetchExecutionInfo(emulationExecutionId)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
    }

    const refresh = () => {
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
        setSelectedEmulationExecution(null)
        setSelectedEmulationExecutionInfo(null)
        fetchEmulationExecutionIds()
    }

    const searchFilter = (executionIdObj, searchVal) => {
        return (searchVal === "" || executionIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEIds = emulationExecutionIds.filter(executionIdObj => {
            return searchFilter(executionIdObj, searchVal)
        });
        setFilteredEmulationExecutionIds(filteredEIds)
        setSearchString(searchVal)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const fetchExecutionInfo = useCallback((id_obj) => fetch(
        (`http://` + ip + ':7777/emulation-executions/' + id_obj.value.id + "/info?emulation="
            + id_obj.value.emulation + "&token=" + props.sessionData.token),
        {
            method: "GET",
            headers: new Headers({
                Accept: "application/vnd.github.cloak-preview"
            })
        }
    )
        .then(res => {
            if (res.status === 401) {
                alert.show("Session token expired. Please login again.")
                props.setSessionData(null)
                navigate("/login-page");
                return null
            }
            return res.json()
        })
        .then(response => {
            if (response === null) {
                return
            }
            setSelectedEmulationExecutionInfo(response)
            setLoadingSelectedEmulationExecutionInfo(false)
        })
        .catch(error => console.log("error:" + error)), []);

    const startOrStopEntity = useCallback((id, emulation, start, stop, entity, name, node_ip) => {
        fetch(
            `http://` + ip + ':7777/emulation-executions/' + id + "/" + entity + "?emulation="
            + emulation + "&token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({start: start, stop: stop, name: name, ip: node_ip})
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
                var id_obj = {
                    value: {
                        id: id,
                        emulation: emulation
                    }
                }
                fetchSelectedExecution(id_obj)
                fetchExecutionInfo(id_obj)
                setLoadingSelectedEmulationExecution(true)
                setLoadingSelectedEmulationExecutionInfo(true)
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the control plane
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Control plane for managing emulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        To perform these management operations, a dedicated management network is used.
                        Each component in the emulated infrastructure has a dedicated port to
                        communicate with the management network. The reason for using a dedicated management network
                        instead of carrying management traffic on the same network as the rest of the services is to
                        avoid interference and to simplify control of the network.
                    </p>
                    <div className="text-center">
                        <img src={ControlPlaneImg} alt="Markov chain" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const fetchEmulationExecutionIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulation-executions?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                const emulationExecutionIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setEmulationExecutionIds(emulationExecutionIds)
                setFilteredEmulationExecutionIds(emulationExecutionIds)
                setLoading(false)
                if (emulationExecutionIds.length > 0) {
                    setSelectedEmulationExecutionId(emulationExecutionIds[0])
                    fetchSelectedExecution(emulationExecutionIds[0])
                    fetchExecutionInfo(emulationExecutionIds[0])
                    setLoadingSelectedEmulationExecution(true)
                    setLoadingSelectedEmulationExecutionInfo(true)
                } else {
                    setLoadingSelectedEmulationExecution(false)
                    setLoadingSelectedEmulationExecutionInfo(false)
                    setSelectedEmulationExecution(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSelectedExecution = useCallback((id_obj) => {
        fetch(
            (`http://` + ip + ':7777/emulation-executions/' + id_obj.value.id + "?emulation="
                + id_obj.value.emulation + "&token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setSelectedEmulationExecution(response)
                setLoadingSelectedEmulationExecution(false)
                if (response !== null && response !== undefined) {
                    const containerOptions = response.emulation_env_config.containers_config.containers.map((c, index) => {
                        return {
                            value: c,
                            label: c.full_name_str
                        }
                    })
                    setEmulationExecutionContainerOptions(containerOptions)
                }

            })
            .catch(error => console.log("error:" + error))
    }, []);

    const wrapper = createRef();

    useEffect(() => {
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
        fetchEmulationExecutionIds()
    }, [fetchEmulationExecutionIds]);

    const SelectedExecutionView = (props) => {
        if (props.loading || props.loadingSelectedEmulationExecution || props.loadingSelectedEmulationExecutionInfo
            || props.selectedEmulationExecution === null || props.selectedEmulationExecution === undefined ||
            props.selectedEmulationExecutionInfo === undefined || props.selectedEmulationExecutionInfo === null) {
            if (props.loadingSelectedEmulationExecution || props.loadingSelectedEmulationExecutionInfo) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching execution... </span>
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
                        Selected execution:
                    </h3>
                    <Accordion defaultActiveKey="0">
                        <ExecutionControlPlane
                            execution={props.selectedEmulationExecution} wrapper={wrapper}
                            key={props.selectedEmulationExecution.name}
                            sessionData={props.sessionData}
                            info={props.selectedEmulationExecutionInfo}
                            startOrStopEntity={props.startOrStopEntity}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const SelectEmulationExecutionIdDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationExecutionIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No running executions are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching executions... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (<div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    Selected emulation execution:
                    <div className="conditionalDist inline-block selectEmulation">
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationExecutionId}
                                defaultValue={props.selectedEmulationExecutionId}
                                options={props.emulationExecutionIds}
                                onChange={updateEmulationExecutionId}
                                placeholder="Select an emulation execution"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    return (
        <div className="container-fluid">
            <h3 className="managementTitle"> Emulations Control Plane </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationExecutionIdDropdownOrSpinner
                            loading={loading} emulationExecutionIds={filteredEmulationExecutionIds}
                            selectedEmulationExecutionId={selectedEmulationExecutionId}
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
                <div className="col-sm-1">
                </div>
            </div>
            <SelectedExecutionView loadingSelectedEmulationExecution={loadingSelectedEmulationExecution}
                                   loadingSelectedEmulationExecutionInfo={loadingSelectedEmulationExecutionInfo}
                                   selectedEmulationExecution={selectedEmulationExecution}
                                   selectedEmulationExecutionInfo={selectedEmulationExecutionInfo}
                                   emulationExecutionContainerOptions={emulationExecutionContainerOptions}
                                   startOrStopEntity={startOrStopEntity}
            />
        </div>
    );
}

ControlPlane.propTypes = {};
ControlPlane.defaultProps = {};
export default ControlPlane;
