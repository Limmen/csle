import React, {useState, useEffect, useCallback} from 'react';
import './Downloads.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Accordion from 'react-bootstrap/Accordion';
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

const Downloads = (props) => {
    const [showTracesDatasetsInfoModal, setShowTracesDatasetsInfoModal] = useState(false);
    const [tracesDatasets, setTracesDatasets] = useState([]);
    const [filteredTracesDatasets, setFilteredTracesDatasets] = useState([]);
    const [searchStringTracesDatasets, setSearchStringTracesDatasets] = useState("");
    const [loadingTracesDatasets, setLoadingTracesDatasets] = useState(true);
    const ip = "localhost"
    const alert = useAlert();
    const navigate = useNavigate();

    const fetchTracesDatasets = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/traces-datasets',
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
                setTracesDatasets(response);
                setFilteredTracesDatasets(response);
                setLoadingTracesDatasets(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const removeAllTracesDatasetsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/traces-datasets' + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
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
    }, []);

    const removeTracesDatasetRequest = useCallback((tracesDataset) => {
        fetch(
            `http://` + ip + ':7777/traces-datasets/' + tracesDataset.id + "?token=" + props.sessionData.token,
            {
                method: "DELETE",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
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
    }, []);

    useEffect(() => {
        setLoadingTracesDatasets(true);
        fetchTracesDatasets()
    }, [fetchTracesDatasets]);


    const refreshTracesDatasets = () => {
        setLoadingTracesDatasets(true)
        fetchTracesDatasets()
    }

    const removeAllTracesDatasets = () => {
        setLoadingTracesDatasets(true)
        removeAllTracesDatasetsRequest()
    }

    const removeTraceDataset = (traceDataset) => {
        setLoadingTracesDatasets(true)
        removeTracesDatasetRequest(traceDataset)
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
                    <Modal.Title id="contained-modal-title-vcenter">
                        Traces datasets
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Traces datasets</h4>
                    <p className="modalText">
                        Traces datasets contain sequences of measurements from a security scenario playing out in
                        an emulated IT infrastructure. A sequence contains a set of time-steps. Each time-step in the
                        sequence
                        includes various measurements, e.g. attacker actions, defender actions, system metrics, and log
                        files.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
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

    const removeTracesDatasetConfirm = (traceDataset) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the trace dataset with name' + traceDataset.name + "? this action " +
                "cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeTraceDataset(traceDataset)
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
                                    Are you sure you want to delete the trace dataset {traceDataset.name}? this action
                                    cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeTraceDataset(traceDataset)
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
                    {props.tracesDataset.file_format}, columns: {props.tracesDatasets.columns}
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
                if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
                    return (
                        <div className="table-responsive">
                            <Table bordered hover>
                                <thead>
                                <tr className="tracesDatasetsTable">
                                    <th>Download Link</th>
                                    <th>Download count</th>
                                    <th>File format</th>
                                    <th>Number of traces</th>
                                    <th>Number of files</th>
                                    <th>Size (GB)</th>
                                    <th>Date added</th>
                                    <th>Description</th>
                                    <th>Citation</th>
                                    <th>Added by</th>
                                    <th></th>
                                </tr>
                                </thead>
                                <tbody>
                                {props.tracesDatasets.map((tracesDataset, index) =>
                                    <tr className="tracesDatasetsTable" key={tracesDataset.id + "-" + index}>
                                        <td>
                                            <a href={"/traces-datasets/" + tracesDataset.id + "?download=true"}
                                               download>
                                                {tracesDataset.name}
                                            </a>
                                        </td>
                                        <td>{tracesDataset.download_count}</td>
                                        <FileFormatCellDatasetTrace tracesDataset={tracesDataset}/>
                                        <td>{tracesDataset.num_traces}</td>
                                        <td>{tracesDataset.num_files}</td>
                                        <td>Uncompressed: {tracesDataset.size_in_gb},
                                            compressed: {tracesDataset.compressed_size_in_gb}</td>
                                        <td>{tracesDataset.date_added}</td>
                                        <td>{tracesDataset.description}</td>
                                        <td>{tracesDataset.citation}</td>
                                        <td>{tracesDataset.added_by}</td>
                                        <td>
                                            <Button variant="danger"
                                                    onClick={() => removeTracesDatasetConfirm(tracesDataset)} size="sm">
                                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                                            </Button>
                                        </td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
                        </div>
                    )
                } else {
                    return (
                        <div className="table-responsive">
                            <Table bordered hover>
                                <thead>
                                <tr className="tracesDatasetsTable">
                                    <th>Download Link</th>
                                    <th>Download count</th>
                                    <th>File format</th>
                                    <th>Number of traces</th>
                                    <th>Number of files</th>
                                    <th>Size (GB)</th>
                                    <th>Date added</th>
                                    <th>Description</th>
                                    <th>Citation</th>
                                    <th>Added by</th>
                                </tr>
                                </thead>
                                <tbody>
                                {props.tracesDatasets.map((tracesDataset, index) =>
                                    <tr className="tracesDatasetsTable" key={tracesDataset.id + "-" + index}>
                                        <td>
                                            <a href={"/traces-datasets/" + tracesDataset.id + "?download=true"}
                                               download>
                                                {tracesDataset.name}
                                            </a>
                                        </td>
                                        <td>{tracesDataset.download_count}</td>
                                        <FileFormatCellDatasetTrace tracesDataset={tracesDataset}/>
                                        <td>{tracesDataset.num_traces}</td>
                                        <td>{tracesDataset.num_files}</td>
                                        <td>Uncompressed: {tracesDataset.size_in_gb},
                                            compressed: {tracesDataset.compressed_size_in_gb}</td>
                                        <td>{tracesDataset.date_added}</td>
                                        <td>{tracesDataset.description}</td>
                                        <td>{tracesDataset.citation}</td>
                                        <td>{tracesDataset.added_by}</td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
                        </div>
                    )
                }
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
        setSearchStringTracesDatasets(searchVal)
    }

    const searchHandlerTracesDatasets = useDebouncedCallback(
        (event) => {
            searchChangeTracesDatasets(event)
        },
        350
    );

    return (
        <div className="Downloads">
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Traces Datasets
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
        </div>
    );
}

Downloads.propTypes = {};
Downloads.defaultProps = {};
export default Downloads;