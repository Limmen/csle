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
import debounce from 'lodash.debounce';

const Emulations = () => {
    const [emulations, setEmulations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [filteredEmulations, setFilteredEmulations] = useState([]);
    const [showOnlyRunningEmulations, setShowOnlyRunningEmulations] = useState(false);
    const [searchString, setSearchString] = useState("");
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchEmulations = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                console.log(response)
                setEmulations(response);
                setFilteredEmulations(response);
                setLoading(false)
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
                fetchEmulations()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeEmulation = (emulation) => {
        setLoading(true)
        removeEmulationRequest(emulation.name)
    }

    useEffect(() => {
        setLoading(true)
        fetchEmulations();
    }, [fetchEmulations]);

    const refresh = () => {
        setLoading(true)
        fetchEmulations()
    }

    const info = () => {
        setShowInfoModal(true)
    }

    const searchFilter = (emulation, searchVal) => {
        return (searchVal === "" ||
            emulation.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            emulation.name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            emulation.descr.toLowerCase().indexOf(searchVal.toString()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmulations = emulations.filter(emulation => {
            return searchFilter(emulation, searchVal)
        });
        setFilteredEmulations(filteredEmulations)
        setSearchString(searchVal)
    }

    const runningEmulationsChange = (event) => {
        if (!showOnlyRunningEmulations) {
            const filteredEms = filteredEmulations.filter(emulation => {
                return emulation.running
            });
            setFilteredEmulations(filteredEms)
        } else {
            const filteredEms = emulations.filter(emulation => {
                return searchFilter(emulation, searchString)
            });
            setFilteredEmulations(filteredEms)
        }
        setShowOnlyRunningEmulations(!showOnlyRunningEmulations)
    }

    const searchHandler = useCallback(debounce(searchChange, 350), []);

    const EmulationAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.emulations.map((emulation, index) =>
                        <Emulation emulation={emulation} wrapper={wrapper} key={emulation.name + "-" + index}
                                   removeEmulation={removeEmulation}/>
                    )}
                </Accordion>
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

    const wrapper = createRef();

    return (
        <div className="Emulations">
            <div className="row">
                <div className="col-sm-2">
                </div>
                <div className="col-sm-3">
                    <h3 className="text-center inline-block emulationsHeader">
                        Emulations
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
                    </h3>
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
                <div className="col-sm-3">
                    <Form>
                        <Form.Check
                            inline
                            type="switch"
                            id="runningEmulationsSwitch"
                            label="Show only running emulations"
                            className="runningCheck"
                            onChange={runningEmulationsChange}
                        />
                    </Form>
                </div>
            </div>
            <EmulationAccordions loading={loading} emulations={filteredEmulations}/>
        </div>
    );
}

Emulations.propTypes = {};
Emulations.defaultProps = {};
export default Emulations;
