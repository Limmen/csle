import React, {useState, useEffect, useCallback} from 'react';
import Table from 'react-bootstrap/Table'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import './ContainerImages.css';

const ContainerImages = () => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState([]);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchImages = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/images',
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
                    delay={{show: 250, hide: 400}}
                    overlay={renderRefreshTooltip()}
                >
                    <Button variant="button" onClick={refresh}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            </h3>
            <SpinnerOrTable images={images} loading={loading}/>
        </div>
    );
}

ContainerImages.propTypes = {};
ContainerImages.defaultProps = {};
export default ContainerImages;
