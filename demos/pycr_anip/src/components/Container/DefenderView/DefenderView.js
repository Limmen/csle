import React from 'react';
import './DefenderView.css';
import { Outlet, NavLink } from "react-router-dom";

const DefenderView = () => {

    return (
        <div className="Defender">
            <div className="row">
                <div className="col-sm-2">
                        <div className="nav flex-column nav-pills" id="v-pills-tab" role="tablist"
                             aria-orientation="vertical">
                                <NavLink to={`network`} role="tab" aria-controls="v-pills-home" aria-selected="true"
                                      className="nav-link pillslabel" activeClassName="active" id="v-pills-home-tab" data-toggle="pill">
                                    IT-Infrastructure
                                </NavLink>
                            <NavLink to={`log`} role="tab" aria-controls="v-pills-home" aria-selected="true"
                                  className="nav-link pillslabel" activeClassName="active" id="v-pills-home-tab" data-toggle="pill">
                                Activity Log
                            </NavLink>
                            <NavLink to={`metrics`} activeClassName="active" role="tab" aria-controls="v-pills-home" aria-selected="true"
                                  className="nav-link pillslabel" id="v-pills-home-tab" data-toggle="pill">
                                Infrastructure metrics
                            </NavLink>
                            <NavLink to={`policy`} activeClassName="active" role="tab" aria-controls="v-pills-home" aria-selected="true"
                                     className="nav-link pillslabel" id="v-pills-home-tab" data-toggle="pill">
                                Defender Policy
                            </NavLink>
                        </div>
                </div>
                <div className="col-sm-8">
                    <div className="row">
                        <Outlet/>
                    </div>
                </div>
                <div className="col-sm-2"></div>
            </div>
        </div>
    );
}

DefenderView.propTypes = {};
DefenderView.defaultProps = {};
export default DefenderView;

//<LoginAttemptsChart/>
//<WarningAlertsChart/>
//<AttackerMetricsCharts/>
//<AccumulatedMetricsChart/>
//<DefenderPolicyChart/>