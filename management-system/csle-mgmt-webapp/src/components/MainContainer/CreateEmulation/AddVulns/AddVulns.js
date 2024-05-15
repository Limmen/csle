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
              <tr>
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
              <tr>
                <td>Vulnerability needed Root access</td>
                <td>
                  <select
                    value={props.container.vulns[vulnIndex].vulnRoot}
                    onChange={(e) => props.handleVulnAccessChange(e, props.containerIndex, vulnIndex)}>
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </select>
                </td>
              </tr>
              <tr className="custom-td">
                <td>Vulnerability type</td>
                <td>
                  <select
                    value={props.container.vulns[vulnIndex].vulnType}
                    onChange={(e) => props.handleVulnTypeChange(e, props.containerIndex, vulnIndex)}>
                    <option value="0">Weak password</option>
                    <option value="1">Remote code execution</option>
                    <option value="2">SQL injection</option>
                    <option value="3">Privilage escalation</option>
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

AddVulns.propTypes = {};
AddVulns.defaultProps = {};
export default AddVulns;
