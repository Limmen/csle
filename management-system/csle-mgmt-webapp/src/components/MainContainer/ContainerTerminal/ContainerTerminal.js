import React, {useEffect, useState, useCallback} from 'react';
import './ContainerTerminal.css';
import {Terminal} from 'xterm';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Select from 'react-select'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import {useDebouncedCallback} from 'use-debounce';
import ContainerTerminalImg from './ContainerTerminal.png'
import io from 'socket.io-client';
import {FitAddon} from 'xterm-addon-fit';
import {WebLinksAddon} from 'xterm-addon-web-links';
import {SearchAddon} from 'xterm-addon-search';
import {useNavigate} from "react-router-dom";
import {useLocation} from "react-router-dom";
import {useAlert} from "react-alert";
import {
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    WS_CONNECT_ERROR,
    WS_CONNECT_MSG,
    WS_DISCONNECT_MSG,
    WS_CONTAINER_TERMINAL_INPUT_MSG,
    WS_CONTAINER_TERMINAL_NAMESPACE,
    WS_CONTAINER_TERMINAL_OUTPUT_MSG,
    WS_RESIZE_MSG,
    HTTP_PREFIX,
    EMULATION_EXECUTIONS_RESOURCE,
    EMULATION_QUERY_PARAM,
    HTTP_REST_GET,
    IDS_QUERY_PARAM,
    INFO_SUBRESOURCE,
    IP_QUERY_PARAM
} from "../../Common/constants";

/**
 * Component representing the /container-terminal-page
 */
