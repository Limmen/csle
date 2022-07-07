import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Simulations.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import MarkovChain from './Markov.png'
import Simulation from "./Simulation/Simulation";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import {useDebouncedCallback} from 'use-debounce';

const Simulations = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [simulations, setSimulations] = useState([]);
    const [simulationIds, setSimulationIds] = useState([]);
    const [selectedSimulation, setSelectedSimulation] = useState(null);
    const [selectedSimulationId, setSelectedSimulationId] = useState(null);
    const [filteredSimulations, setFilteredSimulations] = useState([]);
    const [filteredSimulationIds, setFilteredSimulationsIds] = useState([]);
    const [searchString, setSearchString] = useState("");
    const [loading, setLoading] = useState(true);
    const [loadingSelectedSimulation, setLoadingSelectedSimulation] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchSimulationsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationsdataids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const simulationIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", name: " + id_obj.simulation
                    }
                })
                setSimulationIds(simulationIds)
                setFilteredSimulationsIds(simulationIds)
                setLoading(false)
                if (simulationIds.length > 0) {
                    setSelectedSimulationId(simulationIds[0])
                    fetchSimulation(simulationIds[0])
                    setLoadingSelectedSimulation(true)
                } else {
                    setLoadingSelectedSimulation(false)
                    setSelectedSimulation(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchSimulation = useCallback((simulation_id) => {
        fetch(
            `http://` + ip + ':7777/simulationsdata/get/' + simulation_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedSimulation(response)
                setLoadingSelectedSimulation(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSimulationsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationsdata/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSimulationsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true);
        fetchSimulationsIds();
    }, [fetchSimulationsIds]);


    const removeSimulationRequest = useCallback((simulation_name) => {
        fetch(
            `http://` + ip + ':7777/simulationsdata/remove/' + simulation_name,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSimulationsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeSimulation = (simulation) => {
        setLoading(true)
        removeSimulationRequest(simulation.name)
        setSelectedSimulation(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulations from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the simulation environments
        </Tooltip>
    );

    const renderRemoveAllSimulationsTooltop = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all simulations.
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        fetchSimulationsIds()
    }

    const removeAllSimulations = () => {
        setLoading(true)
        removeAllSimulationsRequest()
        setSelectedSimulation(null)
    }

    const searchFilter = (simIdObj, searchVal) => {
        return (searchVal === "" || simIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredSimsIds = simulationIds.filter(simulation_id_obj => {
            return searchFilter(simulation_id_obj, searchVal)
        });
        setFilteredSimulationsIds(filteredSimsIds)
        setSearchString(searchVal)

        var selectedSimulationRemoved = false
        if(!loadingSelectedSimulation && filteredSimsIds.length > 0){
            for (let i = 0; i < filteredSimsIds.length; i++) {
                if(selectedSimulation !== null && selectedSimulation !== undefined &&
                    selectedSimulation.id === filteredSimsIds[i].value) {
                    selectedSimulationRemoved = true
                }
            }
            if(!selectedSimulationRemoved) {
                setSelectedSimulationId(filteredSimsIds[0])
                fetchSimulation(filteredSimsIds[0])
                setLoadingSelectedSimulation(true)
            }
        } else {
            setSelectedSimulation(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

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
                        Simulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Simulation of emulated infrastructures</h4>
                    <p className="modalText">
                        A simulation is defined as a Markov decision process or stochastic game, which models
                        how a discrete-time dynamical system is evolved and can be controlled.
                    </p>
                    <div className="text-center">
                        <img src={MarkovChain} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SimulationAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.simulations.map((simulation, index) =>
                        <Simulation simulation={simulation} wrapper={wrapper} key={simulation.name + "-" + index}
                                    removeSimulation={removeSimulation}
                        />
                    )}
                </Accordion>
            )
        }
    }

    const SimulationAccordion = (props) => {
        if (props.loadingSelectedSimulation || props.selectedSimulation === null || props.selectedSimulation === undefined) {
            if (props.loadingSelectedSimulation) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching simulation... </span>
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
                    <Simulation simulation={props.selectedSimulation} wrapper={wrapper}
                                key={props.selectedSimulation.name}
                                removeSimulation={removeSimulation}
                    />
                </Accordion>
            )
        }
    }

    const updateSelectedSimulationId = (selectedId) => {
        setSelectedSimulationId(selectedId)
        fetchSimulation(selectedId)
        setLoadingSelectedSimulation(true)
    }

    const SelectSimulationOrSpinner = (props) => {
        if (!props.loading && props.simulationIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No simulations are available</span>
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
                    <span className="spinnerLabel"> Fetching simulations... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Simulation:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSimulationId}
                                defaultValue={props.selectedSimulationId}
                                options={props.simulationIds}
                                onChange={updateSelectedSimulationId}
                                placeholder="Select simulation"
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
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllSimulationsTooltop}
                    >
                        <Button variant="danger" onClick={removeAllSimulations}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                </div>
            )
        }
    }

    const wrapper = createRef();

    return (
        <div className="Simulations">
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                    <SelectSimulationOrSpinner loading={loading}
                                               simulationIds={filteredSimulationIds}
                                               selectedSimulationId={selectedSimulationId}
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
            <SimulationAccordion loadingSelectedSimulation={loadingSelectedSimulation}
                                 selectedSimulation={selectedSimulation}/>
        </div>
    );
}

Simulations.propTypes = {};
Simulations.defaultProps = {};
export default Simulations;
