import React, {useState, useEffect, createRef, useCallback} from 'react';
import './Emulations.css';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import Emulation from "./Emulation/Emulation";
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import ConfigSpace from './ConfigSpace.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import { useDebouncedCallback } from 'use-debounce';

const Emulations = () => {
    const [emulationIds, setEmulationIds] = useState([]);
    const [selectedEmulationId, setSelectedEmulationId] = useState(null);
    const [selectedEmulation, setSelectedEmulation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulation, setLoadingSelectedEmulation] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredEmulationsIds, setFilteredEmulationsIds] = useState([]);
    const [showOnlyRunningEmulations, setShowOnlyRunningEmulations] = useState(false);
    const [searchString, setSearchString] = useState("");
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchEmulationIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationsdataids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const emulationIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", name: " + id_obj.simulation
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

    const removeEmulationRequest = useCallback((emulation_name) => {
        fetch(
            `http://` + ip + ':7777/emulationsdata/remove/' + emulation_name,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchEmulationIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchEmulation = useCallback((emulation_id) => {
        fetch(
            `http://` + ip + ':7777/emulationsdata/get/' + emulation_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedEmulation(response)
                setLoadingSelectedEmulation(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllEmulationsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationsdata/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchEmulationIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeEmulation = (emulation) => {
        setLoading(true)
        removeEmulationRequest(emulation.name)
        setSelectedEmulation(null)
    }

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

    const removeAllEmulations = () => {
        setLoading(true)
        removeAllEmulationsRequest()
        setSelectedEmulation(null)
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
        if(!loadingSelectedEmulation && filteredEmsIds.length > 0){
            for (let i = 0; i < filteredEmsIds.length; i++) {
                if(selectedEmulation !== null && selectedEmulation !== undefined &&
                    selectedEmulation.id === filteredEmsIds[i].value) {
                    selectedEmulationRemoved = true
                }
            }
            if(!selectedEmulationRemoved) {
                setSelectedEmulationId(filteredEmsIds[0])
                fetchEmulation(filteredEmsIds[0])
                setLoadingSelectedEmulation(true)
            }
        } else {
            setSelectedEmulation(null)
        }
    }

    const runningEmulationsChange = (event) => {
        if (!showOnlyRunningEmulations) {
            const filteredEms = filteredEmulationsIds.filter(emulation => {
                return emulation.running
            });
            setFilteredEmulationsIds(filteredEms)
        } else {
            const filteredEms = emulationIds.filter(emulation => {
                return searchFilter(emulation, searchString)
            });
            setFilteredEmulationsIds(filteredEms)
        }
        setShowOnlyRunningEmulations(!showOnlyRunningEmulations)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const EmulationAccordion = (props) => {
        if (props.loadingSelectedEmulation || props.selectedEmulation === null || props.selectedEmulation === undefined) {
            if(props.loadingSelectedEmulation) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching emulation... </span>
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
                <Accordion defaultActiveKey="0">
                    <Emulation emulation={props.selectedEmulation}
                               wrapper={wrapper} key={props.selectedEmulation.name}
                               removeEmulation={removeEmulation}/>
                </Accordion>
            )
        }
    }

    const SelectEmulationOrSpinner = (props) => {
        if (!props.loading && props.emulationIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No emulations are available</span>
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
                    <span className="spinnerLabel"> Fetching emulations... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Emulation:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
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

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveEmulationsTooltip}
                    >
                        <Button variant="danger" onClick={removeAllEmulations}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
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
                    <Modal.Title id="contained-modal-title-vcenter">
                        Emulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Emulation of Computer Infrastructures</h4>
                    <p className="modalText">
                        An emulated infrastructure consists of a a cluster of machines that
                        runs a virtualization layer provided by Docker containers
                        and virtual links. It implements network isolation and traffic
                        shaping on the containers using network namespaces and the
                        NetEm module in the Linux kernel. Resource constraints
                        of the containers, e.g. CPU and memory constraints, are
                        enforced using cgroups. The configuration of an emulated infrastructure includes
                        the topology, resource constraints, vulnerabilities, services, users, etc.
                    </p>
                    <div className="text-center">
                        <img src={ConfigSpace} alt="Emulated infrastructures"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulations from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the emulation environments
        </Tooltip>
    );

    const renderRemoveEmulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all emulations
        </Tooltip>
    );

    const wrapper = createRef();

    return (
        <div className="Emulations">
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationOrSpinner loading={loading}
                                                   emulationIds={filteredEmulationsIds}
                                                   selectedEmulationId={selectedEmulationId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
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
                <div className="col-sm-2">
                </div>
            </div>
            <EmulationAccordion loadingSelectedEmulation={loadingSelectedEmulation}
                                selectedEmulation={selectedEmulation}/>
        </div>
    );
}

Emulations.propTypes = {};
Emulations.defaultProps = {};
export default Emulations;
