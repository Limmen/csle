import React from 'react';
import './Header.css';
import {NavLink} from "react-router-dom";
import Glyphicon from '@strongdm/glyphicon'
import {Dropdown} from "react-bootstrap"
import TraceDropdownElement from "./TraceDropdownElement/TraceDropdownElement";
import mdp from "./pycr_101_s1.png"

const Header = (props) => {

    const NextStop = (props) => {
        if (props.traces.length > 0) {
            var nextStop = null
            for (let i = 0; i < props.traces[props.activeTrace].stop_actions.length; i++) {
                if (props.traces[props.activeTrace].stop_actions[i].l === props.l) {
                    return props.traces[props.activeTrace].stop_actions[i].command
                }
            }
            return "-"
        } else {
            return "-"
        }
    }

    return (
        <div className="Header">
            <div className="row">
                <div className="col-sm-2 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <Dropdown className="traceDropdownDemo">
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
                    <h6 className="timeStepControls">
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
                        <span className="nextStopLabel">Next stop: <code>{NextStop(props)}</code></span>
                    </h6>
                </div>
                <div className="col-sm-8 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <h3 className="display-9 align-content-center fw-bold  title">
                        Intrusion Prevention through Optimal  Stopping
                    </h3>
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    </nav>
                    <ul className="nav nav-tabs justify-content-center navtabsheader">
                        <li className="nav-item navtabheader">
                            <NavLink className="nav-link navtablabel" to={"demo"}  activeClassName="active">
                                Demo
                            </NavLink>
                        </li>
                        <li className="nav-item navtabheader">
                            <NavLink className="nav-link navtablabel" to={"log"}
                                     activeClassName="active">
                                ActivityLog
                            </NavLink>
                        </li>
                        <li className="nav-item navtabheader">
                            <NavLink className="nav-link navtablabel" to={"config"}
                                     activeClassName="active">
                                Infrastructure Configuration
                            </NavLink>
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
