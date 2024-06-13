import React, {useState, useEffect, useCallback} from 'react';
import './Downloads.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import InputGroup from 'react-bootstrap/InputGroup';
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import fileDownload from 'react-file-download'
import {useAlert} from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {HTTP_PREFIX, HTTP_REST_DELETE, HTTP_REST_GET, LOGIN_PAGE_RESOURCE,
    STATISTICS_DATASETS_RESOURCE, TRACES_DATASETS_RESOURCE, TOKEN_QUERY_PARAM} from "../../Common/constants";

/**
 *  Component representing the /downloads-page
 */
const Downloads = (props) => {
    const [showTracesDatasetsInfoModal, setShowTracesDatasetsInfoModal] = useState(false);
    const [showTracesDatasetInfoModal, setShowTracesDatasetInfoModal] = useState(false);
    const [modalSelectedTracesDataset, setModalSelectedTracesDataset] = useState(null);
    const [tracesDatasets, setTracesDatasets] = useState([]);
    const [filteredTracesDatasets, setFilteredTracesDatasets] = useState([]);
    const [loadingTracesDatasets, setLoadingTracesDatasets] = useState(true);
    const [showStatisticsDatasetsInfoModal, setShowStatisticsDatasetsInfoModal] = useState(false);
    const [showStatisticsDatasetInfoModal, setShowStatisticsDatasetInfoModal] = useState(false);
    const [modalSelectedStatisticsDataset, setModalSelectedStatisticsDataset] = useState(null);
    const [statisticsDatasets, setStatisticsDatasets] = useState([]);
    const [filteredStatisticsDatasets, setFilteredStatisticsDatasets] = useState([]);
    const [loadingStatisticsDatasets, setLoadingStatisticsDatasets] = useState(true);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchTracesDatasets = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRACES_DATASETS_RESOURCE}`,
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
                setTracesDatasets(response);
                setFilteredTracesDatasets(response);
                setLoadingTracesDatasets(false)
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port]);


    const removeAllTracesDatasetsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRACES_DATASETS_RESOURCE}?${TOKEN_QUERY_PARAM}=`
                +`${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchTracesDatasets()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, fetchTracesDatasets, setSessionData, alert]);

    const removeTracesDatasetRequest = useCallback((tracesDataset) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${TRACES_DATASETS_RESOURCE}/${tracesDataset.id}?`
                +`${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchTracesDatasets()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, fetchTracesDatasets, setSessionData, alert]);


    const refreshTracesDatasets = () => {
        setLoadingTracesDatasets(true)
        fetchTracesDatasets()
    }

    const removeAllTracesDatasets = () => {
        setLoadingTracesDatasets(true)
        removeAllTracesDatasetsRequest()
    }

    const removeTracesDataset = (tracesDataset) => {
        setLoadingTracesDatasets(true)
        removeTracesDatasetRequest(tracesDataset)
    }

    const renderRefreshTracesDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload traces datasets from the backend
        </Tooltip>
    );

    const renderInfoTracesDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the traces datasets.
        </Tooltip>
    );

    const InfoModalTracesDatasets = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Traces datasets
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Traces datasets contain sequences of measurements from a security scenario playing out in
                        an emulated IT infrastructure. A sequence contains a set of time-steps. Each time-step in the
                        sequence
                        includes various measurements, e.g. attacker actions, defender actions, system metrics, and log
                        files.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const InfoModalTracesDataset = (props) => {
        if(props.tracesDataset === null || props.tracesDataset === undefined) {
            return (<Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        .
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>)
        }
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        {props.tracesDataset.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="table-responsive">
                        <Table bordered hover>
                            <thead>
                            <tr className="tracesDatasetsTable">
                                <th>
                                    Attribute
                                </th>
                                <th>
                                    Value
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Download link</td>
                                <td>
                                    <a href={"/traces-datasets/" + props.tracesDataset.id + "?download=true"}
                                       download>
                                        {props.tracesDataset.name}.{props.tracesDataset.file_format}
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td>Download count</td>
                                <td>{props.tracesDataset.download_count}</td>
                            </tr>
                            <tr>
                                <td>File format</td>
                                <FileFormatCellDatasetTrace tracesDataset={props.tracesDataset}/>
                            </tr>
                            <tr>
                                <td>Number of traces</td>
                                <td>{props.tracesDataset.num_traces}</td>
                            </tr>
                            <tr>
                                <td>Number of files</td>
                                <td>{props.tracesDataset.num_files}</td>
                            </tr>
                            <tr>
                                <td>Size (GB)</td>
                                <td>
                                    Uncompressed: {props.tracesDataset.size_in_gb},
                                    compressed: {props.tracesDataset.compressed_size_in_gb}
                                </td>
                            </tr>
                            <tr>
                                <td>Date added</td>
                                <td>
                                    {props.tracesDataset.date_added}
                                </td>
                            </tr>
                            <tr>
                                <td>Description</td>
                                <td>
                                    {props.tracesDataset.description}
                                </td>
                            </tr>
                            <tr>
                                <td>Citation</td>
                                <td>{props.tracesDataset.citation}</td>
                            </tr>
                            <tr>
                                <td>Added by</td>
                                <td>{props.tracesDataset.added_by}</td>
                            </tr>
                            </tbody>
                        </Table>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const removeAllTracesDatasetsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all traces datasets? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllTracesDatasets()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all traces datasets? this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllTracesDatasets()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeTracesDatasetConfirm = (tracesDataset) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the trace dataset with name' + tracesDataset.name + "? this action " +
                "cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeTracesDataset(tracesDataset)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the trace dataset {tracesDataset.name}? this action
                                    cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeTracesDataset(tracesDataset)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const renderRemoveAllTracesDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all traces datasets.
        </Tooltip>
    );

    const ActionsCellTracesDataset = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <td>
                    <Button variant="button" onClick={() => {
                        setModalSelectedTracesDataset(props.tracesDataset)
                        setShowTracesDatasetInfoModal(true)
                    }
                    }
                            className="infoButton3">
                        <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                    </Button>
                    <InfoModalTracesDataset show={showTracesDatasetInfoModal}
                                            onHide={() => setShowTracesDatasetInfoModal(false)}
                                            tracesDataset={modalSelectedTracesDataset}
                    />
                    <Button variant="danger"
                            onClick={() => removeTracesDatasetConfirm(props.tracesDataset)} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </td>)
        } else {
            return (<td>
                <Button variant="button" onClick={() => {
                    setModalSelectedTracesDataset(props.tracesDataset)
                    setShowTracesDatasetInfoModal(true)
                }
                }
                        className="infoButton3">
                    <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                </Button>
                <InfoModalTracesDataset show={showTracesDatasetInfoModal}
                                        onHide={() => setShowTracesDatasetInfoModal(false)}
                                        tracesDataset={modalSelectedTracesDataset}
                />
            </td>)
        }
    }

    const FileFormatCellDatasetTrace = (props) => {
        if (props.tracesDataset.file_format === "json") {
            return (
                <td>
                    {props.tracesDataset.file_format},
                    <Button className="downloadLink" variant="link"
                            onClick={() => fileDownload(JSON.stringify(props.tracesDataset.data_schema), "schema.json")}>
                        schema.json
                    </Button>
                </td>
            )
        } else {
            return (
                <td>
                    {props.tracesDataset.file_format}, columns: {props.tracesDataset.columns}
                </td>
            )
        }
    }

    const DeleteAllTracesDatasetsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllTracesDatasetsTooltip}
                >
                    <Button variant="danger" onClick={removeAllTracesDatasetsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }


    const SpinnerOrTracesDatasetsTable = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            if (props.tracesDatasets === null || props.tracesDatasets === undefined || props.tracesDatasets.length === 0) {
                return (
                    <p className="downloadLink"> No traces datasets are available</p>
                )
            } else {
                return (
                    <div className="table-responsive">
                        <Table bordered hover>
                            <thead>
                            <tr className="tracesDatasetsTable">
                                <th>Download Link</th>
                                <th>Download count</th>
                                <th>Number of traces</th>
                                <th>Size (GB)</th>
                                <th>Date added</th>
                                <th></th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.tracesDatasets.map((tracesDataset, index) =>
                                <tr className="tracesDatasetsTable" key={tracesDataset.id + "-" + index}>
                                    <td>
                                        <a href={"/traces-datasets/" + tracesDataset.id + "?download=true"}
                                           download>
                                            {tracesDataset.name}.{tracesDataset.file_format}
                                        </a>
                                    </td>
                                    <td>{tracesDataset.download_count}</td>
                                    <td>{tracesDataset.num_traces}</td>
                                    <td>Uncompressed: {tracesDataset.size_in_gb},
                                        compressed: {tracesDataset.compressed_size_in_gb}</td>
                                    <td>{tracesDataset.date_added}</td>
                                    <ActionsCellTracesDataset
                                        sessionData={props.sessionData}
                                        tracesDataset={tracesDataset}
                                        className={"actionsTracesDataset-" + index + "-" + tracesDataset.id}
                                    />
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                )
            }
        }
    }

    const searchFilterTracesDatasets = (tracesDataset, searchVal) => {
        return (searchVal === "" ||
            tracesDataset.name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChangeTracesDatasets = (event) => {
        var searchVal = event.target.value
        const fTracesDatasets = tracesDatasets.filter(tracesDataset => {
            return searchFilterTracesDatasets(tracesDataset, searchVal)
        });
        setFilteredTracesDatasets(fTracesDatasets)
    }

    const searchHandlerTracesDatasets = useDebouncedCallback(
        (event) => {
            searchChangeTracesDatasets(event)
        },
        350
    );

    const fetchStatisticsDatasets = useCallback(() => {
        fetch(
            `http://` + ip + ':' + port + '/statistics-datasets',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                return res.json()
            })
            .then(response => {
                setStatisticsDatasets(response);
                setFilteredStatisticsDatasets(response);
                setLoadingStatisticsDatasets(false)
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port]);


    const removeAllStatisticsDatasetsRequest = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${STATISTICS_DATASETS_RESOURCE}?`
                + `${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchStatisticsDatasets()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, setSessionData, fetchStatisticsDatasets]);

    const removeStatisticsDatasetRequest = useCallback((statisticsDataset) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${STATISTICS_DATASETS_RESOURCE}/${statisticsDataset.id}`
                + `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchStatisticsDatasets()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, setSessionData, fetchStatisticsDatasets]);


    const refreshStatisticsDatasets = () => {
        setLoadingStatisticsDatasets(true)
        fetchStatisticsDatasets()
    }

    const removeAllStatisticsDatasets = () => {
        setLoadingStatisticsDatasets(true)
        removeAllStatisticsDatasetsRequest()
    }

    const removeStatisticsDataset = (statisticsDataset) => {
        setLoadingStatisticsDatasets(true)
        removeStatisticsDatasetRequest(statisticsDataset)
    }

    const renderRefreshStatisticsDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload statistics datasets from the backend
        </Tooltip>
    );

    const renderInfoStatisticsDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the statistics datasets.
        </Tooltip>
    );

    const InfoModalStatisticsDatasets = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Statistics datasets
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Statistics datasets contain average statistics from running a large number of security
                        scenarios an emulated IT infrastructure and measuring the various parameters.
                    </p>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const removeAllStatisticsDatasetsConfirm = () => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete all statistics datasets? this action cannot be undone',
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeAllStatisticsDatasets()
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete all statistics datasets? this action cannot be
                                    undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeAllStatisticsDatasets()
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete them.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const removeStatisticsDatasetConfirm = (statisticsDataset) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the statistics dataset with name' + statisticsDataset.name + "? this action " +
                "cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeStatisticsDataset(statisticsDataset)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the statistics dataset {statisticsDataset.name}?
                                    this action
                                    cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeStatisticsDataset(statisticsDataset)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const renderRemoveAllStatisticsDatasetsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all statistics datasets.
        </Tooltip>
    );

    const DeleteAllStatisticsDatasetsOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAllStatisticsDatasetsTooltip}
                >
                    <Button variant="danger" onClick={removeAllStatisticsDatasetsConfirm} size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const InfoModalStatisticsDataset = (props) => {
        if(props.statisticsDataset === null || props.statisticsDataset === undefined) {
            return (<Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        .
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>)
        }
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        {props.statisticsDataset.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="table-responsive">
                        <Table bordered hover>
                            <thead>
                            <tr className="statisticsDatasetsTable">
                                <th>
                                    Attribute
                                </th>
                                <th>
                                    Value
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Download link</td>
                                <td>
                                    <a href={"/statistics-datasets/" + props.statisticsDataset.id + "?download=true"}
                                       download>
                                        {props.statisticsDataset.name}.{props.statisticsDataset.file_format}
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td>Download count</td>
                                <td>{props.statisticsDataset.download_count}</td>
                            </tr>
                            <tr>
                                <td>File format</td>
                                <td>{props.statisticsDataset.file_format}</td>
                            </tr>
                            <tr>
                                <td>Number of measurements</td>
                                <td>{props.statisticsDataset.num_measurements}</td>
                            </tr>
                            <tr>
                                <td>Number of metrics</td>
                                <td>{props.statisticsDataset.num_metrics}</td>
                            </tr>
                            <tr>
                                <td>Number of conditions</td>
                                <td>{props.statisticsDataset.num_conditions}</td>
                            </tr>
                            <tr>
                                <td>Number of files</td>
                                <td>{props.statisticsDataset.num_files}</td>
                            </tr>
                            <tr>
                                <td>Size (GB)</td>
                                <td>
                                    Uncompressed: {props.statisticsDataset.size_in_gb},
                                    compressed: {props.statisticsDataset.compressed_size_in_gb}
                                </td>
                            </tr>
                            <tr>
                                <td>Date added</td>
                                <td>
                                    {props.statisticsDataset.date_added}
                                </td>
                            </tr>
                            <tr>
                                <td>Description</td>
                                <td>
                                    {props.statisticsDataset.description}
                                </td>
                            </tr>
                            <tr>
                                <td>Citation</td>
                                <td>{props.statisticsDataset.citation}</td>
                            </tr>
                            <tr>
                                <td>Added by</td>
                                <td>{props.statisticsDataset.added_by}</td>
                            </tr>
                            <tr>
                                <td>Metrics</td>
                                <td>{props.statisticsDataset.metrics}</td>
                            </tr>
                            <tr>
                                <td>Conditions</td>
                                <td>{props.statisticsDataset.conditions}</td>
                            </tr>
                            </tbody>
                        </Table>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const ActionsCellStatisticsDataset = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <td>
                    <Button variant="button" onClick={() => {
                        setModalSelectedStatisticsDataset(props.statisticsDataset)
                        setShowStatisticsDatasetInfoModal(true)
                    }}
                            className="infoButton3">
                        <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                    </Button>
                    <InfoModalStatisticsDataset show={showStatisticsDatasetInfoModal}
                                                onHide={() => setShowStatisticsDatasetInfoModal(false)}
                                                statisticsDataset={modalSelectedStatisticsDataset}
                    />
                    <Button variant="danger"
                            onClick={() => removeStatisticsDatasetConfirm(props.statisticsDataset)}
                            size="sm">
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </td>)
        } else {
            return (<td>
                <Button variant="button" onClick={() => {
                    setModalSelectedStatisticsDataset(props.statisticsDataset)
                    setShowStatisticsDatasetInfoModal(true)
                }}
                        className="infoButton3">
                    <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                </Button>
                <InfoModalStatisticsDataset show={showStatisticsDatasetInfoModal}
                                            onHide={() => setShowStatisticsDatasetInfoModal(false)}
                                            statisticsDataset={modalSelectedStatisticsDataset}
                />
            </td>)
        }
    }


    const SpinnerOrStatisticsDatasetsTable = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"/>
                </Spinner>)
        } else {
            if (props.statisticsDatasets === null || props.statisticsDatasets === undefined || props.statisticsDatasets.length === 0) {
                return (
                    <p className="downloadLink"> No statistics datasets are available</p>
                )
            } else {
                return (
                    <div className="table-responsive">
                        <Table bordered hover>
                            <thead>
                            <tr className="statisticsDatasetsTable">
                                <th>Download Link</th>
                                <th>Download count</th>
                                <th>Counts</th>
                                <th>Size (GB)</th>
                                <th>Date added</th>
                                <th/>
                            </tr>
                            </thead>
                            <tbody>
                            {props.statisticsDatasets.map((statisticsDataset, index) =>
                                <tr className="statisticsDatasetsTable" key={statisticsDataset.id + "-" + index}>
                                    <td>
                                        <a href={"/statistics-datasets/" + statisticsDataset.id + "?download=true"}
                                           download>
                                            {statisticsDataset.name}.{statisticsDataset.file_format}
                                        </a>
                                    </td>
                                    <td>{statisticsDataset.download_count}</td>
                                    <td>
                                        Measurements: {statisticsDataset.num_measurements},
                                        Metrics: {statisticsDataset.num_metrics},
                                        Conditions: {statisticsDataset.num_conditions},
                                        Files: {statisticsDataset.num_files}
                                    </td>
                                    <td>Uncompressed: {statisticsDataset.size_in_gb},
                                        compressed: {statisticsDataset.compressed_size_in_gb}</td>
                                    <td>{statisticsDataset.date_added}</td>
                                    <ActionsCellStatisticsDataset sessionData={props.sessionData}
                                                              statisticsDataset={statisticsDataset}/>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                )
            }
        }
    }

    const searchFilterStatisticsDatasets = (statisticsDataset, searchVal) => {
        return (searchVal === "" ||
            statisticsDataset.name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChangeStatisticsDatasets = (event) => {
        var searchVal = event.target.value
        const fStatisticsDatasets = statisticsDatasets.filter(statisticsDataset => {
            return searchFilterStatisticsDatasets(statisticsDataset, searchVal)
        });
        setFilteredStatisticsDatasets(fStatisticsDatasets)
    }

    const searchHandlerStatisticsDatasets = useDebouncedCallback(
        (event) => {
            searchChangeStatisticsDatasets(event)
        },
        350
    );

    useEffect(() => {
        setLoadingTracesDatasets(true);
        fetchTracesDatasets()
        setLoadingStatisticsDatasets(true);
        fetchStatisticsDatasets()
    }, [fetchTracesDatasets, fetchStatisticsDatasets]);

    return (
        <div className="Downloads">
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Traces datasets
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshTracesDatasetsTooltip}
                        >
                            <Button variant="button" onClick={refreshTracesDatasets}>
                                <i className="fa fa-refresh refreshButton3" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderInfoTracesDatasetsTooltip}
                            className="overLayInfo"
                        >
                            <Button variant="button" onClick={() => setShowTracesDatasetsInfoModal(true)}
                                    className="infoButton3">
                                <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModalTracesDatasets show={showTracesDatasetsInfoModal}
                                                 onHide={() => setShowTracesDatasetsInfoModal(false)}/>
                        <DeleteAllTracesDatasetsOrEmpty sessionData={props.sessionData}/>
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
                                onChange={searchHandlerTracesDatasets}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <SpinnerOrTracesDatasetsTable tracesDatasets={filteredTracesDatasets} loading={loadingTracesDatasets}
                                          sessionData={props.sessionData}
            />


            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Statistics datasets
                        <OverlayTrigger
                            placement="right"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshStatisticsDatasetsTooltip}
                        >
                            <Button variant="button" onClick={refreshStatisticsDatasets}>
                                <i className="fa fa-refresh refreshButton3" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderInfoStatisticsDatasetsTooltip}
                            className="overLayInfo"
                        >
                            <Button variant="button" onClick={() => setShowStatisticsDatasetsInfoModal(true)}
                                    className="infoButton3">
                                <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModalStatisticsDatasets show={showStatisticsDatasetsInfoModal}
                                                     onHide={() => setShowStatisticsDatasetsInfoModal(false)}/>
                        <DeleteAllStatisticsDatasetsOrEmpty sessionData={props.sessionData}/>
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
                                onChange={searchHandlerStatisticsDatasets}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2"></div>
            </div>

            <SpinnerOrStatisticsDatasetsTable statisticsDatasets={filteredStatisticsDatasets}
                                              loading={loadingStatisticsDatasets}
                                              sessionData={props.sessionData}/>
        </div>
    );
}

Downloads.propTypes = {};
Downloads.defaultProps = {};
export default Downloads;