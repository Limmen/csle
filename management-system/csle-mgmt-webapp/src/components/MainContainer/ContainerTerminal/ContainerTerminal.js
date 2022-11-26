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
import io from 'socket.io-client';
import {FitAddon} from 'xterm-addon-fit';
import {WebLinksAddon} from 'xterm-addon-web-links';
import {SearchAddon} from 'xterm-addon-search';
import {useNavigate} from "react-router-dom";
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
    HTTP_PREFIX, EMULATION_EXECUTIONS_RESOURCE, EMULATION_QUERY_PARAM, HTTP_REST_GET, IDS_QUERY_PARAM, INFO_SUBRESOURCE
} from "../../Common/constants";
import getIps from "../../Common/getIps";

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

    const updateRunningContainer = (runningContainer) => {
        setSelectedRunningContainer(runningContainer)
        // setupConnection()
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
                const runningContainerIds = response.running_containers.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: id_obj.full_name_str
                    }
                })
                setLoadingSelectedEmulationExecutionInfo(false)
                setRunningContainerIds(runningContainerIds)
                setFilteredRunningContainerIds(runningContainerIds)
                if (runningContainerIds.length > 0) {
                    setSelectedRunningContainer(runningContainerIds[0])
                    // setupConnection()
                }
            })
            .catch(error => console.log("error:" + error)),
        [ip, navigate, port, alert, props.sessionData.token, setSessionData]);

    const renderRefreshTerminalTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reset terminal connection.
        </Tooltip>
    );

    const refreshTerminal = () => {
        if (socketState !== null) {
            socketState.disconnect()
        }
        window.location.reload(false);
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
                        The terminal to the container is setup as follows. The browser communicated with the backend
                        over a websocket. The backend opens an SSH tunnel to the container and then pipes the input and
                        outputs from the SSH tunnel to the websocket.
                    </p>
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
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData, fetchSelectedExecution,
        fetchExecutionInfo]);

    const setupConnection = () => {
        console.log("setup connection")
        term.open(document.getElementById('sshTerminal'));
        console.log("OPENED term")
        fitAddon.fit();
        term.resize(15, 40);
        fitAddon.fit();
        term.writeln('')
        term.onData((data) => {
            socket.emit(WS_CONTAINER_TERMINAL_INPUT_MSG,
                {input: data, token: props.sessionData.token});
        });
        const socket = io.connect(`${ip}:${port}/${WS_CONTAINER_TERMINAL_NAMESPACE}?${TOKEN_QUERY_PARAM}` +
            `=${props.sessionData.token}`, {'forceNew': true});
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
            Setup terminal
        </Tooltip>)
    }

    const StartTerminalButton = (props) => (
        <OverlayTrigger
            placement="right"
            delay={{show: 0, hide: 0}}
            overlay={startShellTooltip}
        >
            <Button variant="secondary" className="startButton" size="sm"
                    onClick={() =>  setupConnection()}>
                Connect to {props.ip}
                <i className="fa fa-terminal startStopIcon startStopIcon2" aria-hidden="true"/>
            </Button>
        </OverlayTrigger>
    );

    const TerminalConnect = (props) => {
        if(props.socketState == null){
            return (
                <StartTerminalButton ip={getIps(props.selectedRunningContainer.value.ips_and_networks)[0]}/>
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
                    Terminal to IP: {getIps(props.selectedRunningContainer.value.ips_and_networks)[0]}
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTerminalTooltip}
                    >
                        <Button variant="button" onClick={refreshTerminal}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
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

    const SelectRunningContainerIdDropdownOrSpinner = (props) => {

        if (props.runningContainerIds.length === 0 || props.selectedRunningContainer === null) {
            return (
                <div>
                    <span className="emptyText">No running containers are available</span>
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
        } else {
            return (
                <div>
                    <div className="row">
                        <div className="col-sm-7">
                            <h4 className="text-center inline-block emulationsHeader">
                                <div>
                                    <OverlayTrigger
                                        placement="right"
                                        delay={{show: 0, hide: 0}}
                                        overlay={renderRefreshTooltip}
                                    >
                                        <Button variant="button" onClick={refresh}>
                                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                                        </Button>
                                    </OverlayTrigger>

                                    Selected container:
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
                                   info={selectedEmulationExecutionInfo}
                                   sessionData={props.sessionData}
                                   runningContainerIds={runningContainerIds}
                                   selectedRunningContainer={selectedRunningContainer}
            />
            <div className="row">
                <div className="col-sm-1">
                    <span id="status">connecting...</span>
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
