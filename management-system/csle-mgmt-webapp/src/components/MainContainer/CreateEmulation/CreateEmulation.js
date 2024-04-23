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
  const [idsEnabled, setIdsEnabled] = useState(true);

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
        flagPermission: true, interfaces: [], reachableByAgent: true}]);
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

  const handleContainerIdsEnabledChange = (event) => {
    const idsValue = event.target.value === 'true'; // Convert string to boolean
    setIdsEnabled(idsValue);
    console.log("Emulation IDS enabled is: " + idsValue)
  };

  const handleContainerReachableByAgentChange = (event, index) => {
    const reachableValue = event.target.value === 'true'; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      updatedContainers[index] = {
        ...updatedContainers[index],
        reachableByAgent: reachableValue
      };
      console.log("container" + index + " reachable by agebt is " + reachableValue);
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

  const [newInterface, setNewInterface] = useState({ name: '', ip: '', subnetMask:'', subnetPrefix: '',
    physicalInterface:'', bitmask:'', limitPacketsQueue:30000, packetDelayMs:2, packetDelayJitterMs:0.5});

  const inputNameRef = useRef(null);
  const inputIPRef = useRef(null);
  const inputSubnetMaskRef = useRef(null);
  const inputLimitPacketsQueueRef = useRef(null);
  const inputPacketDelayMsRef = useRef(null);
  const inputPacketDelayJitterMsRef = useRef(null);


  const [shouldFocusName, setShouldFocusName] = useState(false);
  const [shouldFocusIP, setShouldFocusIP] = useState(false);
  const [shouldFocusSubnetMask, setShouldFocusSubnetMask] = useState(false);
  const [shouldFocusLimitPacketsQueue, setShouldFocusLimitPacketsQueue] = useState(false);
  const [shouldFocusPacketDelayMs, setShouldFocusPacketDelayMs] = useState(false);
  const [shouldFocusPacketDelayJitterMs, setShouldFocusPacketDelayJitterMs] = useState(false);

  const handleContainerInterfaceNameChange = (event, containerIndex, interfaceIndex) => {
    const newName = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        name: newName
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
    setShouldFocusName(true); // Set flag to focus on name input
    setShouldFocusIP(false); // Clear flag for IP input
    setShouldFocusSubnetMask(false);
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    console.log("The container number "+ containerIndex+ " and interface number " + interfaceIndex + ":"
      + containers[containerIndex].interfaces[interfaceIndex].name);
  };

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
    setShouldFocusIP(true); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusSubnetMask(false)
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    console.log("The container number "+ containerIndex+ " and interface number " + interfaceIndex + ":"
      + containers[containerIndex].interfaces[interfaceIndex].ip);
  };

  const handleContainerInterfaceSubnetMaskChange = (event, containerIndex, interfaceIndex) => {
    const newSubnetMask = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        subnetMask: newSubnetMask
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
    setShouldFocusSubnetMask(true)
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
  };

  const handleContainerInterfaceLimitPacketsQueueChange = (event, containerIndex, interfaceIndex) => {
    const newLimitPacketsQueue = event.target.value;
    if (/^-?\d*$/.test(newLimitPacketsQueue)){
      setContainers(prevContainers => {
        const updatedContainers = [...prevContainers];
        const containerToUpdate = { ...updatedContainers[containerIndex] };
        const updatedInterfaces = [...containerToUpdate.interfaces];
        updatedInterfaces[interfaceIndex] = {
          ...updatedInterfaces[interfaceIndex],
          limitPacketsQueue: newLimitPacketsQueue
        };
        containerToUpdate.interfaces = updatedInterfaces;
        updatedContainers[containerIndex] = containerToUpdate;
        return updatedContainers;
      });
    }
    setShouldFocusLimitPacketsQueue(true);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
  };

  const handleContainerInterfacePacketDelayMs = (event, containerIndex, interfaceIndex) => {
    const newPacketDelayMs = event.target.value;
    if (/^-?\d*$/.test(newPacketDelayMs)){
      setContainers(prevContainers => {
        const updatedContainers = [...prevContainers];
        const containerToUpdate = { ...updatedContainers[containerIndex] };
        const updatedInterfaces = [...containerToUpdate.interfaces];
        updatedInterfaces[interfaceIndex] = {
          ...updatedInterfaces[interfaceIndex],
          packetDelayMs: newPacketDelayMs
        };
        containerToUpdate.interfaces = updatedInterfaces;
        updatedContainers[containerIndex] = containerToUpdate;
        return updatedContainers;
      });
    }
    setShouldFocusPacketDelayMs(true);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusPacketDelayJitterMs(false)
  };

  const handleContainerInterfacePacketDelayJitterMs = (event, containerIndex, interfaceIndex) => {
    const newPacketDelayJitterMs = event.target.value;
    if (/^-?\d*$/.test(newPacketDelayJitterMs)){
      setContainers(prevContainers => {
        const updatedContainers = [...prevContainers];
        const containerToUpdate = { ...updatedContainers[containerIndex] };
        const updatedInterfaces = [...containerToUpdate.interfaces];
        updatedInterfaces[interfaceIndex] = {
          ...updatedInterfaces[interfaceIndex],
          packetDelayJitterMs: newPacketDelayJitterMs
        };
        containerToUpdate.interfaces = updatedInterfaces;
        updatedContainers[containerIndex] = containerToUpdate;
        return updatedContainers;
      });
    }
    setShouldFocusPacketDelayJitterMs(true);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
  };

  // Use useEffect to focus on the input field when containers state changes
  useEffect(() => {
    // Check if the container state has changed, then focus on the input field
    if (inputNameRef.current && shouldFocusName) {
      inputNameRef.current.focus();
    } else if (inputIPRef.current && shouldFocusIP) {
      inputIPRef.current.focus();
    } else if (inputSubnetMaskRef.current && shouldFocusSubnetMask) {
      inputSubnetMaskRef.current.focus();
    } else if (inputLimitPacketsQueueRef.current && shouldFocusLimitPacketsQueue) {
      inputLimitPacketsQueueRef.current.focus();
    } else if (inputPacketDelayMsRef.current && shouldFocusPacketDelayMs) {
      inputPacketDelayMsRef.current.focus();
    } else if (inputPacketDelayJitterMsRef.current && shouldFocusPacketDelayJitterMs) {
      inputPacketDelayJitterMsRef.current.focus();
    }
  }, [containers, shouldFocusName, shouldFocusIP, shouldFocusSubnetMask, shouldFocusLimitPacketsQueue,
    shouldFocusPacketDelayMs, shouldFocusPacketDelayJitterMs]);

  const handleAddContainerInterface = (containerIndex) => {
    // Initialize the interface
    const interfaceToAdd = {
      name: 'New interface',
      ip: '0.0.0.0',
      subnetMask: '255.255.255.0',
      subnetPrefix: '',
      physicalInterface: '',
      bitmask: '255.255.255.0',
      limitPacketsQueue: 30000,
      packetDelayMs: 2,
      packetDelayJitterMs:0.5
    };

    setContainers(prevContainers => {
      // Create a copy of the containers array
      const updatedContainers = [...prevContainers];

      // Ensure the containerIndex is valid
      if (containerIndex >= 0 && containerIndex < updatedContainers.length) {
        // Get the container at the specified index
        const container = updatedContainers[containerIndex];

        // Check if the interface already exists in the container's interfaces array
        const interfaceExists = container.interfaces.some(existingInterface =>
            existingInterface.name === interfaceToAdd.name
          // You may need to adjust the condition based on your interface properties
        );

        // Add the interface only if it doesn't already exist
        if (!interfaceExists) {
          container.interfaces.push(interfaceToAdd);
        }
      }

      // Return the updated containers array
      return updatedContainers;
    });
  };

  const handleDeleteContainerInterface = (containerIndex, interfaceIndex) => {
    setContainers(prevContainers => {
      // Create a copy of the containers array
      const updatedContainers = prevContainers.map((container, index) => {
        if (index === containerIndex) {
          // Create a new array of interfaces excluding the one to be removed
          const updatedInterfaces = container.interfaces.filter(
            (_, i) => i !== interfaceIndex
          );

          // Return a new container object with updated interfaces
          return { ...container, interfaces: updatedInterfaces };
        }
        return container;
      });

      // Return the updated containers array
      return updatedContainers;
    });
  };

  const handleContainerNetworkPhysicalInterface = (event, containerIndex, interfaceIndex) => {
    const physicalInterfaceValue = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        physicalInterface: physicalInterfaceValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      console.log("The network interface is " +
        updatedContainers[containerIndex].interfaces[interfaceIndex].physicalInterface)
      return updatedContainers;
    });
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
                    <td>IDS enabled</td>
                    <td>
                      <select value={idsEnabled}
                              onChange={(e) => handleContainerIdsEnabledChange(e)}>
                        <option value="true">True</option>
                        <option value="false">False</option>

                      </select>
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
                                Delete the container {containers[index].name} &nbsp;&nbsp;
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
                                    <tr>
                                      <td>Reachable by agent</td>
                                      <td>
                                        <select value={containers[index].reachableByAgent}
                                                onChange={(e) => handleContainerReachableByAgentChange(e, index)}>
                                          <option value="true">True</option>
                                          <option value="false">False</option>

                                        </select>
                                      </td>
                                    </tr>
                                    </tbody>
                                  </Table>
                                </div>
                                <div>
                                  Add a network interface to container {containers[index].name} &nbsp;&nbsp;
                                  <Button type="button" onClick={() => handleAddContainerInterface(index)}
                                          variant="success" size="sm">
                                    <i className="fa fa-plus" aria-hidden="true" />
                                  </Button>
                                </div>
                                <div className="table-responsive">
                                  <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                      <th>Interface Attribute</th>
                                      <th>Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {containers[index].interfaces.map((containerInterfaces, interfaceIndex) => (
                                      <React.Fragment
                                        key={containerInterfaces.name + '-' + interfaceIndex + '-' + index}>
                                        <tr>
                                          <td> Name</td>
                                          <td>
                                            <input
                                              ref={inputNameRef}
                                              type="text"
                                              value={containerInterfaces.name}
                                              onChange={(event) => handleContainerInterfaceNameChange(event, index, interfaceIndex)}
                                            />
                                            <Button type="button" onClick={() =>
                                              handleDeleteContainerInterface(index, interfaceIndex)}
                                                    variant="danger" size="sm" style={{ marginLeft: '5px' }}>
                                              <i className="fa fa-trash startStopIcon" aria-hidden="true" />
                                            </Button>
                                          </td>
                                        </tr>
                                        <tr key={containerInterfaces.ip + '-' + interfaceIndex}>
                                          <td> IP</td>
                                          <td>
                                            <input
                                              ref={inputIPRef}
                                              type="text"
                                              value={containerInterfaces.ip}
                                              onChange={(event) => handleContainerInterfaceIPChange(event, index, interfaceIndex)}
                                            />
                                          </td>
                                        </tr>
                                        <tr key={containerInterfaces.subnet_mask + '-' + interfaceIndex}>
                                          <td> Subnet mask</td>
                                          <td>
                                            <input
                                              ref={inputSubnetMaskRef}
                                              type="text"
                                              value={containerInterfaces.subnetMask}
                                              onChange={(event) =>
                                                handleContainerInterfaceSubnetMaskChange(event, index, interfaceIndex)}
                                            />
                                          </td>
                                        </tr>
                                        <tr>
                                          <td>Physical interface</td>
                                          <td>
                                            <select
                                              value={containers[index].interfaces[interfaceIndex].physicalInterface}
                                              onChange={(e) => handleContainerNetworkPhysicalInterface(e, index, interfaceIndex)}>
                                              <option value="eth0">eth0</option>
                                              <option value="eth1">eth1</option>
                                              <option value="eth2">eth2</option>
                                              <option value="eth3">eth3</option>
                                              <option value="eth4">eth4</option>
                                              <option value="eth5">eth5</option>
                                              <option value="eth6">eth6</option>
                                              <option value="eth7">eth7</option>
                                              <option value="eth8">eth8</option>
                                              <option value="eth9">eth9</option>
                                              <option value="eth10">eth10</option>

                                            </select>
                                          </td>
                                        </tr>
                                        <tr
                                          key={containerInterfaces.limitPacketsQueue + '-' + interfaceIndex}>
                                          <td> Limit packets queue</td>
                                          <td>
                                            <input
                                              ref={inputLimitPacketsQueueRef}
                                              type="text"
                                              value={containerInterfaces.limitPacketsQueue}
                                              onChange={(event) =>
                                                handleContainerInterfaceLimitPacketsQueueChange(event, index,
                                                  interfaceIndex)}
                                            />
                                          </td>
                                        </tr>
                                        <tr
                                            key={containerInterfaces.packetDelayMs + '-' + interfaceIndex}>
                                          <td> Packet delay (ms)</td>
                                          <td>
                                            <input
                                              ref={inputPacketDelayMsRef}
                                              type="text"
                                              value={containerInterfaces.packetDelayMs}
                                              onChange={(event) =>
                                                handleContainerInterfacePacketDelayMs(event, index,
                                                  interfaceIndex)}
                                            />
                                          </td>
                                        </tr>
                                        <tr className="custom-td"
                                            key={containerInterfaces.packetDelayJitterMs + '-' + interfaceIndex}>
                                          <td> Packet delay jitter (ms)</td>
                                          <td>
                                            <input
                                              ref={inputPacketDelayJitterMsRef}
                                              type="text"
                                              value={containerInterfaces.packetDelayJitterMs}
                                              onChange={(event) =>
                                                handleContainerInterfacePacketDelayJitterMs(event, index,
                                                  interfaceIndex)}
                                            />
                                          </td>
                                        </tr>
                                      </React.Fragment>
                                    ))}
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
