import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddUsers.css';

/**
 * Component representing the AddUsers part of the create emulation page
 */
const AddUsers = (props) => {

  const rootAccessOptions = [
    {
      value: true,
      label: "True"
    },
    {
      value: false,
      label: "False"
    }
  ]

  const [selectedRootAccess, setSelectedRootAccess] = useState(rootAccessOptions[0]);

  const updatedRootAccess = (rootAccessOption) => {
    setSelectedRootAccess(rootAccessOption)
    props.handleContainerUserAccessChange(rootAccessOption.value, props.containerIndex)
  }

  return (
    <div>
      <div>
        Add a user to the container {props.container.name} &nbsp;&nbsp;
        <Button type="button"
                onClick={() => props.handleAddUser(props.containerIndex)}
                variant="success" size="sm">
          <i className="fa fa-plus" aria-hidden="true" />
        </Button>
      </div>
      <div className="table-responsive-user">
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>User Attribute</th>
            <th>Value</th>
          </tr>
          </thead>
          <tbody>
          {props.container.users.map((containerUsers, userIndex) => (
            <React.Fragment
              key={'form-user-' + containerUsers.userName + '-' + userIndex + '-' + props.containerIndex}>
              <tr
                key={'user-name-' + containerUsers.userName + '-' + userIndex + '-' + props.containerIndex}>
                <td> <Button type="button" onClick={() =>
                    props.handleDeleteContainerUser(props.containerIndex, userIndex)}
                             variant="danger" size="sm"
                             style={{ marginRight: '5px' }}>
                  <i className="fa fa-trash startStopIcon"
                     aria-hidden="true" />
                </Button> Username</td>
                <td>
                  <FormControl
                      ref={props.inputUserNameRef}
                      value={containerUsers.userName}
                      onChange={(event) => props.handleContainerUserNameChange(event, props.containerIndex, userIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Username"
                  />
                </td>
              </tr>
              <tr key={'pw-' + containerUsers.pw + '-' + userIndex + '-' + props.containerIndex}>
                <td> Password</td>
                <td>
                  <FormControl
                      ref={props.inputPwRef}
                      value={containerUsers.pw}
                      onChange={(event) => props.handleContainerUserPwChange(event, props.containerIndex, userIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Password"
                  />
                </td>
              </tr>
              <tr className="custom-td">
                <td> Root Access</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedRootAccess}
                      defaultValue={selectedRootAccess}
                      options={rootAccessOptions}
                      onChange={updatedRootAccess}
                      placeholder="Root access"
                      className="createEmulationInput"
                      size="sm"
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

AddUsers.propTypes = {};
AddUsers.defaultProps = {};
export default AddUsers;
