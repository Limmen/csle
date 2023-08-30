import React, {useState, useEffect, useCallback} from 'react';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import './ContainerImages.css';
import Docker from './docker.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import formatBytes from "../../Common/formatBytes";
import {HTTP_PREFIX, IMAGES_RESOURCE, LOGIN_PAGE_RESOURCE, TOKEN_QUERY_PARAM} from "../../Common/constants";

const ContainerImages = (props) => {
    /**
     * Component representing the /images-page
     *
     * @param props
     * @returns {JSX.Element}
     * @constructor
     */
    const [images, setImages] = useState([]);
    const [filteredImages, setFilteredImages] = useState([]);
    const [loading, setLoading] = useState([]);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchImages = useCallback(() => {
        /**
         * Fetches container images from the REST API backend
         *
         * @type {(function(): void)|*}
         */
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${IMAGES_RESOURCE}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: "GET",
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
                if(response === null) {
                    return
                }
                setImages(response);
                setFilteredImages(response);
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData, setSessionData]);

    useEffect(() => {
        setLoading(true)
        fetchImages()
    }, [fetchImages]);

    const refresh = () => {
        setLoading(true)
        fetchImages()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload images from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the container images.
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
                        Container images
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        Emulation environments are built using Docker containers which encapsulate
                        functionalities of emulated hosts and can be connected in complex networks.
                        From the list of docker images, new emulation environments can be generated programmatically
                        by combining images in novel topologies and configurations.
                    </p>
                    <div className="text-center">
                        <img src={Docker} alt="Docker" width="700" className="img-fluid"/>
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
                        <tr className="containerImagesTable">
                            <th>Name</th>
                            <th> Size</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.images.map((img, index) =>
                            <tr className="containerImagesTable" key={img.name + "-" + index}>
                                <td>{img.name}</td>
                                <td>{formatBytes(img.size, 2)}</td>
                            </tr>
                        )}
                        </tbody>
                    </Table>
                </div>
            )
        }
    }

    const searchFilter = (image, searchVal) => {
        return (searchVal === "" ||
            image.name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const fImg = images.filter(img => {
            return searchFilter(img, searchVal)
        });
        setFilteredImages(fImg)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    return (
        <div className="ContainerImages">
            <h3 className="managementTitle"> Management of Container Images </h3>
            <div className="row">
                <div className="col-sm-3">
                </div>
                <div className="col-sm-3">
                    <h3> Container Images
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
            <SpinnerOrTable images={filteredImages} loading={loading}/>
        </div>
    );
}

ContainerImages.propTypes = {};
ContainerImages.defaultProps = {};
export default ContainerImages;
