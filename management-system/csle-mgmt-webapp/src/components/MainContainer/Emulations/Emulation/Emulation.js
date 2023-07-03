import React, {useState} from 'react';
import './Emulation.css';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'
import getIps from "../../../Common/getIps";
import getTransportProtocolStr from "../../../Common/getTransportProtocolStr";
import convertListToCommaSeparatedString from "../../../Common/convertListToCommaSeparatedString";
import ElasticImg from "./Elastic.png"
import SnortImg from "./Snort.png"
import KafkaImg from "./Kafka.png"
import DockerImg from "./Docker.png"
import OssecImg from "./Ossec.png"
import BeatsImg from "./Beats.png"
import getBoolStr from "../../../Common/getBoolStr";

/**
 * Component representing the /emulations/<id> resource
 */
const Emulation = (props) => {
    const [loading, setLoading] = useState(false);
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [topologyOpen, setTopologyOpen] = useState(false);
    const [containersOpen, setContainersOpen] = useState(false);
    const [flagsOpen, setFlagsOpen] = useState(false);
    const [usersOpen, setUsersOpen] = useState(false);
    const [servicesOpen, setServicesOpen] = useState(false);
    const [vulnerabilitiesOpen, setVulnerabilitiesOpen] = useState(false);
    const [resourcesOpen, setResourcesOpen] = useState(false);
    const [networkInterfacesOpen, setNetworkInterfacesOpen] = useState(false);
    const [clientPopulationOpen, setClientPopulationOpen] = useState(false);
    const [clientsOpen, setClientsOpen] = useState(false);
    const [trafficOpen, setTrafficOpen] = useState(false);
    const [workflowServicesOpen, setWorkflowServicesOpen] = useState(false);
    const [workflowMarkovChainsOpen, setWorkflowMarkovChainsOpen] = useState(false);
    const [kafkaOpen, setKafkaOpen] = useState(false);
    const [elkOpen, setElkOpen] = useState(false);
    const [hostManagerConfigOpen, setHostManagerConfigOpen] = useState(false);
    const [trafficManagersConfigOpen, setTrafficManagersConfigOpen] = useState(false);
    const [snortManagerConfigOpen, setSnortManagerConfigOpen] = useState(false);
    const [ossecManagerConfigOpen, setOSSECManagerConfigOpen] = useState(false);
    const [dockerStatsManagerConfigOpen, setDockerStatsManagerConfigOpen] = useState(false);
    const [kafkaTopicsOpen, setKafkaTopicsOpen] = useState(false);
    const [firewallOpen, setFirewallOpen] = useState(false);
    const [staticAttackerSequenceOpen, setStaticAttackerSequenceOpen] = useState(false);
    const [ovsSwitchesOpen, setOvsSwitchesOpen] = useState(false);
    const [sdnControllerConfigOpen, setSdnControllerConfigOpen] = useState(false);
    const [beatsOpen, setBeatsOpen] = useState(false);
    const emulation = props.emulation

    const startorStopEmulationPre = (emulation) => {
        setLoading(true)
        props.startOrStopEmulation(emulation.id)
    }

    const getSubnetMasks = (emulation) => {
        let networks = emulation.containers_config.networks
        const subnets = []
        for (let i = 0; i < networks.length; i++) {
            subnets.push(networks[i].subnet_mask)
        }
        return subnets.join(", ")
    }

    const removeExecutionPre = (emulation, ip_first_octet) => {
        setLoading(true)
        props.removeExecution(emulation, ip_first_octet)
    }

    const getNetworkNames = (emulation) => {
        let networks = emulation.containers_config.networks
        const network_names = []
        for (let i = 0; i < networks.length; i++) {
            network_names.push(networks[i].name)
        }
        return network_names.join(", ")
    }

    const getRootStr = (root) => {
        if (root) {
            return "Yes"
        } else {
            return "No"
        }
    }

    const getStatus = (emulation) => {
        if (loading) {
            if (emulation.running) {
                return "stopping.."
            } else {
                return "starting.."
            }
        }
        if (emulation.running) {
            return "running"
        } else {
            return "stopped"
        }
    }

    const getSpinnerOrCircle = (emulation) => {
        if (loading) {
            return (<Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
            />)
        }
        if (emulation.running) {
            return (
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg>
            )
        } else {
            return (
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <circle r="15" cx="15" cy="15" fill="red"></circle>
                </svg>
            )
        }
    }

    const getId = () => {
        if (props.execution) {
            return (<span>{props.execution_ip_octet}</span>)
        } else {
            return <span>{emulation.id}</span>
        }
    }

    const renderRemoveEmulationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove emulation
        </Tooltip>
    );

    const renderRemoveAndCleanExecutionTooltip = (props) => {
        if (props.execution) {
            return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
                Stop and remove execution
            </Tooltip>)
        } else {
            return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
                Stop and remove all executions of the emulation
            </Tooltip>)
        }
    }

    const renderStopEmulationTooltip = (props) => {
        if (props.execution) {
            return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
                Stop execution
            </Tooltip>)
        } else {
            return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
                Stop all executions of the emulation
            </Tooltip>)
        }
    }

    const SdnControllerConfig = (props) => {
        if (props.emulation.sdn_controller_config === null || props.emulation.sdn_controller_config === undefined) {
            return (<span> </span>)
        } else {
            return (
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setSdnControllerConfigOpen(!sdnControllerConfigOpen)}
                            aria-controls="sdnControllerConfigBody"
                            aria-expanded={sdnControllerConfigOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">SDN Controller Config
                                <i className="fa fa-sitemap headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={sdnControllerConfigOpen}>
                        <div id="sdnControllerConfigBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Container name</th>
                                        <th>Container os</th>
                                        <th>IPs</th>
                                        <th>Controller module</th>
                                        <th>Port</th>
                                        <th>Web port</th>
                                        <th>Time step length (s)</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td>{props.emulation.sdn_controller_config.container.full_name_str}</td>
                                        <td>{props.emulation.sdn_controller_config.container.os}</td>
                                        <td>{getIps(props.emulation.sdn_controller_config.container.ips_and_networks).join(", ")}</td>
                                        <td>{props.emulation.sdn_controller_config.controller_module_name}</td>
                                        <td>{props.emulation.sdn_controller_config.controller_port}</td>
                                        <td>{props.emulation.sdn_controller_config.controller_web_api_port}</td>
                                        <td>{props.emulation.sdn_controller_config.time_step_len_seconds}</td>
                                    </tr>
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>
            )
        }
    }

    const RenderActions = (props) => {
        if (props.sessionData === null || props.sessionData === undefined || !props.sessionData.admin) {
            return (<></>)
        }
        if (!props.execution) {
            return (
                <h5 className="semiTitle">
                    Actions:
                    <OverlayTrigger
                        className="removeButton"
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveEmulationTooltip}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeEmulation(emulation)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <SpinnerOrStatus emulation={emulation}/>
                </h5>
            )
        } else {
            return (
                <h5 className="semiTitle">
                    Actions:
                    <SpinnerOrDeleteButton execution_ip_octet={props.execution_ip_octet}/>
                </h5>
            )
        }
    }

    const SpinnerOrDeleteButton = (props) => {
        if (loading) {
            return (
                <Spinner
                    as="span"
                    animation="grow"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                />
            )
        } else {
            return (
                <OverlayTrigger
                    className="removeButton"
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderRemoveAndCleanExecutionTooltip}
                >
                    <Button variant="danger" className="removeButton" size="sm"
                            onClick={() => removeExecutionPre(emulation, props.execution_ip_octet)}>
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        }
    };

    const ArrivalConfigStr = (props) => {
        var config_str = ""
        if(props.client.arrival_config.client_arrival_type === 0) {
            config_str = `Constant arrival process; λ= ${props.client.arrival_config.lamb}`
            return config_str
        }
        if(props.client_population_config.arrival_config.client_arrival_type === 1) {
            config_str = `Sine modulated arrival process; λ= ${props.client.arrival_config.lamb}, `
            config_str = config_str + `time scaling factor=${props.client.arrival_config.time_scaling_factor}, `
            config_str = config_str + `time scaling factor=${props.client.arrival_config.period_scaling_factor}`
            return config_str
        }
        if(props.client_population_config.arrival_config.client_arrival_type === 2) {
            config_str = `Spiking arrival process; `
            config_str = config_str + `exponents=${convertListToCommaSeparatedString(props.client.arrival_config.exponents)}, `
            config_str = config_str + `factors=${convertListToCommaSeparatedString(props.client.arrival_config.factors)}`
            return config_str
        }
        if(props.client_population_config.arrival_config.client_arrival_type === 3) {
            config_str = `Piece-wise constant process; `
            config_str = config_str + `breakvalues=${convertListToCommaSeparatedString(props.client.arrival_config.breakvalues)}, `
            config_str = config_str + `breakpoints=${convertListToCommaSeparatedString(props.client.arrival_config.breakpoints)}`
            return config_str
        }
        if(props.client_population_config.arrival_config.client_arrival_type === 4) {
            config_str = `EPTMP process; `
            config_str = config_str + `phis=${convertListToCommaSeparatedString(props.client.arrival_config.phis)}, `
            config_str = config_str + `thetas=${convertListToCommaSeparatedString(props.client.arrival_config.thetas)}, `
            config_str = config_str + `omegas=${convertListToCommaSeparatedString(props.client.arrival_config.omegas)}, `
            config_str = config_str + `gammas=${convertListToCommaSeparatedString(props.client.arrival_config.gammas)}`
            return config_str
        }
    };


    const SpinnerOrStatus = (props) => {
        if (loading) {
            if (emulation.name.running) {
                return (
                    <Spinner
                        as="span"
                        animation="grow"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                    />
                )
            } else {
                return (
                    <Spinner
                        as="span"
                        animation="grow"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                    />
                )
            }
        } else {
            if (emulation.running) {
                return (
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopEmulationTooltip}
                    >
                        <Button variant="warning" className="startButton" size="sm"
                                onClick={() => startorStopEmulationPre(emulation)}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            } else {
                return (
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAndCleanExecutionTooltip}
                    >
                        <Button variant="success" className="startButton" size="sm"
                                onClick={() => startorStopEmulationPre(emulation)}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            }
        }
    };


    return (
        <Card key={emulation.name} ref={props.wrapper}>
            <Card.Header>
                <Accordion.Toggle as={Button} variant="link" eventKey={emulation.name} className="mgHeader">
                    <span className="subnetTitle">ID: {getId()}, emulation name: {emulation.name}</span>
                    # Containers: {emulation.containers_config.containers.length}, Status: {getStatus(emulation)}
                    {getSpinnerOrCircle(emulation)}
                </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={emulation.name}>
                <Card.Body>

                    <RenderActions execution={props.execution} removeEmulation={props.removeEmulation}
                                   removeExecution={props.removeExecution} execution_ip_octet={props.execution_ip_octet}
                                   sessionData={props.sessionData}
                    />
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
                                            <td>{emulation.descr}</td>
                                        </tr>
                                        <tr>
                                            <td>Status</td>
                                            <td>{getStatus(emulation)} <SpinnerOrStatus emulation={emulation}/></td>
                                        </tr>
                                        <tr>
                                            <td>Emulation name</td>
                                            <td>{emulation.name}</td>
                                        </tr>
                                        <tr>
                                            <td>Subnets</td>
                                            <td>{getSubnetMasks(emulation)}</td>
                                        </tr>
                                        <tr>
                                            <td>Network names</td>
                                            <td>{getNetworkNames(emulation)}</td>
                                        </tr>
                                        <tr>
                                            <td># Containers</td>
                                            <td>{emulation.containers_config.containers.length}</td>
                                        </tr>
                                        <tr>
                                            <td>csle-collector version</td>
                                            <td>{emulation.csle_collector_version}</td>
                                        </tr>
                                        <tr>
                                            <td>csle-ryu
                                                version
                                            </td>
                                            <td>{emulation.csle_ryu_version}</td>
                                        </tr>
                                        <tr>
                                            <td>Configuration</td>
                                            <td>
                                                <Button variant="link" className="dataDownloadLink"
                                                        onClick={() => fileDownload(JSON.stringify(emulation), "config.json")}>
                                                    config.json
                                                </Button>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>


                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setTopologyOpen(!topologyOpen)}
                                aria-controls="topologyBody"
                                aria-expanded={topologyOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Topology
                                    <i className="fa fa-sitemap headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={topologyOpen}>
                            <div id="topologyBody" className="cardBodyHidden">
                                <img src={`data:image/jpeg;base64,${emulation.image}`} className="topologyImg img-fluid"
                                     alt="Topology"/>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setContainersOpen(!containersOpen)}
                                aria-controls="containersBody"
                                aria-expanded={containersOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Containers <i className="fa fa-cubes headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={containersOpen}>
                            <div id="containersBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Container name</th>
                                            <th>IP Addresses</th>
                                            <th>External IP</th>
                                            <th>Physical host</th>
                                            <th>Operating system</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.containers_config.containers.map((container, index) =>
                                            <tr key={container.full_name_str + "-" + index}>
                                                <td>{container.full_name_str}</td>
                                                <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                                <td>{container.docker_gw_bridge_ip}</td>
                                                <td>{container.physical_host_ip}</td>
                                                <td>{container.os}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setFlagsOpen(!flagsOpen)}
                                aria-controls="flagsBody"
                                aria-expanded={flagsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Flags
                                    <i className="fa fa-flag headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={flagsOpen}>
                            <div id="flagsBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Flag name</th>
                                            <th>Flag ID</th>
                                            <th>Path</th>
                                            <th>Score</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.flags_config.node_flag_configs.map((flag_config, index) =>
                                            flag_config.flags.map((flag, index) =>
                                                <tr key={flag_config.ip + "-" + flag.id}>
                                                    <td>{flag_config.ip}</td>
                                                    <td>{flag_config.docker_gw_bridge_ip}</td>
                                                    <td>{flag_config.physical_host_ip}</td>
                                                    <td>{flag.name}</td>
                                                    <td>{flag.id}</td>
                                                    <td>{flag.path}</td>
                                                    <td>{flag.score}</td>
                                                </tr>))}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setUsersOpen(!usersOpen)}
                                aria-controls="usersBody"
                                aria-expanded={usersOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Users <i className="fa fa-user headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={usersOpen}>
                            <div id="usersBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Username</th>
                                            <th>Password</th>
                                            <th>Root</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.users_config.users_configs.map((user_config, index) =>
                                            user_config.users.map((user, index) =>
                                                <tr key={user_config.ip + "-" + user.username}>
                                                    <td>{user_config.ip}</td>
                                                    <td>{user_config.docker_gw_bridge_ip}</td>
                                                    <td>{user_config.physical_host_ip}</td>
                                                    <td>{user.username}</td>
                                                    <td>{user.pw}</td>
                                                    <td>{getRootStr(user.root)}</td>
                                                </tr>))}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setServicesOpen(!servicesOpen)}
                                aria-controls="servicesBody"
                                aria-expanded={servicesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Services <i className="fa fa-signal headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={servicesOpen}>
                            <div id="servicesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>Service name</th>
                                            <th>Port</th>
                                            <th>Transport protocol</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.services_config.services_configs.map((service_config, index) =>
                                            service_config.services.map((service, index) =>
                                                <tr key={service_config.ip + "-" + service.name + "-" + index}>
                                                    <td>{service_config.ip}</td>
                                                    <td>{service.name}</td>
                                                    <td>{service.port}</td>
                                                    <td>{getTransportProtocolStr(service.protocol)}</td>
                                                </tr>))}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setVulnerabilitiesOpen(!vulnerabilitiesOpen)}
                                aria-controls="vulnerabilitiesBody"
                                aria-expanded={vulnerabilitiesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Vulnerabilities <i className="fa fa-ambulance headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={vulnerabilitiesOpen}>
                            <div id="vulnerabilitiesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Name</th>
                                            <th>Port</th>
                                            <th>Transport protocol</th>
                                            <th>Root</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.vuln_config.vulnerabilities.map((vuln, index) =>
                                            <tr key={vuln.ip + "-" + vuln.name + "-" + index}>
                                                <td>{vuln.ip}</td>
                                                <td>{vuln.docker_gw_bridge_ip}</td>
                                                <td>{vuln.physical_host_ip}</td>
                                                <td>{vuln.name}</td>
                                                <td>{vuln.port}</td>
                                                <td>{getTransportProtocolStr(vuln.protocol)}</td>
                                                <td>{getRootStr(vuln.root)}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setResourcesOpen(!resourcesOpen)}
                                aria-controls="resourcesBody"
                                aria-expanded={resourcesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Resources
                                    <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={resourcesOpen}>
                            <div id="resourcesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IPs</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Container</th>
                                            <th>Memory</th>
                                            <th>CPUs</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.resources_config.node_resources_configurations.map((rc, index) =>
                                            <tr key={rc.container_name + "-" + index}>
                                                <td>{getIps(rc.ips_and_network_configs)}</td>
                                                <td>{rc.docker_gw_bridge_ip}</td>
                                                <td>{rc.physical_host_ip}</td>
                                                <td>{rc.container_name}</td>
                                                <td>{rc.available_memory_gb}GB</td>
                                                <td>{rc.num_cpus}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>


                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setNetworkInterfacesOpen(!networkInterfacesOpen)}
                                aria-controls="networkInterfacesBody"
                                aria-expanded={networkInterfacesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Network interfaces <i className="fa fa-podcast headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={networkInterfacesOpen}>
                            <div id="networkInterfacesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>Interface</th>
                                            <th>Rate</th>
                                            <th>Duplicate packet %</th>
                                            <th>Packet loss %</th>
                                            <th>Packet burst %</th>
                                            <th>Propagation delay</th>
                                            <th>Jitter delay</th>
                                            <th>Overhead</th>
                                            <th>Reorder %</th>
                                            <th>Corrupt %</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.resources_config.node_resources_configurations.filter(rc => (rc !== null && rc !== undefined &&
                                            rc.ips_and_network_configs !== null
                                            && rc.ips_and_network_configs !== undefined)).map((rc, index) => {
                                            return rc.ips_and_network_configs.filter((rc_net) =>
                                                rc_net !== null && rc_net !== undefined).map((rc_net, index) => {
                                                    return (<tr key={rc_net[0] + "-" + index}>
                                                        <td>{rc_net[0]}</td>
                                                        <td>{rc_net[1].interface}</td>
                                                        <td>{rc_net[1].rate_limit_mbit}Mbit/s</td>
                                                        <td>{rc_net[1].packet_duplicate_percentage}%</td>
                                                        <td>{rc_net[1].loss_gemodel_h}%</td>
                                                        <td>{rc_net[1].loss_gemodel_p}%</td>
                                                        <td>{rc_net[1].packet_delay_distribution}, {rc_net[1].packet_delay_ms}ms</td>
                                                        <td>{rc_net[1].packet_delay_jitter_ms}ms</td>
                                                        <td>{rc_net[1].packet_overhead}bytes</td>
                                                        <td>{rc_net[1].packet_reorder_percentage}%</td>
                                                        <td>{rc_net[1].packet_corrupt_percentage}%</td>
                                                    </tr>)
                                                }
                                            )
                                        })}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>
                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setClientPopulationOpen(!clientPopulationOpen)}
                                aria-controls="clientPopulationBody"
                                aria-expanded={clientPopulationOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Client population <i className="fa fa-users headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={clientPopulationOpen}>
                            <div id="clientPopulationBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>t</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.traffic_config.client_population_config.ip}>
                                            <td>{emulation.traffic_config.client_population_config.ip}</td>
                                            <td>{emulation.traffic_config.client_population_config.docker_gw_bridge_ip}</td>
                                            <td>{emulation.traffic_config.client_population_config.physical_host_ip}</td>
                                            <td>{emulation.traffic_config.client_population_config.client_time_step_len_seconds}s</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setClientsOpen(!clientsOpen)}
                                aria-controls="clientsBody"
                                aria-expanded={clientsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Client types <i className="fa fa-users headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={clientsOpen}>
                            <div id="clientsBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Client ID</th>
                                            <th>Arrival process</th>
                                            <th>Workflow distribution</th>
                                            <th>μ</th>
                                            <th>Exponential service time</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.traffic_config.client_population_config.clients.map((client, index) =>
                                            <tr key={client.id + "-" + index}>
                                                <td>{client.id}</td>
                                                <td><ArrivalConfigStr client={client}/></td>
                                                <td>{JSON.stringify(client.workflow_distribution)}</td>
                                                <td>{client.mu}</td>
                                                <td>{getBoolStr(client.exponential_service_time)}</td>
                                            </tr>)}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setTrafficOpen(!trafficOpen)}
                                aria-controls="trafficBody"
                                aria-expanded={trafficOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Traffic commands
                                    <i className="fa fa-chrome headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={trafficOpen}>
                            <div id="trafficBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Target IP</th>
                                            <th>Command</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.traffic_config.node_traffic_configs.map((node_traffic_config, index) =>
                                            node_traffic_config.commands.map((cmd, index2) =>
                                                <tr key={node_traffic_config.ip + "-" + cmd + "-" + index + "-" + index2}>
                                                    <td>{node_traffic_config.ip}</td>
                                                    <td>{cmd}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setWorkflowServicesOpen(!workflowServicesOpen)}
                                aria-controls="workflowServicesBody"
                                aria-expanded={workflowServicesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Workflow services
                                    <i className="fa fa-chrome headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={workflowServicesOpen}>
                            <div id="workflowServicesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Service ID</th>
                                            <th>IP</th>
                                            <th>Commands</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.traffic_config.client_population_config.workflows_config.workflow_services.map((workflow_service, index) =>
                                            workflow_service.ips_and_commands.map((ip_cmd, index2) =>
                                                <tr key={ip_cmd[0] + "-" + ip_cmd[1] + "-" + index + "-" + index2}>
                                                    <td>{workflow_service.id}</td>
                                                    <td>{ip_cmd[0]}</td>
                                                    <td>{convertListToCommaSeparatedString(ip_cmd[1])}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setWorkflowMarkovChainsOpen(!workflowMarkovChainsOpen)}
                                aria-controls="workflowMarkovChainsBody"
                                aria-expanded={workflowMarkovChainsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Workflow Markov Chains
                                    <i className="fa fa-chrome headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={workflowMarkovChainsOpen}>
                            <div id="workflowMarkovChainsBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Initial state</th>
                                            <th>Transition matrix</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.traffic_config.client_population_config.workflows_config.workflow_markov_chains.map((workflow_mc, index) =>
                                            <tr key={workflow_mc.id + "-" + index}>
                                                <td>{workflow_mc.id}</td>
                                                <td>{workflow_mc.initial_state}</td>
                                                <td>{JSON.stringify(workflow_mc.transition_matrix)}</td>
                                            </tr>)}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setKafkaOpen(!kafkaOpen)}
                                aria-controls="kafkaBody"
                                aria-expanded={kafkaOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Kafka configuration
                                    <img src={KafkaImg} alt="Kafka" className="img-fluid headerIcon kafka"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={kafkaOpen}>
                            <div id="kafkaBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Container</th>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Operating system</th>
                                            <th>Kafka port</th>
                                            <th>Kafka Manager GRPC API port</th>
                                            <th>Kafka Manager Log file</th>
                                            <th>Kafka Manager GRPC max workers</th>
                                            <th>Memory</th>
                                            <th>CPUs</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.kafka_config.container.full_name_str}>
                                            <td>{emulation.kafka_config.container.full_name_str}</td>
                                            <td>{getIps(emulation.kafka_config.container.ips_and_networks)}</td>
                                            <td>{emulation.kafka_config.container.docker_gw_bridge_ip}</td>
                                            <td>{emulation.kafka_config.container.physical_host_ip}</td>
                                            <td>{emulation.kafka_config.container.os}</td>
                                            <td>{emulation.kafka_config.kafka_port}</td>
                                            <td>{emulation.kafka_config.kafka_manager_port}</td>
                                            <td>{emulation.kafka_config.kafka_manager_log_dir}{emulation.kafka_config.kafka_manager_log_file}</td>
                                            <td>{emulation.kafka_config.kafka_manager_max_workers}</td>
                                            <td>{emulation.kafka_config.resources.available_memory_gb}GB</td>
                                            <td>{emulation.kafka_config.resources.num_cpus}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setKafkaTopicsOpen(!kafkaTopicsOpen)}
                                aria-controls="kafkaTopicsBody"
                                aria-expanded={kafkaTopicsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Kafka topics
                                    <img src={KafkaImg} alt="Kafka" className="img-fluid headerIcon kafka"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={kafkaTopicsOpen}>
                            <div id="kafkaTopicsBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Partitions</th>
                                            <th>Replicas</th>
                                            <th>Retention time (hours)</th>
                                            <th>Attributes</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.kafka_config.topics.map((topic, index) =>
                                            <tr key={topic.name + "-" + index}>
                                                <td>{topic.name}</td>
                                                <td>{topic.num_partitions}</td>
                                                <td>{topic.num_replicas}</td>
                                                <td>{topic.retention_time_hours}</td>
                                                <td>{topic.attributes.join(",")}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setElkOpen(!elkOpen)}
                                aria-controls="elkBody"
                                aria-expanded={elkOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    ELK configuration
                                    <img src={ElasticImg} alt="Elastic" className="img-fluid headerIcon elastic"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={elkOpen}>
                            <div id="elkBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Container</th>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>Operating system</th>
                                            <th>Elasticsearch port</th>
                                            <th>ELK Manager GRPC API port</th>
                                            <th>ELK Manager log file</th>
                                            <th>ELK Manager GRPC max workers</th>
                                            <th>Kibana port</th>
                                            <th>Logstash port</th>
                                            <th>Memory</th>
                                            <th>CPUs</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.elk_config.container.full_name_str}>
                                            <td>{emulation.elk_config.container.full_name_str}</td>
                                            <td>{getIps(emulation.elk_config.container.ips_and_networks)}</td>
                                            <td>{emulation.elk_config.container.docker_gw_bridge_ip}</td>
                                            <td>{emulation.elk_config.container.physical_host_ip}</td>
                                            <td>{emulation.elk_config.container.os}</td>
                                            <td>{emulation.elk_config.elastic_port}</td>
                                            <td>{emulation.elk_config.elk_manager_port}</td>
                                            <td>{emulation.elk_config.elk_manager_log_dir}{emulation.elk_config.elk_manager_log_file}</td>
                                            <td>{emulation.elk_config.elk_manager_max_workers}</td>
                                            <td>{emulation.elk_config.kibana_port}</td>
                                            <td>{emulation.elk_config.logstash_port}</td>
                                            <td>{emulation.elk_config.resources.available_memory_gb}GB</td>
                                            <td>{emulation.elk_config.resources.num_cpus}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setHostManagerConfigOpen(!hostManagerConfigOpen)}
                                aria-controls="hostManagerConfigBody"
                                aria-expanded={hostManagerConfigOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Host managers configuration
                                    <i className="fa fa-linux headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={hostManagerConfigOpen}>
                            <div id="hostManagerConfigBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Host managers GRPC API port</th>
                                            <th>Host managers log file</th>
                                            <th>Host managers GRPC max workers</th>
                                            <th>Time-step length (s)</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.host_manager_config.host_manager_port}>
                                            <td>{emulation.host_manager_config.host_manager_port}</td>
                                            <td>{emulation.host_manager_config.host_manager_log_dir}{emulation.host_manager_config.host_manager_log_file}</td>
                                            <td>{emulation.host_manager_config.host_manager_max_workers}</td>
                                            <td>{emulation.host_manager_config.time_step_len_seconds}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setTrafficManagersConfigOpen(!trafficManagersConfigOpen)}
                                aria-controls="trafficManagersConfigBody"
                                aria-expanded={trafficManagersConfigOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">Traffic managers configuration
                                    <i className="fa fa-linux headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={trafficManagersConfigOpen}>
                            <div id="trafficManagersConfigBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Traffic manager IP</th>
                                            <th>External IP</th>
                                            <th>Physical server</th>
                                            <th>GRPC API port</th>
                                            <th>Log file</th>
                                            <th>GRPC Max workers</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.traffic_config.node_traffic_configs.map((node_traffic_config, index) =>
                                            <tr key={node_traffic_config.ip + "-" + index}>
                                                <td>{node_traffic_config.ip}</td>
                                                <td>{node_traffic_config.docker_gw_bridge_ip}</td>
                                                <td>{node_traffic_config.physical_host_ip}</td>
                                                <td>{node_traffic_config.traffic_manager_port}</td>
                                                <td>{node_traffic_config.traffic_manager_log_dir}{node_traffic_config.traffic_manager_log_file}</td>
                                                <td>{node_traffic_config.traffic_manager_max_workers}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setSnortManagerConfigOpen(!snortManagerConfigOpen)}
                                aria-controls="snortManagerConfigBody"
                                aria-expanded={snortManagerConfigOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Snort IDS managers configuration
                                    <img src={SnortImg} alt="Snort" className="img-fluid headerIcon elastic"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={snortManagerConfigOpen}>
                            <div id="snortManagerConfigBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Snort IDS managers GRPC API port</th>
                                            <th>Snort IDS managers Log file</th>
                                            <th>Snort IDS managers GRPC max workers</th>
                                            <th>Time-step length (s)</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.snort_ids_manager_config.snort_ids_manager_port}>
                                            <td>{emulation.snort_ids_manager_config.snort_ids_manager_port}</td>
                                            <td>{emulation.snort_ids_manager_config.snort_ids_manager_log_dir}{emulation.snort_ids_manager_config.snort_ids_manager_log_file}</td>
                                            <td>{emulation.snort_ids_manager_config.snort_ids_manager_max_workers}</td>
                                            <td>{emulation.snort_ids_manager_config.time_step_len_seconds}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setOSSECManagerConfigOpen(!ossecManagerConfigOpen)}
                                aria-controls="ossecManagerConfigBody"
                                aria-expanded={ossecManagerConfigOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    OSSEC IDS managers configuration
                                    <img src={OssecImg} alt="OSSEC" className="img-fluid headerIcon kafka"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={ossecManagerConfigOpen}>
                            <div id="ossecManagerConfigBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>OSSEC IDS managers GRPC API port</th>
                                            <th>OSSEC IDS managers log file</th>
                                            <th>OSSEC IDS managers GRPC max workers</th>
                                            <th>Time-step length (s)</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.ossec_ids_manager_config.ossec_ids_manager_port}>
                                            <td>{emulation.ossec_ids_manager_config.ossec_ids_manager_port}</td>
                                            <td>{emulation.ossec_ids_manager_config.ossec_ids_manager_log_dir}{emulation.ossec_ids_manager_config.ossec_ids_manager_log_file}</td>
                                            <td>{emulation.ossec_ids_manager_config.ossec_ids_manager_max_workers}</td>
                                            <td>{emulation.ossec_ids_manager_config.time_step_len_seconds}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setDockerStatsManagerConfigOpen(!dockerStatsManagerConfigOpen)}
                                aria-controls="dockerStatsManagerConfigBody"
                                aria-expanded={dockerStatsManagerConfigOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Docker stats managers configuration
                                    <img src={DockerImg} alt="Docker" className="img-fluid headerIcon kafka"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={dockerStatsManagerConfigOpen}>
                            <div id="dockerStatsManagerConfigBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Docker stats managers GRPC API port</th>
                                            <th>Docker stats managers log file</th>
                                            <th>Docker stats managers GRPC max workers</th>
                                            <th>Time-step length (s)</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr key={emulation.docker_stats_manager_config.docker_stats_manager_port}>
                                            <td>{emulation.docker_stats_manager_config.docker_stats_manager_port}</td>
                                            <td>{emulation.docker_stats_manager_config.docker_stats_manager_log_dir}{emulation.docker_stats_manager_config.docker_stats_manager_log_file}</td>
                                            <td>{emulation.docker_stats_manager_config.docker_stats_manager_max_workers}</td>
                                            <td>{emulation.docker_stats_manager_config.time_step_len_seconds}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setFirewallOpen(!firewallOpen)}
                                aria-controls="firewallBody"
                                aria-expanded={firewallOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Firewall configurations
                                    <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={firewallOpen}>
                            <div id="firewallBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Hostname</th>
                                            <th>IP</th>
                                            <th>Default forward policy</th>
                                            <th>Default input policy</th>
                                            <th>Default output policy</th>
                                            <th>Default gateway</th>
                                            <th>Network name</th>
                                            <th>Subnet mask</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.topology_config.node_configs.map((node_config, index) =>
                                            node_config.ips_gw_default_policy_networks.map((ip_fw_config, index2) =>
                                                <tr key={node_config.hostname + "-" + ip_fw_config.ip + "-" + index + "-" + index2}>
                                                    <td>{node_config.hostname}</td>
                                                    <td>{ip_fw_config.ip}</td>
                                                    <td>{ip_fw_config.default_forward}</td>
                                                    <td>{ip_fw_config.default_input}</td>
                                                    <td>{ip_fw_config.default_output}</td>
                                                    <td>{ip_fw_config.default_gw}</td>
                                                    <td>{ip_fw_config.network.name}</td>
                                                    <td>{ip_fw_config.network.subnet_mask}</td>
                                                </tr>)
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setStaticAttackerSequenceOpen(!staticAttackerSequenceOpen)}
                                aria-controls="attackerSequenceBody"
                                aria-expanded={staticAttackerSequenceOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Static attacker sequences
                                    <i className="fa fa-user-secret headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={staticAttackerSequenceOpen}>
                            <div id="attackerSequenceBody" className="cardBodyHidden">
                                {Object.keys(emulation.static_attacker_sequences).map((attackerName, index) =>
                                    (<div key={attackerName + "-" + index}>
                                            <h5 className="semiTitle">
                                                Static {attackerName} attacker sequence
                                            </h5>
                                            <div className="table-responsive">
                                                <Table striped bordered hover>
                                                    <thead>
                                                    <tr>
                                                        <th>Attacker name</th>
                                                        <th>Time-step</th>
                                                        <th>Action name</th>
                                                        <th>Action id</th>
                                                        <th>Action index</th>
                                                        <th>Action commands</th>
                                                        <th>Action description</th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    {emulation.static_attacker_sequences[attackerName].map((action, index2) =>
                                                        <tr key={attackerName + "-" + index + "-" + index2}>
                                                            <td>{attackerName}</td>
                                                            <td>{index2}</td>
                                                            <td>{action.name}</td>
                                                            <td>{action.id}</td>
                                                            <td>{action.index}</td>
                                                            <td>{action.cmds.join(",")}</td>
                                                            <td>{action.descr}</td>
                                                        </tr>
                                                    )}
                                                    </tbody>
                                                </Table>
                                            </div>
                                        </div>
                                    )
                                )}
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setOvsSwitchesOpen(!ovsSwitchesOpen)}
                                aria-controls="ovsSwitchesBody"
                                aria-expanded={ovsSwitchesOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Open vSwitch switches configurations
                                    <i className="fa fa-code headerIcon" aria-hidden="true"></i>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={ovsSwitchesOpen}>
                            <div id="ovsSwitchesBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Container name</th>
                                            <th>Controller ip</th>
                                            <th>Controller port</th>
                                            <th>Controller transport protocol</th>
                                            <th>IP</th>
                                            <th>External IP</th>
                                            <th>Physical host</th>
                                            <th>OpenFlow protocols</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.ovs_config.switch_configs.map((switch_config, index) =>
                                            <tr key={switch_config.container_name + "-" + index}>
                                                <td>{switch_config.container_name}</td>
                                                <td>{switch_config.controller_ip}</td>
                                                <td>{switch_config.controller_port}</td>
                                                <td>{switch_config.controller_transport_protocol}</td>
                                                <td>{switch_config.ip}</td>
                                                <td>{switch_config.docker_gw_bridge_ip}</td>
                                                <td>{switch_config.physical_host_ip}</td>
                                                <td>{switch_config.openflow_protocols.join(", ")}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card className="subCard">
                        <Card.Header>
                            <Button
                                onClick={() => setBeatsOpen(!beatsOpen)}
                                aria-controls="beatsBody"
                                aria-expanded={beatsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle">
                                    Beats configuration
                                    <img src={BeatsImg} alt="Beats" className="img-fluid headerIcon beats"/>
                                </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={beatsOpen}>
                            <div id="beatsBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Container ip</th>
                                            <th># Elastic shards</th>
                                            <th>Reload enabled</th>
                                            <th>Filebeat modules</th>
                                            <th>Heartbeat hosts</th>
                                            <th>Kafka input</th>
                                            <th>Log files paths</th>
                                            <th>Metricbeat modules</th>
                                            <th>Start filebeat automatically</th>
                                            <th>Start packetbeat automatically</th>
                                            <th>Start metricbeat automatically</th>
                                            <th>Start heartbeat automatically</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {emulation.beats_config.node_beats_configs.map((node_beats_config, index) =>
                                            <tr key={node_beats_config.ip + "-" + index}>
                                                <td>{node_beats_config.ip}</td>
                                                <td>{emulation.beats_config.num_elastic_shards}</td>
                                                <td>{getBoolStr(emulation.beats_config.reload_enabled)}</td>
                                                <td>{convertListToCommaSeparatedString(node_beats_config.filebeat_modules)}</td>
                                                <td>{convertListToCommaSeparatedString(node_beats_config.heartbeat_hosts_to_monitor)}</td>
                                                <td>{getBoolStr(node_beats_config.kafka_input)}</td>
                                                <td>{convertListToCommaSeparatedString(node_beats_config.log_files_paths)}</td>
                                                <td>{convertListToCommaSeparatedString(node_beats_config.metricbeat_modules)}</td>
                                                <td>{node_beats_config.start_filebeat_automatically.toString()}</td>
                                                <td>{node_beats_config.start_packetbeat_automatically.toString()}</td>
                                                <td>{node_beats_config.start_metricbeat_automatically.toString()}</td>
                                                <td>{node_beats_config.start_heartbeat_automatically.toString()}</td>
                                            </tr>
                                        )}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <SdnControllerConfig emulation={emulation}/>

                </Card.Body>
            </Accordion.Collapse>
        </Card>)
}

Emulation.propTypes = {};

Emulation.defaultProps = {};

export default Emulation;
