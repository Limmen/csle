import React, {useState, useEffect, useCallback, useRef} from 'react'
import './CreateEmulation.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion'
import Collapse from 'react-bootstrap/Collapse'
import Select from 'react-select'
import {
    HTTP_PREFIX,
    CREATE_EMULATION_RESOURCE,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    CONTAINERS_OS,
    DEFAULT_INTERFACE_CONFIG
} from '../../Common/constants'
import serverIp from "../../Common/serverIp"
import serverPort from "../../Common/serverPort"
import {useNavigate} from "react-router-dom"
import {useAlert} from "react-alert"
import AddServices from "./AddServices/AddServices";
import AddInterfaces from "./AddInterfaces/AddInterfaces"
import AddUsers from './AddUsers/AddUsers'
import AddContainerGeneral from './AddContainerGeneral/AddContainerGeneral'
import AddEmulationGeneral from './AddEmulationGeneral/AddEmulationGeneral'
import AddVulns from './AddVulns/AddVulns'

/**
 * Component representing the /create-emulation-page
 */
const CreateEmulation = (props) => {

    // State variables
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false)
    const [containerOpen, setContainerOpen] = useState(false)
    const ip = serverIp
    const port = serverPort
    const alert = useAlert()
    const navigate = useNavigate()
    const setSessionData = props.setSessionData
    const [filteredImages, setFilteredImages] = useState([])
    const [loading, setLoading] = useState([])
    const [idsEnabled, setIdsEnabled] = useState(true)
    const [images, setImages] = useState([])
    const [selectedImage, setSelectedImage] = useState('')
    const [containers, setContainers] = useState([])
    const [showPopup, setShowPopup] = useState(false)
    const [newUser, setNewUser] = useState({userName: '', pw: '', root: "false"})
    const [newVulnCredentials, setNewVulnCredentials] = useState({vulnCredUsername: 'username', vulnCredPw: 'password',
        vulnCredRoot: "false"})
    const inputUserNameRef = useRef(null)
    const inputPwRef = useRef(null)
    const inputRootRef = useRef(null)
    const [shouldFocusUserName, setShouldFocusUserName] = useState(false)
    const [shouldFocusPw, setShouldFocusPw] = useState(false)
    const [shouldFocusRoot, setShouldFocusRoot] = useState(false)
    const [description, setDescription] = useState({description: ''})
    const [nameValue, setNameValue] = useState('')
    const [networkIdValue, setNetworkIdValue] = useState('')
    const [levelValue, setLevelValue] = useState('')
    const [versionValue, setVersionValue] = useState('')
    const [timeStepLengthValue, setTimeStepLengthValue] = useState('')
    const [newService, setNewService] = useState({name: '', protocol: '0', port: '', serviceIp: ''})
    const inputServiceProtocolRef = useRef(null)
    const inputServicePortRef = useRef(null)
    const inputServiceIpRef = useRef(null)
    const inputServiceNameRef = useRef(null)
    const [shouldFocusServiceProtocol, setShouldFocusServiceProtocol] = useState(false)
    const [shouldFocusServicePort, setShouldFocusServicePort] = useState(false)
    const [shouldFocusServiceIp, setShouldFocusServiceIp] = useState(false)
    const [shouldFocusServiceName, setShouldFocusServiceName] = useState(false)
    const [newInterface, setNewInterface] = useState(DEFAULT_INTERFACE_CONFIG)
    const inputNameRef = useRef(null)
    const inputIPRef = useRef(null)
    const inputSubnetMaskRef = useRef(null)
    const inputLimitPacketsQueueRef = useRef(null)
    const inputPacketDelayMsRef = useRef(null)
    const inputPacketDelayJitterMsRef = useRef(null)
    const inputPacketDelayCorrelationPercentageRef = useRef(null)
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
    const inputVulnCredPwForChangeRef = useRef(null)
    const inputVulnCredUsernameForChangeRef = useRef(null)
    const inputCpuRef = useRef(null)
    const inputMemRef = useRef(null)
    const inputFlagIdRef = useRef(null)
    const inputFlagScoreRef = useRef(null)
    const inputPacketDelayDistributionRef = useRef(null)
    const inputPacketLossTypeRef = useRef(null)
    const inputVulnNameRef = useRef(null)
    const inputVulnServiceNameRef = useRef(null)
    const inputVulnCredUsernameRef = useRef(null)
    const inputVulnCredPwRef = useRef(null)
    const [shouldFocusVulnName, setShouldFocusVulnName] = useState(false)
    const [shouldFocusVulnCredUsername, setShouldFocusVulnCredUsername] = useState(false)
    const [shouldFocusVulnCredPw, setShouldFocusVulnCredPw] = useState(false)
    const [shouldFocusVulnCredUsernameForChange, setShouldFocusVulnCredUsernameForChange] = useState(false)
    const [shouldFocusVulnCredPwForChange, setShouldFocusVulnCredPwForChange] = useState(false)
    const [shouldFocusName, setShouldFocusName] = useState(false)
    const [shouldFocusIP, setShouldFocusIP] = useState(false)
    const [shouldFocusSubnetMask, setShouldFocusSubnetMask] = useState(false)
    const [shouldFocusLimitPacketsQueue, setShouldFocusLimitPacketsQueue] = useState(false)
    const [shouldFocusPacketDelayMs, setShouldFocusPacketDelayMs] = useState(false)
    const [shouldFocusPacketDelayJitterMs, setShouldFocusPacketDelayJitterMs] = useState(false)
    const [shouldFocusPacketDelayCorrelationPercentage, setShouldFocusPacketDelayCorrelationPercentage] = useState(false)
    const [shouldFocusLossGemodelp, setShouldFocusLossGemodelp] = useState(false)
    const [shouldFocusLossGemodelr, setShouldFocusLossGemodelr] = useState(false)
    const [shouldFocusLossGemodelk, setShouldFocusLossGemodelk] = useState(false)
    const [shouldFocusLossGemodelh, setShouldFocusLossGemodelh] = useState(false)
    const [shouldFocusPacketCorruptPercentage, setShouldFocusPacketCorruptPercentage] = useState(false)
    const [shouldFocusPacketCorruptCorrelationPercentage, setShouldFocusPacketCorruptCorrelationPercentage]
      = useState(false)
    const [shouldFocusPacketDuplicatePercentage, setShouldFocusPacketDuplicatePercentage] = useState(false)
    const [shouldFocusPacketDuplicateCorrelationPercentage, setShouldFocusPacketDuplicateCorrelationPercentage]
      = useState(false)
    const [shouldFocusPacketReorderPercentage, setShouldFocusPacketReorderPercentage] = useState(false)
    const [shouldFocusPacketReorderCorrelationPercentage, setShouldFocusPacketReorderCorrelationPercentage]
      = useState(false)
    const [shouldFocusPacketReorderGap, setShouldFocusPacketReorderGap] = useState(false)
    const [shouldFocusRateLimitMbit, setShouldFocusRateLimitMbit] = useState(false)
    const [shouldFocusPacketOverheadBytes, setShouldFocusPacketOverheadBytes] = useState(false)
    const [shouldFocusCellOverheadBytes, setShouldFocusCellOverheadBytes] = useState(false)
    const [shouldFocusDefaultGateway, setShouldFocusDefaultGateway] = useState(false)
    const [shouldFocusTrafficManagerPort, setShouldFocusTrafficManagerPort] = useState(false)
    const [shouldFocusTrafficManagerLogFile, setShouldFocusTrafficManagerLogFile] = useState(false)
    const [shouldFocusTrafficManagerLogDir, setShouldFocusTrafficManagerLogDir] = useState(false)
    const [shouldFocusTrafficManagerMaxWorkers, setShouldFocusTrafficManagerMaxWorkers] = useState(false)
    const [shouldFocusCpu, setShouldFocusCpu] = useState(false)
    const [shouldFocusMem, setShouldFocusMem] = useState(false)
    const [shouldFocusFlagId, setShouldFocusFlagId] = useState(false)
    const [shouldFocusFlagScore, setShouldFocusFlagScore] = useState(false)
    const [shouldFocusPacketDelayDistribution, setShouldFocusPacketDelayDistribution] = useState(false)
    const [shouldFocusPacketLossType, setShouldFocusPacketLossType] = useState(false)
    const containerAndOs = Object.keys(CONTAINERS_OS).map(key => ({
        name: key,
        os: CONTAINERS_OS[key][0].os,
        label: `${key} (${CONTAINERS_OS[key][0].os})`,
        value: key
    }))
    const [newContainer, setNewContainer] = useState(containerAndOs[0])


    const handleDescriptionChange = (event) => {
        setDescription({
            description: event.target.value
        })
    }
    const handleNameChange = (event) => {
        setNameValue(event.target.value)
    }

    const handleNetworkIdChange = (event) => {
        const networkValue = event.target.value
        if (/^-?\d*$/.test(networkValue)) {
            setNetworkIdValue(event.target.value)
        }
    }

    const handleLevelChange = (event) => {
        const leveValue = event.target.value
        if (/^-?\d*$/.test(leveValue)) {
            setLevelValue(event.target.value)
        }
    }

    const handleVersionChange = (event) => {
        setVersionValue(event.target.value)
    }

    const handleTimeStepLengthChange = (event) => {
        const timeStepValue = event.target.value
        if (/^-?\d*$/.test(timeStepValue)) {
            setTimeStepLengthValue(event.target.value)
        }
    }

    const addContainer = () => {
        setShowPopup(true)
    }

    const handleClosePopup = () => {
        setShowPopup(false)
        setNewContainer({name: '', os: ''})
    }

    const handleConfirmAdd = () => {
        setContainers(prevContainers => [...prevContainers,
            {
                name: newContainer.name, os: newContainer.os, version: '', level: '', restartPolicy: '', networkId: '',
                subnetMask: '', subnetPrefix: '', cpu: '', mem: '', flagId: '', flagScore: '',
                flagPermission: true, interfaces: [], reachableByAgent: true, users: [], services: [], vulns: []
            }])
        handleClosePopup()
    }

    const handleContainerSelectChange = (selectedContainer) => {
        // const selectedOption = JSON.parse(e.target.value)
        // setNewContainer({name: selectedOption.name, os: selectedOption.os})
        setNewContainer(selectedContainer)
    }

    const deleteContainer = (index) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            updatedContainers.splice(index, 1)
            return updatedContainers
        })
    }

    const toggleContainerAccordion = (index) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            updatedContainers[index] = {
                ...updatedContainers[index],
                containerAccordionOpen: !updatedContainers[index].containerAccordionOpen
            }
            return updatedContainers
        })
    }

    const handleContainerFlagPermissionChange = (permissionValue, index) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            updatedContainers[index] = {
                ...updatedContainers[index],
                flagPermission: permissionValue
            }
            return updatedContainers
        })
    }

    const handleContainerIdsEnabledChange = (idsValue) => {
        setIdsEnabled(idsValue)
    }

    const handleContainerReachableByAgentChange = (reachableValue, index) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            updatedContainers[index] = {
                ...updatedContainers[index],
                reachableByAgent: reachableValue
            }
            return updatedContainers
        })
    }
    const deFocus = () => {
        setShouldFocusUserName(false)
        setShouldFocusPw(false)
        setShouldFocusRoot(false)
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
        setShouldFocusPacketDelayJitterMs(false)
        setShouldFocusPacketDelayMs(false)
        setShouldFocusLimitPacketsQueue(false)
        setShouldFocusSubnetMask(false)
        setShouldFocusIP(false)
        setShouldFocusName(false)
        setShouldFocusDefaultGateway(false)
        setShouldFocusTrafficManagerPort(false)
        setShouldFocusTrafficManagerLogFile(false)
        setShouldFocusTrafficManagerLogDir(false)
        setShouldFocusTrafficManagerMaxWorkers(false)
        setShouldFocusMem(false)
        setShouldFocusFlagId(false)
        setShouldFocusFlagScore(false)
        setShouldFocusCpu(false)
        setShouldFocusPacketDelayDistribution(false)
        setShouldFocusPacketLossType(false)
        setShouldFocusServiceIp(false)
        setShouldFocusServicePort(false)
        setShouldFocusServiceProtocol(false)
        setShouldFocusVulnName(false)
        setShouldFocusServiceName(false)
        setShouldFocusVulnCredUsername(false)
        setShouldFocusVulnCredPw(false)
        setShouldFocusVulnCredUsernameForChange(false)
        setShouldFocusVulnCredPwForChange(false)
    }

    const createEmulationRequest = useCallback(() => {
      /**
       * Makes a reqeust to the REST API backend to create the new emulation
       *
       * @type {(function(): void)|*}
       */
      const requestData = {
          // Include state values here
          emulationName: nameValue,
          emulationNetworkId: networkIdValue,
          emulationLevel: levelValue,
          emulationVersion: versionValue,
          emulationTimeStepLength: timeStepLengthValue,
          emulationIdsEnabled: idsEnabled,
          emulationDescription: description,
          emulationContainer: containers,
      };

      fetch(
        `${HTTP_PREFIX}${ip}:${port}/${CREATE_EMULATION_RESOURCE}?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
        {
          method: "POST",
          headers: new Headers({
            Accept: "application/vnd.github.cloak-preview"
          }),

            body: JSON.stringify(requestData),
        }

      )
        .then(res => {
          if(res.status === 401) {
            alert.show("Session token expired. Please login again.")
            setSessionData(null)
            navigate(`/${LOGIN_PAGE_RESOURCE}`)
            return null
          }
          return res.json()
        })
        .then(response => {
          if(response === null) {
            return
          }
          console.log("Backend request was successful")
        })
        .catch(error => console.log("error:" + error))
    }, [alert, ip, navigate, port, props.sessionData, setSessionData, nameValue, networkIdValue, levelValue,
        versionValue, timeStepLengthValue, idsEnabled, description, containers])


    const handleContainerUserNameChange = (event, containerIndex, userIndex) => {
        const userNameValue = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedUsers = [...containerToUpdate.users]
            updatedUsers[userIndex] = {
                ...updatedUsers[userIndex],
                userName: userNameValue
            }
            containerToUpdate.users = updatedUsers
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusUserName(true)
    }

    const handleContainerVulnNameChange = (event, containerIndex, vulnIndex) => {
        const vulnNameValue = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedVulns = [...containerToUpdate.vulns]
            updatedVulns[vulnIndex] = {
                ...updatedVulns[vulnIndex],
                vulnName: vulnNameValue
            }
            containerToUpdate.vulns = updatedVulns
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusVulnName(true)
    }

    const handleContainerVulnAccessChange = (vulnAccessValue, containerIndex, vulnIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedVulns = [...containerToUpdate.vulns]
            updatedVulns[vulnIndex] = {
                ...updatedVulns[vulnIndex],
                vulnRoot: vulnAccessValue
            }
            containerToUpdate.vulns = updatedVulns
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
    }
    const handleContainerVulnTypeChange = (vulnTypeValue, containerIndex, vulnIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedVulns = [...containerToUpdate.vulns]
            updatedVulns[vulnIndex] = {
                ...updatedVulns[vulnIndex],
                vulnType: vulnTypeValue
            }
            containerToUpdate.vulns = updatedVulns
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
    }


    const handleContainerUserPwChange = (event, containerIndex, userIndex) => {
        const PwValue = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedUsers = [...containerToUpdate.users]
            updatedUsers[userIndex] = {
                ...updatedUsers[userIndex],
                pw: PwValue
            }
            containerToUpdate.users = updatedUsers
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPw(true)
    }

    const handleContainerUserAccessChange = (userAccessValue, containerIndex, userIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedUsers = [...containerToUpdate.users]
            updatedUsers[userIndex] = {
                ...updatedUsers[userIndex],
                root: userAccessValue
            }
            containerToUpdate.users = updatedUsers
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusUserName(true)
    }

    const handleContainerServiceProtocolChange = (newProtocol, containerIndex, serviceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedServices = [...containerToUpdate.services]
            updatedServices[serviceIndex] = {
                ...updatedServices[serviceIndex],
                protocol: newProtocol
            }
            containerToUpdate.services = updatedServices
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusServiceProtocol(true)
    }

    const handleContainerServicePortChange = (event, containerIndex, serviceIndex) => {
        const newPort = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedServices = [...containerToUpdate.services]
            updatedServices[serviceIndex] = {
                ...updatedServices[serviceIndex],
                port: newPort
            }
            containerToUpdate.services = updatedServices
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusServicePort(true)
    }

    const handleContainerServiceIpChange = (event, containerIndex, serviceIndex) => {
        const newServiceIp = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedServices = [...containerToUpdate.services]
            updatedServices[serviceIndex] = {
                ...updatedServices[serviceIndex],
                serviceIp: newServiceIp
            }
            containerToUpdate.services = updatedServices
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusServiceIp(true)
    }

    const handleContainerVulnServiceChange = (event, containerIndex, vulnIndex) => {
        const newVulnService = event.target.value

        setContainers(prevContainers => {
            const updatedContainers = prevContainers.map((container, index) => {
                if (index === containerIndex) {
                    const updatedVulns = container.vulns.map((vuln, vIndex) => {
                        if (vIndex === vulnIndex) {
                            return {
                                ...vuln,
                                vulnService: newVulnService
                            };
                        }
                        return vuln;
                    });
                    return {
                        ...container,
                        vulns: updatedVulns
                    };
                }
                return container;
            });
            return updatedContainers;
        });
        deFocus()
    };

    const handleContainerServiceNameChange = (event, containerIndex, serviceIndex) => {
        const newServiceName = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedServices = [...containerToUpdate.services]
            updatedServices[serviceIndex] = {
                ...updatedServices[serviceIndex],
                name: newServiceName
            }
            containerToUpdate.services = updatedServices
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusServiceName(true)
    }

    const handleContainerCpuChange = (event, index) => {
        const cpuValue = event.target.value
        if (/^-?\d*$/.test(cpuValue)) {
            setContainers(prevContainers => {
                const updatedContainers = [...prevContainers]
                updatedContainers[index] = {
                    ...updatedContainers[index],
                    cpu: cpuValue
                }
                return updatedContainers
            })
        }
        deFocus()
        setShouldFocusCpu(true)
    }


    const handleContainerMemoryChange = (event, index) => {
        const memValue = event.target.value
        if (/^-?\d*$/.test(memValue)) {
            setContainers(prevContainers => {
                const updatedContainers = [...prevContainers]
                updatedContainers[index] = {
                    ...updatedContainers[index],
                    mem: memValue
                }
                return updatedContainers
            })
        }
        deFocus()
        setShouldFocusMem(true)
    }


    const handleContainerFlagIdChange = (event, index) => {
        const flagIdValue = event.target.value
        if (/^-?\d*$/.test(flagIdValue)) {
            setContainers(prevContainers => {
                const updatedContainers = [...prevContainers]
                updatedContainers[index] = {
                    ...updatedContainers[index],
                    flagId: flagIdValue
                }
                return updatedContainers
            })
        }
        deFocus()
        setShouldFocusFlagId(true)
    }


    const handleContainerFlagScoreChange = (event, index) => {
        const flagScoreValue = event.target.value
        if (/^-?\d*$/.test(flagScoreValue)) {
            setContainers(prevContainers => {
                const updatedContainers = [...prevContainers]
                updatedContainers[index] = {
                    ...updatedContainers[index],
                    flagScore: flagScoreValue
                }
                return updatedContainers
            })
        }
        deFocus()
        setShouldFocusFlagScore(true)
    }

    const handleContainerInterfaceNameChange = (event, containerIndex, interfaceIndex) => {
        const newName = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                name: newName
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusName(true)
    }

    const handleContainerInterfaceIPChange = (event, containerIndex, interfaceIndex) => {
        const newIP = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                ip: newIP
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusIP(true)
    }

    const handleContainerInterfaceSubnetMaskChange = (event, containerIndex, interfaceIndex) => {
        const newSubnetMask = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                subnetMask: newSubnetMask
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusSubnetMask(true)
    }

    const handleContainerInterfaceLimitPacketsQueueChange = (event, containerIndex, interfaceIndex) => {
        const newLimitPacketsQueue = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                limitPacketsQueue: newLimitPacketsQueue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusLimitPacketsQueue(true)
    }

    const handleContainerInterfacePacketDelayMs = (event, containerIndex, interfaceIndex) => {
        const newPacketDelayMs = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDelayMs: newPacketDelayMs
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDelayMs(true)
    }

    const handleContainerInterfacePacketDelayJitterMs = (event, containerIndex, interfaceIndex) => {
        const newPacketDelayJitterMs = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDelayJitterMs: newPacketDelayJitterMs
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDelayJitterMs(true)
    }

    const handleContainerInterfacePacketDelayCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketDelayCorrelationPercentage = event.target.value

        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces];
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDelayCorrelationPercentage: newPacketDelayCorrelationPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDelayCorrelationPercentage(true)
    }

    const handleContainerInterfaceLossGemodelp = (event, containerIndex, interfaceIndex) => {
        const newLossGemodelp = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                lossGemodelp: newLossGemodelp
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusLossGemodelp(true)
    }

    const handleContainerInterfaceLossGemodelr = (event, containerIndex, interfaceIndex) => {
        const newLossGemodelr = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                lossGemodelr: newLossGemodelr
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusLossGemodelr(true)
    }

    const handleContainerInterfaceLossGemodelk = (event, containerIndex, interfaceIndex) => {
        const newLossGemodelk = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                lossGemodelk: newLossGemodelk
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusLossGemodelk(true)
    }
    const handleContainerInterfaceLossGemodelh = (event, containerIndex, interfaceIndex) => {
        const newLossGemodelh = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                lossGemodelh: newLossGemodelh
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusLossGemodelh(true)
    }

    const handleContainerInterfacePacketCorruptPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketCorruptPercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetCorruptPercentage: newPacketCorruptPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketCorruptPercentage(true)
    }

    const handleContainerInterfacePacketCorruptCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketCorruptCorrelationPercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetCorruptCorrelationPercentage: newPacketCorruptCorrelationPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketCorruptCorrelationPercentage(true)
    }

    const handleContainerInterfacePacketDuplicatePercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketDuplicatePercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDuplicatePercentage: newPacketDuplicatePercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDuplicatePercentage(true)
    }

    const handleContainerInterfacePacketDuplicateCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketDuplicateCorrelationPercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDuplicateCorrelationPercentage: newPacketDuplicateCorrelationPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDuplicateCorrelationPercentage(true)
    }

    const handleContainerInterfacePacketReorderPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketReorderPercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetReorderPercentage: newPacketReorderPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketReorderPercentage(true)
    }

    const handleContainerInterfacePacketReorderCorrelationPercentage = (event, containerIndex, interfaceIndex) => {
        const newPacketReorderCorrelationPercentage = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetReorderCorrelationPercentage: newPacketReorderCorrelationPercentage
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketReorderCorrelationPercentage(true)
    }

    const handleContainerInterfacePacketReorderGap = (event, containerIndex, interfaceIndex) => {
        const newPacketReorderGap = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetReorderGap: newPacketReorderGap
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketReorderGap(true)
    }

    const handleContainerInterfaceRateLimitMbit = (event, containerIndex, interfaceIndex) => {
        const newRateLimitMbit = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                rateLimitMbit: newRateLimitMbit
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusRateLimitMbit(true)
    }

    const handleContainerInterfacePacketOverheadBytes = (event, containerIndex, interfaceIndex) => {
        const newPacketOverheadBytes = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetOverheadBytes: newPacketOverheadBytes
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketOverheadBytes(true)
    }

    const handleContainerInterfaceCellOverheadBytes = (event, containerIndex, interfaceIndex) => {
        const newCellOverheadBytes = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                cellOverheadBytes: newCellOverheadBytes
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusCellOverheadBytes(true)
    }

    const handleContainerInterfaceDefaultGateway = (event, containerIndex, interfaceIndex) => {
        const newDefaultGateway = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                defaultGateway: newDefaultGateway
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusDefaultGateway(true)
    }

    const handleContainerInterfaceTrafficManagerPort = (event, containerIndex, interfaceIndex) => {
        const newTrafficManagerPort = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                trafficManagerPort: newTrafficManagerPort
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusTrafficManagerPort(true)
    }

    const handleContainerInterfaceTrafficManagerLogFile = (event, containerIndex, interfaceIndex) => {
        const newTrafficManagerLogFile = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                trafficManagerLogFile: newTrafficManagerLogFile
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusTrafficManagerLogFile(true)
    }

    const handleContainerInterfaceTrafficManagerLogDir = (event, containerIndex, interfaceIndex) => {
        const newTrafficManagerLogDir = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                trafficManagerLogDir: newTrafficManagerLogDir
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusTrafficManagerLogDir(true)
    }

    const handleContainerInterfaceTrafficManagerMaxWorkers = (event, containerIndex, interfaceIndex) => {
        const newTrafficManagerMaxWorkers = event.target.value
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                trafficManagerMaxWorkers: newTrafficManagerMaxWorkers
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate

            return updatedContainers
        })
        deFocus()
        setShouldFocusTrafficManagerMaxWorkers(true)
    }

    // Use useEffect to focus on the input field when containers state changes
    useEffect(() => {
        if (inputNameRef.current && shouldFocusName) {
            inputNameRef.current.focus()
        } else if (inputIPRef.current && shouldFocusIP) {
            inputIPRef.current.focus()
        } else if (inputSubnetMaskRef.current && shouldFocusSubnetMask) {
            inputSubnetMaskRef.current.focus()
        } else if (inputLimitPacketsQueueRef.current && shouldFocusLimitPacketsQueue) {
            inputLimitPacketsQueueRef.current.focus()
        } else if (inputPacketDelayMsRef.current && shouldFocusPacketDelayMs) {
            inputPacketDelayMsRef.current.focus()
        } else if (inputPacketDelayJitterMsRef.current && shouldFocusPacketDelayJitterMs) {
            inputPacketDelayJitterMsRef.current.focus()
        } else if (inputPacketDelayCorrelationPercentageRef.current && shouldFocusPacketDelayCorrelationPercentage) {
            inputPacketDelayCorrelationPercentageRef.current.focus()
        } else if (inputLossGemodelpRef.current && shouldFocusLossGemodelp) {
            inputLossGemodelpRef.current.focus()
        } else if (inputLossGemodelrRef.current && shouldFocusLossGemodelr) {
            inputLossGemodelrRef.current.focus()
        } else if (inputLossGemodelkRef.current && shouldFocusLossGemodelk) {
            inputLossGemodelkRef.current.focus()
        } else if (inputLossGemodelhRef.current && shouldFocusLossGemodelh) {
            inputLossGemodelhRef.current.focus()
        } else if (inputPacketCorruptPercentageRef.current && shouldFocusPacketCorruptPercentage) {
            inputPacketCorruptPercentageRef.current.focus()
        } else if (inputPacketCorruptCorrelationPercentageRef.current && shouldFocusPacketCorruptCorrelationPercentage) {
            inputPacketCorruptCorrelationPercentageRef.current.focus()
        } else if (inputPacketDuplicatePercentageRef.current && shouldFocusPacketDuplicatePercentage) {
            inputPacketDuplicatePercentageRef.current.focus()
        } else if (inputPacketDuplicateCorrelationPercentageRef.current && shouldFocusPacketDuplicateCorrelationPercentage) {
            inputPacketDuplicateCorrelationPercentageRef.current.focus()
        } else if (inputPacketReorderPercentageRef.current && shouldFocusPacketReorderPercentage) {
            inputPacketReorderPercentageRef.current.focus()
        } else if (inputPacketReorderCorrelationPercentageRef.current && shouldFocusPacketReorderCorrelationPercentage) {
            inputPacketReorderCorrelationPercentageRef.current.focus()
        } else if (inputPacketReorderGapRef.current && shouldFocusPacketReorderGap) {
            inputPacketReorderGapRef.current.focus()
        } else if (inputRateLimitMbitRef.current && shouldFocusRateLimitMbit) {
            inputRateLimitMbitRef.current.focus()
        } else if (inputPacketOverheadBytesRef.current && shouldFocusPacketOverheadBytes) {
            inputPacketOverheadBytesRef.current.focus()
        } else if (inputCellOverheadBytesRef.current && shouldFocusCellOverheadBytes) {
            inputCellOverheadBytesRef.current.focus()
        } else if (inputCpuRef.current && shouldFocusCpu) {
            inputCpuRef.current.focus()
        } else if (inputMemRef.current && shouldFocusMem) {
            inputMemRef.current.focus()
        } else if (inputFlagIdRef.current && shouldFocusFlagId) {
            inputFlagIdRef.current.focus()
        } else if (inputFlagScoreRef.current && shouldFocusFlagScore) {
            inputFlagScoreRef.current.focus()
        } else if (inputDefaultGatewayRef.current && shouldFocusDefaultGateway) {
            inputDefaultGatewayRef.current.focus()
        } else if (inputTrafficManagerPortRef.current && shouldFocusTrafficManagerPort) {
            inputTrafficManagerPortRef.current.focus()
        } else if (inputTrafficManagerLogDirRef.current && shouldFocusTrafficManagerLogDir) {
            inputTrafficManagerLogDirRef.current.focus()
        } else if (inputTrafficManagerLogFileRef.current && shouldFocusTrafficManagerLogFile) {
            inputTrafficManagerLogFileRef.current.focus()
        } else if (inputTrafficManagerMaxWorkersRef.current && shouldFocusTrafficManagerMaxWorkers) {
            inputTrafficManagerMaxWorkersRef.current.focus()
        } else if (inputPacketDelayDistributionRef.current && shouldFocusPacketDelayDistribution) {
            inputPacketDelayDistributionRef.current.focus()
        } else if (inputPacketLossTypeRef.current && shouldFocusPacketLossType) {
            inputPacketLossTypeRef.current.focus()
        } else if (inputUserNameRef.current && shouldFocusUserName) {
            inputUserNameRef.current.focus()
        } else if (inputPwRef.current && shouldFocusPw) {
            inputPwRef.current.focus()
        } else if (inputRootRef.current && shouldFocusRoot) {
            inputRootRef.current.focus()
        } else if (inputServiceIpRef.current && shouldFocusServiceIp) {
            inputServiceIpRef.current.focus()
        } else if (inputServicePortRef.current && shouldFocusServicePort) {
            inputServicePortRef.current.focus()
        } else if (inputServiceProtocolRef.current && shouldFocusServiceProtocol) {
            inputServiceProtocolRef.current.focus()
        } else if (inputServiceNameRef.current && shouldFocusServiceName) {
            inputServiceNameRef.current.focus()
        } else if (inputVulnNameRef.current && shouldFocusVulnName) {
            inputVulnNameRef.current.focus()
        } else if (inputVulnServiceNameRef.current && shouldFocusVulnName) {
            inputVulnServiceNameRef.current.focus()
        } else if (inputVulnCredUsernameRef.current && shouldFocusVulnCredUsername) {
            inputVulnCredUsernameRef.current.focus()
        } else if (inputVulnCredPwRef.current && shouldFocusVulnCredPw) {
            inputVulnCredPwRef.current.focus()
        }
        else if (inputVulnCredPwForChangeRef.current && shouldFocusVulnCredPwForChange) {
            inputVulnCredPwForChangeRef.current.focus()
        }
        else if (inputVulnCredUsernameForChangeRef.current && shouldFocusVulnCredUsernameForChange) {
            inputVulnCredUsernameForChangeRef.current.focus()
        }
    }, [containers, shouldFocusName, shouldFocusIP, shouldFocusSubnetMask, shouldFocusLimitPacketsQueue,
        shouldFocusPacketDelayMs, shouldFocusPacketDelayJitterMs, shouldFocusPacketDelayCorrelationPercentage,
        shouldFocusLossGemodelp, shouldFocusLossGemodelr, shouldFocusLossGemodelk, shouldFocusLossGemodelh,
        shouldFocusPacketCorruptPercentage, shouldFocusPacketCorruptCorrelationPercentage,
        shouldFocusPacketDuplicatePercentage, shouldFocusPacketDuplicateCorrelationPercentage,
        shouldFocusPacketReorderPercentage, shouldFocusPacketReorderCorrelationPercentage, shouldFocusPacketReorderGap,
        shouldFocusRateLimitMbit, shouldFocusPacketOverheadBytes, shouldFocusCellOverheadBytes,
        shouldFocusCpu, shouldFocusFlagId, shouldFocusMem, shouldFocusFlagScore, shouldFocusDefaultGateway,
        shouldFocusTrafficManagerPort, shouldFocusTrafficManagerLogDir, shouldFocusTrafficManagerLogFile,
        shouldFocusTrafficManagerMaxWorkers, shouldFocusPacketDelayDistribution, shouldFocusPacketLossType,
        shouldFocusUserName, shouldFocusPw, shouldFocusRoot, shouldFocusServiceIp, shouldFocusServicePort,
        shouldFocusServiceProtocol, shouldFocusServiceName, shouldFocusVulnName, shouldFocusVulnCredUsername,
        shouldFocusVulnCredPw, shouldFocusVulnCredPwForChange, shouldFocusVulnCredUsernameForChange])

    const handleContainerInterfacePacketDelayDistribution = (packetDelayDistributionValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetDelayDistribution: packetDelayDistributionValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketDelayDistribution(true)
    }

    const handleContainerInterfacePacketLossType = (packetLossTypeValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                packetLossType: packetLossTypeValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
        deFocus()
        setShouldFocusPacketLossType(true)
    }

    const handleContainerInterfaceDefaultInput = (defaultInputValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                defaultInput: defaultInputValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
    }

    const handleContainerInterfaceDefaultOutput = (defaultOutputValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                defaultOutput: defaultOutputValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
    }

    const handleContainerInterfaceDefaultForward = (defaultForwardValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                defaultForward: defaultForwardValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
    }

    const handleAddContainerUser = (containerIndex) => {
        const userToAdd = {
            userName: '',
            pw: '',
            root: "False"
        }
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            if (containerIndex >= 0 && containerIndex < updatedContainers.length) {
                const container = updatedContainers[containerIndex]
                const userExists = container.users.some(existingUser =>
                  existingUser.userName === userToAdd.userName
                )
                if (!userExists) {
                    container.users.push(userToAdd)
                }
            }
            return updatedContainers
        })
    }

    const handleAddContainerService = (containerIndex) => {
        const serviceToAdd = {
            name: 'Service name',
            protocol: '0',
            port: '',
            serviceIp: ''
        }
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            if (containerIndex >= 0 && containerIndex < updatedContainers.length) {
                const container = updatedContainers[containerIndex]
                const serviceExists = container.services.some(existingService =>
                  existingService.name === serviceToAdd.name
                )
                if (!serviceExists) {
                    container.services.push(serviceToAdd)
                }
            }
            return updatedContainers
        })
        deFocus()
    }

    const handleAddVulnCredentials = (containerIndex, vulnIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers];
            const selectedVuln = updatedContainers[containerIndex].vulns[vulnIndex];

            // Check if the credential already exists
            const existingCredential = selectedVuln.vulnCredentials.find(cred =>
              cred.vulnCredUsername === newVulnCredentials.vulnCredUsername &&
              cred.vulnCredPw === newVulnCredentials.vulnCredPw &&
              cred.vulnCredRoot === newVulnCredentials.vulnCredRoot
            );

            // If the credential doesn't exist, add it
            if (!existingCredential) {
                selectedVuln.vulnCredentials = [...selectedVuln.vulnCredentials, newVulnCredentials];
            }

            return updatedContainers;
        });

        // Optionally, reset the newVulnCredentials after adding
        setNewVulnCredentials({ vulnCredUsername: 'username', vulnCredPw: 'password', vulnCredRoot: 'False' });
        deFocus()
    };

    const handleVulnCredentialChange = (value, containerIndex, vulnIndex, credIndex, fieldName) => {

        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers];
            const selectedVuln = updatedContainers[containerIndex].vulns[vulnIndex];
            const updatedCredentials = [...selectedVuln.vulnCredentials];

            // Update the specified field of the credential with the given index
            if (credIndex >= 0 && credIndex < updatedCredentials.length) {
                updatedCredentials[credIndex][fieldName] = value;
                selectedVuln.vulnCredentials = updatedCredentials;

                return updatedContainers;
            }

            // If the credential index is invalid, return the previous state
            return prevContainers;
        });
    };


    const handleDeleteVulnCredential = (containerIndex, vulnIndex, credentialIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers];
            const selectedVuln = updatedContainers[containerIndex].vulns[vulnIndex];
            const updatedCredentials = [...selectedVuln.vulnCredentials];

            // Remove the credential from the array
            updatedCredentials.splice(credentialIndex, 1);
            selectedVuln.vulnCredentials = updatedCredentials;

            return updatedContainers;
        });
    };


    const handleNewCredentialChange = (event) => {
        const { name, value } = event.target;
        setNewVulnCredentials((prevCredentials) => ({
            ...prevCredentials,
            [name]: value,
        }));
        deFocus()
        if (name === 'vulnCredPw') {
            setShouldFocusVulnCredPw(true)
        } else if (name === 'vulnCredUsername') {
            setShouldFocusVulnCredUsername(true)
        }
    };

    const handleAddContainerVulns = (containerIndex) => {
        const vulnsToAdd = {
            vulnName: 'Vulnerability name',
            vulnType: '',
            vulnService: '',
            vulnRoot: '',
            vulnCredentials: []
        };

        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers];

            if (containerIndex >= 0 && containerIndex < updatedContainers.length)
            {
                const container = updatedContainers[containerIndex];

                // Check if the vulnerability exist

                const vulnExists = container.vulns.some(existingVuln =>
                  existingVuln.vulnName === vulnsToAdd.vulnName
                )

                if (!vulnExists)
                {
                    // Add the new vulnerability only if none exists
                    container.vulns.push(vulnsToAdd);
                }
            }

            return updatedContainers;
        });

        // Ensure that the following actions are only taken when the function is explicitly called
        deFocus();
    };




    const handleDeleteContainerUser = (containerIndex, userIndex) => {
        setContainers(prevContainers => {
            return prevContainers.map((container, index) => {
                if (index === containerIndex) {
                    const updatedUsers = container.users.filter(
                      (_, i) => i !== userIndex
                    )
                    return {...container, users: updatedUsers}
                }
                return container
            })
        })
        deFocus()
    }

    const handleDeleteContainerService = (containerIndex, serviceIndex) => {
        setContainers(prevContainers => {
            return prevContainers.map((container, index) => {
                if (index === containerIndex) {
                    const updatedService = container.services.filter(
                      (_, i) => i !== serviceIndex
                    )
                    return {...container, services: updatedService}
                }
                return container
            })
        })
        deFocus()
    }

    const handleDeleteContainerVuln = (containerIndex, vulnIndex) => {
        setContainers(prevContainers => {
            return prevContainers.map((container, index) => {
                if (index === containerIndex) {
                    const updatedVuln = container.vulns.filter(
                      (_, i) => i !== vulnIndex
                    )
                    return {...container, vulns: updatedVuln}
                }
                return container
            })
        })
        deFocus()
    }


    const handleAddContainerInterface = (containerIndex) => {
        const interfaceToAdd = {
            name: 'New interface',
            ip: '0.0.0.0',
            subnetMask: '255.255.255.0',
            subnetPrefix: '',
            physicalInterface: 'eth0',
            bitmask: '255.255.255.0',
            limitPacketsQueue: 30000,
            packetDelayMs: 2,
            packetDelayJitterMs: 0.5,
            packetDelayCorrelationPercentage: 25,
            packetDelayDistribution: '0',
            packetLossType: '0',
            lossGemodelp: '0.02',
            lossGemodelr: '0.97',
            lossGemodelk: '0.98',
            lossGemodelh: '0.0001',
            packetCorruptPercentage: "0.00001",
            packetCorruptCorrelationPercentage: "25",
            packetDuplicatePercentage: "0.00001",
            packetDuplicateCorrelationPercentage: "25",
            packetReorderPercentage: "0.0025",
            packetReorderCorrelationPercentage: "25",
            packetReorderGap: "5",
            rateLimitMbit: "1000",
            packetOverheadBytes: "0",
            cellOverheadBytes: "0",
            defaultGateway: "0.0.0.0",
            defaultInput: "accept",
            defaultOutput: "accept",
            defaultForward: "drop",
            trafficManagerPort: "50043",
            trafficManagerLogFile: "traffic_manager.log",
            trafficManagerLogDir: "/",
            trafficManagerMaxWorkers: "10"
        }

        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            if (containerIndex >= 0 && containerIndex < updatedContainers.length) {
                const container = updatedContainers[containerIndex]
                const interfaceExists = container.interfaces.some(existingInterface =>
                  existingInterface.name === interfaceToAdd.name
                )
                if (!interfaceExists) {
                    container.interfaces.push(interfaceToAdd)
                }
            }
            return updatedContainers
        })
        deFocus()
    }

    const handleDeleteContainerInterface = (containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            return prevContainers.map((container, index) => {
                if (index === containerIndex) {
                    const updatedInterfaces = container.interfaces.filter(
                      (_, i) => i !== interfaceIndex
                    )
                    return {...container, interfaces: updatedInterfaces}
                }
                return container
            })
        })
    }

    const handleContainerNetworkPhysicalInterface = (physicalInterfaceValue, containerIndex, interfaceIndex) => {
        setContainers(prevContainers => {
            const updatedContainers = [...prevContainers]
            const containerToUpdate = {...updatedContainers[containerIndex]}
            const updatedInterfaces = [...containerToUpdate.interfaces]
            updatedInterfaces[interfaceIndex] = {
                ...updatedInterfaces[interfaceIndex],
                physicalInterface: physicalInterfaceValue
            }
            containerToUpdate.interfaces = updatedInterfaces
            updatedContainers[containerIndex] = containerToUpdate
            return updatedContainers
        })
    }


    return (
      <div className="CreateEmulation">
          <h3 className="managementTitle"> Create Emulation </h3>
          <div>
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
                                  <i className="fa fa-file-text headerIcon" aria-hidden="true"/>
                              </h5>
                          </Button>
                      </Card.Header>
                      <Collapse in={generalInfoOpen}>
                          <div id="generalInfoBody" className="cardBodyHidden">
                              <AddEmulationGeneral nameValue={nameValue}
                                                   handleNameChange={handleNameChange}
                                                   networkIdValue={networkIdValue}
                                                   handleNetworkIdChange={handleNetworkIdChange}
                                                   levelValue={levelValue}
                                                   handleLevelChange={handleLevelChange}
                                                   versionValue={versionValue}
                                                   handleVersionChange={handleVersionChange}
                                                   timeStepLengthValue={timeStepLengthValue}
                                                   handleTimeStepLengthChange={handleTimeStepLengthChange}
                                                   idsEnabled={idsEnabled}
                                                   handleContainerIdsEnabledChange={handleContainerIdsEnabledChange}
                                                   description={description}
                                                   handleDescriptionChange={handleDescriptionChange}
                              />
                          </div>
                      </Collapse>
                  </Card>
              </Accordion>
              <Accordion defaultActiveKey="1" className="containersAccord">
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
                                  <i className="fa fa-cubes headerIcon" aria-hidden="true"/>
                              </h5>
                          </Button>
                      </Card.Header>
                      <Collapse in={containerOpen} className="containersCollapse">
                          <div id="container" className="cardBodyHidden">
                              <div>
                                  Add a new container &nbsp;&nbsp;
                                  <Button onClick={addContainer}
                                          variant="success" size="sm">
                                      <i className="fa fa-plus" aria-hidden="true" />
                                  </Button>
                                  <div style={{ margin: '20px'}} className="row">
                                      {showPopup && (
                                          <div className="ContainerImageSelection">
                                              <div className="traceTypeSelection inline-block">
                                                  <div className="conditionalDist inline-block conditionalLabel">
                                                      Container image:
                                                  </div>
                                                  <div className="conditionalDist inline-block" style={{width: "500px"}}>
                                                      <Select
                                                          value={newContainer}
                                                          defaultValue={newContainer}
                                                          options={containerAndOs}
                                                          onChange={handleContainerSelectChange}
                                                          placeholder="Container Operating System"
                                                          menuPlacement="bottom"
                                                          className="containerImageDropdown"
                                                      />
                                                  </div>
                                                  <div className="conditionalDist inline-block">
                                                      <Button onClick={handleConfirmAdd}  variant="primary" size="sm" className="confirmContainer inline-block">
                                                          <i className="fa fa-check" aria-hidden="true" />
                                                      </Button>
                                                      <Button onClick={handleClosePopup} variant="danger" size="sm" className="removeContainer inline-block">
                                                          <i className="fa fa-times" aria-hidden="true" />
                                                      </Button>
                                                  </div>
                                              </div>
                                          </div>)}
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
                                                        <i className="fa fa-cube headerIcon" aria-hidden="true"/>
                                                    </h5>
                                                </Button>
                                            </Card.Header>
                                            <Collapse in={container.containerAccordionOpen}>
                                                <div id="eachContainer" className="cardBodyHidden">
                                                    <div>
                                                        Delete the container {containers[index].name} &nbsp;&nbsp;
                                                        <Button onClick={() => deleteContainer(index)}
                                                                variant="danger" size="sm">
                                                            <i className="fa fa-trash startStopIcon"
                                                               aria-hidden="true" />
                                                        </Button>
                                                        <AddContainerGeneral container={containers[index]}
                                                                             handleCpuChange={handleContainerCpuChange}
                                                                             containerIndex={index}
                                                                             handleMemoryChange={handleContainerMemoryChange}
                                                                             handleFlagIdChange={handleContainerFlagIdChange}
                                                                             handleFlagScoreChange={handleContainerFlagScoreChange}
                                                                             handleFlagPermissionChange={handleContainerFlagPermissionChange}
                                                                             handleReachableByAgentChange={handleContainerReachableByAgentChange}
                                                        />

                                                        <AddUsers container={containers[index]}
                                                                  handleAddUser={handleAddContainerUser}
                                                                  containerIndex={index}
                                                                  inputUserNameRef={inputUserNameRef}
                                                                  handleContainerUserNameChange={handleContainerUserNameChange}
                                                                  handleDeleteContainerUser={handleDeleteContainerUser}
                                                                  inputPwRef={inputPwRef}
                                                                  handleContainerUserPwChange={handleContainerUserPwChange}
                                                                  handleContainerUserAccessChange={handleContainerUserAccessChange}
                                                        />

                                                        <AddInterfaces container={containers[index]}
                                                                       addInterfaceHandler={handleAddContainerInterface}
                                                                       containerIndex={index}
                                                                       handleInterfaceNameChange={handleContainerInterfaceNameChange}
                                                                       deleteInterfaceHandler={handleDeleteContainerInterface}
                                                                       handleIPChange={handleContainerInterfaceIPChange}
                                                                       handleSubnetMaskChange={handleContainerInterfaceSubnetMaskChange}
                                                                       handleNetworkPhysicalInterface={handleContainerNetworkPhysicalInterface}
                                                                       handleLimitPacketsQueueChange={handleContainerInterfaceLimitPacketsQueueChange}
                                                                       handlePacketDelayMs={handleContainerInterfacePacketDelayMs}
                                                                       handlePacketDelayJitterMs={handleContainerInterfacePacketDelayJitterMs}
                                                                       handlePacketDelayCorrelationPercentage={handleContainerInterfacePacketDelayCorrelationPercentage}
                                                                       handlePacketDelayDistribution={handleContainerInterfacePacketDelayDistribution}
                                                                       handlePacketLossType={handleContainerInterfacePacketLossType}
                                                                       handleLossGemodelp={handleContainerInterfaceLossGemodelp}
                                                                       handleLossGemodelr={handleContainerInterfaceLossGemodelr}
                                                                       handleLossGemodelk={handleContainerInterfaceLossGemodelk}
                                                                       handleLossGemodelh={handleContainerInterfaceLossGemodelh}
                                                                       handlePacketCorruptPercentage={handleContainerInterfacePacketCorruptPercentage}
                                                                       handlePacketCorruptCorrelationPercentage={handleContainerInterfacePacketCorruptCorrelationPercentage}
                                                                       handlePacketDuplicatePercentage={handleContainerInterfacePacketDuplicatePercentage}
                                                                       handlePacketDuplicateCorrelationPercentage={handleContainerInterfacePacketDuplicateCorrelationPercentage}
                                                                       handlePacketReorderPercentage={handleContainerInterfacePacketReorderPercentage}
                                                                       handlePacketReorderCorrelationPercentage={handleContainerInterfacePacketReorderCorrelationPercentage}
                                                                       handlePacketReorderGap={handleContainerInterfacePacketReorderGap}
                                                                       handleRateLimitMbit={handleContainerInterfaceRateLimitMbit}
                                                                       handlePacketOverheadBytes={handleContainerInterfacePacketOverheadBytes}
                                                                       handleCellOverheadBytes={handleContainerInterfaceCellOverheadBytes}
                                                                       handleDefaultGateway={handleContainerInterfaceDefaultGateway}
                                                                       handleDefaultInput={handleContainerInterfaceDefaultInput}
                                                                       handleDefaultOutput={handleContainerInterfaceDefaultOutput}
                                                                       handleDefaultForward={handleContainerInterfaceDefaultForward}
                                                                       handleTrafficManagerPort={handleContainerInterfaceTrafficManagerPort}
                                                                       handleTrafficManagerLogFile={handleContainerInterfaceTrafficManagerLogFile}
                                                                       handleTrafficManagerLogDir={handleContainerInterfaceTrafficManagerLogDir}
                                                                       handleTrafficManagerMaxWorkers={handleContainerInterfaceTrafficManagerMaxWorkers}

                                                                       inputNameRef={inputNameRef}
                                                                       inputIPRef={inputIPRef}
                                                                       inputSubnetMaskRef={inputSubnetMaskRef}
                                                                       inputPacketDelayMsRef={inputPacketDelayMsRef}
                                                                       inputPacketDelayJitterMsRef={inputPacketDelayJitterMsRef}
                                                                       inputPacketDelayCorrelationPercentageRef={inputPacketDelayCorrelationPercentageRef}
                                                                       inputLossGemodelpRef={inputLossGemodelpRef}
                                                                       inputLossGemodelrRef={inputLossGemodelrRef}
                                                                       inputLossGemodelkRef={inputLossGemodelkRef}
                                                                       inputLossGemodelhRef={inputLossGemodelhRef}
                                                                       inputPacketCorruptPercentageRef={inputPacketCorruptPercentageRef}
                                                                       inputPacketCorruptCorrelationPercentageRef={inputPacketCorruptCorrelationPercentageRef}
                                                                       inputPacketDuplicatePercentageRef={inputPacketDuplicatePercentageRef}
                                                                       inputPacketDuplicateCorrelationPercentageRef={inputPacketDuplicateCorrelationPercentageRef}
                                                                       inputPacketReorderPercentageRef={inputPacketReorderPercentageRef}
                                                                       inputPacketReorderCorrelationPercentageRef={inputPacketReorderCorrelationPercentageRef}
                                                                       inputPacketReorderGapRef={inputPacketReorderGapRef}
                                                                       inputRateLimitMbitRef={inputRateLimitMbitRef}
                                                                       inputPacketOverheadBytesRef={inputPacketOverheadBytesRef}
                                                                       inputCellOverheadBytesRef={inputCellOverheadBytesRef}
                                                                       inputDefaultGatewayRef={inputDefaultGatewayRef}
                                                                       inputTrafficManagerPortRef={inputTrafficManagerPortRef}
                                                                       inputTrafficManagerLogFileRef={inputTrafficManagerLogFileRef}
                                                                       inputTrafficManagerLogDirRef={inputTrafficManagerLogDirRef}
                                                                       inputTrafficManagerMaxWorkersRef={inputTrafficManagerMaxWorkersRef}
                                                                       inputPacketDelayDistributionRef={inputPacketDelayDistributionRef}
                                                                       inputPacketLossTypeRef={inputPacketLossTypeRef}
                                                        />


                                                        <AddServices container={containers[index]}
                                                                     addServiceHandler={handleAddContainerService}
                                                                     containerIndex={index}
                                                                     handleServiceNameChange={handleContainerServiceNameChange}
                                                                     handleDeleteService={handleDeleteContainerService}
                                                                     handleProtocolChange={handleContainerServiceProtocolChange}
                                                                     handleServicePortChange={handleContainerServicePortChange}
                                                                     handleServiceIpChange={handleContainerServiceIpChange}
                                                                     inputServiceNameRef={inputServiceNameRef}
                                                                     inputServicePortRef={inputServicePortRef}
                                                                     inputServiceIpRef={inputServiceIpRef}
                                                        />

                                                        <AddVulns container={containers[index]}
                                                                  containerIndex={index}
                                                                  inputVulnNameRef={inputVulnNameRef}
                                                                  inputVulnServiceNameRef={inputVulnServiceNameRef}
                                                                  newVulnCredentials={newVulnCredentials}
                                                                  inputVulnCredUsernameRef={inputVulnCredUsernameRef}
                                                                  inputVulnCredPwRef={inputVulnCredPwRef}
                                                                  inputVulnCredUsernameForChangeRef={inputVulnCredUsernameForChangeRef}
                                                                  inputVulnCredPwForChangeRef={inputVulnCredPwForChangeRef}
                                                                  handleVulnNameChange={handleContainerVulnNameChange}
                                                                  handleDeleteVuln={handleDeleteContainerVuln}
                                                                  addVulnHandler={handleAddContainerVulns}
                                                                  handleVulnServiceChange={handleContainerVulnServiceChange}
                                                                  handleVulnAccessChange={handleContainerVulnAccessChange}
                                                                  handleVulnTypeChange={handleContainerVulnTypeChange}
                                                                  handleNewCredentialChange={handleNewCredentialChange}
                                                                  handleAddVulnCredentials={handleAddVulnCredentials}
                                                                  handleVulnCredentialChange={handleVulnCredentialChange}
                                                                  handleDeleteVulnCredential={handleDeleteVulnCredential}
                                                        />
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

          <div className="saveEm">

              <h5><br/><br/>Save the emulation</h5>
              <Button onClick={createEmulationRequest}
                      variant="primary" size="md">
                  <i className="fa fa-save" aria-hidden="true"/>
              </Button>
          </div>

      </div>

    )
}

CreateEmulation.propTypes = {}
CreateEmulation.defaultProps = {}
export default CreateEmulation
