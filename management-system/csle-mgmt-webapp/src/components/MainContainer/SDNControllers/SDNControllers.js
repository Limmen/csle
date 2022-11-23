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
import {HTTP_PREFIX} from "../../Common/constants";

/**
 * Component representing the /sdn-controllers-page
 */
const SDNControllers = (props) => {
    const [emulationIds, setEmulationIds] = useState([]);
    const [selectedEmulationId, setSelectedEmulationId] = useState(null);
    const [selectedEmulation, setSelectedEmulation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulation, setLoadingSelectedEmulation] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredEmulationsIds, setFilteredEmulationsIds] = useState([]);
    const [searchString, setSearchString] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    // const ip = "172.31.212.92"

    const fetchEmulationIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/` + ip + ':' + port +'/sdn-controllers?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                if(response === null) {
                    return
                }
                const emulationIds = response.map((id_obj, index) => {
                    var lbl = "ID: " + id_obj.id + ", name: " + id_obj.emulation + ", ip: " + id_obj.ip
                    return {
                        value: id_obj.id,
                        running: id_obj.running,
                        exec_id: id_obj.exec_id,
                        label: lbl
                    }
                })
                setEmulationIds(emulationIds)
                setFilteredEmulationsIds(emulationIds)
                setLoading(false)
                if (emulationIds.length > 0) {
                    setSelectedEmulationId(emulationIds[0])
                    fetchEmulation(emulationIds[0])
                    setLoadingSelectedEmulation(true)
                } else {
                    setLoadingSelectedEmulation(false)
                    setSelectedEmulation(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchEmulation = useCallback((emulation_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/` + ip + ':' + port +'/emulations/' + emulation_id.value + "/executions/"+ emulation_id.exec_id
            + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
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
                if(response === null) {
                    return
                }
                setSelectedEmulation(response)
                setLoadingSelectedEmulation(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchEmulationIds();
    }, [fetchEmulationIds]);

    const updateSelectedEmulationId = (selectedId) => {
        setSelectedEmulationId(selectedId)
        fetchEmulation(selectedId)
        setLoadingSelectedEmulation(true)
    }

    const refresh = () => {
        setLoading(true)
        fetchEmulationIds()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const searchFilter = (em_id_obj, searchVal) => {
        return (searchVal === "" || em_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmsIds = emulationIds.filter(em => {
            return searchFilter(em, searchVal)
        });
        setFilteredEmulationsIds(filteredEmsIds)
        setSearchString(searchVal)

        var selectedEmulationRemoved = false
        if (!loadingSelectedEmulation && filteredEmsIds.length > 0) {
            for (let i = 0; i < filteredEmsIds.length; i++) {
                if (selectedEmulation !== null && selectedEmulation !== undefined &&
                    selectedEmulation.id === filteredEmsIds[i].value) {
                    selectedEmulationRemoved = true
                }
            }
            if (!selectedEmulationRemoved) {
                setSelectedEmulationId(filteredEmsIds[0])
                fetchEmulation(filteredEmsIds[0])
                setLoadingSelectedEmulation(true)
            }
        } else {
            setSelectedEmulation(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const EmulationAccordion = (props) => {
        if (props.loadingSelectedEmulation || props.selectedEmulation === null || props.selectedEmulation === undefined) {
            if (props.loadingSelectedEmulation) {
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
                        <SDNController emulation={props.selectedEmulation}
                                       wrapper={wrapper} key={props.selectedEmulation.name}
                        />
                    </Accordion>
                </div>
            )
        }
    }

    const SelectEmulationOrSpinner = (props) => {
        if (!props.loading && props.emulationIds.length === 0) {
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
                                value={props.selectedEmulationId}
                                defaultValue={props.selectedEmulationId}
                                options={props.emulationIds}
                                onChange={updateSelectedEmulationId}
                                placeholder="Select emulation"
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
                        <SelectEmulationOrSpinner loading={loading}
                                                  emulationIds={filteredEmulationsIds}
                                                  selectedEmulationId={selectedEmulationId}
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
            <EmulationAccordion loadingSelectedEmulation={loadingSelectedEmulation}
                                selectedEmulation={selectedEmulation}/>
        </div>
    );
}

SDNControllers.propTypes = {};
SDNControllers.defaultProps = {};
export default SDNControllers;
