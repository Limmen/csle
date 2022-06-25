import React, {useState, useCallback} from 'react';
import './SDNController.css';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'

const SDNController = (props) => {
    const [loading, setLoading] = useState(false);
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const ip = "localhost"
    // const ip = "172.31.212.92"

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

    const getStatus = (emulation) => {
        if (emulation.running) {
            return "running"
        } else {
            return "stopped"
        }
    }

    const getIps = (ips_and_networks) => {
        const ips = []
        for (let i = 0; i < ips_and_networks.length; i++) {
            ips.push(ips_and_networks[i][0])
        }
        return ips
    }

    const getId = () => {
        return <span>{props.emulation.id}</span>
    }

    const SdnControllerConfig = (props) => {
        if (props.emulation.sdn_controller_config === null || props.emulation.sdn_controller_config === undefined) {
            return (<span> </span>)
        } else {
            return (
                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle">General information</h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
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

    return (
        <Card key={props.emulation.name} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.emulation.name} className="mgHeader">
                <span className="subnetTitle">ID: {getId()}, emulation name: {props.emulation.name}</span>
                Controller IPs: {getIps(props.emulation.sdn_controller_config.container.ips_and_networks).join(", ")},
                Status: {getStatus(props.emulation)}
                {getSpinnerOrCircle(props.emulation)}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.emulation.name}>
            <Card.Body>
                <SdnControllerConfig emulation={props.emulation}/>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

SDNController.propTypes = {};
SDNController.defaultProps = {};
export default SDNController;
