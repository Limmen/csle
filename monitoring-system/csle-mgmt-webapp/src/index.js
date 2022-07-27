import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {Provider as AlertProvider} from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'

// optional configuration
const alertOptions = {
    position: "middle",
    timeout: 5000,
    offset: '40px',
    // you can also just use 'scale'
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

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
