import React from 'react';
import './ContainersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import getIps from "../../src/components/Common/getIps";
import SpinnerOrButton from "../../src/components/MainContainer/ControlPlane/ExecutionControlPlane/SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../../src/components/MainContainer/ControlPlane/ExecutionControlPlane/LogsButton/LogsButton";

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
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.runningContainersOpen}>
                <div id="activeNetworksBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all containers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("container-stop-all")}
                            running={true} entity="container"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all containers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("container-start-all")}
                            running={false} entity="container"
                            name="start-all" ip="start-all"
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
                                    <td className="containerRunningStatus"> Running</td>
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("container-"
                                                + container.full_name_str)}
                                            running={true} entity="container"
                                            name={container.full_name_str} ip={container.full_name_str}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={container.full_name_str} entity="container"/>
                                        <ShellButton
                                            loading={props.loadingEntities.includes("container-" +
                                                container.full_name_str + "-shell")}
                                            name={container.full_name_str}/>
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
                                            loading={props.loadingEntities.includes("container-" +
                                                container.full_name_str)}
                                            running={false} entity="container"
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
