import React from 'react';
import './Header.css';
import {NavLink} from "react-router-dom";
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';

const Header = () => {

    const renderEmulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            List of emulation configurations
        </Tooltip>
    );

    const renderSimulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            List of simulation configurations
        </Tooltip>
    );

    const renderMonitoringTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Real-time monitoring of emulations
        </Tooltip>
    );

    const renderTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            List of traces from running emulation episodes
        </Tooltip>
    );

    const renderEmulationStatisticsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Statistics collected from emulations
        </Tooltip>
    );

    const renderSystemModelsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            System models learned from data
        </Tooltip>
    );

    const renderPolicyExaminationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Interactive examination of learned security policies
        </Tooltip>
    );

    const renderContainerImagesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            List of container images
        </Tooltip>
    );

    const renderTrainingResultsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Results from training executions
        </Tooltip>
    );

    const renderPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Learned policies
        </Tooltip>
    );

    const renderJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Ongoing jobs in the environment
        </Tooltip>
    );

    const renderSdnControllersTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Information about SDN controllers
        </Tooltip>
    );

    const renderAboutTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Information about the environment
        </Tooltip>
    );

    return (<div className="Header">
            <div className="row">
                <div className="col-sm-12 p-5 mb-4 bg-light rounded-3 jumbotron blue-grey lighten-5">
                    <h1 className="text-center title">
                        Cyber Security Learning Environment (CSLE)
                    </h1>

                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    </nav>
                    <ul className="nav nav-tabs justify-content-center navtabsheader">
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderEmulationsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"emulations"}>
                                    Emulations
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderSimulationsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"simulations"}>
                                    Simulations
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderMonitoringTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"monitoring"}>
                                    Monitoring
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderTracesTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"traces"}>
                                    Traces
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderEmulationStatisticsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"emulationstatistics"}>
                                    Statistics
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderSystemModelsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"systemmodels"}>
                                    System models
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderPolicyExaminationTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"policyexamination"}>
                                    Policy Examination
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderContainerImagesTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"images"}>
                                    Images
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderTrainingResultsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"training"}>
                                    Training
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderPoliciesTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"policies"}>
                                    Policies
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderJobsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"jobs"}>
                                    Jobs
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderSdnControllersTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"sdncontrollers"}>
                                    SDN Controllers
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderAboutTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"about"}>
                                    About
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    )
};

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
