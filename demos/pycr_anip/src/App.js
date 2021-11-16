import React from 'react';
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
import {BrowserRouter, Routes, Route} from "react-router-dom";
import 'react-pro-sidebar/dist/css/styles.css';

function App() {
  return (
      <div className="App index container-fluid">
        <div className="row contentRow">
          <div className="col-sm-12">
              <BrowserRouter>
                  <Routes>
                      <Route path="/" element={<Container />}>
                          <Route path="" element={<DefaultView />} />
                          <Route path="defender" element={<DefenderView />} >
                              <Route path="" element={<DefenderDefaultPage />} />
                              <Route path='network' element={<DefenderNetwork />} />
                              <Route path='metrics' element={<InfrastructureMetrics />} />
                              <Route path='log' element={<DefenderLog />} />
                              <Route path='policy' element={<DefenderPolicy />} />
                          </Route>
                          <Route path="attacker" element={<AttackerView />}>
                              <Route path="" element={<AttackerDefaultPage />} />
                              <Route path='network' element={<AttackerNetwork />} />
                              <Route path='reconstate' element={<AttackerNetwork />} />
                              <Route path='log' element={<AttackerLog />} />
                          </Route>
                          <Route path="*" element={<NotFound />} />
                      </Route>
                  </Routes>
              </BrowserRouter>
          </div>
        </div>
      </div>
  );
}

export default App;
