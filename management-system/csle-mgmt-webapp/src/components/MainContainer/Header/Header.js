import React, {useState, useEffect, useCallback} from 'react';
import './Header.css';
import {NavLink, useLocation} from "react-router-dom";
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import CsleSmallLogo from './CsleSmallLogo.png'
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    ABOUT_PAGE_RESOURCE,
    CONTAINER_TERMINAL_PAGE_RESOURCE,
    CONTROL_PLANE_PAGE_RESOURCE,
    EMULATION_STATISTICS_PAGE_RESOURCE,
    EMULATIONS_PAGE_RESOURCE,
    IMAGES_PAGE_RESOURCE,
    JOBS_PAGE_RESOURCE,
    LOGS_ADMIN_PAGE_RESOURCE,
    MONITORING_PAGE_RESOURCE,
    POLICIES_PAGE_RESOURCE,
    POLICY_EXAMINATION_PAGE_RESOURCE,
    SDN_CONTROLLERS_PAGE_RESOURCE,
    SIMULATIONS_PAGE_RESOURCE,
    SYSTEM_ADMIN_PAGE_RESOURCE,
    SYSTEM_MODELS_PAGE_RESOURCE,
    TRACES_PAGE_RESOURCE,
    TRAINING_PAGE_RESOURCE,
    USER_ADMIN_PAGE_RESOURCE,
    REGISTER_PAGE_RESOURCE,
    LOGIN_PAGE_RESOURCE,
    DOWNLOADS_PAGE_RESOURCE,
    VERSION_RESOURCE,
    SERVER_CLUSTER_PAGE_RESOURCE,
    CREATE_EMULATION_PAGE_RESOURCE,
    HTTP_PREFIX, HTTP_REST_GET, CONFIG_RESOURCE,
    REGISTRATION_ALLOWED_SUBRESOURCE, REGISTRATION_ALLOWED_PROPERTY
} from "../../Common/constants";

/**
 * The header component that is present on every page
 */
