import React, {useState} from 'react';
import './Header.css';
import {NavLink} from "react-router-dom";
import Glyphicon from '@strongdm/glyphicon'
import {Dropdown, NavDropdown, Nav} from "react-bootstrap"
import TraceDropdownElement from "./TraceDropdownElement/TraceDropdownElement";
import mdp from "./pycr_101_s1.png"
import {LinkContainer} from 'react-router-bootstrap';

const Header = (props) => {

    const [activeNavKey, setActiveNavKey] = useState(0);

    const handleSelect = (key) => {
        setActiveNavKey(Math.trunc(key))
    }

    const handleSelectNonNavBar = (key) => {
        setActiveNavKey(0)
    }

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
                    </h6>
                    <h6 className="timeStepControls2">
                        <span className="stopsRemainingLabel">Stops remaining: {props.l}</span>
                    </h6>
                    <h6 className="timeStepControls3">
                        <span className="nextStopLabel">Next stop: <code>{NextStop(props)}</code></span>
                    </h6>
                </div>
                <div className="col-sm-8 p-5 mb-4 bg-light rounded-3 jumbotron">
                    <h3 className="display-9 align-content-center fw-bold  title">
                        Intrusion Prevention through Optimal Stopping
                    </h3>
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    </nav>
                    <ul className="nav nav-tabs justify-content-center navtabsheader">
                        <li className="nav-item navtabheader">
                                <NavLink className="nav-link navtablabel" to={"demo"} activeClassName="active"
                                         onClick={handleSelectNonNavBar}>
                                    Demo
                                </NavLink>
                        </li>
                        <li className="nav-item navtabheader">
                            <NavDropdown className="navdropdownheader" title="Training" id="basic-nav-dropdown"
                                         activeClassName="active" eventKey={4} active={activeNavKey == 4}>
                                <LinkContainer to="training/attacker">
                                    <NavDropdown.Item eventKey={4.1}>Attacker Training</NavDropdown.Item>
                                </LinkContainer>
                                <LinkContainer to="training/defender">
                                    <NavDropdown.Item eventKey={4.2}>Defender Training</NavDropdown.Item>
                                </LinkContainer>
                            </NavDropdown>
                        </li>
                        <li className="nav-item dropdown navtabheader">
                            <Nav activeKey={activeNavKey} onSelect={handleSelect}>
                                <NavDropdown className="navdropdownheader" title="Logs" id="basic-nav-dropdown"
                                             activeClassName="active" eventKey={3} active={activeNavKey == 3}>
                                    <LinkContainer to="log/attacker">
                                        <NavDropdown.Item eventKey={3.1}>Attacker log</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="log/defender">
                                        <NavDropdown.Item eventKey={3.2}>Defender log</NavDropdown.Item>
                                    </LinkContainer>
                                </NavDropdown>
                            </Nav>
                        </li>
                        <li className="nav-item dropdown navtabheader">
                            <Nav activeKey={activeNavKey} onSelect={handleSelect}>
                                <NavDropdown className="navdropdownheader" title="Configurations" id="basic-nav-dropdown"
                                             activeClassName="active" eventKey={2} active={activeNavKey == 2}>
                                    <LinkContainer to="config/attacker/actionspace">
                                        <NavDropdown.Item eventKey={2.1}>Attacker action space</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/attacker/staticpolicy">
                                        <NavDropdown.Item eventKey={2.2}>Attacker static policy</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/defender/actionspace">
                                        <NavDropdown.Item eventKey={2.3}>Defender action space</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/containers">
                                        <NavDropdown.Item eventKey={2.4}>Containers</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/vulnerabilities">
                                        <NavDropdown.Item eventKey={2.5}>Container Vulnerabilities</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/flags">
                                        <NavDropdown.Item eventKey={2.6}>Container Flags</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/firewalls">
                                        <NavDropdown.Item eventKey={2.7}>Container Firewalls</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/users">
                                        <NavDropdown.Item eventKey={2.8}>Container Users</NavDropdown.Item>
                                    </LinkContainer>
                                    <LinkContainer to="config/infrastructure/clients">
                                        <NavDropdown.Item eventKey={2.9}>Client Population</NavDropdown.Item>
                                    </LinkContainer>
                                </NavDropdown>
                            </Nav>
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
