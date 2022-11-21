import React, {useEffect, useState} from 'react';
import './HostTerminal.css';
import { Terminal } from 'xterm';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Button from 'react-bootstrap/Button'
import io from 'socket.io-client';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { SearchAddon } from 'xterm-addon-search';

/**
 * Component representing the /host-terminal-page
 */
const HostTerminal = (props) => {
    const [socketState, setSocketState] = useState(null);
    const ip = serverIp
    const port = serverPort
    const term = new Terminal({
        cursorBlink: true,
        macOptionIsMeta: true,
        scrollback: true,
        allowProposedApi:true
    });
    const fitAddon = new FitAddon();
    const webLinksAddon = new WebLinksAddon();
    const searchAddon = new SearchAddon();
    term.loadAddon(fitAddon);
    term.loadAddon(webLinksAddon);
    term.loadAddon(searchAddon);

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reset terminal connection.
        </Tooltip>
    );

    const refresh = () => {
        if(socketState !== null) {
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
            socket.emit("pty-input", { input: data });
        });
        const socket = io.connect(ip + ":" + port + "/pty");
        setSocketState(socket)
        const status = document.getElementById("status");

        socket.on("pty-output", function (data) {
            term.write(data.output);
        });

        socket.on("connect", () => {
            fitToscreen();
            status.innerHTML =
                '<span style="background-color: lightgreen;">connected</span>';
            socket.emit("pty-input", { input: "\r" });
        });

        socket.on("disconnect", () => {
            status.innerHTML =
                '<span style="background-color: #ff8383;">disconnected</span>';
        });

        function fitToscreen() {
            fitAddon.fit();
            const dims = { cols: term.cols, rows: term.rows };
            socket.emit("resize", dims);
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
                Host Terminal
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
                        Host: {serverIp}, Status: <span id="status">connecting...</span>
                    </span>
                    <div id="sshTerminal" className="sshTerminal2">

                    </div>
                </div>
                <div className="col-sm-1"></div>
            </div>
        </div>
    );
}

HostTerminal.propTypes = {};
HostTerminal.defaultProps = {};
export default HostTerminal;
