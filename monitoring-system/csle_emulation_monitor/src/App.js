import React from 'react';
import './App.css';
import Container from "./components/Container/Container";
import NotFound from "./components/Container/NotFound/NotFound";
import Emulations from "./components/Container/Emulations/Emulations";
import Monitoring from "./components/Container/Monitoring/Monitoring";
import Traces from "./components/Container/Traces/Traces";
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
                                <Route path="monitoring" index element={<Monitoring/>}>
                                </Route>
                                <Route path="traces" index element={<Traces/>}>
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
