import React, {useState, useEffect, useCallback} from 'react';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import './ServerCluster.css';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import getBoolStr from "../../Common/getBoolStr";
import SystemArch from './SystemArch.png'
import {HTTP_PREFIX, HTTP_REST_GET, LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM, SERVER_CLUSTER_RESOURCE} from "../../Common/constants";

/**
 *  Component representing the /server-cluster-page
 */
const ServerCluster = (props) => {
    const [loadingServerCluster, setLoadingServerCluster] = useState(true);
    const [serverCluster, setServerCluster] = useState([]);
    const [filteredServerCluster, setFilteredServerCluster] = useState([]);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchServerCluster = useCallback((path) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${SERVER_CLUSTER_RESOURCE}`
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
                console.log("RECEIVED")
                console.log(response)
                setLoadingServerCluster(false)
                setServerCluster(response.cluster_nodes)
                setFilteredServerCluster(response.cluster_nodes)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, navigate, props.sessionData.token, setSessionData]);


    const refresh = () => {
        setLoadingServerCluster(true)
        fetchServerCluster()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload server cluster configuration from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the server cluster.
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Server cluster of the CSLE installation
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        The management system of CSLE is a distributed system that consist of N >=1 physical servers connected through an IP network.
                        One of the servers is designated to be the "leader" and the other servers are "workers"
                        Workers can perform local management actions but not actions that affect the overall system state.
                        These actions are routed to the leader, which applies them sequentially to ensure
                        consistent updates to the system state.
                    </p>
                    <div className="text-center">
                        <img src={SystemArch} alt="ServerCluster" width="300" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SpinnerOrTable = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="table-responsive">
                    <Table bordered hover>
                        <thead>
                        <tr className="serverClusterTable">
                            <th>IP</th>
                            <th>CPU (Cores)</th>
                            <th>RAM (GB)</th>
                            <th>Leader</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.serverCluster.map((node, index) =>
                            <tr className="serverClusterTable" key={node.ip + "-" + index}>
                                <td>{node.ip}</td>
                                <td>-</td>
                                <td>-</td>
                                <td>{getBoolStr(node.leader)}</td>
                                <td>-</td>
                            </tr>
                        )}
                        </tbody>
                    </Table>
                </div>
            )
        }
    }

    const searchFilter = (node, searchVal) => {
        return (searchVal === "" ||
            node.ip.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fServerCluster = serverCluster.filter(node => {
            return searchFilter(node, searchVal)
        });
        console.log("Setting filtered server cluster")
        console.log(fServerCluster)
        setFilteredServerCluster(fServerCluster)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    useEffect(() => {
        setLoadingServerCluster(true)
        fetchServerCluster()
    }, [fetchServerCluster]);

    return (
        <div className="ServerCluster">
            <h3 className="managementTitle"> Server Cluster Configuration </h3>
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Physical servers
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshTooltip}
                        >
                            <Button variant="button" onClick={refresh}>
                                <i className="fa fa-refresh refreshButton3" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderInfoTooltip}
                            className="overLayInfo"
                        >
                            <Button variant="button" onClick={() => setShowInfoModal(true)} className="infoButton3">
                                <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <SpinnerOrTable serverCluster={filteredServerCluster} loading={loadingServerCluster}/>
        </div>
    );
}

ServerCluster.propTypes = {};
ServerCluster.defaultProps = {};
export default ServerCluster;