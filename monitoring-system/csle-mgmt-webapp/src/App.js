import React, {useState} from 'react';
import './App.css';
import MainContainer from "./components/MainContainer/MainContainer";
import NotFound from "./components/MainContainer/NotFound/NotFound";
import Emulations from "./components/MainContainer/Emulations/Emulations";
import Monitoring from "./components/MainContainer/Monitoring/Monitoring";
import Traces from "./components/MainContainer/Traces/Traces";
import EmulationStatistics from "./components/MainContainer/EmulationStatistics/EmulationStatistics";
import SystemModels from "./components/MainContainer/SystemModels/SystemModels";
import PolicyExamination from "./components/MainContainer/PolicyExamination/PolicyExamination";
import ContainerImages from "./components/MainContainer/ContainerImages/ContainerImages";
import Simulations from "./components/MainContainer/Simulations/Simulations";
import TrainingResults from "./components/MainContainer/TrainingResults/TrainingResults";
import About from "./components/MainContainer/About/About";
import Login from "./components/MainContainer/Login/Login";
import Policies from "./components/MainContainer/Policies/Policies";
import Jobs from "./components/MainContainer/Jobs/Jobs";
import SDNControllers from "./components/MainContainer/SDNControllers/SDNControllers";
import {BrowserRouter, Routes, Route} from "react-router-dom";

function App() {
    const [token, setToken] = useState(null);
    return (
        <div className="App container-fluid">
            <div className="row">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<MainContainer/>}>
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
                                <Route path="login-page" index element={<Login setToken={setToken}/>}>
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
