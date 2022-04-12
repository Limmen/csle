import React, {useState, useCallback, useEffect} from 'react';
import './PolicyExamination.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import ReactFlow, {
    ReactFlowProvider
} from 'react-flow-renderer';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import PolicyExaminationSystem from './Architecture.png'
import ApplicationServer from "./AttackerNetwork/ApplicationServer/ApplicationServer";
import ApplicationServerNotFound from "./AttackerNetwork/ApplicationServerNotFound/ApplicationServerNotFound";
import ApplicationServerCompromised from "./AttackerNetwork/ApplicationServerCompromised/ApplicationServerCompromised";
import Gateway from "./AttackerNetwork/Gateway/Gateway";
import Client from "./AttackerNetwork/Client/Client";
import Attacker from "./AttackerNetwork/Attacker/Attacker";
import AttackerNotStarted from "./AttackerNetwork/AttackerNotStarted/AttackerNotStarted";
import Defender from "./AttackerNetwork/Defender/Defender";
import IDS from "./AttackerNetwork/IDS/IDS";
import Firewall from "./AttackerNetwork/Firewall/Firewall";
import Switch from "./AttackerNetwork/Switch/Switch";
import SwitchNotFound from "./AttackerNetwork/SwitchNotFound/SwitchNotFound";
import getElements from './getElements';
import Spinner from 'react-bootstrap/Spinner'
import PolicyAndBeliefChart from "./PolicyAndBeliefChart/PolicyAndBeliefChart";
import DeltaAlertsLineChart from "./DeltaAlertsLineChart/DeltaAlertsLineChart";
import Select from 'react-select'

const onLoad = (reactFlowInstance) => {
    reactFlowInstance.fitView();
}

