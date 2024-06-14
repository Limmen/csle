import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddServices.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddServices = (props) => {

    const serviceProtocolOptions = [
        {
            value: 0,
            label: "TCP"
        },
        {
            value: 1,
            label: "UDP"
        }
    ]
    const [selectedServiceProtocol, setSelectedServiceProtocol] = useState(serviceProtocolOptions[0]);

    const updatedServiceProtocol = (selectedServiceProtocolOption, serviceIndex) => {
        setSelectedServiceProtocol(selectedServiceProtocolOption)
        props.handleProtocolChange(selectedServiceProtocolOption.value, props.containerIndex, serviceIndex)
    }

    return (
        <div>
            <div>
                Add services to the container {props.container.name} &nbsp;&nbsp;
                <Button type="button"
                        onClick={() => props.addServiceHandler(props.containerIndex)}
                        variant="success" size="sm">
                    <i className="fa fa-plus" aria-hidden="true"/>
                </Button>
            </div>

            <div className="table-responsive-service">
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Service Attribute</th>
                        <th>Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.container.services.map((containerService, serviceIndex) => (
                        <React.Fragment
                            key={'form-service-' + containerService.protocol + '-' + serviceIndex + '-' + props.containerIndex}>
                            <tr
                                key={'service-name-' + containerService.name + '-' + serviceIndex + '-' + props.containerIndex}>
                                <td> <Button type="button" onClick={() =>
                                    props.handleDeleteService(props.containerIndex, serviceIndex)}
                                             variant="danger" size="sm"
                                             style={{marginRight: '5px'}}>
                                    <i className="fa fa-trash startStopIcon"
                                       aria-hidden="true"/>
                                </Button> Service name</td>
                                <td>
                                    <FormControl
                                        ref={props.inputServiceNameRef}
                                        value={containerService.name}
                                        onChange={(event) => props.handleServiceNameChange(event, props.containerIndex, serviceIndex)}
                                        size="sm"
                                        className="createEmulationInput"
                                        placeholder="Name"
                                    />
                                </td>
                            </tr>
                            <tr key={'service-protocol' + containerService.protocol + '-' + serviceIndex + '-' + props.containerIndex}>
                                <td> Service protocol</td>
                                <td>
                                    <Select
                                        style={{display: 'inline-block'}}
                                        value={selectedServiceProtocol}
                                        defaultValue={selectedServiceProtocol}
                                        options={serviceProtocolOptions}
                                        onChange={(value) => updatedServiceProtocol(value, props.containerIndex, serviceIndex)}
                                        placeholder="Transport protocol for the service"
                                        className="createEmulationInput"
                                        size="sm"
                                    />
                                </td>
                            </tr>
                            <tr key={'service-port' + containerService.port + '-' + serviceIndex + '-' + props.containerIndex}>
                                <td> Service port</td>
                                <td>
                                    <FormControl
                                        ref={props.inputServicePortRef}
                                        value={containerService.port}
                                        onChange={(event) => props.handleServicePortChange(event, props.containerIndex, serviceIndex)}
                                        size="sm"
                                        className="createEmulationInput"
                                        placeholder="Service port"
                                    />
                                </td>
                            </tr>
                            <tr className="custom-td">
                                <td> Service IP</td>
                                <td>
                                    <FormControl
                                        ref={props.inputServiceIpRef}
                                        value={containerService.serviceIp}
                                        onChange={(e) => props.handleServiceIpChange(e, props.containerIndex, serviceIndex)}
                                        size="sm"
                                        className="createEmulationInput"
                                        placeholder="Service IP"
                                    />
                                </td>
                            </tr>
                        </React.Fragment>
                    ))}
                    </tbody>
                </Table>
            </div>
        </div>
    )
}

AddServices.propTypes = {};
AddServices.defaultProps = {};
export default AddServices;
