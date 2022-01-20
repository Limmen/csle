import React, { useState } from 'react';
import './Container.css';
import {Outlet} from "react-router-dom";
import Header from "./Header/Header";
import Footer from "./Footer/Footer";

const Container = (props) => {

    return (
        <div className="Container">
            <Header t={props.t} l={props.l} incrementT={props.incrementT} decrementT={props.decrementT}
                    traces={props.traces} activeTrace={props.activeTrace}
                    setActiveTrace={props.setActiveTrace} lastT={props.lastT}
                    firstT={props.firstT}
            />
            <div className="row">
                <div className="col-sm-12">
                    <Outlet/>
                </div>
            </div>
            <Footer/>
        </div>
    );
}

Container.propTypes = {};
Container.defaultProps = {};
export default Container;