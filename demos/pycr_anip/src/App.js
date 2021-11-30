import React, {useState, useEffect, useRef} from 'react';
import './App.css';
import Container from "./components/Container/Container";
import NotFound from "./components/Container/NotFound/NotFound";
import Demo from "./components/Container/Demo/Demo";
import DockerContainerConfigurations
    from "./components/Container/DockerContainerConfigurations/DockerContainerConfigurations";
import AttackerActionSpaceConfig
    from "./components/Container/AttackerActionSpaceConfig/AttackerActionSpaceConfig";
import AttackerStaticPolicyConfig
    from "./components/Container/AttackerStaticPolicyConfig/AttackerStaticPolicyConfig";
import DefenderActionSpaceConfig
    from "./components/Container/DefenderActionSpaceConfig/DefenderActionSpaceConfig";
import VulnerabilitiesConfig
    from "./components/Container/VulnerabilitiesConfig/VulnerabilitiesConfig";
import FlagsConfig
    from "./components/Container/FlagsConfig/FlagsConfig";
import FirewallsConfig
    from "./components/Container/FirewallsConfig/FirewallsConfig";
import UsersConfig
    from "./components/Container/UsersConfig/UsersConfig";
import TrafficConfig
    from "./components/Container/TrafficConfig/TrafficConfig";
import DefenderLog from "./components/Container/DefenderLog/DefenderLog";
import AttackerLog from "./components/Container/AttackerLog/AttackerLog";
import DefenderTraining from "./components/Container/DefenderTraining/DefenderTraining";
import AttackerTraining from "./components/Container/AttackerTraining/AttackerTraining";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import 'react-pro-sidebar/dist/css/styles.css';

function App() {
    //const ip = "172.31.212.92"
    const ip = "localhost"

    const [t, setT] = useState(0);
    const [l, setL] = useState(1);
    const [traces, setTraces] = useState([]);
    const [activeTrace, setActiveTrace] = useState(0);
    const [defenderPolicies, setDefenderPolicies] = useState([1, 2, 3, 4, 5, 6]);
    const [activeDefenderPolicy, setActiveDefenderPolicy] = useState(1);
    const [attackerPolicies, setAttackerPolicies] = useState([1, 2, 3, 4, 5, 6]);
    const [activeAttackerPolicy, setActiveAttackerPolicy] = useState(1);

    const tracesRef = React.useRef(traces);
    const setTracesRef = data => {
        tracesRef.current = data
        setTraces(data)
    };

    const tRef = React.useRef(t);
    const setTRef = data => {
        tRef.current = data
        setT(data)
    };

    const lRef = React.useRef(l);
    const setLRef = data => {
        lRef.current = data
        setL(data)
    };

    const activeTraceRef = React.useRef(activeTrace);
    const setActiveTraceRef = data => {
        activeTraceRef.current = data
        setActiveTrace(data)
    };


    useEffect(() => {
        fetch(
            `http://` + ip + ':8888/trajectories',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTracesRef(response.trajectories);
                setActiveTraceRef(0);
                setLRef(response.trajectories[0].maximum_stops);
                setTRef(0)
                window.addEventListener('keydown', e => {
                    handleKeyPress(e)
                });
            })
            .catch(error => console.log("error:" + error));
    }, []);

    const incrementT = () => {
        if (tracesRef.current.length > 0) {
            if (tracesRef.current[activeTraceRef.current].defender_actions[tRef.current + 1] == 0 && lRef.current > 0) {
                setLRef(lRef.current - 1)
            }
            if (tRef.current >= tracesRef.current[activeTraceRef.current].defender_actions.length - 1) {
                setTRef(tracesRef.current[activeTraceRef.current].defender_actions.length - 1)
            } else {
                setTRef(tRef.current + 1)
            }
        }
    }

    const firstT = () => {
        setTRef(0)
        setLRef(tracesRef.current[activeTraceRef.current].maximum_stops);
    }

    const lastT = () => {
        if (tRef.current >= tracesRef.current[activeTraceRef.current].defender_actions.length - 1) {
            setTRef(tracesRef.current[activeTraceRef.current].defender_actions.length - 1)
        } else {
            while (tRef.current < tracesRef.current[activeTraceRef.current].defender_actions.length - 1) {
                if (tracesRef.current[activeTraceRef.current].defender_actions[tRef.current + 1] == 0 && lRef.current > 0) {
                    setLRef(lRef.current - 1)
                }
                setTRef(tRef.current + 1)
            }
        }
    }

    const decrementT = () => {
        if (tracesRef.current[activeTraceRef.current].defender_actions[tRef.current] == 0) {
            setLRef(lRef.current + 1)
        }
        if (tRef.current > 0) {
            setTRef(tRef.current - 1)
        }
    }

    const handleKeyPress = (event) => {
        if (event.key === 'ArrowLeft') {
            decrementT()
        }
        if (event.key === 'ArrowRight') {
            incrementT()
        }
    }

    return (
        <div className="App index container-fluid" onKeyPress={handleKeyPress}>
            <div className="row contentRow">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<Container
                                       t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                       activeTrace={activeTrace} traces={traces}
                                       setActiveTrace={setActiveTraceRef}
                                       lastT={lastT} firstT={firstT}
                                   />}>
                                <Route index element={<Demo
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="demo" element={<Demo
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="log/defender" element={<DefenderLog
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="log/attacker" element={<AttackerLog
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/attacker/actionspace" element={<AttackerActionSpaceConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/attacker/staticpolicy" element={<AttackerStaticPolicyConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/defender/actionspace" element={<DefenderActionSpaceConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/containers" element={<DockerContainerConfigurations
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/vulnerabilities" element={<VulnerabilitiesConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/flags" element={<FlagsConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/firewalls" element={<FirewallsConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/users" element={<UsersConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config/infrastructure/clients" element={<TrafficConfig
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="training/defender" element={<DefenderTraining
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="training/attacker" element={<AttackerTraining
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="*" element={<NotFound/>}/>
                            </Route>
                        </Routes>
                    </BrowserRouter>
                </div>
            </div>
        </div>
    );
}

export default App;
