import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddVulns.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddVulns = (props) => {

  const vulnerabilityRootOptions = [
    {
      value: true,
      label: "true"
    },
    {
      value: false,
      label: "false"
    }
  ]
  const vulnerabilityTypeOptions = [
    {
      value: 0,
      label: "Weak password"
    },
    {
      value: 1,
      label: "Remote code execution"
    },
    {
      value: 2,
      label: "SQL injection"
    },
    {
      value: 3,
      label: "Privilege escalation"
    }
  ]
  const credentialAccessOptions = [
    {
      value: true,
      label: "true"
    },
    {
      value: false,
      label: "false"
    }
  ]

  const [selectedVulnerabilityRoot, setSelectedVulnerabilityRoot] = useState(vulnerabilityRootOptions[0]);
  const [selectedVulnerabilityType, setSelectedVulnerabilityType] = useState(vulnerabilityTypeOptions[0]);
  const [selectedCredentialAccess, setSelectedCredentialAccess] = useState(credentialAccessOptions[0]);

  const updatedSelectedVulnerabilityRoot = (selectedVulnerabilityRootOption, vulnIndex) => {
    setSelectedVulnerabilityRoot(selectedVulnerabilityRootOption)
    props.handleVulnAccessChange(selectedVulnerabilityRootOption.value, props.containerIndex, vulnIndex)
  }

  const updatedSelectedVulnerabilityType = (selectedVulnerabilityTypeOption, vulnIndex) => {
    setSelectedVulnerabilityType(selectedVulnerabilityTypeOption)
    props.handleVulnTypeChange(selectedVulnerabilityTypeOption.value, props.containerIndex, vulnIndex)
  }

  const updatedCredentialAccess = (selectedCredentialAccessOption, vulnIndex, credIndex, credType) => {
    setSelectedCredentialAccess(selectedCredentialAccessOption)
    props.handleVulnCredentialChange(selectedCredentialAccessOption.value, props.containerIndex, vulnIndex, credIndex, credType)
  }

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
                  <FormControl
                      ref={props.inputVulnServiceNameRef}
                      value={props.container.vulns[vulnIndex].name}
                      onChange={(e) => props.handleVulnServiceChange(e, props.containerIndex, vulnIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Vulnerability service"
                  />
                </td>
              </tr>
              <tr>
                <td>Vulnerability needed Root access</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedVulnerabilityRoot}
                      defaultValue={selectedVulnerabilityRoot}
                      options={vulnerabilityRootOptions}
                      onChange={(e) => updatedSelectedVulnerabilityRoot(e, props.containerIndex, vulnIndex)}
                      placeholder="Boolean flag whether vulnerability gives root access or not"
                      className="createEmulationInput"
                      size="sm"
                  />
                </td>
              </tr>
              <tr>
                <td>Vulnerability type</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedVulnerabilityType}
                      defaultValue={selectedVulnerabilityType}
                      options={vulnerabilityTypeOptions}
                      onChange={(e) => updatedSelectedVulnerabilityType(e, props.containerIndex, vulnIndex)}
                      placeholder="Vulnerability type"
                      className="createEmulationInput"
                      size="sm"
                  />
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
                      <label style={{fontSize: '12px', marginRight: '5px'}}>Credential root</label>
                      <Select
                          style={{display: 'inline-block'}}
                          value={selectedCredentialAccess}
                          defaultValue={selectedCredentialAccess}
                          options={credentialAccessOptions}
                          onChange={(e) => updatedCredentialAccess(e, props.containerIndex, vulnIndex, credIndex, 'vulnCredRoot')}
                          placeholder="Boolean flag whether the vulnerability gives root access or not"
                          className="createEmulationInput"
                          size="sm"
                      />
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
