import React, {useState} from 'react';
import './App.css';
import Management from "./components/HeaderNav/Management/Management";
import HeaderNav from "./components/HeaderNav/HeaderNav";
import NotFound from "./components/HeaderNav/Management/NotFound/NotFound";
import Emulations from "./components/HeaderNav/Management/Emulations/Emulations";
import Monitoring from "./components/HeaderNav/Management/Monitoring/Monitoring";
import Traces from "./components/HeaderNav/Management/Traces/Traces";
import EmulationStatistics from "./components/HeaderNav/Management/EmulationStatistics/EmulationStatistics";
import SystemModels from "./components/HeaderNav/Management/SystemModels/SystemModels";
import PolicyExamination from "./components/HeaderNav/Management/PolicyExamination/PolicyExamination";
import ContainerImages from "./components/HeaderNav/Management/ContainerImages/ContainerImages";
import Simulations from "./components/HeaderNav/Management/Simulations/Simulations";
import TrainingResults from "./components/HeaderNav/Management/TrainingResults/TrainingResults";
import About from "./components/HeaderNav/Management/About/About";
import Login from "./components/HeaderNav/Management/Login/Login";
import Policies from "./components/HeaderNav/Management/Policies/Policies";
import Jobs from "./components/HeaderNav/Management/Jobs/Jobs";
import SDNControllers from "./components/HeaderNav/Management/SDNControllers/SDNControllers";
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
                                   element={<HeaderNav/>}>
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
