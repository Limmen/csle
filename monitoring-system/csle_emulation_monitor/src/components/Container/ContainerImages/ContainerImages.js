import React, {useState, useEffect, useCallback} from 'react';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import './ContainerImages.css';
import Docker from './docker.png'

const ContainerImages = () => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState([]);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchImages = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/imagesdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setImages(response);
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchImages()
    }, []);

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
                    <Modal.Title id="contained-modal-title-vcenter">
                        Container images
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Containers</h4>
                    <p className="modalText">
                        Emulation environments are built using Docker containers which encapsulate
                        functionalities of emulated hosts and can be connected in complex networks.
                        From the list of docker images, new emulation environments can be generated programmatically
                        by combining images in novel topologies and configurations.
                    </p>
                    <div className="text-center">
                        <img src={Docker} alt="Docker" width="700"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
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
                <Table bordered hover>
                    <thead>
                    <tr className="containerImagesTable">
                        <th>Name</th>
                        <th> Size (bytes)</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.images.map((img, index) =>
                        <tr className="containerImagesTable" key={img.name + "-" + index}>
                            <td>{img.name}</td>
                            <td>{img.size}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>
            )
        }
    }

    return (
        <div className="Monitoring">
            <h3> Container Images
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRefreshTooltip()}
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
            <SpinnerOrTable images={images} loading={loading}/>
        </div>
    );
}

ContainerImages.propTypes = {};
ContainerImages.defaultProps = {};
export default ContainerImages;
