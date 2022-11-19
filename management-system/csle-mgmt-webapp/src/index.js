import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {Provider as AlertProvider} from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'

const alertOptions = {
    position: "middle",
    timeout: 5000,
    offset: '40px',
    transition: 'scale'
}
ReactDOM.render(
    <React.StrictMode>
        <AlertProvider template={AlertTemplate} {...alertOptions}>
            <App/>
        </AlertProvider>
    </React.StrictMode>,
    document.getElementById('root')
);
reportWebVitals();
