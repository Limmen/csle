import React, {useState, useEffect, useCallback, useRef} from 'react';
import './HostTerminal.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import { Terminal } from 'xterm';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
// import { XTerm } from 'xterm-for-react'
import io from 'socket.io-client';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { SearchAddon } from 'xterm-addon-search';
import { WebSocketServer } from "ws";

/**
 * Component representing the /terminal-page
 */
const HostTerminal = (props) => {
    const ip = serverIp
    const port = serverPort
    // const alert = useAlert();
    // const navigate = useNavigate();
    // const ip = "172.31.212.92"
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


    useEffect(() => {
        console.log("component did mount")
        term.open(document.getElementById('sshTerminal'));
        term.attachCustomKeyEventHandler(customKeyEventHandler);
        fitAddon.fit();
        term.resize(15, 50);
        console.log(`size: ${term.cols} columns, ${term.rows} rows`);
        fitAddon.fit();
        term.writeln("Welcome to pyxterm.js!");
        term.writeln("https://github.com/cs01/pyxterm.js");
        term.writeln('')
        term.writeln("You can copy with ctrl+shift+x");
        term.writeln("You can paste with ctrl+shift+v");
        term.writeln('')
        term.onData((data) => {
            console.log("browser terminal received new data:", data);
            socket.emit("pty-input", { input: data });
        });

        // const socket = io.connect("/pty");
        const socket = io.connect(ip + ":" + port + "/pty");
        // const socket = new WebSocket('ws://' + ip + ":" + port + "/pty");
        const status = document.getElementById("status");

        socket.on("pty-output", function (data) {
            console.log("new output received from server:", data.output);
            term.write(data.output);
        });

        socket.on("connect", () => {
            fitToscreen();
            status.innerHTML =
                '<span style="background-color: lightgreen;">connected</span>';
        });

        socket.on("disconnect", () => {
            status.innerHTML =
                '<span style="background-color: #ff8383;">disconnected</span>';
        });

        function fitToscreen() {
            fitAddon.fit();
            const dims = { cols: term.cols, rows: term.rows };
            console.log("sending new dimensions to server's pty", dims);
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

        /**
         * Handle copy and paste events
         */
        function customKeyEventHandler(e) {
            if (e.type !== "keydown") {
                return true;
            }
            if (e.ctrlKey && e.shiftKey) {
                const key = e.key.toLowerCase();
                if (key === "v") {
                    // ctrl+shift+v: paste whatever is in the clipboard
                    navigator.clipboard.readText().then((toPaste) => {
                        term.writeText(toPaste);
                    });
                    return false;
                } else if (key === "c" || key === "x") {
                    // ctrl+shift+x: copy whatever is highlighted to clipboard

                    // 'x' is used as an alternate to 'c' because ctrl+c is taken
                    // by the terminal (SIGINT) and ctrl+shift+c is taken by the browser
                    // (open devtools).
                    // I'm not aware of ctrl+shift+x being used by anything in the terminal
                    // or browser
                    const toCopy = term.getSelection();
                    navigator.clipboard.writeText(toCopy);
                    term.focus();
                    return false;
                }
            }
            return true;
        }
    }, []);

    return (
        <div className="Terminal">
            <h3 className="managementTitle"> Terminal </h3>
            <div className="row">
                <div className="col-sm-1">
                </div>
                <div className="col-sm-10">
                    <span>
                        status: <span id="status">connecting...</span>
                    </span>
                    <div id="sshTerminal" className="sshTerminal">

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
