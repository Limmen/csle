import React from 'react';
import './Header.css';
import {NavLink, useLocation} from "react-router-dom";
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import CsleLogo from './CsleLogo.png'
import CsleSmallLogo from './CsleSmallLogo.png'

/**
 * The header component that is present on every page
 */
const Header = (props) => {
    const location = useLocation();
    const managementDropdownRoutes = ["/simulations-page", "/emulations-page", "/monitoring-page", "/traces-page",
        "/emulation-statistics-page", "/system-models-page", "/policy-examination-page", "/images-page",
        "/training-page", "/policies-page", "/jobs-page", "/sdn-controllers-page", "/control-plane-page",
        "/host-terminal-page", "/container-terminal-page"]
    const adminDropdownRoutes = ["/user-admin-page", "/system-admin-page", "/logs-admin-page"]

    const ActionsCellTracesDataset = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <li className="nav-item dropdown navtabheader">
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderAdminTooltip}>
                        <a className={"nav-link dropdown-toggle navtablabel largeFont "
                            + (adminDropdownRoutes.includes(location.pathname) ? 'active' : 'notActive')}
                           data-toggle="dropdown"
                           role="button" aria-haspopup="true" aria-expanded="false"
                           id="navbarDropdown"
                        >
                            Administration </a>
                    </OverlayTrigger>
                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderUserAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={"user-admin-page"} data-toggle="tab">
                                User administration
                            </NavLink>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderSystemAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={"system-admin-page"} data-toggle="tab">
                                System administration
                            </NavLink>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderLogsAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={"logs-admin-page"} data-toggle="tab">
                                Logs administration
                            </NavLink>
                        </OverlayTrigger>
                    </div>
                </li>
            )
        } else {
            return (<></>)
        }
    }

    const renderManagementTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management and operation of the environment
        </Tooltip>
    );

    const renderEmulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of emulations
        </Tooltip>
    );

    const renderSimulationsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of simulations
        </Tooltip>
    );

    const renderMonitoringTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Real-time monitoring of emulations
        </Tooltip>
    );

    const renderTracesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of collected traces
        </Tooltip>
    );

    const renderEmulationStatisticsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of statistics collected from emulations
        </Tooltip>
    );

    const renderSystemModelsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of system models
        </Tooltip>
    );

    const renderPolicyExaminationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Interactive examination of learned security policies
        </Tooltip>
    );

    const renderContainerImagesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of container images
        </Tooltip>
    );

    const renderTrainingResultsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of training results
        </Tooltip>
    );

    const renderPoliciesTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of learned security policies
        </Tooltip>
    );

    const renderJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of jobs
        </Tooltip>
    );

    const renderSdnControllersTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Management of SDN controllers
        </Tooltip>
    );

    const renderControlPlaneTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Control plane for emulations
        </Tooltip>
    );

    const renderHostTerminalTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Terminal access to the host of the management system
        </Tooltip>
    );

    const renderContainerTerminalTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Terminal access to containers of emulations
        </Tooltip>
    );

    const renderAboutTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Information about CSLE
        </Tooltip>
    );

    const renderAdminTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Administration of the environment.
        </Tooltip>
    );

    const renderUserAdminTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Administration of user accounts.
        </Tooltip>
    );

    const renderSystemAdminTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Administration of system configuration.
        </Tooltip>
    );

    const renderLogsAdminTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Administration of system logs.
        </Tooltip>
    );

    const renderLoginTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Login page
        </Tooltip>
    );

    const renderRegisterTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Register page
        </Tooltip>
    );

    const renderDownloadsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Page with download links to datasets
        </Tooltip>
    );

    return (<div className="Header">
            <div className="row">
                <div className="col-sm-12 p-5 mb-4 bg-light rounded-3 jumbotron blue-grey lighten-5">
                    <h1 className="text-center title">
                        Cyber Security Learning Environment (CSLE)
                        <img src={CsleSmallLogo} alt="CSLE logo" className="img-fluid csleLogo" height="190px" width="130px" />
                    </h1>

                    <ul className="nav nav-tabs justify-content-center navtabsheader navbar-expand">
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderRegisterTooltip()}>
                                <NavLink className="nav-link navtablabel largeFont" to={"register-page"}>
                                    Register
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderLoginTooltip()}>
                                <NavLink className="nav-link navtablabel largeFont" to={"login-page"}>
                                    Login
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderAboutTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"about-page"}>
                                    About
                                </NavLink>
                            </OverlayTrigger>
                        </li>

                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderDownloadsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={"downloads-page"}>
                                    Downloads
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item dropdown navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderManagementTooltip}>
                                <a className={"nav-link dropdown-toggle navtablabel largeFont "
                                    + (managementDropdownRoutes.includes(location.pathname) ? 'active' : 'notActive')}
                                   data-toggle="dropdown"
                                   role="button" aria-haspopup="true" aria-expanded="false"
                                   id="navbarDropdown"
                                >
                                    Management</a>
                            </OverlayTrigger>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderEmulationsTooltip}
                                    data-toggle="tab">
                                    <NavLink className="dropdown-item" to={"emulations-page"} data-toggle="tab">
                                        Emulations
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSimulationsTooltip}>
                                    <NavLink className="dropdown-item" to={"simulations-page"}>
                                        Simulations
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderMonitoringTooltip}>
                                    <NavLink className="dropdown-item" to={"monitoring-page"}>
                                        Monitoring
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderTracesTooltip}>
                                    <NavLink className="dropdown-item" to={"traces-page"}>
                                        Traces
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderEmulationStatisticsTooltip}>
                                    <NavLink className="dropdown-item" to={"emulation-statistics-page"}>
                                        Statistics
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSystemModelsTooltip}>
                                    <NavLink className="dropdown-item" to={"system-models-page"}>
                                        System Models
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderPolicyExaminationTooltip}>
                                    <NavLink className="dropdown-item" to={"policy-examination-page"}>
                                        Policy Examination
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderContainerImagesTooltip}>
                                    <NavLink className="dropdown-item" to={"images-page"}>
                                        Container Images
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderTrainingResultsTooltip}>
                                    <NavLink className="dropdown-item" to={"training-page"}>
                                        Training Results
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderPoliciesTooltip}>
                                    <NavLink className="dropdown-item" to={"policies-page"}>
                                        Policies
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderJobsTooltip}>
                                    <NavLink className="dropdown-item" to={"jobs-page"}>
                                        Jobs
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSdnControllersTooltip}>
                                    <NavLink className="dropdown-item" to={"sdn-controllers-page"}>
                                        SDN Controllers
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderControlPlaneTooltip}>
                                    <NavLink className="dropdown-item" to={"control-plane-page"}>
                                        Control Plane
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderHostTerminalTooltip}>
                                    <NavLink className="dropdown-item" to={"host-terminal-page"}>
                                        Host Terminal
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderContainerTerminalTooltip}>
                                    <NavLink className="dropdown-item" to={"container-terminal-page"}>
                                        Container Terminal
                                    </NavLink>
                                </OverlayTrigger>
                            </div>
                        </li>
                        <ActionsCellTracesDataset sessionData={props.sessionData} setSessionData={props.setSessionData}/>
                    </ul>
                </div>
            </div>
        </div>
    )
};

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
