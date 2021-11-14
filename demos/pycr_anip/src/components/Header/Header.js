import React from 'react';
import './Header.css';

const Header = () => (
    <div className="Header">
        <div className="p-5 mb-4 bg-light rounded-3 jumbotron">
                <h3 className="display-9 align-content-center fw-bold  title">Intrusion Prevention through Optimal Stopping</h3>
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="col-sm-5"></div>
                <div className="col-sm-2">
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav">
                            <li className="nav-item active">
                                <a className="nav-link fw-bold" href="#">Defender's View</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link fw-bold" href="#">Attacker's View</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div className="col-sm-5"></div>
                </nav>
        </div>
    </div>
);
Header.propTypes = {};

Header.defaultProps = {};

export default Header;
