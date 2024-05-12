import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddVulns.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddVulns = (props) => {

  return (
    <div>
      <div>
        Add a vulnerability to the container {props.container.name} &nbsp;&nbsp;
        <Button type="button"
                onClick={() => props.addVulnHandler(props.containerIndex)}
                variant="success" size="sm">
          <i className="fa fa-plus" aria-hidden="true"/>
        </Button>
      </div>

      <div className="table-responsive-vulns">
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>Vulnerability Attribute</th>
            <th>Value</th>
          </tr>
          </thead>
          <tbody>
          {props.container.vulns.map((containerVuln, vulnIndex) => (
            <React.Fragment
              key={'form-vul-' + containerVuln.protocol + '-' + vulnIndex + '-' + props.containerIndex}>
              <tr
                key={'vul-name-' + containerVuln.name + '-' + vulnIndex + '-' + props.containerIndex}>
                <td> Vulnerability name</td>
                <td>
                  <input
                    ref={props.inputVulnNameRef}
                    type="text"
                    value={containerVuln.vulnName}
                    onChange={(event) => props.handleVulnNameChange(event, props.containerIndex, vulnIndex)}
                  />
                  <Button type="button" onClick={() =>
                    props.handleDeleteVuln(props.containerIndex, vulnIndex)}
                          variant="danger" size="sm"
                          style={{ marginLeft: '5px' }}>
                    <i className="fa fa-trash startStopIcon"
                       aria-hidden="true" />
                  </Button>
                </td>
              </tr>
              <tr className="custom-td">
                <td>Vulnerability service</td>
                <td>
                  <select
                    value={props.container.vulns[vulnIndex].name}
                    onChange={(e) => props.handleVulnServiceChange(e, props.containerIndex, vulnIndex)}>
                    <option value="">Select Service</option>
                    {props.container.services.map((serviceToUse, indexToUse) => (
                      <option
                        key={'vuln-service-name' + indexToUse}
                        value={indexToUse}>{serviceToUse.name}</option>
                    ))}
                  </select>
                </td>
              </tr>


              {/*<tr key={'service-protocol' + containerService.protocol + '-' + serviceIndex + '-' + props.containerIndex}>*/}
              {/*  <td> Service protocol</td>*/}
              {/*  <td>*/}
              {/*    <select*/}
              {/*      value={containerService.protocol}*/}
              {/*      onChange={(e) => props.handleProtocolChange(e, props.containerIndex, serviceIndex)}>*/}
              {/*      <option value="tcp">tcp</option>*/}
              {/*      <option value="udp">udp</option>*/}
              {/*    </select>*/}
              {/*  </td>*/}
              {/*</tr>*/}
              {/*<tr key={'service-port' + containerService.port + '-' + serviceIndex + '-' + props.containerIndex}>*/}
              {/*  <td> Service port</td>*/}
              {/*  <td>*/}
              {/*    <input*/}
              {/*      ref={props.inputServicePortRef}*/}
              {/*      type="text"*/}
              {/*      value={containerService.port}*/}
              {/*      onChange={(event) => props.handleServicePortChange(event, props.containerIndex, serviceIndex)}*/}
              {/*    />*/}
              {/*  </td>*/}
              {/*</tr>*/}

            </React.Fragment>
          ))}
          </tbody>
        </Table>
      </div>
    </div>
  )
}

AddVulns.propTypes = {};
AddVulns.defaultProps = {};
export default AddVulns;
