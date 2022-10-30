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

/**
 * Component representing the /emulations/<id> resource
 */
const Emulation = (props) => {
    const [loading, setLoading] = useState(false);
    const [emulation, setEmulation] = useState(props.emulation);
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
    const [trafficOpen, setTrafficOpen] = useState(false);
    const [kafkaOpen, setKafkaOpen] = useState(false);
    const [kafkaTopicsOpen, setKafkaTopicsOpen] = useState(false);
    const [firewallOpen, setFirewallOpen] = useState(false);
    const [staticAttackerSequenceOpen, setStaticAttackerSequenceOpen] = useState(false);
    const [ovsSwitchesOpen, setOvsSwitchesOpen] = useState(false);
    const [sdnControllerConfigOpen, setSdnControllerConfigOpen] = useState(false);
    const ip = "localhost"
    // const ip = "172.31.212.92"

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

    const getArrivalProcessStr = (process) => {
        if (process === 0) {
            return "Poisson"
        }
        if (process === 1) {
            return "Sinus modulated Poisson"
        }
        return "unknown"
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
        if(props.execution){
            return (<span>{props.execution_ip_octet}</span>)
        } else {
            return <span>{emulation.id}</span>
        }
    }

    const renderStartEmulationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start emulation
        </Tooltip>
    );

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
                            <h5 className="semiTitle">SDN Controller Config</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={sdnControllerConfigOpen}>
                        <div id="sdnControllerConfigBody" className="cardBodyHidden">
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
                    </Collapse>
                </Card>
            )
        }
    }

    const RenderActions = (props) => {
        if(props.sessionData === null || props.sessionData === undefined || !props.sessionData.admin){
            return (<></>)
        }
        if(!props.execution){
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
                            <h5 className="semiTitle"> General information about the emulation</h5>
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
                                        <td>Configuration</td>
                                        <td>
                                            <Button variant="link"
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
                            <h5 className="semiTitle">Topology</h5>
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
                            <h5 className="semiTitle">Containers</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={containersOpen}>
                        <div id="containersBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>Container name</th>
                                    <th>IP Addresses</th>
                                    <th>Operating system</th>
                                </tr>
                                </thead>
                                <tbody>
                                {emulation.containers_config.containers.map((container, index) =>
                                    <tr key={container.full_name_str + "-" + index}>
                                        <td>{container.full_name_str}</td>
                                        <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                        <td>{container.os}</td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Flags</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={flagsOpen}>
                        <div id="flagsBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>IP</th>
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
                                            <td>{flag.name}</td>
                                            <td>{flag.id}</td>
                                            <td>{flag.path}</td>
                                            <td>{flag.score}</td>
                                        </tr>))}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Users</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={usersOpen}>
                        <div id="usersBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>IP</th>
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
                                            <td>{user.username}</td>
                                            <td>{user.pw}</td>
                                            <td>{getRootStr(user.root)}</td>
                                        </tr>))}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Services</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={servicesOpen}>
                        <div id="servicesBody" className="cardBodyHidden">
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
                                            <td>{service.protocol}</td>
                                        </tr>))}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Vulnerabilities</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={vulnerabilitiesOpen}>
                        <div id="vulnerabilitiesBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>IP</th>
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
                                        <td>{vuln.name}</td>
                                        <td>{vuln.port}</td>
                                        <td>{vuln.protocol}</td>
                                        <td>{getRootStr(vuln.root)}</td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Resources</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={resourcesOpen}>
                        <div id="resourcesBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>Container</th>
                                    <th>Memory</th>
                                    <th>CPUs</th>
                                </tr>
                                </thead>
                                <tbody>
                                {emulation.resources_config.node_resources_configurations.map((rc, index) =>
                                    <tr key={rc.container_name + "-" + index}>
                                        <td>{rc.container_name}</td>
                                        <td>{rc.available_memory_gb}GB</td>
                                        <td>{rc.num_cpus}</td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Network interfaces</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={networkInterfacesOpen}>
                        <div id="networkInterfacesBody" className="cardBodyHidden">
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
                            <h5 className="semiTitle">Client population</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={clientPopulationOpen}>
                        <div id="clientPopulationBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>IP</th>
                                    <th>Arrival process</th>
                                    <th>λ</th>
                                    <th>μ</th>
                                    <th>time-scaling</th>
                                    <th>period-scaling</th>
                                    <th>t</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr key={emulation.traffic_config.client_population_config.ip}>
                                    <td>{emulation.traffic_config.client_population_config.ip}</td>
                                    <td>{getArrivalProcessStr(emulation.traffic_config.client_population_config.client_process_type)}</td>
                                    <td>{emulation.traffic_config.client_population_config.lamb}</td>
                                    <td>{emulation.traffic_config.client_population_config.mu}</td>
                                    <td>{emulation.traffic_config.client_population_config.time_scaling_factor}</td>
                                    <td>{emulation.traffic_config.client_population_config.period_scaling_factor}</td>
                                    <td>{emulation.traffic_config.client_population_config.client_time_step_len_seconds}s</td>
                                </tr>
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Traffic commands</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={trafficOpen}>
                        <div id="trafficBody" className="cardBodyHidden">
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
                            <h5 className="semiTitle">Kafka log</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={kafkaOpen}>
                        <div id="kafkaBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>Container</th>
                                    <th>IP</th>
                                    <th>Operating system</th>
                                    <th>Kafka port</th>
                                    <th>GRPC API port</th>
                                    <th>Memory</th>
                                    <th>CPUs</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr key={emulation.log_sink_config.container.full_name_str}>
                                    <td>{emulation.log_sink_config.container.full_name_str}</td>
                                    <td>{getIps(emulation.log_sink_config.container.ips_and_networks)}</td>
                                    <td>{emulation.log_sink_config.container.os}</td>
                                    <td>{emulation.log_sink_config.kafka_port}</td>
                                    <td>{emulation.log_sink_config.default_grpc_port}</td>
                                    <td>{emulation.log_sink_config.resources.available_memory_gb}GB</td>
                                    <td>{emulation.log_sink_config.resources.num_cpus}</td>
                                </tr>
                                </tbody>
                            </Table>
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
                            <h5 className="semiTitle">Kafka topics</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={kafkaTopicsOpen}>
                        <div id="kafkaTopicsBody" className="cardBodyHidden">
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
                                {emulation.log_sink_config.topics.map((topic, index) =>
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
                            <h5 className="semiTitle">Firewall configurations</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={firewallOpen}>
                        <div id="firewallBody" className="cardBodyHidden">
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
                            <h5 className="semiTitle">Static attacker sequences</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={staticAttackerSequenceOpen}>
                        <div id="attackerSequenceBody" className="cardBodyHidden">
                            {Object.keys(emulation.static_attacker_sequences).map((attackerName, index) =>
                                (<div key={attackerName + "-" + index}>
                                        <h5 className="semiTitle">
                                            Static {attackerName} attacker sequence
                                        </h5>
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
                                            {Object.keys(emulation.static_attacker_sequences).map((attackerName, index) =>
                                                emulation.static_attacker_sequences[attackerName].map((action, index2) =>
                                                    <tr key={attackerName + "-" + index + "-" + index2}>
                                                        <td>{attackerName}</td>
                                                        <td>{index2}</td>
                                                        <td>{action.name}</td>
                                                        <td>{action.id}</td>
                                                        <td>{action.index}</td>
                                                        <td>{action.cmds.join(",")}</td>
                                                        <td>{action.descr}</td>
                                                    </tr>)
                                            )}
                                            </tbody>
                                        </Table>
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
                            <h5 className="semiTitle">Open vSwitch switches configurations </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={ovsSwitchesOpen}>
                        <div id="ovsSwitchesBody" className="cardBodyHidden">
                            <Table striped bordered hover>
                                <thead>
                                <tr>
                                    <th>Container name</th>
                                    <th>Controller ip</th>
                                    <th>Controller port</th>
                                    <th>Controller transport protocol</th>
                                    <th>IP</th>
                                    <th>OpenFlow protocols</th>
                                </tr>
                                </thead>
                                <tbody>
                                {emulation.ovs_config.switch_configs.map((switch_config, index) =>
                                    <tr key={switch_config.container_name + "-" + index}>
                                        <td>{switch_config.container_name}</td>
                                        <td>{switch_config.controler_ip}</td>
                                        <td>{switch_config.controller_port}</td>
                                        <td>{switch_config.controller_transport_protocol}</td>
                                        <td>{switch_config.ip}</td>
                                        <td>{switch_config.openflow_protocols.join(", ")}</td>
                                    </tr>
                                )}
                                </tbody>
                            </Table>
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
