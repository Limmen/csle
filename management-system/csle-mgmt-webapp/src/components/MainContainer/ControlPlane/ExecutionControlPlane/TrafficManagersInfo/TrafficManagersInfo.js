import React from 'react';
import './TrafficManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

/**
 * Subcomponent of the /control-plane page that contains information about traffic managers
 */
const TrafficManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setTrafficManagersOpen(!props.trafficManagersOpen)}
                    aria-controls="trafficManagersBody"
                    aria-expanded={props.trafficManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Traffic managers </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.trafficManagersOpen}>
                <div id="trafficManagersBody" className="cardBodyHidden">
                    <div className="aggregateActionsContainer">
                        <span className="aggregateActions">Stop all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("traffic-manager-stop-all")}
                            running={true} entity="traffic-manager"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all managers:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("traffic-manager-start-all")}
                            running={false} entity="traffic-manager"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Stop all generators:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("traffic-generator-stop-all")}
                            running={true} entity="traffic-generator"
                            name="stop-all" ip="stop-all"
                            startOrStop={props.startOrStop}
                        />
                        <span className="aggregateActions">Start all generators:</span>
                        <SpinnerOrButton
                            loading={props.loadingEntities.includes("traffic-generator-start-all")}
                            running={false} entity="traffic-generator"
                            name="start-all" ip="start-all"
                            startOrStop={props.startOrStop}
                        />
                    </div>
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Service</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.trafficManagersInfo.traffic_managers_statuses.map((status, index) =>
                                <tr key={"traffic-manager-" + index}>
                                    <td>Traffic Manager</td>
                                    <td>{props.trafficManagersInfo.ips[index]}</td>
                                    <td>{props.trafficManagersInfo.ports[index]}</td>
                                    {props.activeStatus(props.trafficManagersInfo.traffic_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("traffic-manager-" +
                                                props.trafficManagersInfo.ips[index])}
                                            running={props.trafficManagersInfo.traffic_managers_running[index]}
                                            entity={"traffic-manager"} name={"traffic-manager"}
                                            ip={props.trafficManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                    entity="traffic-manager"/>
                                    </td>
                                </tr>
                            )}
                            {props.trafficManagersInfo.traffic_managers_statuses.map((status, index) =>
                                <tr key={"traffic-generator-" + index}>
                                    <td>Traffic Generator</td>
                                    <td>{props.trafficManagersInfo.ips[index]}</td>
                                    <td>-</td>
                                    {props.activeStatus(status.running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes("traffic-generator-" +
                                                props.trafficManagersInfo.ips[index])}
                                            running={status.running}
                                            entity={"traffic-generator"} name={"traffic-generator"}
                                            ip={props.trafficManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.trafficManagersInfo.ips[index]}
                                                    entity="traffic-manager"/>
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

TrafficManagersInfo.propTypes = {};
TrafficManagersInfo.defaultProps = {};
export default TrafficManagersInfo;
