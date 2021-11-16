import React, { useState } from 'react';
import './Container.css';
import {Outlet} from "react-router-dom";
import Header from "./Header/Header";
import Footer from "./Footer/Footer";

const Container = () => {
    const [t, setT] = useState(0);
    const [l, setL] = useState(3);

    const incrementT = () => {
        setT(t+1)
    }

    const decrementT = () => {
        if (t > 0) {
            setT(t-1)
        }
    }

    return (
        <div className="Container">
            <Header t={t} l={l} incrementT={incrementT} decrementT={decrementT}></Header>
            <div className="row contentRow">
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