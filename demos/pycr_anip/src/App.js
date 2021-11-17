import React, {useState, useEffect, useRef} from 'react';
import './App.css';
import DefenderView from "./components/Container/DefenderView/DefenderView";
import AttackerView from "./components/Container/AttackerView/AttackerView";
import DefaultView from "./components/Container/DefaultView/DefaultView";
import DefenderNetwork from "./components/Container/DefenderView/DefenderNetwork/DefenderNetwork";
import AttackerNetwork from "./components/Container/AttackerView/AttackerNetwork/AttackerNetwork";
import InfrastructureMetrics from "./components/Container/DefenderView/InfrastructureMetrics/InfrastructureMetrics";
import DefenderDefaultPage from "./components/Container/DefenderView/DefenderDefaultPage/DefenderDefaultPage";
import AttackerDefaultPage from "./components/Container/AttackerView/AttackerDefaultPage/AttackerDefaultPage";
import Container from "./components/Container/Container";
import DefenderLog from "./components/Container/DefenderView/DefenderLog/DefenderLog";
import AttackerLog from "./components/Container/AttackerView/AttackerLog/AttackerLog";
import NotFound from "./components/NotFound/NotFound";
import DefenderPolicy from "./components/Container/DefenderView/DefenderPolicy/DefenderPolicy";
import AttackerPolicy from "./components/Container/AttackerView/AttackerPolicy/AttackerPolicy";
import AttackerMetrics from "./components/Container/AttackerView/AttackerMetrics/AttackerMetrics";
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
                                <Route path="" element={<DefaultView/>}/>
                                <Route path="defender" element={<DefenderView/>}>
                                    <Route path="" element={<DefenderDefaultPage/>}/>
                                    <Route path='network' element={<DefenderNetwork/>}/>
                                    <Route path='metrics' element={<InfrastructureMetrics
                                        traces={traces} activeTrace={activeTrace} t={t}
                                    />}
                                    />
                                    <Route path='log' element={<DefenderLog
                                        activeTrace={activeTrace} traces={traces} t={t}/>}/>
                                    <Route path='policy' element={
                                        <DefenderPolicy defenderPolicies={defenderPolicies}
                                                        activeDefenderPolicy={activeDefenderPolicy}
                                                        setActiveDefenderPolicy={setActiveDefenderPolicy}
                                                        activeTrace={activeTrace} traces={traces}
                                                        t={t}
                                    />} />
                                </Route>
                                <Route path="attacker" element={<AttackerView/>}>
                                    <Route path="" element={<AttackerDefaultPage/>}/>
                                    <Route path='network' element={<AttackerNetwork
                                        traces={traces} activeTrace={activeTrace} t={t}
                                    />}/>
                                    <Route path='log' element={<AttackerLog activeTrace={activeTrace}
                                                                            traces={traces} t={t}/>}/>
                                    <Route path='metrics' element={<AttackerMetrics
                                        traces={traces} activeTrace={activeTrace} t={t}
                                    />}
                                    />
                                    <Route path='policy' element={
                                        <AttackerPolicy
                                        attackerPolicies={attackerPolicies}
                                        activeAttackerPolicy={activeAttackerPolicy}
                                        setActiveAttackerPolicy={setActiveAttackerPolicy}
                                        activeTrace={activeTrace} traces={traces}
                                        />
                                    }
                                    />
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