const Header = (props) => {
    const [version, setVersion] = useState("0.0.1");
    const [registerAllowed, setRegisterAllowed] = useState(false);
    const ip = serverIp
    const port = serverPort
    const location = useLocation();
    const managementDropdownRoutes = [`/${SIMULATIONS_PAGE_RESOURCE}`, `/${EMULATIONS_PAGE_RESOURCE}`,
        `/${MONITORING_PAGE_RESOURCE}`, `/${TRACES_PAGE_RESOURCE}`,
        `/${EMULATION_STATISTICS_PAGE_RESOURCE}`, `/${SYSTEM_MODELS_PAGE_RESOURCE}`,
        `/${POLICY_EXAMINATION_PAGE_RESOURCE}`, `/${IMAGES_PAGE_RESOURCE}`,
        `/${TRAINING_PAGE_RESOURCE}`, `/${POLICIES_PAGE_RESOURCE}`, `/${JOBS_PAGE_RESOURCE}`,
        `/${SDN_CONTROLLERS_PAGE_RESOURCE}`, `/${CONTROL_PLANE_PAGE_RESOURCE}`,
        `/${CONTAINER_TERMINAL_PAGE_RESOURCE}`, `/${CREATE_EMULATION_PAGE_RESOURCE}`]
    const adminDropdownRoutes = [`/${USER_ADMIN_PAGE_RESOURCE}`, `/${SYSTEM_ADMIN_PAGE_RESOURCE}`,
        `/${LOGS_ADMIN_PAGE_RESOURCE}`]


    const fetchVersion = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${VERSION_RESOURCE}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                return res.json()
            })
            .then(response => {
                setVersion(response.version)
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port]);

    const fetchRegistrationAllowed = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CONFIG_RESOURCE}/${REGISTRATION_ALLOWED_SUBRESOURCE}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                return res.json()
            })
            .then(response => {
                if(response !== null && response !== undefined) {
                    setRegisterAllowed(response[REGISTRATION_ALLOWED_PROPERTY])
                }
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port]);


    useEffect(() => {
        fetchVersion()
        fetchRegistrationAllowed()
    }, [fetchVersion, fetchRegistrationAllowed]);

    const AdministrationDropDown = (props) => {
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
                            Administration <i className="fa fa-user headerIcon" aria-hidden="true"></i>
                        </a>
                    </OverlayTrigger>
                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderUserAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={USER_ADMIN_PAGE_RESOURCE} data-toggle="tab">
                                User administration <i className="fa fa-user headerIcon" aria-hidden="true"></i>
                            </NavLink>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderSystemAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={SYSTEM_ADMIN_PAGE_RESOURCE} data-toggle="tab">
                                System administration <i className="fa fa-linux headerIcon" aria-hidden="true"></i>
                            </NavLink>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderLogsAdminTooltip}
                            data-toggle="tab">
                            <NavLink className="dropdown-item" to={LOGS_ADMIN_PAGE_RESOURCE} data-toggle="tab">
                                Logs administration <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </NavLink>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderServerClusterTooltip}>
                            <NavLink className="dropdown-item" to={SERVER_CLUSTER_PAGE_RESOURCE}>
                                Cluster administration <i className="fa fa-server headerIcon" aria-hidden="true"></i>
                            </NavLink>
                        </OverlayTrigger>
                    </div>
                </li>
            )
        } else {
            return (<></>)
        }
    }

    const ContainerTerminalPageLinkOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={props.renderContainerTerminalTooltip}>
                    <NavLink className="dropdown-item" to={CONTAINER_TERMINAL_PAGE_RESOURCE}>
                        Container Terminal <i className="fa fa-terminal headerIcon" aria-hidden="true"></i>
                    </NavLink>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const RegisterPageOrEmpty = (props) => {
        if (props.registerAllowed) {
            return (
                <li className="nav-item navtabheader">
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={props.renderRegisterTooltip}>
                        <NavLink className="nav-link navtablabel largeFont" to={REGISTER_PAGE_RESOURCE}>
                            Register
                            <i className="fa fa-user headerIcon" aria-hidden="true"></i>
                        </NavLink>
                    </OverlayTrigger>
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

    const renderCreateEmulationTooltip = (props) => (
      <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
          Creation of new emulations
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

    const renderServerClusterTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Page with server cluster information.
        </Tooltip>
    );

    return (<div className="Header">
            <div className="row">
                <div className="col-sm-12 p-5 mb-4 bg-light rounded-3 jumbotron blue-grey lighten-5">
                    <h1 className="text-center title">
                        Cyber Security Learning Environment (CSLE)
                        <img src={CsleSmallLogo} alt="CSLE logo" className="img-fluid csleLogo" height="190px"
                             width="130px" />
                    </h1>
                    <span className="csleVersion">Version: {version}</span>

                    <ul className="nav nav-tabs justify-content-center navtabsheader navbar-expand">
                        <RegisterPageOrEmpty renderRegisterTooltip={renderRegisterTooltip}
                                             registerAllowed={registerAllowed}/>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderLoginTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={LOGIN_PAGE_RESOURCE}>
                                    Login <i className="fa fa-sign-in headerIcon" aria-hidden="true"></i>
                                </NavLink>
                            </OverlayTrigger>
                        </li>
                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderAboutTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={ABOUT_PAGE_RESOURCE}>
                                    About
                                    <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                                </NavLink>
                            </OverlayTrigger>
                        </li>

                        <li className="nav-item navtabheader">
                            <OverlayTrigger
                                placement="top"
                                delay={{show: 0, hide: 0}}
                                overlay={renderDownloadsTooltip}>
                                <NavLink className="nav-link navtablabel largeFont" to={DOWNLOADS_PAGE_RESOURCE}>
                                    Downloads <i className="fa fa-download headerIcon" aria-hidden="true"></i>
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
                                    Management <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                                </a>
                            </OverlayTrigger>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderEmulationsTooltip}
                                    data-toggle="tab">
                                    <NavLink className="dropdown-item" to={EMULATIONS_PAGE_RESOURCE} data-toggle="tab">
                                        Emulations <i className="fa fa-linux headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSimulationsTooltip}>
                                    <NavLink className="dropdown-item" to={SIMULATIONS_PAGE_RESOURCE}>
                                        Simulations <i className="fa fa-code headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderMonitoringTooltip}>
                                    <NavLink className="dropdown-item" to={MONITORING_PAGE_RESOURCE}>
                                        Monitoring <i className="fa fa-area-chart headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderTracesTooltip}>
                                    <NavLink className="dropdown-item" to={TRACES_PAGE_RESOURCE}>
                                        Traces <i className="fa fa-database headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderEmulationStatisticsTooltip}>
                                    <NavLink className="dropdown-item" to={EMULATION_STATISTICS_PAGE_RESOURCE}>
                                        Statistics <i className="fa fa-pie-chart headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSystemModelsTooltip}>
                                    <NavLink className="dropdown-item" to={SYSTEM_MODELS_PAGE_RESOURCE}>
                                        System Models <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderPolicyExaminationTooltip}>
                                    <NavLink className="dropdown-item" to={POLICY_EXAMINATION_PAGE_RESOURCE}>
                                        Policy Examination <i className="fa fa-search headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderContainerImagesTooltip}>
                                    <NavLink className="dropdown-item" to={IMAGES_PAGE_RESOURCE}>
                                        Container Images <i className="fa fa-cubes headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderTrainingResultsTooltip}>
                                    <NavLink className="dropdown-item" to={TRAINING_PAGE_RESOURCE}>
                                        Training Results
                                        <i className="fa fa-line-chart headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderPoliciesTooltip}>
                                    <NavLink className="dropdown-item" to={POLICIES_PAGE_RESOURCE}>
                                        Policies <i className="fa fa-lightbulb-o headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderJobsTooltip}>
                                    <NavLink className="dropdown-item" to={JOBS_PAGE_RESOURCE}>
                                        Jobs <i className="fa fa-play headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderSdnControllersTooltip}>
                                    <NavLink className="dropdown-item" to={SDN_CONTROLLERS_PAGE_RESOURCE}>
                                        SDN Controllers <i className="fa fa-podcast headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <OverlayTrigger
                                    placement="right"
                                    delay={{show: 0, hide: 0}}
                                    overlay={renderControlPlaneTooltip}>
                                    <NavLink className="dropdown-item" to={CONTROL_PLANE_PAGE_RESOURCE}>
                                        Control Plane <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>
                                <ContainerTerminalPageLinkOrEmpty
                                    renderContainerTerminalTooltip={renderContainerTerminalTooltip}
                                    sessionData={props.sessionData}
                                />
                                <OverlayTrigger
                                  placement="right"
                                  delay={{show: 0, hide: 0}}
                                  overlay={renderCreateEmulationTooltip}>
                                    <NavLink className="dropdown-item" to={CREATE_EMULATION_PAGE_RESOURCE}>
                                        Create emulation <i className="fa fa-plus headerIcon" aria-hidden="true"></i>
                                    </NavLink>
                                </OverlayTrigger>

                            </div>
                        </li>
                        <AdministrationDropDown sessionData={props.sessionData} setSessionData={props.setSessionData}/>
                    </ul>
                </div>
            </div>
        </div>
    )
};

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
