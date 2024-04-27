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
    physicalInterface:'', bitmask:'', limitPacketsQueue:30000, packetDelayMs:2, packetDelayJitterMs:0.5,
    packetDelayCorrelationPercentage:25, packetDelayDistribution:'0', packetLossType:'0',lossGemodelp: 0.02,
    lossGemodelr:0.97, lossGemodelk:0.98, lossGemodelh:0.0001, packetCorruptPercentage:0.00001,
    packetCorruptCorrelationPercentage:25, packetDuplicatePercentage:0.00001,
    packetDuplicateCorrelationPercentage:25, packetReorderPercentage:0.0025,
    packetReorderCorrelationPercentage:25, packetReorderGap:5, rateLimitMbit:1000,
    packetOverheadBytes:0, cellOverheadBytes:0, defaultGateway:"0.0.0.0", defaultInput:"accpet", defaultOutput:"accept",
    defaultForward:"Drop", trafficManagerPort:"50043", trafficManagerLogFile:"traffic_manager.log",
    trafficManagerLogDir:"/", trafficManagerMaxWorkers:"10"
  });

  const inputNameRef = useRef(null);
  const inputIPRef = useRef(null);
  const inputSubnetMaskRef = useRef(null);
  const inputLimitPacketsQueueRef = useRef(null);
  const inputPacketDelayMsRef = useRef(null);
  const inputPacketDelayJitterMsRef = useRef(null);
  const inputPacketDelayCorrelationPercentageRef = useRef(null);
  const inputLossGemodelpRef = useRef(null)
  const inputLossGemodelrRef = useRef(null)
  const inputLossGemodelkRef = useRef(null)
  const inputLossGemodelhRef = useRef(null)
  const inputPacketCorruptPercentageRef = useRef(null)
  const inputPacketCorruptCorrelationPercentageRef = useRef(null)
  const inputPacketDuplicatePercentageRef = useRef(null)
  const inputPacketDuplicateCorrelationPercentageRef = useRef(null)
  const inputPacketReorderPercentageRef = useRef(null)
  const inputPacketReorderCorrelationPercentageRef = useRef(null)
  const inputPacketReorderGapRef = useRef(null)
  const inputRateLimitMbitRef = useRef(null)
  const inputPacketOverheadBytesRef = useRef(null)
  const inputCellOverheadBytesRef = useRef(null)
  const inputDefaultGatewayRef = useRef(null)
  const inputTrafficManagerPortRef = useRef(null)
  const inputTrafficManagerLogFileRef = useRef(null)
  const inputTrafficManagerLogDirRef = useRef(null)
  const inputTrafficManagerMaxWorkersRef = useRef(null)
  const inputCpuRef = useRef(null)
  const inputMemRef = useRef(null)
  const inputFlagIdRef = useRef(null)
  const inputFlagScoreRef = useRef(null)
  const inputPacketDelayDistributionRef = useRef(null)
  const inputPacketLossTypeRef = useRef(null)


  const [shouldFocusName, setShouldFocusName] = useState(false);
  const [shouldFocusIP, setShouldFocusIP] = useState(false);
  const [shouldFocusSubnetMask, setShouldFocusSubnetMask] = useState(false);
  const [shouldFocusLimitPacketsQueue, setShouldFocusLimitPacketsQueue] = useState(false);
  const [shouldFocusPacketDelayMs, setShouldFocusPacketDelayMs] = useState(false);
  const [shouldFocusPacketDelayJitterMs, setShouldFocusPacketDelayJitterMs] = useState(false);
  const [shouldFocusPacketDelayCorrelationPercentage, setShouldFocusPacketDelayCorrelationPercentage] = useState(false);
  const [shouldFocusLossGemodelp, setShouldFocusLossGemodelp] = useState(false);
  const [shouldFocusLossGemodelr, setShouldFocusLossGemodelr] = useState(false);
  const [shouldFocusLossGemodelk, setShouldFocusLossGemodelk] = useState(false);
  const [shouldFocusLossGemodelh, setShouldFocusLossGemodelh] = useState(false);
  const [shouldFocusPacketCorruptPercentage, setShouldFocusPacketCorruptPercentage] = useState(false);
  const [shouldFocusPacketCorruptCorrelationPercentage, setShouldFocusPacketCorruptCorrelationPercentage]
    = useState(false);
  const [shouldFocusPacketDuplicatePercentage, setShouldFocusPacketDuplicatePercentage] = useState(false);
  const [shouldFocusPacketDuplicateCorrelationPercentage, setShouldFocusPacketDuplicateCorrelationPercentage]
    = useState(false);
  const [shouldFocusPacketReorderPercentage, setShouldFocusPacketReorderPercentage] = useState(false);
  const [shouldFocusPacketReorderCorrelationPercentage, setShouldFocusPacketReorderCorrelationPercentage]
    = useState(false);
  const [shouldFocusPacketReorderGap, setShouldFocusPacketReorderGap] = useState(false);
  const [shouldFocusRateLimitMbit, setShouldFocusRateLimitMbit] = useState(false);
  const [shouldFocusPacketOverheadBytes, setShouldFocusPacketOverheadBytes] = useState(false);
  const [shouldFocusCellOverheadBytes, setShouldFocusCellOverheadBytes] = useState(false);
  const [shouldFocusDefaultGateway, setShouldFocusDefaultGateway] = useState(false);
  const [shouldFocusTrafficManagerPort, setShouldFocusTrafficManagerPort] = useState(false);
  const [shouldFocusTrafficManagerLogFile, setShouldFocusTrafficManagerLogFile] = useState(false);
  const [shouldFocusTrafficManagerLogDir, setShouldFocusTrafficManagerLogDir] = useState(false);
  const [shouldFocusTrafficManagerMaxWorkers, setShouldFocusTrafficManagerMaxWorkers] = useState(false);

  const [shouldFocusCpu, setShouldFocusCpu] = useState(false);
  const [shouldFocusMem, setShouldFocusMem] = useState(false);
  const [shouldFocusFlagId, setShouldFocusFlagId] = useState(false);
  const [shouldFocusFlagScore, setShouldFocusFlagScore] = useState(false);
  const [shouldFocusPacketDelayDistribution, setShouldFocusPacketDelayDistribution] = useState(false);
  const [shouldFocusPacketLossType, setShouldFocusPacketLossType] = useState(false);


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
    setShouldFocusCpu(true);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusMem(false);
    setShouldFocusName(false);
    setShouldFocusIP(false); // Clear flag for IP input
    setShouldFocusSubnetMask(false);
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
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

    setShouldFocusMem(true);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusName(false);
    setShouldFocusIP(false); // Clear flag for IP input
    setShouldFocusSubnetMask(false);
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
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
    setShouldFocusFlagId(true);
    setShouldFocusFlagScore(false);
    setShouldFocusName(false);
    setShouldFocusMem(false);
    setShouldFocusCpu(false);
    setShouldFocusIP(false); // Clear flag for IP input
    setShouldFocusSubnetMask(false);
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
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
    setShouldFocusFlagScore(true);
    setShouldFocusName(false);
    setShouldFocusFlagId(false);
    setShouldFocusMem(false);
    setShouldFocusCpu(false);
    setShouldFocusIP(false); // Clear flag for IP input
    setShouldFocusSubnetMask(false);
    setShouldFocusLimitPacketsQueue(false)
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

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
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
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
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].ip)
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
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].subnetMask)
  };

  const handleContainerInterfaceLimitPacketsQueueChange = (event, containerIndex, interfaceIndex) => {
    const newLimitPacketsQueue = event.target.value;
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

    setShouldFocusLimitPacketsQueue(true);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusPacketDelayMs(false);
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value limit packet Q is: " + containers[containerIndex].interfaces[interfaceIndex].limitPacketsQueue)
  };

  const handleContainerInterfacePacketDelayMs = (event, containerIndex, interfaceIndex) => {
    const newPacketDelayMs = event.target.value;
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

    setShouldFocusPacketDelayMs(true);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusPacketDelayJitterMs(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value Packet Delay MS is: " + containers[containerIndex].interfaces[interfaceIndex].packetDelayMs)
  };

  const handleContainerInterfacePacketDelayJitterMs = (event, containerIndex, interfaceIndex) => {
    const newPacketDelayJitterMs = event.target.value;
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

    setShouldFocusPacketDelayJitterMs(true);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].packetDelayJitterMs)
  };

  const handleContainerInterfacePacketDelayCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketDelayCorrelationPercentage = event.target.value;

    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetDelayCorrelationPercentage: newPacketDelayCorrelationPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });

    setShouldFocusPacketDelayCorrelationPercentage(true)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false); // Set flag to focus on IP input
    setShouldFocusName(false); // Clear flag for name input
    setShouldFocusLossGemodelp(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].packetDelayCorrelationPercentage)
  };

  const handleContainerInterfaceLossGemodelp = (event, containerIndex, interfaceIndex) => {
    const newLossGemodelp = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        lossGemodelp: newLossGemodelp
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusLossGemodelp(true)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].lossGemodelp)
  };

  const handleContainerInterfaceLossGemodelr = (event, containerIndex, interfaceIndex) => {
    const newLossGemodelr = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        lossGemodelr: newLossGemodelr
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusLossGemodelr(true)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].lossGemodelr)
  };

  const handleContainerInterfaceLossGemodelk = (event, containerIndex, interfaceIndex) => {
    const newLossGemodelk = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        lossGemodelk: newLossGemodelk
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusLossGemodelk(true)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusLossGemodelh(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].lossGemodelk)
  };
  const handleContainerInterfaceLossGemodelh = (event, containerIndex, interfaceIndex) => {
    const newLossGemodelh = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        lossGemodelh: newLossGemodelh
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusLossGemodelh(true)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
    console.log("The value is: " + containers[containerIndex].interfaces[interfaceIndex].lossGemodelp)
  };

  const handleContainerInterfacePacketCorruptPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketCorruptPercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetCorruptPercentage: newPacketCorruptPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketCorruptPercentage(true)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketCorruptCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketCorruptCorrelationPercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetCorruptCorrelationPercentage: newPacketCorruptCorrelationPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketCorruptCorrelationPercentage(true)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketDuplicatePercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketDuplicatePercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetDuplicatePercentage: newPacketDuplicatePercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketDuplicatePercentage(true)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketDuplicateCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketDuplicateCorrelationPercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetDuplicateCorrelationPercentage: newPacketDuplicateCorrelationPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketDuplicateCorrelationPercentage(true)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketReorderPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketReorderPercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetReorderPercentage: newPacketReorderPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketReorderPercentage(true)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketReorderCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
    const newPacketReorderCorrelationPercentage = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetReorderCorrelationPercentage: newPacketReorderCorrelationPercentage
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketReorderCorrelationPercentage(true)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketReorderGap(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketReorderGap = (event, containerIndex, interfaceIndex) => {
    const newPacketReorderGap = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetReorderGap: newPacketReorderGap
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketReorderGap(true)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceRateLimitMbit = (event, containerIndex, interfaceIndex) => {
    const newRateLimitMbit = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        rateLimitMbit: newRateLimitMbit
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusRateLimitMbit(true)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfacePacketOverheadBytes = (event, containerIndex, interfaceIndex) => {
    const newPacketOverheadBytes = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetOverheadBytes: newPacketOverheadBytes
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusPacketOverheadBytes(true)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceCellOverheadBytes = (event, containerIndex, interfaceIndex) => {
    const newCellOverheadBytes = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        cellOverheadBytes: newCellOverheadBytes
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusCellOverheadBytes(true)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusDefaultGateway(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceDefaultGateway = (event, containerIndex, interfaceIndex) => {
    const newDefaultGateway = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        defaultGateway: newDefaultGateway
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusDefaultGateway(true)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceTrafficManagerPort = (event, containerIndex, interfaceIndex) => {
    const newTrafficManagerPort = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        trafficManagerPort: newTrafficManagerPort
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusTrafficManagerPort(true)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceTrafficManagerLogFile = (event, containerIndex, interfaceIndex) => {
    const newTrafficManagerLogFile = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        trafficManagerLogFile: newTrafficManagerLogFile
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusTrafficManagerLogFile(true)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceTrafficManagerLogDir = (event, containerIndex, interfaceIndex) => {
    const newTrafficManagerLogDir = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        trafficManagerLogDir: newTrafficManagerLogDir
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusTrafficManagerLogDir(true)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
  };

  const handleContainerInterfaceTrafficManagerMaxWorkers = (event, containerIndex, interfaceIndex) => {
    const newTrafficManagerMaxWorkers = event.target.value;
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        trafficManagerMaxWorkers: newTrafficManagerMaxWorkers
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;

      return updatedContainers;
    });
    setShouldFocusTrafficManagerMaxWorkers(true)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
    setShouldFocusPacketLossType(false)
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
      } else if (inputPacketDelayCorrelationPercentageRef.current && shouldFocusPacketDelayCorrelationPercentage) {
        inputPacketDelayCorrelationPercentageRef.current.focus();
      } else if (inputLossGemodelpRef.current && shouldFocusLossGemodelp) {
        inputLossGemodelpRef.current.focus();
      } else if (inputLossGemodelrRef.current && shouldFocusLossGemodelr) {
        inputLossGemodelrRef.current.focus();
      } else if (inputLossGemodelkRef.current && shouldFocusLossGemodelk) {
        inputLossGemodelkRef.current.focus();
      } else if (inputLossGemodelhRef.current && shouldFocusLossGemodelh) {
        inputLossGemodelhRef.current.focus();
      } else if (inputPacketCorruptPercentageRef.current && shouldFocusPacketCorruptPercentage) {
        inputPacketCorruptPercentageRef.current.focus();
      } else if (inputPacketCorruptCorrelationPercentageRef.current && shouldFocusPacketCorruptCorrelationPercentage) {
        inputPacketCorruptCorrelationPercentageRef.current.focus();
      } else if (inputPacketDuplicatePercentageRef.current && shouldFocusPacketDuplicatePercentage) {
        inputPacketDuplicatePercentageRef.current.focus();
      } else if (inputPacketDuplicateCorrelationPercentageRef.current && shouldFocusPacketDuplicateCorrelationPercentage) {
        inputPacketDuplicateCorrelationPercentageRef.current.focus();
      } else if (inputPacketReorderPercentageRef.current && shouldFocusPacketReorderPercentage) {
        inputPacketReorderPercentageRef.current.focus();
      } else if (inputPacketReorderCorrelationPercentageRef.current && shouldFocusPacketReorderCorrelationPercentage) {
        inputPacketReorderCorrelationPercentageRef.current.focus();
      } else if (inputPacketReorderGapRef.current && shouldFocusPacketReorderGap) {
        inputPacketReorderGapRef.current.focus();
      } else if (inputRateLimitMbitRef.current && shouldFocusRateLimitMbit) {
        inputRateLimitMbitRef.current.focus();
      } else if (inputPacketOverheadBytesRef.current && shouldFocusPacketOverheadBytes) {
        inputPacketOverheadBytesRef.current.focus();
      } else if (inputCellOverheadBytesRef.current && shouldFocusCellOverheadBytes) {
        inputCellOverheadBytesRef.current.focus();
      } else if (inputCpuRef.current && shouldFocusCpu) {
        inputCpuRef.current.focus();
      } else if (inputMemRef.current && shouldFocusMem) {
        inputMemRef.current.focus();
      } else if (inputFlagIdRef.current && shouldFocusFlagId) {
        inputFlagIdRef.current.focus();
      } else if (inputFlagScoreRef.current && shouldFocusFlagScore) {
        inputFlagScoreRef.current.focus();
      } else if (inputDefaultGatewayRef.current && shouldFocusDefaultGateway) {
        inputDefaultGatewayRef.current.focus();
      } else if (inputTrafficManagerPortRef.current && shouldFocusTrafficManagerPort) {
        inputTrafficManagerPortRef.current.focus();
      } else if (inputTrafficManagerLogDirRef.current && shouldFocusTrafficManagerLogDir) {
        inputTrafficManagerLogDirRef.current.focus();
      } else if (inputTrafficManagerLogFileRef.current && shouldFocusTrafficManagerLogFile) {
        inputTrafficManagerLogFileRef.current.focus();
      } else if (inputTrafficManagerMaxWorkersRef.current && shouldFocusTrafficManagerMaxWorkers) {
        inputTrafficManagerMaxWorkersRef.current.focus();
      } else if (inputPacketDelayDistributionRef.current && shouldFocusPacketDelayDistribution) {
        inputPacketDelayDistributionRef.current.focus();
      } else if (inputPacketLossTypeRef.current && shouldFocusPacketLossType) {
        inputPacketLossTypeRef.current.focus();
      }
    }, [containers, shouldFocusName, shouldFocusIP, shouldFocusSubnetMask, shouldFocusLimitPacketsQueue,
      shouldFocusPacketDelayMs, shouldFocusPacketDelayJitterMs, shouldFocusPacketDelayCorrelationPercentage,
      shouldFocusLossGemodelp], shouldFocusLossGemodelr, shouldFocusLossGemodelk, shouldFocusLossGemodelh,
    shouldFocusPacketCorruptPercentage, shouldFocusPacketCorruptCorrelationPercentage,
    shouldFocusPacketDuplicatePercentage, shouldFocusPacketDuplicateCorrelationPercentage,
    shouldFocusPacketReorderPercentage, shouldFocusPacketReorderCorrelationPercentage, shouldFocusPacketReorderGap,
    shouldFocusRateLimitMbit, shouldFocusPacketOverheadBytes, shouldFocusCellOverheadBytes,
    shouldFocusCpu, shouldFocusFlagId, shouldFocusMem, shouldFocusFlagScore, shouldFocusDefaultGateway,
    shouldFocusTrafficManagerPort, shouldFocusTrafficManagerLogDir, shouldFocusTrafficManagerLogFile,
    shouldFocusTrafficManagerMaxWorkers, shouldFocusPacketDelayDistribution, shouldFocusPacketLossType);

  const handleContainerInterfacePacketDelayDistribution = (event, containerIndex, interfaceIndex) => {
    const packetDelayDistributionValue = event.target.value; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetDelayDistribution: packetDelayDistributionValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
    setShouldFocusPacketDelayDistribution(true)
    setShouldFocusPacketLossType(false)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
  };

  const handleContainerInterfacePacketLossType = (event, containerIndex, interfaceIndex) => {
    const packetLossTypeValue = event.target.value; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        packetLossType: packetLossTypeValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
    setShouldFocusPacketLossType(true)
    setShouldFocusTrafficManagerMaxWorkers(false)
    setShouldFocusTrafficManagerLogDir(false)
    setShouldFocusTrafficManagerLogFile(false)
    setShouldFocusTrafficManagerPort(false)
    setShouldFocusDefaultGateway(false)
    setShouldFocusCellOverheadBytes(false)
    setShouldFocusPacketOverheadBytes(false)
    setShouldFocusRateLimitMbit(false)
    setShouldFocusPacketReorderGap(false)
    setShouldFocusPacketReorderCorrelationPercentage(false)
    setShouldFocusPacketReorderPercentage(false)
    setShouldFocusPacketDuplicateCorrelationPercentage(false)
    setShouldFocusPacketDuplicatePercentage(false)
    setShouldFocusPacketCorruptCorrelationPercentage(false)
    setShouldFocusPacketCorruptPercentage(false)
    setShouldFocusLossGemodelh(false)
    setShouldFocusLossGemodelk(false)
    setShouldFocusLossGemodelr(false)
    setShouldFocusLossGemodelp(false)
    setShouldFocusPacketDelayCorrelationPercentage(false)
    setShouldFocusPacketDelayJitterMs(false);
    setShouldFocusPacketDelayMs(false);
    setShouldFocusLimitPacketsQueue(false);
    setShouldFocusSubnetMask(false);
    setShouldFocusIP(false);
    setShouldFocusName(false);
    setShouldFocusMem(false);
    setShouldFocusFlagId(false);
    setShouldFocusFlagScore(false);
    setShouldFocusCpu(false);
    setShouldFocusPacketDelayDistribution(false)
  };

  const handleContainerInterfaceDefaultInput = (event, containerIndex, interfaceIndex) => {
    const defaultInputValue = event.target.value; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        defaultInput: defaultInputValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
  };

  const handleContainerInterfaceDefaultOutput = (event, containerIndex, interfaceIndex) => {
    const defaultOutputValue = event.target.value; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        defaultOutput: defaultOutputValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
  };

  const handleContainerInterfaceDefaultForward = (event, containerIndex, interfaceIndex) => {
    const defaultForwardValue = event.target.value; // Convert string to boolean
    setContainers(prevContainers => {
      const updatedContainers = [...prevContainers];
      const containerToUpdate = { ...updatedContainers[containerIndex] };
      const updatedInterfaces = [...containerToUpdate.interfaces];
      updatedInterfaces[interfaceIndex] = {
        ...updatedInterfaces[interfaceIndex],
        defaultForward: defaultForwardValue
      };
      containerToUpdate.interfaces = updatedInterfaces;
      updatedContainers[containerIndex] = containerToUpdate;
      return updatedContainers;
    });
  };


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
      packetDelayJitterMs:0.5,
      packetDelayCorrelationPercentage:25,
      packetDelayDistribution:'0',
      packetLossType:'0',
      lossGemodelp:'0.02',
      lossGemodelr:'0.97',
      lossGemodelk:'0.98',
      lossGemodelh:'0.0001',
      packetCorruptPercentage:"0.00001",
      packetCorruptCorrelationPercentage:"25",
      packetDuplicatePercentage: "0.00001",
      packetDuplicateCorrelationPercentage:"25",
      packetReorderPercentage: "0.0025",
      packetReorderCorrelationPercentage: "25",
      packetReorderGap:"5",
      rateLimitMbit:"1000",
      packetOverheadBytes:"0",
      cellOverheadBytes:"0",
      defaultGateway:"0.0.0.0",
      defaultInput:"accept",
      defaultOutput:"accept",
      defaultForward:"drop",
      trafficManagerPort:"50043",
      trafficManagerLogFile:"traffic_manager.log",
      trafficManagerLogDir:"/",
      trafficManagerMaxWorkers:"10"
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
    console.log("Length of interface is:" + containers[containerIndex].interfaces.length)
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
                                  <React.Fragment key={'form-' + containerInterfaces.name + '-' + interfaceIndex + '-' + index}>
                                    <tr key={'interface-' + containerInterfaces.name + '-' + interfaceIndex + '-' + index}>
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
                                    <tr key={'ip-' + containerInterfaces.ip + '-' + interfaceIndex  + '-' + index}>
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
                                    <tr key={'subnet-' + containerInterfaces.subnetMask + '-' + interfaceIndex  + '-' + index}>
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
                                    <tr
                                      key={'eth-' + containerInterfaces.physicalInterface + '-' +
                                        interfaceIndex  + '-' + index}>
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
                                      key={'packet-limit-'+containerInterfaces.limitPacketsQueue + '-' +
                                        interfaceIndex  + '-' + index}>
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
                                      key={'packet-delay-' + containerInterfaces.packetDelayMs + '-' + interfaceIndex  + '-' + index}>
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
                                    <tr
                                      key={'packet-jitter-' + containerInterfaces.packetDelayJitterMs + '-' + interfaceIndex  + '-' + index}>
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
                                    <tr
                                      key={'packet-correlation-' + containerInterfaces.packetDelayCorrelationPercentage + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Packet delay correlation percentage</td>
                                      <td>
                                        <input
                                          ref={inputPacketDelayCorrelationPercentageRef}
                                          type="text"
                                          value={containerInterfaces.packetDelayCorrelationPercentage}
                                          onChange={(event) =>
                                            handleContainerInterfacePacketDelayCorrelationPercentage(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td> Packet delay distribution</td>
                                      <td>
                                        <select value={containerInterfaces.packetDelayDistribution}
                                                onChange={(e) => handleContainerInterfacePacketDelayDistribution(e, index,
                                                  interfaceIndex)} ref={inputPacketDelayDistributionRef}>
                                          <option value="0">Uniform</option>
                                          <option value="1">Normal</option>
                                          <option value="2">Pareto</option>
                                          <option value="3">Pareto normal</option>
                                        </select>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td> Packet loss type</td>
                                      <td>
                                        <select value={containerInterfaces.packetLossType}
                                                onChange={(e) => handleContainerInterfacePacketLossType(e, index,
                                                  interfaceIndex)} ref={inputPacketLossTypeRef}>
                                          <option value="0">Random</option>
                                          <option value="1">State</option>
                                          <option value="2">Gemodel</option>
                                        </select>
                                      </td>
                                    </tr>
                                    <tr
                                      key={'loss-gemodelp-' + containerInterfaces.lossGemodelp + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Loss Gemodel P</td>
                                      <td>
                                        <input
                                          ref={inputLossGemodelpRef}
                                          type="text"
                                          value={containerInterfaces.lossGemodelp}
                                          onChange={(event) =>
                                            handleContainerInterfaceLossGemodelp(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    <tr
                                      key={'loss-gemodelr-' +containerInterfaces.lossGemodelr + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Loss Gemodel R</td>
                                      <td>
                                        <input
                                          ref={inputLossGemodelrRef}
                                          type="text"
                                          value={containerInterfaces.lossGemodelr}
                                          onChange={(event) =>
                                            handleContainerInterfaceLossGemodelr(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    <tr
                                      key={'loss-gemodelk-' + containerInterfaces.lossGemodelk + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Loss Gemodel K</td>
                                      <td>
                                        <input
                                          ref={inputLossGemodelkRef}
                                          type="text"
                                          value={containerInterfaces.lossGemodelk}
                                          onChange={(event) =>
                                            handleContainerInterfaceLossGemodelk(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    <tr
                                      key={'loss-gemodelh-' + containerInterfaces.lossGemodelh + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Loss Gemodel H</td>
                                      <td>
                                        <input
                                          ref={inputLossGemodelhRef}
                                          type="text"
                                          value={containerInterfaces.lossGemodelh}
                                          onChange={(event) =>
                                            handleContainerInterfaceLossGemodelh(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    <tr
                                      key={'packet-corruption-' + containerInterfaces.packetCorruptPercentage + '-'
                                        + interfaceIndex + '-' + index}>
                                      <td> Packet corruption percentage</td>
                                      <td>
                                        <input
                                          ref={inputPacketCorruptPercentageRef}
                                          type="text"
                                          value={containerInterfaces.packetCorruptPercentage}
                                          onChange={(event) =>
                                            handleContainerInterfacePacketCorruptPercentage(event, index,
                                              interfaceIndex)}
                                        />
                                      </td>
                                    </tr>
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetCorruptCorrelationPercentage + '-'*/}
                                    {/*    + interfaceIndex + '-' + index}>*/}
                                    {/*  <td> Packet corruption correlation percentage</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketCorruptCorrelationPercentageRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetCorruptCorrelationPercentage}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketCorruptCorrelationPercentage(event, index,*/}
                                    {/*          interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetDuplicatePercentage + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet duplicate percentage</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketDuplicatePercentageRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetDuplicatePercentage}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketDuplicatePercentage(event, index,*/}
                                    {/*          interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetDuplicateCorrelationPercentage + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet duplicate correlation percentage</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketDuplicateCorrelationPercentageRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetDuplicateCorrelationPercentage}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketDuplicateCorrelationPercentage(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetReorderPercentage + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet reorder percentage</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketReorderPercentageRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetReorderPercentage}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketReorderPercentage(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetReorderCorrelationPercentage + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet reorder correlation percentage</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketReorderCorrelationPercentageRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetReorderCorrelationPercentage}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketReorderCorrelationPercentage(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetReorderGap + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet reorder gap</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketReorderGapRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetReorderGap}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketReorderGap(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.rateLimitMbitRef + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Rate limit M bit</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputRateLimitMbitRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.rateLimitMbit}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceRateLimitMbit(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.packetOverheadBytes + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Packet overhead bytes</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputPacketOverheadBytesRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.packetOverheadBytes}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfacePacketOverheadBytes(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.cellOverheadBytes + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Cell overhead bytes</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputCellOverheadBytesRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.cellOverheadBytes}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceCellOverheadBytes(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.defaultGateway + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Default gateway</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputDefaultGatewayRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.defaultGateway}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceDefaultGateway(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr>*/}
                                    {/*  <td> Firewall rule: default input</td>*/}
                                    {/*  <td>*/}
                                    {/*    <select value={containerInterfaces.defaultInput}*/}
                                    {/*            onChange={(e) => handleContainerInterfaceDefaultInput(e, index,*/}
                                    {/*              interfaceIndex)}>*/}
                                    {/*      <option value="accept">Accept</option>*/}
                                    {/*      <option value="drop">Drop</option>*/}
                                    {/*    </select>*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr>*/}
                                    {/*  <td> Firewall rule: default output</td>*/}
                                    {/*  <td>*/}
                                    {/*    <select value={containerInterfaces.defaultOutput}*/}
                                    {/*            onChange={(e) => handleContainerInterfaceDefaultOutput(e, index,*/}
                                    {/*              interfaceIndex)}>*/}
                                    {/*      <option value="accept">Accept</option>*/}
                                    {/*      <option value="drop">Drop</option>*/}
                                    {/*    </select>*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr>*/}
                                    {/*  <td> Firewall rule: default forward</td>*/}
                                    {/*  <td>*/}
                                    {/*    <select value={containerInterfaces.defaultForward}*/}
                                    {/*            onChange={(e) => handleContainerInterfaceDefaultForward(e, index,*/}
                                    {/*              interfaceIndex)}>*/}
                                    {/*      <option value="accept">Accept</option>*/}
                                    {/*      <option value="drop">Drop</option>*/}
                                    {/*    </select>*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}


                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.trafficManagerPort + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Traffic manager port</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputTrafficManagerPortRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.trafficManagerPort}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceTrafficManagerPort(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.trafficManagerLogFile + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Traffic manager log file</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputTrafficManagerLogFileRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.trafficManagerLogFile}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceTrafficManagerLogFile(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr*/}
                                    {/*  key={containerInterfaces.trafficManagerLogDir + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Traffic manager log directory</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputTrafficManagerLogDirRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.trafficManagerLogDir}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceTrafficManagerLogDir(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
                                    {/*<tr className="custom-td"*/}
                                    {/*  key={containerInterfaces.trafficManagerMaxWorkers + '-'*/}
                                    {/*    + interfaceIndex}>*/}
                                    {/*  <td> Traffic manager maximum workers</td>*/}
                                    {/*  <td>*/}
                                    {/*    <input*/}
                                    {/*      ref={inputTrafficManagerMaxWorkersRef}*/}
                                    {/*      type="text"*/}
                                    {/*      value={containerInterfaces.trafficManagerMaxWorkers}*/}
                                    {/*      onChange={(event) =>*/}
                                    {/*        handleContainerInterfaceTrafficManagerMaxWorkers(event,*/}
                                    {/*          index, interfaceIndex)}*/}
                                    {/*    />*/}
                                    {/*  </td>*/}
                                    {/*</tr>*/}
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
