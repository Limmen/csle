import React, {useEffect, useState} from 'react';
import './ContainerTerminal.css';
import {Terminal} from 'xterm';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Button from 'react-bootstrap/Button'
import io from 'socket.io-client';
import {FitAddon} from 'xterm-addon-fit';
import {WebLinksAddon} from 'xterm-addon-web-links';
import {SearchAddon} from 'xterm-addon-search';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import {
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM, WS_CONNECT_ERROR,
    WS_CONNECT_MSG, WS_DISCONNECT_MSG, WS_CONTAINER_TERMINAL_INPUT_MSG,
    WS_CONTAINER_TERMINAL_NAMESPACE, WS_CONTAINER_TERMINAL_OUTPUT_MSG, WS_RESIZE_MSG
} from "../../Common/constants";

/**
 * Component representing the /container-terminal-page
 */
const ContainerTerminal = (props) => {
    const [socketState, setSocketState] = useState(null);
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

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reset terminal connection.
        </Tooltip>
    );

    const refresh = () => {
        if (socketState !== null) {
            socketState.disconnect()
        }
        window.location.reload(false);
    }

    const setupConnection = () => {
        term.open(document.getElementById('sshTerminal'));
        fitAddon.fit();
        term.resize(15, 40);
        fitAddon.fit();
        term.writeln('')
        term.onData((data) => {
            socket.emit(WS_CONTAINER_TERMINAL_INPUT_MSG,
                {input: data, token: props.sessionData.token});
        });
        const socket = io.connect(`${ip}:${port}/${WS_CONTAINER_TERMINAL_NAMESPACE}` +
            +`?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`);
        setSocketState(socket)
        const status = document.getElementById("status");

        socket.on(WS_CONTAINER_TERMINAL_OUTPUT_MSG, function (data) {
            term.write(data.output);
        });

        socket.on(WS_CONNECT_ERROR, () => {
            alert.show("Websocket connection failed. You are not authorized to setup a connection.")
            navigate(`/${LOGIN_PAGE_RESOURCE}`);
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

    useEffect(() => {
        setupConnection()
    }, []);

    return (
        <div className="Terminal">
            <h3 className="managementTitle">
                Container Terminal
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRefreshTooltip}
                >
                    <Button variant="button" onClick={refresh}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            </h3>
            <div className="row">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <span>
                        Container: {serverIp}, Status: <span id="status">connecting...</span>
                    </span>
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
