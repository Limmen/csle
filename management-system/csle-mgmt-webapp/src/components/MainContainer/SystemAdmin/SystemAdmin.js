import React, {useState, useEffect, useCallback} from 'react';
import './SystemAdmin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory from 'react-bootstrap-table2-editor';
import { Type } from 'react-bootstrap-table2-editor';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {HTTP_PREFIX, HTTP_REST_GET, HTTP_REST_PUT, CONFIG_RESOURCE,
    TOKEN_QUERY_PARAM, LOGIN_PAGE_RESOURCE} from "../../Common/constants";


/**
 * Component representing the /system-admin-page
 */
const SystemAdmin = (props) => {
    const [parametersConfig, setParametersConfig] = useState([]);
    const [clusterConfig, setClusterConfig] = useState([]);
    const [loading, setLoading] = useState(true);
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const parameterConfigColumns = [
        {
            dataField: 'param',
            text: 'Parameter'
        },
        {
            dataField: 'value',
            text: 'Value'
        }
    ];

    const clusterConfigColumns = [
        {
            dataField: 'ip',
            text: 'IP'
        },
        {
            dataField: 'leader',
            text: 'Leader',
            editor: {
                type: Type.SELECT,
                options: [{
                    value: 'true',
                    label: 'true'
                }, {
                    value: 'false',
                    label: 'false'
                }
                ]
            }
        }
    ];

    const fetchConfig = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CONFIG_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                setParametersConfig(response.parameters)
                setClusterConfig(response.cluster_config.cluster_nodes)
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, [ip, alert, navigate, port, props.sessionData.token, setSessionData]);

    const refresh = useCallback(() => {
        setLoading(true)
        fetchConfig()
    }, [fetchConfig])

    const updateConfig = useCallback((config) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${CONFIG_RESOURCE}`
            + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_PUT,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({config: config})
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                if(res.status === 400) {
                    alert.show("Invalid request, could not update configuration")
                    return null
                }
                return res.json()
            })
            .then(response => {
                refresh()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, alert, navigate, port, refresh, props.sessionData.token, setSessionData]);


    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulations from the backend
        </Tooltip>
    );

    const ConfigTableOrSpinner = (props) => {
        if (!props.loading && props.config.length === 0) {
            return (
                <div>
                    <span className="emptyText">No configuration is available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching configuration... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="configTable">
                    <BootstrapTable
                        keyField="id"
                        data={ props.config }
                        columns={ parameterConfigColumns }
                        cellEdit={ cellEditFactory({ mode: 'click' }) }
                    />
                </div>
            )
        }
    }


    const ClusterConfigTableOrSpinner = (props) => {
        if (!props.loading && props.config.length === 0) {
            return (
                <div>
                    <span className="emptyText">No cluster configuration is available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching configuration... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="configTable">
                    <BootstrapTable
                        keyField="id"
                        data={ props.config }
                        columns={ clusterConfigColumns }
                        cellEdit={ cellEditFactory({ mode: 'click' }) }
                    />
                </div>
            )
        }
    }

    const saveConfig = () => {
        var clusterConfigObj = {
            "cluster_nodes" : clusterConfig
        }
        var configObj = {}
        configObj["cluster_config"] = clusterConfigObj
        configObj["parameters"] = parametersConfig
        updateConfig(configObj)
    }

    useEffect(() => {
        setLoading(true);
        fetchConfig()
    }, [fetchConfig]);

    return (
        <div className="Admin">
            <h3> System Configuration (click in a cell to edit, press enter to save)
                <button type="submit" className="btn btn-primary btn-sm saveUsersBtn" onClick={saveConfig}>
                    Save
                </button>
            </h3>
            <div className="row">
                <div className="col-sm-1"></div>
                <div className="col-sm-10">
                    <ConfigTableOrSpinner config={parametersConfig} loading={loading} />
                </div>
                <div className="col-sm-1"></div>
            </div>

            <h3> Cluster Configuration (click in a cell to edit, press enter to save)
                <button type="submit" className="btn btn-primary btn-sm saveUsersBtn" onClick={saveConfig}>
                    Save
                </button>
            </h3>
            <div className="row">
                <div className="col-sm-1"></div>
                <div className="col-sm-10">
                    <ClusterConfigTableOrSpinner config={clusterConfig} loading={loading} />
                </div>
                <div className="col-sm-1"></div>
            </div>
        </div>
    );
}

SystemAdmin.propTypes = {};
SystemAdmin.defaultProps = {};
export default SystemAdmin;
