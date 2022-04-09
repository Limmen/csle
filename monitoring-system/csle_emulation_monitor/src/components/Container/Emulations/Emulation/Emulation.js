import React, {useState, useCallback} from 'react';
import './Emulation.css';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';

const Emulation = (props) => {
    const [loading, setLoading] = useState(false);
    const [emulation,setEmulation] = useState(props.emulation);
    const ip = "localhost"
    // const ip = "172.31.212.92"


    const startOrStopEmulationRequest = useCallback((emulation_name) => {
        fetch(
            `http://` + ip + ':7777/emulations/' + emulation_name,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setLoading(false)
                setEmulation(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startorStopEmulation = (emulation) => {
        setLoading(true)
        startOrStopEmulationRequest(emulation.name)
    }

    const getSubnetMasks = (emulation) => {
        let networks = emulation.containers_config.networks
        const subnets = []
        for (let i = 0; i < networks.length; i++) {
            subnets.push(networks[i].subnet_mask)
        }
        return subnets.join(", ")
    }

    const getNetworkNames = (emulation) => {
        let networks = emulation.containers_config.networks
        const network_names = []
        for (let i = 0; i < networks.length; i++) {
            network_names.push(networks[i].name)
        }
        return network_names.join(", ")
    }

    const getIps = (ips_and_networks) => {
        const ips = []
        for (let i = 0; i < ips_and_networks.length; i++) {
            ips.push(ips_and_networks[i][0])
        }
        return ips
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

    const renderStartEmulationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start emulation
        </Tooltip>
    );

    const renderStopEmulationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop emulation
        </Tooltip>
    );


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
                        overlay={renderStopEmulationTooltip()}
                    >
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startorStopEmulation(emulation)}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            } else {
                return (
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStartEmulationTooltip}
                    >
                        <Button variant="outline-dark" className="startButton"
                                onClick={() => startorStopEmulation(emulation)}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                )
            }
        }
    };


    return (<Card key={emulation.name} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={emulation.name} className="mgHeader">
                <span className="subnetTitle">ID: {emulation.id}, name: {emulation.name}</span>
                # Containers: {emulation.containers_config.containers.length}, Status: {getStatus(emulation)}
                {getSpinnerOrCircle(emulation)}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={emulation.name}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information about the emulation:
                </h5>
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
                <h5 className="semiTitle">
                    Topology
                </h5>
                <img src={`data:image/jpeg;base64,${emulation.image}`} className="topologyImg" alt="Topology"/>
                <h5 className="semiTitle">
                    Containers:
                </h5>
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
                            <td>{getIps(container.ips_and_networks)}</td>
                            <td>{container.os}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>

                <h5 className="semiTitle">
                    Flags:
                </h5>
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

                <h5 className="semiTitle">
                    Users:
                </h5>
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

                <h5 className="semiTitle">
                    Services:
                </h5>
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


                <h5 className="semiTitle">
                    Vulnerabilities:
                </h5>
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

                <h5 className="semiTitle">
                    Resources:
                </h5>
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

                <h5 className="semiTitle">
                    Network interfaces:
                </h5>
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
                    {emulation.resources_config.node_resources_configurations.filter(rc =>
                        rc !== null && rc !== undefined &&
                        rc.ips_gw_default_policy_networks !== null
                        && rc.ips_gw_default_policy_networks !== undefined).map((rc, index) =>
                        rc.ips_gw_default_policy_networks.filter((rc_net) =>
                            rc_net !== null && rc_net !== undefined).map((rc_net, index) =>
                            <tr key={rc_net[0] + "-" + index}>
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
                            </tr>
                        ))}
                    </tbody>
                </Table>

                <h5 className="semiTitle">
                    Client population:
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>IP</th>
                        <th>Arrival process</th>
                        <th>λ</th>
                        <th>μ</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr key={emulation.traffic_config.client_population_config.ip}>
                        <td>{emulation.traffic_config.client_population_config.ip}</td>
                        <td>{emulation.traffic_config.client_population_config.client_population_process_type}</td>
                        <td>{emulation.traffic_config.client_population_config.lamb}</td>
                        <td>{emulation.traffic_config.client_population_config.mu}</td>
                    </tr>
                    </tbody>
                </Table>

                <h5 className="semiTitle">
                    Traffic commands:
                </h5>
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

                <h5 className="semiTitle">
                    Kafka log:
                </h5>
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

                <h5 className="semiTitle">
                    Kafka Topics:
                </h5>
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

                <h5 className="semiTitle">
                    Firewall configurations:
                </h5>
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
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Emulation.propTypes = {};

Emulation.defaultProps = {};

export default Emulation;
