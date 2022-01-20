import React from 'react';
import './index.css';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import $ from 'jquery';
import {render} from "react-dom";

const rootElement = document.getElementById("root");
render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
rootElement
)
;

