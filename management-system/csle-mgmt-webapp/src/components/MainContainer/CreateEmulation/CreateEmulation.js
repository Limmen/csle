import React, {useState, useEffect, useCallback} from 'react';
import './CreateEmulation.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'
import { HTTP_PREFIX, IMAGES_RESOURCE, LOGIN_PAGE_RESOURCE, TOKEN_QUERY_PARAM } from '../../Common/constants'
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import formatBytes from "../../Common/formatBytes";
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";

import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Modal from 'react-bootstrap/Modal'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';

/**
 * Component representing the /create-emulation-page
 */
const CreateEmulation = (props) => {

  //main pages states
  const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
  const [containerOpen, setContainerOpen] = useState(false);
  const ip = serverIp
  const port = serverPort
  const alert = useAlert();
  const navigate = useNavigate();
  const setSessionData = props.setSessionData
  const [filteredImages, setFilteredImages] = useState([]);
  const [loading, setLoading] = useState([]);

  // general info states
  const [description, setDescription] = useState({
    description: ''
  });
  const handleDescriptionChange = (event) => {
    setDescription({
      description: event.target.value
    });
    // console.log(description.description)
  };

  // contrainers state
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState('');

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

  const handleImageChange = (event) => {
    setSelectedImage(event.target.value);
    console.log(selectedImage)
  };

  const SpinnerOrTable = (props) => {
    if (props.loading) {
      return (
        <Spinner animation="border" role="status">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="select-responsive">
          <select value={selectedImage} onChange={handleImageChange}>
            <option value="">--Please choose an option--</option>
            {props.images.map((img, index) =>
              <option value={img.name + "-" + index}>{img.name} &nbsp;&nbsp;&nbsp;&nbsp;  {formatBytes(img.size, 2)}</option>
            )}

          </select>
        </div>
      )
    }
  }


  return (
        <div className="CreateEmulation">
          <h3 className="managementTitle"> Create Emulation </h3>
          <Accordion defaultActiveKey="0">
            <Card className="subCard">
              <Card.Header>
                <Button
                  onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                  aria-controls="generalInfoBody"
                  aria-expanded={generalInfoOpen}
                  variant="link"
                >
                  <h5 className="semiTitle">
                    General information about the emulation
                    <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                  </h5>
                </Button>
              </Card.Header>
              <Collapse in={generalInfoOpen}>
                <div id="generalInfoBody" className="cardBodyHidden">
                  <div className="table-responsive">
                    <Table striped bordered hover>
                      <thead>
                      <tr>
                        <th>Attribute</th>
                        <th> Value</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td>Description</td>
                        <td>
                          <textarea
                            id="description"
                            value={description.textareaValue}
                            onChange={handleDescriptionChange}
                            rows="4"
                            style={{ width: '100%', boxSizing: 'border-box' }}
                          />
                        </td>
                      </tr>
                      </tbody>
                    </Table>
                  </div>
                </div>
              </Collapse>
            </Card>
          </Accordion>
          <Accordion defaultActiveKey="1">
            <Card className="subCard">
              <Card.Header>
                <Button
                  onClick={() => setContainerOpen(!containerOpen)}
                  aria-controls="container"
                  aria-expanded={containerOpen}
                  variant="link"
                >
                  <h5 className="semiTitle">
                    Containers
                    <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                  </h5>
                </Button>
              </Card.Header>
              <Collapse in={containerOpen}>
                <div id="container" className="cardBodyHidden">
                  <div className="table-responsive">
                    <Table striped bordered hover>
                      <thead>
                      <tr>
                        <th>Attribute</th>
                        <th> Value</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td>Images</td>
                        <td>
                          <SpinnerOrTable images={filteredImages} loading={loading}/>
                        </td>
                      </tr>
                      </tbody>
                    </Table>
                  </div>
                </div>
              </Collapse>
            </Card>
          </Accordion>

        </div>
    );
}

CreateEmulation.propTypes = {};
CreateEmulation.defaultProps = {};
export default CreateEmulation;
