import React, {useState} from 'react';
import './Header.css';
import {NavLink} from "react-router-dom";
import Glyphicon from '@strongdm/glyphicon'

const Header = (props) => (

    <div className="Header">
        <div className="row">
            <div className="col-sm-2 p-5 mb-4 bg-light rounded-3 jumbotron"></div>
            <div className="col-sm-10 p-5 mb-4 bg-light rounded-3 jumbotron">
                <h3 className="display-9 align-content-center fw-bold  title">Intrusion Prevention through Optimal
                    Stopping - DEMO</h3>
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                </nav>
                <h6 className="timeStepControls">
                    <span className="timestepLabel">Time-step: {props.t}</span>
                    <button type="submit" className="btn"><Glyphicon glyph='chevron-left' onClick={props.decrementT}/>
                    </button>
                    <button type="submit" className="btn"><Glyphicon glyph='chevron-right' onClick={props.incrementT}/>
                    </button>
                    <span className="stopsRemainingLabel">Stops remaining: {props.l}</span>
                </h6>
                <ul className="nav nav-tabs justify-content-center navtabsheader">
                    <li className="nav-item navtabheader">
                        <NavLink className="nav-link navtablabel" to={"defender"} activeClassName="active"> Defender's
                            View</NavLink>
                    </li>
                    <li className="nav-item navtabheader">
                        <NavLink className="nav-link navtablabel" to={"attacker"} activeClassName="active"> Attacker's
                            View </NavLink>
                    </li>
                </ul>
            </div>
        </div>
    </div>
);
Header.propTypes = {};

Header.defaultProps = {};

export default Header;
