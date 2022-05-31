import React from 'react';
import './App.css';
import Container from "./components/Container/Container";
import NotFound from "./components/Container/NotFound/NotFound";
import Emulations from "./components/Container/Emulations/Emulations";
import Monitoring from "./components/Container/Monitoring/Monitoring";
import Traces from "./components/Container/Traces/Traces";
import EmulationStatistics from "./components/Container/EmulationStatistics/EmulationStatistics";
import SystemModels from "./components/Container/SystemModels/SystemModels";
import PolicyExamination from "./components/Container/PolicyExamination/PolicyExamination";
import ContainerImages from "./components/Container/ContainerImages/ContainerImages";
import Simulations from "./components/Container/Simulations/Simulations";
import TrainingResults from "./components/Container/TrainingResults/TrainingResults";
import About from "./components/Container/About/About";
import Policies from "./components/Container/Policies/Policies";
import Jobs from "./components/Container/Jobs/Jobs";
import {BrowserRouter, Routes, Route} from "react-router-dom";

function App() {
    return (
        <div className="App index container-fluid">
            <div className="row contentRow">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<Container/>}>
                                <Route index element={<Emulations/>}>
                                </Route>
                                <Route path="emulations" index element={<Emulations/>}>
                                </Route>
                                <Route path="simulations" index element={<Simulations/>}>
                                </Route>
                                <Route path="monitoring" index element={<Monitoring/>}>
                                </Route>
                                <Route path="traces" index element={<Traces/>}>
                                </Route>
                                <Route path="emulationstatistics" index element={<EmulationStatistics/>}>
                                </Route>
                                <Route path="systemmodels" index element={<SystemModels/>}>
                                </Route>
                                <Route path="policyexamination" index element={<PolicyExamination/>}>
                                </Route>
                                <Route path="images" index element={<ContainerImages/>}>
                                </Route>
                                <Route path="training" index element={<TrainingResults/>}>
                                </Route>
                                <Route path="policies" index element={<Policies/>}>
                                </Route>
                                <Route path="jobs" index element={<Jobs/>}>
                                </Route>
                                <Route path="about" index element={<About/>}>
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
