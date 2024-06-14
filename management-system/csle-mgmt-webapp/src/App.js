import React from 'react';
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
import UserAdmin from "./components/MainContainer/UserAdmin/UserAdmin";
import SystemAdmin from "./components/MainContainer/SystemAdmin/SystemAdmin";
import LogsAdmin from "./components/MainContainer/LogsAdmin/LogsAdmin";
import Login from "./components/MainContainer/Login/Login";
import Register from "./components/MainContainer/Register/Register";
import Policies from "./components/MainContainer/Policies/Policies";
import Jobs from "./components/MainContainer/Jobs/Jobs";
import ControlPlane from "./components/MainContainer/ControlPlane/ControlPlane";
import SDNControllers from "./components/MainContainer/SDNControllers/SDNControllers";
import Downloads from "./components/MainContainer/Downloads/Downloads";
import CreateEmulation from "./components/MainContainer/CreateEmulation/CreateEmulation";
import ServerCluster from "./components/MainContainer/ServerCluster/ServerCluster";
import ContainerTerminal from "./components/MainContainer/ContainerTerminal/ContainerTerminal";
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import useSession from "./components/MainContainer/SessionManagement/useSession";
import { useAlert } from "react-alert";
import {
    LOGIN_PAGE_RESOURCE,
    EMULATIONS_PAGE_RESOURCE,
    SIMULATIONS_PAGE_RESOURCE,
    EMULATION_STATISTICS_PAGE_RESOURCE,
    MONITORING_PAGE_RESOURCE,
    TRACES_PAGE_RESOURCE,
    POLICY_EXAMINATION_PAGE_RESOURCE,
    IMAGES_PAGE_RESOURCE,
    TRAINING_PAGE_RESOURCE,
    POLICIES_PAGE_RESOURCE,
    SDN_CONTROLLERS_PAGE_RESOURCE,
    CONTROL_PLANE_PAGE_RESOURCE,
    CONTAINER_TERMINAL_PAGE_RESOURCE,
    ABOUT_PAGE_RESOURCE,
    DOWNLOADS_PAGE_RESOURCE,
    REGISTER_PAGE_RESOURCE,
    USER_ADMIN_PAGE_RESOURCE,
    SYSTEM_ADMIN_PAGE_RESOURCE,
    LOGS_ADMIN_PAGE_RESOURCE,
    SYSTEM_MODELS_PAGE_RESOURCE,
    JOBS_PAGE_RESOURCE,
    SERVER_CLUSTER_PAGE_RESOURCE,
    CREATE_EMULATION_PAGE
} from "./components/Common/constants";

function App() {
    /**
     * Container component containing the main components of the page and defining the routes
     * @returns {JSX.Element}
     * @constructor
     */
    const {sessionData, setSessionData} = useSession();
    const alert = useAlert();

    const ProtectedRoute = ({
                                user,
                                redirectPath = `/${LOGIN_PAGE_RESOURCE}`,
                                children,
                            }) => {
        if (!sessionData) {
            alert.show("Only logged in users can access this page")
            return <Navigate to={redirectPath} replace/>;
        }
        return children;
    };

    return (
        <div className="App container-fluid">
            <div className="row">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<MainContainer sessionData={sessionData}
                                                           setSessionData={setSessionData}/>}>
                                <Route index element={<Navigate to="login-page" />}>
                                </Route>
                                <Route path={EMULATIONS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Emulations sessionData={sessionData}
                                                    setSessionData={setSessionData}
                                        />
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path={SIMULATIONS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Simulations sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path={MONITORING_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Monitoring sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path={TRACES_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Traces sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={EMULATION_STATISTICS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <EmulationStatistics sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={SYSTEM_MODELS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <SystemModels sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={POLICY_EXAMINATION_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <PolicyExamination sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={IMAGES_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <ContainerImages sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={TRAINING_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <TrainingResults sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={POLICIES_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Policies sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={JOBS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <Jobs sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={SDN_CONTROLLERS_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <SDNControllers sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={CONTROL_PLANE_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <ControlPlane sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={CONTAINER_TERMINAL_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <ContainerTerminal sessionData={sessionData} setSessionData={setSessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={ABOUT_PAGE_RESOURCE} index element={<About/>}>
                                </Route>
                                <Route path={DOWNLOADS_PAGE_RESOURCE} index
                                       element={<Downloads sessionData={sessionData}
                                                           setSessionData={setSessionData}/>}>
                                </Route>
                                <Route path={LOGIN_PAGE_RESOURCE} index element={<Login setSessionData={setSessionData}
                                                                               sessionData={sessionData}/>}>
                                </Route>
                                <Route path={REGISTER_PAGE_RESOURCE} index element={<Register />}>
                                </Route>
                                <Route path={USER_ADMIN_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                    <UserAdmin sessionData={sessionData} setSessionData={setSessionData} />
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={SYSTEM_ADMIN_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <SystemAdmin sessionData={sessionData} setSessionData={setSessionData} />
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={LOGS_ADMIN_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <LogsAdmin sessionData={sessionData} setSessionData={setSessionData} />
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={SERVER_CLUSTER_PAGE_RESOURCE} index element={
                                    <ProtectedRoute>
                                        <ServerCluster sessionData={sessionData} setSessionData={setSessionData} />
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path={CREATE_EMULATION_PAGE} index element={
                                    <ProtectedRoute>
                                        <CreateEmulation sessionData={sessionData} setSessionData={setSessionData} />
                                    </ProtectedRoute>
                                }>
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
