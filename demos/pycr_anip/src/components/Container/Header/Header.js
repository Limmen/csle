import React from 'react';
import './Header.css';
import {NavLink} from "react-router-dom";
import Glyphicon from '@strongdm/glyphicon'
import {Dropdown} from "react-bootstrap"
import TraceDropdownElement from "./TraceDropdownElement/TraceDropdownElement";
import mdp from "./pycr_101_s1.png"

const Header = (props) => {

    return (
        <div className="Header">
            <div className="row">
                <div className="col-sm-2 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <h6 className="timeStepControls">
                        <Dropdown className="traceDropdown">
                            <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="sm">
                                Trace: {props.activeTrace}
                            </Dropdown.Toggle>

                            <Dropdown.Menu variant="dark">
                                {props.traces.map((trace, index) =>
                                    <TraceDropdownElement trace={trace} index={index} key={index}
                                                          setActiveTrace={props.setActiveTrace}/>
                                )}
                            </Dropdown.Menu>
                        </Dropdown>
                        <span className="timestepLabel">Time-step: {props.t + 1}</span>

                        <button type="submit" className="btn" onClick={props.firstT} className="shortCutT">
                            1
                        </button>

                        <button type="submit" className="btn"><Glyphicon glyph='chevron-left'
                                                                         onClick={props.decrementT}/>
                        </button>
                        <button type="submit" className="btn"><Glyphicon glyph='chevron-right'
                                                                         onClick={props.incrementT}/>
                        </button>

                        <button type="submit" className="btn" onClick={props.lastT} className="shortCutT">
                            T∅
                        </button>

                        <span className="stopsRemainingLabel">Stops remaining: {props.l}</span>
                    </h6>
                </div>
                <div className="col-sm-8 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <h3 className="display-9 align-content-center fw-bold  title">Intrusion Prevention through Optimal
                        Stopping - DEMO</h3>
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    </nav>
                    <ul className="nav nav-tabs justify-content-center navtabsheader">
                        <li className="nav-item navtabheader">
                            <NavLink className="nav-link navtablabel" to={"defender"}  activeClassName="active">
                                Defender's  View
                            </NavLink>
                        </li>
                        <li className="nav-item navtabheader">
                            <NavLink className="nav-link navtablabel" to={"attacker"}
                                     activeClassName="active"> Attacker's
                                View </NavLink>
                        </li>
                    </ul>
                </div>
                <div className="col-sm-2 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <img className="mdp img-responsive" src={mdp} alt={"MDP"}/>
                </div>
            </div>
        </div>
    );
}
Header.propTypes = {};

Header.defaultProps = {};

export default Header;
