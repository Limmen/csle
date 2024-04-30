import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddServices.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddServices = (props) => {

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
                                <td> Service name</td>
                                <td>
                                    <input
                                        ref={props.inputServiceNameRef}
                                        type="text"
                                        value={containerService.name}
                                        onChange={(event) => props.handleServiceNameChange(event, props.containerIndex, serviceIndex)}
                                    />
                                    <Button type="button" onClick={() =>
                                        props.handleDeleteService(props.containerIndex, serviceIndex)}
                                            variant="danger" size="sm"
                                            style={{marginLeft: '5px'}}>
                                        <i className="fa fa-trash startStopIcon"
                                           aria-hidden="true"/>
                                    </Button>
                                </td>
                            </tr>
                            <tr key={'service-protocol' + containerService.protocol + '-' + serviceIndex + '-' + props.containerIndex}>
                                <td> Service protocol</td>
                                <td>
                                    <select
                                        value={containerService.protocol}
                                        onChange={(e) => props.handleProtocolChange(e, props.containerIndex, serviceIndex)}>
                                        <option value="tcp">tcp</option>
                                        <option value="udp">udp</option>
                                    </select>
                                </td>
                            </tr>
                            <tr key={'service-port' + containerService.port + '-' + serviceIndex + '-' + props.containerIndex}>
                                <td> Service port</td>
                                <td>
                                    <input
                                        ref={props.inputServicePortRef}
                                        type="text"
                                        value={containerService.port}
                                        onChange={(event) => props.handleServicePortChange(event, props.containerIndex, serviceIndex)}
                                    />
                                </td>
                            </tr>
                            <tr className="custom-td">
                                <td> Service IP</td>
                                <td>
                                    <select
                                        value={containerService.serviceIp}
                                        onChange={(e) => props.handleServiceIpChange(e, props.containerIndex, serviceIndex)}>
                                        <option value="">Select IP</option>
                                        {props.container.interfaces.map((interfaceToUse, indexToUse) => (
                                            <option
                                                key={"service-ip" + indexToUse}
                                                value={interfaceToUse.ip}>{interfaceToUse.ip}</option>
                                        ))}
                                    </select>
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
