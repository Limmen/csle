import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddUsers.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddUsers = (props) => {

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
                <td> Username</td>
                <td>
                  <input
                    ref={props.inputUserNameRef}
                    type="text"
                    value={containerUsers.userName}
                    onChange={(event) => props.handleContainerUserNameChange(event, props.containerIndex, userIndex)}
                  />
                  <Button type="button" onClick={() =>
                    props.handleDeleteContainerUser(props.containerIndex, userIndex)}
                          variant="danger" size="sm"
                          style={{ marginLeft: '5px' }}>
                    <i className="fa fa-trash startStopIcon"
                       aria-hidden="true" />
                  </Button>
                </td>
              </tr>
              <tr key={'pw-' + containerUsers.pw + '-' + userIndex + '-' + props.containerIndex}>
                <td> Password</td>
                <td>
                  <input
                    ref={props.inputPwRef}
                    type="text"
                    value={containerUsers.pw}
                    onChange={(event) => props.handleContainerUserPwChange(event, props.containerIndex, userIndex)}
                  />
                </td>
              </tr>
              <tr className="custom-td">
                <td> Root Access</td>
                <td>
                  <select value={containerUsers.root}
                          onChange={(e) => props.handleContainerUserAccessChange(e, props.containerIndex,
                            userIndex)}>
                    <option value="True">True</option>
                    <option value="False">false</option>
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

AddUsers.propTypes = {};
AddUsers.defaultProps = {};
export default AddUsers;
