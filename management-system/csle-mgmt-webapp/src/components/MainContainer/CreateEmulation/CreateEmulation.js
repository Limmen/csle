import React, {useState, useEffect, useCallback, useRef} from 'react';
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

import CONTAINER_IMAGES from './ContainersNameAndOs';
import containersNameAndOs from './ContainersNameAndOs'
import getIps from '../../Common/getIps'

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

  const inputRef = useRef(null);

  // general info states
  const [description, setDescription] = useState({
    description: ''
  });
  const [nameValue, setNameValue] = useState('');
  const [networkIdValue, setNetworkIdValue] = useState('');
  const [levelValue, setLevelValue] = useState('');
  const [versionValue, setVersionValue] = useState('');
  const [timeStepLengthValue, setTimeStepLengthValue] = useState('');


  const handleDescriptionChange = (event) => {
    setDescription({
      description: event.target.value
    });
    // console.log(description.description)
  };
  const handleNameChange = (event) => {
    setNameValue(event.target.value);
    console.log("Name value:", nameValue);
  };
  const handleNetworkIdChange = (event) => {
    const networkValue = event.target.value;
    if (/^-?\d*$/.test(networkValue)) {
      setNetworkIdValue(event.target.value);
      console.log("Network ID value:", networkIdValue);
    }
  };

  const handleLevelChange = (event) => {
    const leveValue = event.target.value;
    if (/^-?\d*$/.test(leveValue)) {
      setLevelValue(event.target.value);
      console.log("Level value:", levelValue);
    }
  };

  const handleVersionChange = (event) => {
    setVersionValue(event.target.value);
    console.log("Versioin value:", versionValue);
  };

  const handleTimeStepLengthChange = (event) => {
    const timeStepValue = event.target.value;
    if (/^-?\d*$/.test(timeStepValue)) {
      setTimeStepLengthValue(event.target.value);
      console.log("Time step length value:", timeStepLengthValue);
    }
  };

  // containers state
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState('');
  const [containers, setContainers] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [newContainer, setNewContainer] = useState({ name: '', os: '' });
  const [newInterface, setNewInterface] = useState({ name: '', ip: '' });
  const [clicks, setClicks] = useState(1);

  const addContainer = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
    setNewContainer({ name: '', os: '' });
  };

  const handleConfirmAdd = () => {
    setContainers(prevContainers => [...prevContainers,
      { name: newContainer.name, os: newContainer.os, version: '', level: '', restartPolicy: '', networkId: '',
        subnetMask: '', subnetPrefix: '', cpu:'', mem:'', flagId:'', flagScore:'',
        flagPermission: true, interfaces: []}]);
    handleClosePopup();
  };

  const containerAndOs = Object.keys(containersNameAndOs).map(key => ({
    name: key,
    os: containersNameAndOs[key][0].os
  }));

  const handleContainerSelectChange = (e) => {
    // Extract the selected option from the event
    const selectedOption = JSON.parse(e.target.value);
    console.log('Selected option:', selectedOption.name, "->",selectedOption.os);
    // Call both functions
    setNewContainer({ name: selectedOption.name, os: selectedOption.os });
  };

  const deleteContainer = (index) => {
    setContainers(prevContainers => {
      // Create a new array without the container at the specified index
      const updatedContainers = [...prevContainers];
      updatedContainers.splice(index, 1);
      return updatedContainers;
    });
  };

  const toggleContainerAccordion = (index) => {
    setContainers(prevContainers => {
      // Create a new array with the updated container
      const updatedContainers = [...prevContainers];
      updatedContainers[index] = {
        ...updatedContainers[index],
        containerAccordionOpen: !updatedContainers[index].containerAccordionOpen // Toggle the value
      };
      return updatedContainers;
    });
  };

  const handleContainerCpuChange = (event, index) => {
    const cpuValue = event.target.value;
    if (/^-?\d*$/.test(cpuValue)) {
      setContainers(prevContainers => {
        // Create a new array with the updated container
        const updatedContainers = [...prevContainers];
        updatedContainers[index] = {
          ...updatedContainers[index],
          cpu: cpuValue // Update the value
        };
        console.log("container" + index + " cpu is " + cpuValue);
        return updatedContainers;
      });
    }
  };

  const handleContainerMemoryChange = (event, index) => {
    const memValue = event.target.value;
    if (/^-?\d*$/.test(memValue)) {
      setContainers(prevContainers => {
        // Create a new array with the updated container
        const updatedContainers = [...prevContainers];
        updatedContainers[index] = {
          ...updatedContainers[index],
          mem: memValue // Update the value
        };
        console.log("container" + index + " memory is " + memValue);
        return updatedContainers;
      });
    }
  };

  const handleContainerFlagIdChange = (event, index) => {
    const flagIdValue = event.target.value;
    if (/^-?\d*$/.test(flagIdValue)) {
      setContainers(prevContainers => {
        // Create a new array with the updated container
        const updatedContainers = [...prevContainers];
        updatedContainers[index] = {
          ...updatedContainers[index],
          flagId: flagIdValue // Update the value
        };
        console.log("container" + index + " flag ID is " + flagIdValue);
        return updatedContainers;
      });
    }
  };

  const handleContainerFlagScoreChange = (event, index) => {
    const flagScoreValue = event.target.value;
    if (/^-?\d*$/.test(flagScoreValue)) {
      setContainers(prevContainers => {
        // Create a new array with the updated container
        const updatedContainers = [...prevContainers];
        updatedContainers[index] = {
          ...updatedContainers[index],
          flagScore: flagScoreValue // Update the value
        };
        console.log("container" + index + " flag score is " + flagScoreValue);
        return updatedContainers;
      });
    }
  };

  const handleContainerFlagPermissionChange = (event, index) => {
    const permissionValue = event.target.value === 'true'; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      updatedContainers[index] = {
        ...updatedContainers[index],
        flagPermission: permissionValue
      };
      console.log("container" + index + " flag permission is " + permissionValue);
      return updatedContainers;
    });
  };

  // const fetchImages = useCallback(() => {
  //   /**
  //    * Fetches container images from the REST API backend
  //    *
  //    * @type {(function(): void)|*}
  //    */
  //   fetch(
  //     `${HTTP_PREFIX}${ip}:${port}/${IMAGES_RESOURCE}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
  //     {
  //       method: "GET",
  //       headers: new Headers({
  //         Accept: "application/vnd.github.cloak-preview"
  //       })
  //     }
  //   )
  //     .then(res => {
  //       if(res.status === 401) {
  //         alert.show("Session token expired. Please login again.")
  //         setSessionData(null)
  //         navigate(`/${LOGIN_PAGE_RESOURCE}`);
  //         return null
  //       }
  //       return res.json()
  //     })
  //     .then(response => {
  //       if(response === null) {
  //         return
  //       }
  //       setImages(response);
  //       setFilteredImages(response);
  //       setLoading(false)
  //     })
  //     .catch(error => console.log("error:" + error))
  // }, [alert, ip, navigate, port, props.sessionData, setSessionData]);
  //
  // useEffect(() => {
  //   setLoading(true)
  //   fetchImages()
  // }, [fetchImages]);
  //
  // const handleImageChange = (index, selectedImage) => {
  //   setContainers(prevContainers => {
  //     // Create a new array with the updated container
  //     const updatedContainers = [...prevContainers];
  //     updatedContainers[index] = {
  //       ...updatedContainers[index],
  //       image: selectedImage // Toggle the value
  //     };
  //     return updatedContainers;
  //   });
  //   // setSelectedImage(event.target.value);
  //   console.log(containers[index].os)
  // };
  //
  // const SpinnerOrTable = (props) => {
  //   if (props.loading) {
  //     return (
  //       <Spinner animation="border" role="status">
  //         <span className="visually-hidden"></span>
  //       </Spinner>)
  //   } else {
  //     return (
  //       <div className="select-responsive">
  //         <select value={containers[props.index].image} onChange={(e) => handleContainerSelectChange(e)}>
  //           <option value="">--Please choose an option--</option>
  //           {props.images.map((img, index) =>
  //             <option value={img.name + "-" + index}>{img.name} &nbsp;&nbsp;&nbsp;&nbsp; {formatBytes(img.size, 2)}</option>
  //           )}
  //
  //         </select>
  //       </div>
  //     )
  //   }
  // }

  const handleContainerInterfaceIPChange = (event, containerIndex, interfaceIndex) => {
    const newIP = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        ip: newIP
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
    console.log("The container number "+ containerIndex+ " and interface number " + interfaceIndex + ":"
      + containers[containerIndex].interfaces[interfaceIndex].ip)
  };

  // Use useEffect to focus on the input field when containers state changes
  useEffect(() => {
    // Check if the container state has changed, then focus on the input field
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [containers]);
/*
  const handleContainerInterfaceIPChange = (event,containerIndex, interfaceIndex) => {
    const newIP = event.target.value;
    const interfaceToAdd = { name: 'New interface', ip: newIP };

    // Clear input fields by updating the state
    setNewInterface(interfaceToAdd);

    setContainers(prevContainers => {
      // Create a new array with the updated container
      const updatedContainers = [...prevContainers];
      const updatedInterfaces = [...prevContainers[containerIndex].interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        ip: newIP // Update the value
      }
      updatedContainers[containerIndex] = {
        ...updatedContainers[containerIndex],
        interfaces: updatedInterfaces // Update the value
      };
      console.log("containerofff");
      return updatedContainers;
    })
  };
*/
  const handleAddContainerInterface = (containerIndex) => {
    // Create a new interface object with empty values
    const interfaceToAdd = { name: 'New interface', ip: '0.0.0.0' };

    // Clear input fields by updating the state
    setNewInterface(interfaceToAdd);

    let updatedContainers = []
    for (let i = 0; i < containers.length; i++) {
      if(i === containerIndex) {
        containers[i].interfaces.push(interfaceToAdd)
      }
      updatedContainers.push(containers[i])
    }
    setContainers(updatedContainers)
  };


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
                    <td>Name</td>
                    <td>
                      <input
                        type="text"
                        value={nameValue}
                        onChange={handleNameChange}
                      />
                    </td>
                        </tr>
                        <tr>
                          <td>Network ID</td>
                          <td>
                            <input
                              type="text"
                              value={networkIdValue}
                              onChange={handleNetworkIdChange}
                            />
                          </td>
                        </tr>
                        <tr>
                          <td>Level</td>
                          <td>
                            <input
                              type="text"
                              value={levelValue}
                              onChange={handleLevelChange}
                            />
                          </td>
                        </tr>
                        <tr>
                          <td>Version</td>
                          <td>
                            <input
                              type="text"
                              value={versionValue}
                              onChange={handleVersionChange}
                            />
                          </td>
                        </tr>
                        <tr>
                          <td>Time step length in Seconds</td>
                          <td>
                            <input
                              type="text"
                              value={timeStepLengthValue}
                              onChange={handleTimeStepLengthChange}
                            />
                          </td>
                        </tr>
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
                    <i className="fa fa-cubes headerIcon" aria-hidden="true"></i>
                  </h5>
                </Button>
              </Card.Header>
              <Collapse in={containerOpen}>
                <div id="container" className="cardBodyHidden">
                  <div>
                    Add a new container &nbsp;&nbsp;
                    <Button onClick={addContainer}
                            variant="success" size="sm">
                      <i className="fa fa-plus" aria-hidden="true"/>
                    </Button>
                    <div style={{ margin: '20px' }}>
                      {showPopup && (
                        <div className="popup">
                          <div>
                            <h5>Enter Container Name:</h5>
                          </div>
                          <div className="popup-content" style={{
                            display: 'flex', justifyContent: 'center',
                            alignItems: 'center'
                          }}>

                            <select value={JSON.stringify(newContainer)} onChange={(e) => handleContainerSelectChange(e)}>
                              <option value="">--Please choose an option--</option>
                              {containerAndOs.map((option, index) => (
                                <option key={index} value={JSON.stringify(option)}>
                                  {`${option.name} (${option.os})`}
                                </option>
                              ))}

                            </select>

                            <Button onClick={handleConfirmAdd}
                                    variant="primary" size="sm" style={{ marginLeft: '5px' }}>
                              <i className="fa fa-check" aria-hidden="true" />
                            </Button>
                            <Button onClick={handleClosePopup}
                                    variant="danger" size="sm" style={{ marginLeft: '2px' }}>
                              <i className="fa fa-times" aria-hidden="true" />
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>


                    {containers.map((container, index) => (
                      <Accordion defaultActiveKey={index}>
                        <card className="subCard">
                          <Card.Header>
                            <Button
                              onClick={() => toggleContainerAccordion(index)}
                              aria-controls="container"
                              aria-expanded={container.containerAccordionOpen}
                              variant="link"
                            >
                            <h5 className="semiTitle">
                                {containers[index].name}
                                <i className="fa fa-cube headerIcon" aria-hidden="true"></i>
                              </h5>
                            </Button>
                          </Card.Header>
                          <Collapse in={container.containerAccordionOpen}>
                            <div id="eachContainer" className="cardBodyHidden">
                              <div>
                                Delete the container &nbsp;&nbsp;
                                <Button onClick={() => deleteContainer(index)}
                                        variant="danger" size="sm">
                                  <i className="fa fa-trash startStopIcon" aria-hidden="true" />
                                </Button>
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
                                      <td>Name</td>
                                      <td>
                                        {containers[index].name}
                                        {/*<SpinnerOrTable images={filteredImages} loading={loading} index={index} />*/}
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>OS</td>
                                      <td>
                                        {containers[index].os}
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>Number of allocated CPU cores</td>
                                      <td>
                                        <input
                                          type="text"
                                          value={containers[index].cpu}
                                          onChange={(event) => handleContainerCpuChange(event, index)}
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>Available memory in GB</td>
                                      <td>
                                        <input
                                          type="text"
                                          value={containers[index].mem}
                                          onChange={(event) => handleContainerMemoryChange(event, index)}
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>Flag ID</td>
                                      <td>
                                        <input
                                          type="text"
                                          value={containers[index].flagId}
                                          onChange={(event) => handleContainerFlagIdChange(event, index)}
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>Flag score</td>
                                      <td>
                                        <input
                                          type="text"
                                          value={containers[index].flagScore}
                                          onChange={(event) => handleContainerFlagScoreChange(event, index)}
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>Flag requires root permission</td>
                                      <td>
                                        <select value={containers[index].flagPermission}
                                                onChange={(e) => handleContainerFlagPermissionChange(e, index)}>
                                          <option value="true">True</option>
                                          <option value="false">False</option>

                                        </select>
                                      </td>
                                    </tr>
                                    </tbody>
                                  </Table>
                                </div>
                                <div>
                                  Add a network interface &nbsp;&nbsp;
                                  <Button type="button" onClick={() => handleAddContainerInterface(index)}
                                          variant="primary" size="sm">
                                    <i className="fa fa-plus" aria-hidden="true" />
                                  </Button>
                                </div>
                                <div className="table-responsive">
                                  <Table striped bordered hover>
                                    <tbody>

                                    {containers[index].interfaces.map((containerInterfaces, interfaceIndex) =>
                                      <tr key={containerInterfaces.ip + '-' + interfaceIndex}>
                                        <td>IP</td>
                                        <td>
                                          <input
                                            ref={inputRef}
                                            type="text"
                                            value={containerInterfaces.ip}
                                            onChange={(event) => handleContainerInterfaceIPChange(event, index, interfaceIndex)}
                                          />
                                        </td>
                                      </tr>
                                    )}
                                    </tbody>
                                  </Table>
                                </div>
                              </div>
                            </div>
                          </Collapse>
                        </card>
                      </Accordion>
                    ))}
                  </div>


                </div>
              </Collapse>
            </Card>
          </Accordion>

    </div>
  );
}

CreateEmulation.propTypes = {}
CreateEmulation.defaultProps = {}
export default CreateEmulation
