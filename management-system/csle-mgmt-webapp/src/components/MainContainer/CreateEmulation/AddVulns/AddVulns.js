import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
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
          <i className="fa fa-plus" aria-hidden="true" />
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
                <td> <Button type="button" onClick={() =>
                    props.handleDeleteVuln(props.containerIndex, vulnIndex)}
                             variant="danger" size="sm"
                             style={{ marginRight: '5px' }}>
                  <i className="fa fa-trash startStopIcon"
                     aria-hidden="true" />
                </Button> Vulnerability name</td>
                <td>
                  <FormControl
                      ref={props.inputVulnNameRef}
                      value={containerVuln.vulnName}
                      onChange={(event) => props.handleVulnNameChange(event, props.containerIndex, vulnIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Vulnerability name"
                  />
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
                    <option value="True">True</option>
                    <option value="False">False</option>
                  </select>
                </td>
              </tr>
              <tr>
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
              {props.container.vulns[vulnIndex].vulnCredentials.map((credential, credIndex) => (
                <tr key={`cred-${vulnIndex}-${credIndex}`}>
                  <td>Vulnerability Credential {credIndex + 1}</td>
                  <td>
                    <div>
                      <FormControl
                          ref={props.inputVulnCredUsernameForChangeRef}
                          value={credential.vulnCredUsername}
                          onChange={(e) => props.handleVulnCredentialChange(e, props.containerIndex, vulnIndex, credIndex, 'vulnCredUsername')}
                          size="sm"
                          className="createEmulationInput"
                          placeholder="Credential username"
                      />
                    </div>
                    <div style={{ marginTop: '5px' }}>
                      <FormControl
                          ref={props.inputVulnCredPwForChangeRef}
                          value={credential.vulnCredPw}
                          onChange={(e) => props.handleVulnCredentialChange(e, props.containerIndex, vulnIndex, credIndex, 'vulnCredPw')}
                          size="sm"
                          className="createEmulationInput"
                          placeholder="Credential password"
                      />
                    </div>
                    <div style={{ marginTop: '5px' }}>
                      <label style={{fontSize: '12px', marginRight: '5px'}}>Credentials access level</label>
                      <select
                        value={credential.vulnCredRoot}
                        onChange={(e) => props.handleVulnCredentialChange(e, props.containerIndex, vulnIndex, credIndex, 'vulnCredRoot')}>
                        <option value="True">True</option>
                        <option value="False">False</option>
                      </select>
                    </div>
                    <div style={{ marginTop: '5px' }}>
                      <Button
                        onClick={() => props.handleDeleteVulnCredential(props.containerIndex, vulnIndex, credIndex)}
                        style={{ marginLeft: '5px' }}
                        variant="danger" size="sm">
                        <i className="fa fa-trash" aria-hidden="true" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
              <tr className="custom-td">
                <td>Add vulnerability credentials</td>
                <td>
                  <div style={{ marginTop: '5px' }}>
                    <Button
                      onClick={() => {
                        if (props.containerIndex !== null && vulnIndex !== null) {
                          props.handleAddVulnCredentials(props.containerIndex, vulnIndex);
                        }
                      }}
                      style={{ marginLeft: '5px' }}
                      variant="success" size="sm">
                      <i className="fa fa-plus" aria-hidden="true" />
                    </Button>
                  </div>

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
