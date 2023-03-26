import React from 'react';
import './ContainersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import getIps from "../../../../Common/getIps";
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import ShellButton from "../ShellButton/ShellButton";
import DockerImg from "./../../../Emulations/Emulation/Docker.png"
import {CONTAINER_SUBRESOURCE, STOP_ALL_PROPERTY, START_ALL_PROPERTY} from "../../../../Common/constants";

/**
 * Subcomponent of the /control-plane page that represents information about containers
 */
const ContainersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setRunningContainersOpen(!props.runningContainersOpen)}
                    aria-controls="runningContainersBody"
                    aria-expanded={props.runningContainersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Docker container statuses
                        <img src={DockerImg} alt="Docker" className="img-fluid headerIcon kafka"/>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.runningContainersOpen}>
                <div id="activeNetworksBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all containers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${CONTAINER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
                            running={true} entity={CONTAINER_SUBRESOURCE}
                            name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all containers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes(
                                `${CONTAINER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
                            running={false} entity={CONTAINER_SUBRESOURCE}
                            name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
                            startOrStop={props.startOrStop}
                        />
                    </div>
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Name</th>
                                <th>Image</th>
                                <th>Os</th>
                                <th>IPs</th>
                                <th>External IP</th>
                                <th>Physical server</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.runningContainers.map((container, index) =>
                                <tr key={container.full_name_str + "-" + index}>
                                    <td>{container.full_name_str}</td>
                                    <td>{container.name}</td>
                                    <td>{container.os}</td>
                                    <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                    <td>{container.docker_gw_bridge_ip}</td>
                                    <td>{container.physical_host_ip}</td>
                                    <td className="containerRunningStatus"> Running</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${CONTAINER_SUBRESOURCE}-${container.full_name_str}`)}
                                            running={true} entity={CONTAINER_SUBRESOURCE}
                                            name={container.full_name_str} ip={container.full_name_str}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={container.full_name_str} entity={CONTAINER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                        <ShellButton
                                            loading={props.loadingEntities.includes(
                                                `${CONTAINER_SUBRESOURCE}-${container.full_name_str}`)}
                                            name={container.full_name_str}
                                            ip={container.docker_gw_bridge_ip}
                                            executionId={props.executionId}
                                            emulation={props.emulation}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.stoppedContainers.map((container, index) =>
                                <tr key={container.full_name_str + "-" + index}>
                                    <td>{container.full_name_str}</td>
                                    <td>{container.name}</td>
                                    <td>{container.os}</td>
                                    <td>{getIps(container.ips_and_networks).join(", ")}</td>
                                    <td className="containerStoppedStatus">Stopped</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${CONTAINER_SUBRESOURCE}-${container.full_name_str}`)}
                                            running={false} entity={CONTAINER_SUBRESOURCE}
                                            name={container.full_name_str} ip={container.full_name_str}
                                            startOrStop={props.startOrStop}
                                        />
                                    </td>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </Collapse>
        </Card>
    );
}

ContainersInfo.propTypes = {};
ContainersInfo.defaultProps = {};
export default ContainersInfo;