const PolicyExamination = () => {

    const evolutionSpeedOptions = [
        {
            value: 0,
            label: "No animation"
        },
        {
            value: 1,
            label: "1%"
        },
        {
            value: 25,
            label: "25%"
        },
        {
            value: 50,
            label: "50%"
        },
        {
            value: 75,
            label: "75%"
        },
        {
            value: 100,
            label: "100%"
        }
    ]


    const [showInfoModal, setShowInfoModal] = useState(false);
    const [loading, setLoading] = useState([]);
    const [traces, setTraces] = useState([]);
    const [activeTrace, setActiveTrace] = useState(null);
    const [t, setT] = useState(1);
    const [l, setL] = useState(3);
    const [animationDuration, setAnimationDuration] = useState(evolutionSpeedOptions[0]);
    const [animation, setAnimation] = useState(true);
    const animiationDurationFactor = 50000
    const fullDomain = true
    const fullRange = true
    const ip = "localhost"
    const rawElements = getElements({x: 0, y: 0})
    const [elements, setElements] = useState(rawElements);
    const [isHidden, setIsHidden] = useState(false);
    const [attackerFoundNodes, setAttackerFoundNodes] = useState([]);
    const height = 900
    const nodeTypes = {
        applicationServer: ApplicationServer,
        gateway: Gateway,
        client: Client,
        attacker: Attacker,
        attackerNotStarted: AttackerNotStarted,
        defender: Defender,
        applicationServerNotFound: ApplicationServerNotFound,
        ids: IDS,
        switch: Switch,
        switchNotFound: SwitchNotFound,
        applicationServerCompromised: ApplicationServerCompromised,
        firewall: Firewall
    };
    // const ip = "172.31.212.92"

    // window.addEventListener('keydown', e => {
    //     handleKeyPress(e)
    // });

    const fetchTraces = useCallback(() => {
        fetch(`http://` + ip + ':7777/emulationsimulationtraces', {
            method: "GET", headers: new Headers({
                Accept: "application/vnd.github.cloak-preview"
            })
        })
            .then(res => res.json())
            .then(response => {
                if (response.length > 0) {
                    const tracesOptions = response.map((trace, index) => {
                        return {
                            value: trace,
                            label: "Trace " + index
                        }
                    })
                    setTraces(tracesOptions);
                    setActiveTrace(tracesOptions[0])
                    updateFoundNodes(response[0])
                }
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchTraces()
        setActiveTrace(null)
        setT(0)
        setL(0)
    }, [fetchTraces]);

    const renderInfoTooltip = (props) => (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
        More information about the policy examination.
    </Tooltip>);

    const refresh = () => {
        setLoading(true)
        fetchTraces()
    }

    const animationDurationUpdate = (selectedObj) => {
        setAnimationDuration(selectedObj)
        if (selectedObj.value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const renderRefreshTooltip = (props) => (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
        Reload traces from the backend
    </Tooltip>);

    const handleKeyPress = (event) => {
        if (event.key === 'ArrowLeft') {
            decrementT()
        }
        if (event.key === 'ArrowRight') {
            incrementT()
        }
        if(activeTrace !== null) {
            updateFoundNodes(activeTrace.value)
        }
    }

    const incrementT = () => {
        if (traces.length > 0 && activeTrace !== null) {
            if (activeTrace.value.defender_actions[t + 1] == 0 && l > 0) {
                setL(l - 1)
            }
            if (t >= activeTrace.value.defender_actions.length - 1) {
                setT(activeTrace.value.defender_actions.length - 1)
            } else {
                setT(t + 1)
            }
        }
    }

    const updateTrace = (trace) => {
        if(activeTrace === null || activeTrace === undefined ||
            trace.value.name !== activeTrace.value.name) {
            setActiveTrace(trace)
        }
    }

    const SelectTraceDropdownOrSpinner = (props) => {
        if (props.loading || props.activeTrace === null || props.traces.length === 0) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block selectEmulation">
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.activeTrace}
                            defaultValue={props.activeTrace}
                            options={props.traces}
                            onChange={updateTrace}
                            placeholder="Select a trace"
                        />
                    </div>
                    <div className="conditionalDist inline-block windowLengthDropdown">
                        t={props.t}
                    </div>
                </div>
            )
        }
    }

    // <div className="conditionalDist inline-block windowLengthDropdown" style={{width: "350px"}}>
    //     <Select
    //         style={{display: 'inline-block'}}
    //         value={props.animationDuration}
    //         defaultValue={props.animationDuration}
    //         options={evolutionSpeedOptions}
    //         onChange={animationDurationUpdate}
    //         placeholder="Set the evolution speed"
    //     />
    // </div>
    const updateFoundNodes = (trace) => {
        var attacker_found_nodes = []
        var attacker_compromised_nodes = []
        if (trace !== null) {
            attacker_found_nodes = trace.attacker_found_nodes[t]
            attacker_compromised_nodes = trace.attacker_compromised_nodes[t]
            if (trace.attacker_actions[t] !== trace.attacker_continue_action && trace.attacker_actions[t] !== -1) {
                if (!attacker_found_nodes.includes("attacker")) {
                    attacker_found_nodes.push("attacker")
                }
            }
            if (l < 3) {
                if (!attacker_found_nodes.includes("firewall")) {
                    attacker_found_nodes.push("firewall")
                }
            } else {
                const index = attacker_found_nodes.indexOf("firewall");
                if (index > -1) {
                    attacker_found_nodes.splice(index, 1);
                }
            }
        }
        if (!attacker_found_nodes.includes("client")) {
            attacker_found_nodes.push("client")
        }
        if (!attacker_found_nodes.includes("ids")) {
            attacker_found_nodes.push("ids")
        }
        if (!attacker_found_nodes.includes("gateway")) {
            attacker_found_nodes.push("gateway")
        }
        if (!attacker_found_nodes.includes("defender")) {
            attacker_found_nodes.push("defender")
        }
        setAttackerFoundNodes(attacker_found_nodes)
        setElements((els) => els.map((e, index) => {
            e.isHidden = ((!attacker_found_nodes.includes(e.id)) && !(attacker_found_nodes.includes(e.source) && attacker_found_nodes.includes(e.target)) && !(attacker_found_nodes.includes(e.source) && (e.target.includes("notfound" || e.target.includes("notstarted")))) && !((e.source != undefined && (e.source.includes("notfound") || e.source.includes("notstarted")) && !attacker_found_nodes.includes(e.source)) && (e.target.includes("notfound" || e.target.includes("notstarted")))) && !(e.id.includes("notfound")) && !(e.id.includes("notstarted") && !attacker_found_nodes.includes("attacker")) && !(e.id.includes("compromised") && attacker_compromised_nodes.includes(e.id.replace("_compromised", ""))));
            return e;
        }))
    }

    const decrementT = () => {
        if (activeTrace !== null && activeTrace.value.defender_actions[t] == 0) {
            setL(l + 1)
        }
        if (t > 0) {
            setT(t - 1)
        }
    }

    // useEffect(() => {
    //     setElements((els) => els.map((e, index) => {
    //         e.isHidden = ((!attacker_found_nodes.includes(e.id)) && !(attacker_found_nodes.includes(e.source) && attacker_found_nodes.includes(e.target)) && !(attacker_found_nodes.includes(e.source) && (e.target.includes("notfound" || e.target.includes("notstarted")))) && !((e.source != undefined && (e.source.includes("notfound") || e.source.includes("notstarted")) && !attacker_found_nodes.includes(e.source)) && (e.target.includes("notfound" || e.target.includes("notstarted")))) && !(e.id.includes("notfound")) && !(e.id.includes("notstarted") && !attacker_found_nodes.includes("attacker")) && !(e.id.includes("compromised") && attacker_compromised_nodes.includes(e.id.replace("_compromised", ""))));
    //         return e;
    //     }));
    // }, [attacker_found_nodes]);


    const InfoModal = (props) => {
        return (<Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Interactive examination of learned security policies
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h4>Examination of learned security policies</h4>
                <p className="modalText">
                    The policy examination page allows a user to traverse episodes of
                    Markov decision processes in a controlled manner and to track
                    the actions triggered by security policies. Similar to a software
                    debugger, a user can continue or or halt an episode at any
                    time step and inspect parameters and probability distributions
                    of interest. The system enables insight into the structure of a
                    given policy and in the behavior of a policy in edge cases.
                </p>
                <div className="text-center">
                    <img src={PolicyExaminationSystem} alt="A system for interactive examination of
                        learned security policies"/>
                </div>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>);
    }

    return (
        <div className="policyExamination" onKeyDown={handleKeyPress} tabIndex={0}>
            <h4> Policy Examination
                <span className="infoPolicyExp">
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip()}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton3" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                        className="overLayInfo"
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="infoButton2 fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                </span>
                <SelectTraceDropdownOrSpinner activeTrace={activeTrace} animationDuration={animationDuration}
                                              traces={traces} loading={loading} t={t}/>
            </h4>
            <div className="Demo">
                <div className="row contentRow policyRow">
                    <div className="col-sm-6">
                        <h4 className="cardTitle">
                            The Defender's View
                        </h4>
                        <PolicyAndBeliefChart activeTrace={activeTrace} t={t}
                                              fullDomain={fullDomain} fullRange={fullRange}
                                              animation={animation} animationDuration={animationDuration}
                                              animationDurationFactor={animiationDurationFactor}/>
                        <DeltaAlertsLineChart activeTrace={activeTrace} t={t} fullDomain={fullDomain}
                                              fullRange={fullRange}
                                              animation={animation} animationDuration={animationDuration}
                                              animationDurationFactor={animiationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <h4 className="cardTitle">
                            The Attacker's View
                        </h4>
                        <div className="DefenderObservations row justify-content-center card">
                            <div className="card-header cardHeader"><h4>
                                Intrusion state
                            </h4></div>
                            <div className="card-body">
                                <div className="row">
                                    <div className="Network col-sm-12">
                                        {/*<h4 className="attackerNetworkTitle"> IT Infrastructure Status </h4>*/}
                                        <div className="layoutflow">
                                            <ReactFlowProvider>
                                                <ReactFlow
                                                    style={{height: height}}
                                                    elements={elements}
                                                    onLoad={onLoad}
                                                    nodesDraggable={false}
                                                    nodesConnectable={false}
                                                    paneMoveable={false}
                                                    defaultZoom={1}
                                                    minZoom={1}
                                                    maxZoom={1}
                                                    nodeTypes={nodeTypes}
                                                />
                                            </ReactFlowProvider>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>);
}

PolicyExamination.propTypes = {};
PolicyExamination.defaultProps = {};
export default PolicyExamination;
