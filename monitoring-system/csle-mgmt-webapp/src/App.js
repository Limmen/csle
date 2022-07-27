import React, {useState} from 'react';
import './App.css';
import Management from "./components/NavTest/Management/Container";
import NavTest from "./components/NavTest/NavTest";
import NotFound from "./components/NavTest/Management/NotFound/NotFound";
import Emulations from "./components/NavTest/Management/Emulations/Emulations";
import Monitoring from "./components/NavTest/Management/Monitoring/Monitoring";
import Traces from "./components/NavTest/Management/Traces/Traces";
import EmulationStatistics from "./components/NavTest/Management/EmulationStatistics/EmulationStatistics";
import SystemModels from "./components/NavTest/Management/SystemModels/SystemModels";
import PolicyExamination from "./components/NavTest/Management/PolicyExamination/PolicyExamination";
import ContainerImages from "./components/NavTest/Management/ContainerImages/ContainerImages";
import Simulations from "./components/NavTest/Management/Simulations/Simulations";
import TrainingResults from "./components/NavTest/Management/TrainingResults/TrainingResults";
import About from "./components/NavTest/Management/About/About";
import Login from "./components/NavTest/Management/Login/Login";
import Policies from "./components/NavTest/Management/Policies/Policies";
import Jobs from "./components/NavTest/Management/Jobs/Jobs";
import SDNControllers from "./components/NavTest/Management/SDNControllers/SDNControllers";
import {BrowserRouter, Routes, Route} from "react-router-dom";

function App() {
    const [token, setToken] = useState(null);
    return (
        <div className="App index container-fluid">
            <div className="row contentRow">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<NavTest/>}>
                                <Route index element={<Emulations/>}>
                                </Route>
                                <Route path="emulations-page" index element={<Emulations/>}>
                                </Route>
                                <Route path="simulations-page" index element={<Simulations/>}>
                                </Route>
                                <Route path="monitoring-page" index element={<Monitoring/>}>
                                </Route>
                                <Route path="traces-page" index element={<Traces/>}>
                                </Route>
                                <Route path="emulation-statistics-page" index element={<EmulationStatistics/>}>
                                </Route>
                                <Route path="system-models-page" index element={<SystemModels/>}>
                                </Route>
                                <Route path="policy-examination-page" index element={<PolicyExamination/>}>
                                </Route>
                                <Route path="images-page" index element={<ContainerImages/>}>
                                </Route>
                                <Route path="training-page" index element={<TrainingResults/>}>
                                </Route>
                                <Route path="policies-page" index element={<Policies/>}>
                                </Route>
                                <Route path="jobs-page" index element={<Jobs/>}>
                                </Route>
                                <Route path="sdn-controllers-page" index element={<SDNControllers/>}>
                                </Route>
                                <Route path="about-page" index element={<About/>}>
                                </Route>
                                <Route path="*" element={<NotFound/>}/>
                            </Route>
                            <Route path="login-page" index element={<Login setToken={setToken}/>}>
                            </Route>
                        </Routes>
                    </BrowserRouter>
                </div>
            </div>
        </div>
    );
}

export default App;
