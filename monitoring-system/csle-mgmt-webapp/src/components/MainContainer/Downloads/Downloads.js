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
import { useNavigate } from "react-router-dom";
import fileDownload from 'react-file-download'
import { useAlert } from "react-alert";

const Downloads = (props) => {
    const [showTracesDatasetsInfoModal, setShowTracesDatasetsInfoModal] = useState(false);
    const [tracesDatasets, setTracesDatasets] = useState([]);
    const [filteredTracesDatasets, setFilteredTracesDatasets] = useState([]);
    const [searchStringTracesDatasets, setSearchStringTracesDatasets] = useState("");
    const [loadingTracesDatasets, setLoadingTracesDatasets] = useState(true);
    const ip = "localhost"
    const alert = useAlert();

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
            .then(res => {return res.json()})
            .then(response => {
                console.log("traces datasets:")
                console.log(response)
                setTracesDatasets(response);
                setFilteredTracesDatasets(response);
                setLoadingTracesDatasets(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const fetchTracesDatasetsFile = useCallback((traceDataset) => {
        fetch(
            `http://` + ip + ':7777/traces-datasets/' + traceDataset.id + "?download=true",
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {return res})
            .then(response => {
                console.log("file response:")
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
                        an emulated IT infrastructure. A sequence contains a set of time-steps. Each time-step in the sequence
                        includes various measurements, e.g. attacker actions, defender actions, system metrics, and log files.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }


    const SpinnerOrTracesDatasetsTable = (props) => {
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
                            <th>Schema</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.tracesDatasets.map((tracesDataset, index) =>
                            <tr className="tracesDatasetsTable" key={tracesDataset.id + "-" + index}>
                                <td>
                                    <Button className="downloadLink" variant="link"
                                            onClick={() => fetchTracesDatasetsFile(tracesDataset)}>
                                        {tracesDataset.name}
                                    </Button>
                                </td>
                                <td>{tracesDataset.download_count}</td>
                                <td>{tracesDataset.file_format}</td>
                                <td>{tracesDataset.num_traces}</td>
                                <td>{tracesDataset.num_files}</td>
                                <td>Uncompressed: {tracesDataset.size_in_gb}, compressed: {tracesDataset.compressed_size_in_gb}</td>
                                <td>{tracesDataset.date_added}</td>
                                <td>{tracesDataset.description}</td>
                                <td>{tracesDataset.citation}</td>
                                <td>
                                    <Button className="downloadLink" variant="link"
                                            onClick={() => fileDownload(JSON.stringify(tracesDataset.data_schema), "schema.json")}>
                                        schema.json
                                    </Button>
                                </td>
                            </tr>
                        )}
                        </tbody>
                    </Table>
                </div>
            )
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
                            <Button variant="button" onClick={() => setShowTracesDatasetsInfoModal(true)} className="infoButton3">
                                <i className="infoButton3 fa fa-info-circle" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModalTracesDatasets show={showTracesDatasetsInfoModal}
                                                 onHide={() => setShowTracesDatasetsInfoModal(false)}/>
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
            <SpinnerOrTracesDatasetsTable tracesDatasets={filteredTracesDatasets} loading={loadingTracesDatasets}/>
        </div>
    );
}

Downloads.propTypes = {};
Downloads.defaultProps = {};
export default Downloads;