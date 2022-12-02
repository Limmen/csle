import React from 'react';
import './KafkaManagersInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";
import convertListToCommaSeparatedString from "../../../../Common/convertListToCommaSeparatedString";
import {KAFKA_MANAGER_SUBRESOURCE, KAFKA_SUBRESOURCE} from "../../../../Common/constants";
import KafkaImg from "./../../../Emulations/Emulation/Kafka.png"

/**
 * Subcomponent of the /control-plane page that contains information about kafka managers
 */
const KafkaManagersInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setKafkaManagersOpen(!props.kafkaManagersOpen)}
                    aria-controls="kafkaManagersBody"
                    aria-expanded={props.kafkaManagersOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Kafka managers
                        <img src={KafkaImg} alt="Kafka" className="img-fluid headerIcon kafka"/>
                    </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.kafkaManagersOpen}>
                <div id="kafkaManagersBody" className="cardBodyHidden">
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Service</th>
                                <th>IP</th>
                                <th>Port</th>
                                <th>Topics</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.kafkaManagersInfo.kafka_managers_statuses.map((status, index) =>
                                <tr key={`${KAFKA_MANAGER_SUBRESOURCE}-${index}`}>
                                    <td>Kafka Manager</td>
                                    <td>{props.kafkaManagersInfo.ips[index]}</td>
                                    <td>{props.kafkaManagersInfo.ports[index]}</td>
                                    <td></td>
                                    {props.activeStatus(props.kafkaManagersInfo.kafka_managers_running[index])}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${KAFKA_MANAGER_SUBRESOURCE}-`
                                                + `${props.kafkaManagersInfo.ips[index]}`)}
                                            running={props.kafkaManagersInfo.kafka_managers_running[index]}
                                            entity={KAFKA_MANAGER_SUBRESOURCE} name={KAFKA_MANAGER_SUBRESOURCE}
                                            ip={props.kafkaManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.kafkaManagersInfo.ips[index]}
                                                    entity={KAFKA_MANAGER_SUBRESOURCE}
                                                    getLogs={props.getLogs}
                                        />
                                    </td>
                                </tr>
                            )}
                            {props.kafkaManagersInfo.kafka_managers_statuses.map((status, index) =>
                                <tr key={`${KAFKA_SUBRESOURCE}-${index}`}>
                                    <td>Kafka
                                    </td>
                                    <td>{props.kafkaManagersInfo.ips[index]}</td>
                                    <td>{props.kafkaPort}</td>
                                    <td>{convertListToCommaSeparatedString(status.topics)}</td>
                                    {props.activeStatus(status.running)}
                                    <td>
                                        <SpinnerOrButton
                                            loading={props.loadingEntities.includes(
                                                `${KAFKA_SUBRESOURCE}-`
                                                + `${props.kafkaManagersInfo.ips[index]}`)}
                                            running={status.running}
                                            entity={KAFKA_SUBRESOURCE} name={KAFKA_SUBRESOURCE}
                                            ip={props.kafkaManagersInfo.ips[index]}
                                            startOrStop={props.startOrStop}
                                        />
                                        <LogsButton name={props.kafkaManagersInfo.ips[index]}
                                                    entity={KAFKA_SUBRESOURCE}
                                                    getLogs={props.getLogs}
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

KafkaManagersInfo.propTypes = {};
KafkaManagersInfo.defaultProps = {};
export default KafkaManagersInfo;
