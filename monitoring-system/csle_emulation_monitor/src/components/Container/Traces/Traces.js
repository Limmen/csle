import React, {useState, useEffect, useCallback, createRef} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion';
import EmulationTrace from "./EmulationTrace/EmulationTrace";
import './Traces.css';

const Traces = () => {
    const [emulationTraces, setEmulationTraces] = useState([]);
    const [simulationTraces, setSimulationTraces] = useState([]);
    const [loadingEmulationTraces, setLoadingEmulationTraces] = useState(true);
    const [loadingSimulationTraces, setLoadingSimulationTraces] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const wrapper = createRef();

    const fetchEmulationTraces = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationtraces',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setEmulationTraces(response)
                setLoadingEmulationTraces(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSimulationTraces = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationtraces',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSimulationTraces(response)
                setLoadingSimulationTraces(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoadingEmulationTraces(true)
        setLoadingSimulationTraces(true)
        fetchEmulationTraces()
        fetchSimulationTraces()
    }, []);

    const refreshEmulationTraces = () => {
        setLoadingEmulationTraces(true)
        fetchEmulationTraces()
    }

    const refreshSimulationTraces = () => {
        setLoadingSimulationTraces(true)
        fetchSimulationTraces()
    }

    const renderRefreshEmulationTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulation traces from the backend
        </Tooltip>
    );

    const EmulationTracesAccordions = (props) => {
        if (props.loadingEmulationTraces) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.emulationTraces.map((emulationTrace, index) =>
                        <EmulationTrace emulationTrace={emulationTrace}
                                        wrapper={wrapper} key={emulationTrace.id + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }

    return (
        <div className="Traces">
            <h3 className="text-center inline-block emulationsHeader"> Emulation Traces

                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderRefreshEmulationTracesTooltip}
                >
                    <Button variant="button" onClick={refreshEmulationTraces}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

            </h3>
            <EmulationTracesAccordions loadingEmulationTraces={loadingEmulationTraces} emulationTraces={emulationTraces}/>
        </div>
    );
}

Traces.propTypes = {};
Traces.defaultProps = {};
export default Traces;