const ContainerTerminal = (props) => {
    const [socketState, setSocketState] = useState(null);
    const [emulationExecutionIds, setEmulationExecutionIds] = useState([]);
    const [filteredEmulationExecutionIds, setFilteredEmulationExecutionIds] = useState([]);
    const [selectedEmulationExecutionId, setSelectedEmulationExecutionId] = useState(null);
    const [selectedEmulationExecution, setSelectedEmulationExecution] = useState(null);
    const [selectedEmulationExecutionInfo, setSelectedEmulationExecutionInfo] = useState(null);
    const [runningContainerIds, setRunningContainerIds] = useState([]);
    const [filteredRunningContainerIds, setFilteredRunningContainerIds] = useState([]);
    const [selectedRunningContainer, setSelectedRunningContainer] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationExecution, setLoadingSelectedEmulationExecution] = useState(true);
    const [loadingSelectedEmulationExecutionInfo, setLoadingSelectedEmulationExecutionInfo] = useState(true);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const ip = serverIp
    const port = serverPort
    const term = new Terminal({
        cursorBlink: true,
        macOptionIsMeta: true,
        scrollback: true,
        allowProposedApi: true
    });
    const fitAddon = new FitAddon();
    const webLinksAddon = new WebLinksAddon();
    const searchAddon = new SearchAddon();
    term.loadAddon(fitAddon);
    term.loadAddon(webLinksAddon);
    term.loadAddon(searchAddon);
    const navigate = useNavigate();
    const alert = useAlert();
    const setSessionData = props.setSessionData
    const location = useLocation()

    const fetchSelectedExecution = useCallback((id_obj) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}/${id_obj.value.id}?`
                + `${EMULATION_QUERY_PARAM}=${id_obj.value.emulation}&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, props.sessionData.token, setSessionData]);

    const renderRefreshExecutionsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload data about emulation executions from the backend
        </Tooltip>
    );

    const renderRefreshContainersTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload data about running containers from the backend.
        </Tooltip>
    );

    const updateEmulationExecutionId = (emulationExecutionId) => {
        setSelectedEmulationExecutionId(emulationExecutionId)
        fetchSelectedExecution(emulationExecutionId)
        fetchExecutionInfo(emulationExecutionId)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
    }

    const updateRunningContainer = (runningContainer) => {
        setSelectedRunningContainer(runningContainer)
        destroyTerminal()
    }

    const destroyTerminal = () => {
        if (socketState !== null) {
            socketState.disconnect()
            setSocketState(null)
        }
        term.dispose()
        document.getElementById('sshTerminal').innerHTML = "";
        document.getElementById("status").innerHTML="";
    }

    const refreshExecutions = () => {
        destroyTerminal()
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
        setSelectedEmulationExecution(null)
        setSelectedEmulationExecutionInfo(null)
        fetchEmulationExecutionIds()
    }

    const refreshContainers = () => {
        destroyTerminal()
        setLoadingSelectedEmulationExecutionInfo(true)
        setSelectedEmulationExecutionInfo(null)
        fetchExecutionInfo(selectedEmulationExecutionId)
    }

    const searchFilter = (executionIdObj, searchVal) => {
        return (searchVal === "" || executionIdObj.label.toString().toLowerCase().indexOf(
            searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEIds = emulationExecutionIds.filter(executionIdObj => {
            return searchFilter(executionIdObj, searchVal)
        });
        const filteredCIds = runningContainerIds.filter(containerIdObj => {
            return searchFilter(containerIdObj, searchVal)
        });
        setFilteredEmulationExecutionIds(filteredEIds)
        setFilteredRunningContainerIds(filteredCIds)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const fetchExecutionInfo = useCallback((id_obj) => fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}/${id_obj.value.id}/${INFO_SUBRESOURCE}?`
                + `${EMULATION_QUERY_PARAM}=${id_obj.value.emulation}&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setSelectedEmulationExecutionInfo(response)
                const rContainerIds = response.running_containers.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: id_obj.full_name_str
                    }
                })
                setLoadingSelectedEmulationExecutionInfo(false)
                setRunningContainerIds(rContainerIds)
                setFilteredRunningContainerIds(rContainerIds)
                if (rContainerIds.length > 0) {
                    var match = false
                    if(location.state !== null && location.state.ip !== null && location.state.ip !== undefined) {
                        for (let i = 0; i < rContainerIds.length; i++) {
                            if(rContainerIds[i].value.docker_gw_bridge_ip === location.state.ip) {
                                match = true
                                setSelectedRunningContainer(rContainerIds[i])
                            }
                        }
                        location.state.ip = null
                    }
                    if(!match) {
                        setSelectedRunningContainer(rContainerIds[0])
                    }
                }
            })
            .catch(error => console.log("error:" + error)),
        [ip, navigate, port, alert, props.sessionData.token, setSessionData, location.state]);

    const renderRefreshTerminalTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reset terminal connection.
        </Tooltip>
    );

    const refreshTerminal = () => {
        destroyTerminal()
    }

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
                        Container Terminal
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        The terminal allows executing arbitrary commands inside the given container.
                        It can for example be used to restart services or to setup new user accounts.

                        The browser communicates with the backend over a websocket, which in turn communicates with the
                        container over an SSH tunnel, whose' output is piped through the websocket.
                    </p>
                    <div className="text-center">
                        <img src={ContainerTerminalImg} alt="Container Terminal Setup"
                             className="img-fluid containerTermImg"/>
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
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_EXECUTIONS_RESOURCE}?${IDS_QUERY_PARAM}=true`
            + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
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
                        label: `ID:${id_obj.id}, emulation: ${id_obj.emulation}`
                    }
                })
                setEmulationExecutionIds(emulationExecutionIds)
                setFilteredEmulationExecutionIds(emulationExecutionIds)
                setLoading(false)
                if (emulationExecutionIds.length > 0) {
                    var match = false
                    var selectedExId = emulationExecutionIds[0]
                    if(location.state !== null && location.state.executionId !== null && location.state.emulation !== null) {
                        for (let i = 0; i < emulationExecutionIds.length; i++) {
                            if(emulationExecutionIds[i].value.id === location.state.executionId &&
                                emulationExecutionIds[i].value.emulation === location.state.emulation) {
                                match = true
                                setSelectedEmulationExecutionId(emulationExecutionIds[i])
                                selectedExId = emulationExecutionIds[i]
                            }
                        }
                        location.state.executionId = null
                        location.state.emulation = null
                    }
                    if(!match) {
                        setSelectedEmulationExecutionId(emulationExecutionIds[0])
                    }
                    fetchSelectedExecution(selectedExId)
                    fetchExecutionInfo(selectedExId)
                    setLoadingSelectedEmulationExecution(true)
                    setLoadingSelectedEmulationExecutionInfo(true)
                } else {
                    setLoadingSelectedEmulationExecution(false)
                    setLoadingSelectedEmulationExecutionInfo(false)
                    setSelectedEmulationExecution(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchSelectedExecution,
        fetchExecutionInfo, location.state]);

    const setupConnection = (containerIp, physical_host) => {
        term.open(document.getElementById('sshTerminal'));
        fitAddon.fit();
        term.resize(15, 60);
        fitAddon.fit();
        term.writeln('')
        term.onData((data) => {
            socket.emit(WS_CONTAINER_TERMINAL_INPUT_MSG,
                {input: data, token: props.sessionData.token});
        });
        const socket = io.connect(`${physical_host}:${port}/${WS_CONTAINER_TERMINAL_NAMESPACE}?${TOKEN_QUERY_PARAM}` +
            `=${props.sessionData.token}&${IP_QUERY_PARAM}=${containerIp.replaceAll('.', '-')}`, {'forceNew': true});
        setSocketState(socket)
        const status = document.getElementById("status");

        socket.on(WS_CONTAINER_TERMINAL_OUTPUT_MSG, function (data) {
            term.write(data.output);
        });

        socket.on(WS_CONNECT_ERROR, () => {
            alert.show("Websocket connection failed. You are not authorized to setup a connection.")
            navigate(`/${LOGIN_PAGE_RESOURCE}`);
            socket.disconnect()
        });

        socket.on(WS_CONNECT_MSG, () => {
            fitToscreen();
            status.innerHTML =
                '<span style="background-color: lightgreen;">connected</span>';
            socket.emit(WS_CONTAINER_TERMINAL_INPUT_MSG, {input: "\r", token: props.sessionData.token});
        });

        socket.on(WS_DISCONNECT_MSG, () => {
            status.innerHTML =
                '<span style="background-color: #ff8383;">disconnected</span>';
        });

        function fitToscreen() {
            fitAddon.fit();
            const dims = {cols: term.cols, rows: term.rows, token: props.sessionData.token};
            socket.emit(WS_RESIZE_MSG, dims);
        }

        function debounce(func, wait_ms) {
            let timeout;
            return function (...args) {
                const context = this;
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(context, args), wait_ms);
            };
        }

        window.onresize = debounce(fitToscreen, 50);
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the terminal.
        </Tooltip>
    );

    const startShellTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Connect and setup terminal
        </Tooltip>)
    }

    const StartTerminalButton = (props) => (
        <OverlayTrigger
            placement="right"
            delay={{show: 0, hide: 0}}
            overlay={startShellTooltip}
        >
            <Button variant="secondary" className="connectButton" size="sm"
                    onClick={() =>  setupConnection(props.ip, props.host)}>
                Connect to {props.ip} on host: {props.host}
                <i className="fa fa-terminal connectButtonText" aria-hidden="true"/>
            </Button>
        </OverlayTrigger>
    );

    const TerminalConnect = (props) => {
        if(props.socketState == null){
            return (
                <StartTerminalButton ip={props.selectedRunningContainer.value.docker_gw_bridge_ip}
                                     host={props.selectedRunningContainer.value.physical_host_ip}
                />
            )
        } else {
            return(
                <p>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}>
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    Terminal to IP: {props.selectedRunningContainer.value.docker_gw_bridge_ip} on host:
                    {props.selectedRunningContainer.value.physical_host_ip}
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTerminalTooltip}
                    >
                        <Button variant="button" onClick={refreshTerminal}>
                            <i className="fa fa-times refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </p>
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
                        overlay={renderRefreshExecutionsTooltip}
                    >
                        <Button variant="button" onClick={refreshExecutions}>
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
                        overlay={renderRefreshExecutionsTooltip}
                    >
                        <Button variant="button" onClick={refreshExecutions}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    Execution:
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

    const SelectRunningContainerIdDropdownOrSpinner = (props) => {

        if (props.runningContainerIds.length === 0 || props.selectedRunningContainer === null) {
            return (
                <div>
                    <span className="emptyText">No running containers are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshContainersTooltip}
                    >
                        <Button variant="button" onClick={refreshContainers}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        } else {
            return (
                <div>
                    <div className="row">
                            <h4 className="text-center inline-block emulationsHeader">
                                <div>
                                    <OverlayTrigger
                                        placement="right"
                                        delay={{show: 0, hide: 0}}
                                        overlay={renderRefreshContainersTooltip}
                                    >
                                        <Button variant="button" onClick={refreshContainers}>
                                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                                        </Button>
                                    </OverlayTrigger>

                                    Container:
                                    <div className="conditionalDist inline-block selectEmulation">
                                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                            <Select
                                                style={{display: 'inline-block'}}
                                                value={props.selectedRunningContainer}
                                                defaultValue={props.selectedRunningContainer}
                                                options={props.runningContainerIds}
                                                onChange={updateRunningContainer}
                                                placeholder="Select a running container"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </h4>
                    </div>
                    <TerminalConnect selectedRunningContainer={props.selectedRunningContainer}
                                     socketState={socketState}/>
                </div>
            )
        }
    }

    const SelectedExecutionView = (props) => {
        if (props.loading || props.loadingSelectedEmulationExecution || props.loadingSelectedEmulationExecutionInfo
            || props.selectedEmulationExecution === null || props.selectedEmulationExecution === undefined ||
            props.info === undefined ||
            props.info === null) {
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
                    <SelectRunningContainerIdDropdownOrSpinner
                        runningContainerIds={props.runningContainerIds}
                        selectedRunningContainer={props.selectedRunningContainer}
                    />
                </div>
            )
        }
    }

    useEffect(() => {
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setLoadingSelectedEmulationExecutionInfo(true)
        fetchEmulationExecutionIds()
    }, [fetchEmulationExecutionIds]);


    return (
        <div className="Terminal">
            <h3 className="managementTitle">
                Container Terminals
            </h3>
            <div className="row">
                <div className="col-sm-4">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationExecutionIdDropdownOrSpinner
                            loading={loading} emulationExecutionIds={filteredEmulationExecutionIds}
                            selectedEmulationExecutionId={selectedEmulationExecutionId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <h4 className="text-center inline-block emulationsHeader">
                    <SelectedExecutionView loadingSelectedEmulationExecution={loadingSelectedEmulationExecution}
                                           loadingSelectedEmulationExecutionInfo={loadingSelectedEmulationExecutionInfo}
                                           selectedEmulationExecution={selectedEmulationExecution}
                                           info={selectedEmulationExecutionInfo}
                                           sessionData={props.sessionData}
                                           runningContainerIds={filteredRunningContainerIds}
                                           selectedRunningContainer={selectedRunningContainer}
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
            <div className="row">
                <div className="col-sm-1">
                    <span id="status"></span>
                </div>
                <div className="col-sm-10">
                    <div id="sshTerminal" className="sshTerminal2">

                    </div>
                </div>
                <div className="col-sm-1"></div>
            </div>
        </div>
    );
}

ContainerTerminal.propTypes = {};
ContainerTerminal.defaultProps = {};
export default ContainerTerminal;
