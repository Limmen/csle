import React, {useState, useEffect, useRef} from 'react';
import './App.css';
import Container from "./components/Container/Container";
import NotFound from "./components/Container/NotFound/NotFound";
import Demo from "./components/Container/Demo/Demo";
import InfrastructureConfiguration from "./components/Container/InfrastructureConfiguration/InfrastructureConfiguration";
import ActivityLog from "./components/Container/ActivityLog/ActivityLog";
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
            while(tRef.current < tracesRef.current[activeTraceRef.current].defender_actions.length - 1){
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
        if(event.key === 'ArrowLeft'){
            decrementT()
        }
        if(event.key === 'ArrowRight'){
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
                                <Route path="log" element={<ActivityLog
                                    t={t} l={l} incrementT={incrementT} decrementT={decrementT}
                                    activeTrace={activeTrace} traces={traces}
                                    setActiveTrace={setActiveTraceRef}
                                    lastT={lastT} firstT={firstT}
                                    defenderPolicies={defenderPolicies}
                                    activeDefenderPolicy={activeDefenderPolicy}
                                    setActiveDefenderPolicy={setActiveDefenderPolicy}
                                />}>
                                </Route>
                                <Route path="config" element={<InfrastructureConfiguration
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
