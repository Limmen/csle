import React, {useEffect, useState} from 'react';
import './Demo.css';
import Footer from "./../Container/Footer/Footer";
import './../Container/DefenderView/DefenderPolicy/DefenderPolicy.css';
import ReactFlow, {
    ReactFlowProvider
} from 'react-flow-renderer';
import {
    Area,
    AreaChart,
    CartesianGrid,
    Label,
    Legend, Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";
import Slider from "rc-slider";
import ApplicationServer from "../Container/AttackerView/AttackerNetwork/ApplicationServer/ApplicationServer";
import ApplicationServerNotFound
    from "../Container/AttackerView/AttackerNetwork/ApplicationServerNotFound/ApplicationServerNotFound";
import ApplicationServerCompromised
    from "../Container/AttackerView/AttackerNetwork/ApplicationServerCompromised/ApplicationServerCompromised";
import Gateway from "../Container/AttackerView/AttackerNetwork/Gateway/Gateway";
import Client from "../Container/AttackerView/AttackerNetwork/Client/Client";
import Attacker from "../Container/AttackerView/AttackerNetwork/Attacker/Attacker";
import AttackerNotStarted from "../Container/AttackerView/AttackerNetwork/AttackerNotStarted/AttackerNotStarted";
import Defender from "../Container/AttackerView/AttackerNetwork/Defender/Defender";
import IDS from "../Container/AttackerView/AttackerNetwork/IDS/IDS";
import Firewall from "../Container/AttackerView/AttackerNetwork/Firewall/Firewall";
import Switch from "../Container/AttackerView/AttackerNetwork/Switch/Switch";
import SwitchNotFound from "../Container/AttackerView/AttackerNetwork/SwitchNotFound/SwitchNotFound";
import getElements from './getElements';
import {Dropdown} from "react-bootstrap";
import TraceDropdownElement from "../Container/Header/TraceDropdownElement/TraceDropdownElement";


const onLoad = (reactFlowInstance) => {
    reactFlowInstance.fitView();
}

const Demo = (props) => {

    const NextStop = (props) => {
        if (props.traces.length > 0) {
            var nextStop = null
            for (let i = 0; i < props.traces[props.activeTrace].stop_actions.length; i++) {
                if (props.traces[props.activeTrace].stop_actions[i].l === props.l) {
                    return props.traces[props.activeTrace].stop_actions[i].command
                }
            }
            return "-"
        } else {
            return "-"
        }
    }

    const numCompromised = (props) => {
        if (props.traces.length > 0) {
            return props.traces[props.activeTrace].attacker_number_of_compromised_nodes[props.t]
        } else {
            return 0
        }
    }

    const DefensiveMeasures = (props) => {
        if (props.traces.length > 0) {
            var commands = []
            for (let i = 0; i < props.traces[props.activeTrace].stop_actions.length; i++) {
                if (props.traces[props.activeTrace].stop_actions[i].l > props.l) {
                    commands.push(props.traces[props.activeTrace].stop_actions[i].command)
                }
            }
            return (
                <ul className="list-group list-group-flush">
                    {
                        commands.map((cmd, index) => {
                            return <li key={index} className="list-group-item"><code>{cmd}</code></li>
                        })
                    }
                </ul>
            )
        } else {
            return (<ul className="list-group list-group-flush"></ul>)
        }
    }

    const AttackerActions = (props) => {
        if (props.traces.length > 0) {
            var attackerActions = []
            for (let i = 0; i < props.traces[props.activeTrace].attacker_actions.length; i++) {
                if (i <= Math.max((props.t),0) && i >= Math.max((props.t-3),0)) {
                    var a = 372
                    if (props.traces[props.activeTrace].attacker_actions[i] !== -1) {
                        a = props.traces[props.activeTrace].attacker_actions[i]
                    }
                    if (a !== 372) {
                        attackerActions.push(props.traces[props.activeTrace].attacker_action_descriptions[a].command)
                    }
                }
            }
            return (
                <ul className="list-group list-group-flush">
                    {
                        attackerActions.map((action, index) => {
                            return <li key={index} className="list-group-item"><code>{action}</code></li>
                        })
                    }
                </ul>
            )
        } else {
            return (<ul className="list-group list-group-flush"></ul>)
        }
    }


    const [animationDuration, setAnimationDuration] = useState(0);
    const [animation, setAnimation] = useState(false);
    const animiationDurationFactor = 50000

    const onSliderChange = (value) => {
        setAnimationDuration(value)
        if (value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const PolicyAreaChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].defender_stop_probabilities
                .filter((prob, index) => index <= props.t).map((prob, index) => {
                    return {
                        t: index + 1,
                        StoppingProbability: prob
                    }
                })
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <AreaChart
                        width={width}
                        height={height}
                        data={data}
                        syncId="anyId"
                        margin={margin}
                    >
                        <defs>
                            <linearGradient id="colorProb" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={[1, data.length]}>
                            <Label value="Time-step t" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Probability" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Area type="monotone" dataKey="StoppingProbability" stroke="#8884d8" fill="#82ca9d"
                              isAnimationActive={animation} fillOpacity={1} fill="url(#colorProb)"
                              animationEasing={'linear'}
                              animationDuration={(1 - (animationDuration / 100) * animiationDurationFactor)}/>
                    </AreaChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <AreaChart
                        width={width}
                        height={height}
                        data={[]}
                        syncId="anyId"
                        margin={margin}
                    >
                        <defs>
                            <linearGradient id="colorProb" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="Time-step t" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number" domain={[0, 1]}>
                            <Label angle={270} value="Probability" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Area type="monotone" dataKey="StoppingProbability" stroke="#8884d8" fill="#82ca9d"
                              isAnimationActive={animation} fillOpacity={1} fill="url(#colorProb)"
                              animationEasing={'linear'}
                              animationDuration={(1000 - (animationDuration / 100) * 10000)}/>
                    </AreaChart>
                </ResponsiveContainer>
            )
        }
    }


    const DeltaAlertsLineChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const filteredData = props.traces[props.activeTrace].defender_observations
                .filter((prob, index) => index <= props.t)
            var data = []
            for (let i = 0; i < filteredData.length; i++) {
                var deltaX = filteredData[i][0]
                var deltaY = filteredData[i][1]
                var deltaZ = filteredData[i][2]
                if (i > 0) {
                    deltaX = filteredData[i][0] - filteredData[i - 1][0]
                    deltaY = filteredData[i][1] - filteredData[i - 1][1]
                    deltaZ = filteredData[i][2] - filteredData[i - 1][2]
                }
                data.push(
                    {
                        t: i + 1,
                        "Severe Alerts Δx": deltaX,
                        "Warning Alerts Δy": deltaY,
                        "Login Attempts Δz": deltaZ
                    }
                )
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={[1, data.length]}>
                            <Label value="Time-step t" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="Severe Alerts Δx"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts Δz"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={[]}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="Time-step t" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="Severe Alerts Δx"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={(1000 - (animationDuration / 100) * 10000)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts Δz"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )
        }
    }


    var attacker_found_nodes = []
    var attacker_compromised_nodes = []
    if (props.traces.length > 0) {
        attacker_found_nodes = props.traces[props.activeTrace].attacker_found_nodes[props.t]
        attacker_compromised_nodes = props.traces[props.activeTrace].attacker_compromised_nodes[props.t]
        // for (let i = 0; i < props.traces[props.activeTrace].attacker_found_nodes[props.t].length; i++) {
        //     attacker_found_nodes.push(props.traces[props.activeTrace].attacker_found_nodes[props.t][i])
        // }
        // for (let i = 0; i < props.traces[props.activeTrace].attacker_compromised_nodes[props.t].length; i++) {
        //     attacker_compromised_nodes.push(props.traces[props.activeTrace].attacker_compromised_nodes[props.t][i])
        // }
        if (props.traces[props.activeTrace].attacker_actions[props.t] !== props.traces[props.activeTrace].attacker_continue_action
            && props.traces[props.activeTrace].attacker_actions[props.t] !== -1) {
            if (!attacker_found_nodes.includes("attacker")) {
                attacker_found_nodes.push("attacker")
            }
        }
        if (props.l < 3) {
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

    const rawElements = getElements({x: 0, y: 0})
    const [elements, setElements] = useState(rawElements);
    const [isHidden, setIsHidden] = useState(false);
    const [attackerFoundNodes, setAttackerFoundNodes] = useState(attacker_found_nodes);
    const height = 850
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

    useEffect(() => {
        setElements((els) =>
            els.map((e, index) => {
                e.isHidden = ((!attacker_found_nodes.includes(e.id))
                    && !(attacker_found_nodes.includes(e.source) && attacker_found_nodes.includes(e.target))
                    && !(attacker_found_nodes.includes(e.source) && (e.target.includes("notfound" || e.target.includes("notstarted"))))
                    && !((e.source != undefined && (e.source.includes("notfound") || e.source.includes("notstarted")) && !attacker_found_nodes.includes(e.source))
                        && (e.target.includes("notfound" || e.target.includes("notstarted"))))
                    && !(e.id.includes("notfound"))
                    && !(e.id.includes("notstarted") && !attacker_found_nodes.includes("attacker"))
                    && !(e.id.includes("compromised") && attacker_compromised_nodes.includes(e.id.replace("_compromised", "")))
                );
                return e;
            })
        );
    }, [props, attacker_found_nodes]);

    return (
        <div className="Demo">
            <div className="demoHeader">
                <Dropdown className="traceDropdownDemo">
                    <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="sm">
                        <h1 className="traceDropdownDemoLabel"> Trace: {props.activeTrace} </h1>
                    </Dropdown.Toggle>

                    <Dropdown.Menu variant="dark">
                        {props.traces.map((trace, index) =>
                            <TraceDropdownElement trace={trace} index={index} key={index}
                                                  setActiveTrace={props.setActiveTrace}/>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
                <h1 className="text-left">
                    <span className="headerTimestep">t: {props.t}</span>
                    <span className="headerStops">Stops remaining l: {props.l}</span>
                    <span className="headerNextStop">Next stop: <code>{NextStop(props)}</code></span>
                </h1>
            </div>
            <hr/>
            <div className="row contentRow policyRow">
                <div className="col-sm-6">
                    <div className="row">
                        <div className="DefenderPolicy row justify-content-center card">
                            <div className="card-header cardHeader"><h4>Stopping probability πΘ(stop|h)</h4></div>
                            <div className="card-body">
                                <PolicyAreaChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
                            </div>
                        </div>
                    </div>
                    <h4 className="deltaAlertsRow"></h4>
                    <div className="row">
                        <div className="DefenderObservations row justify-content-center card">
                            <div className="card-header cardHeader"><h4>Observations o = (Δx, Δy, Δz)</h4></div>
                            <div className="card-body">
                                <DeltaAlertsLineChart traces={props.traces} activeTrace={props.activeTrace}
                                                      t={props.t}/>
                            </div>
                            <div className="row">
                                <div className="col-sm-2">
                                    <span className="defenderPolicyPlotSliderLabel">Animation:</span>
                                </div>
                                <div className="col-sm-2">
                                    <Slider
                                        className="defenderPolicyPlotSlider"
                                        min={0}
                                        max={100}
                                        // step={1}
                                        value={animationDuration}
                                        onChange={onSliderChange}
                                        // railStyle={{
                                        //     height: 7,
                                        //     width:200
                                        // }}
                                        // handleStyle={{
                                        //     height: 20,
                                        //     width: 20,
                                        //     marginLeft: -14,
                                        //     marginTop: -7,
                                        //     // backgroundColor: "red",
                                        //     border: 0
                                        // }}
                                        trackStyle={{
                                            background: "none"
                                        }}
                                    />
                                </div>
                                <div className="col-sm-8">

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-sm-6">
                    <div className="DefenderObservations row justify-content-center card">
                        <div className="card-header cardHeader"><h4>Intrusion State</h4></div>
                        <div className="card-body">
                            <div className="row">
                                <div className="Network col-sm-9">
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
                                <div className="col-sm-3">
                                    <h6>Defensive measures:</h6>
                                    <DefensiveMeasures traces={props.traces} activeTrace={props.activeTrace} l={props.l}
                                                       t={props.t}/>
                                    <h6 className="intrusionStateInfo">Last 4 attacker actions:</h6>
                                    <AttackerActions traces={props.traces} activeTrace={props.activeTrace} l={props.l}
                                                       t={props.t}/>
                                    <h6 className="intrusionStateInfo"># Compromised nodes:{numCompromised(props)}</h6>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <Footer/>
        </div>
    );
}

Demo.propTypes = {};
Demo.defaultProps = {};
export default Demo;