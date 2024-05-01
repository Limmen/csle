import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddEmulationGeneral.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddEmulationGeneral = (props) => {

  return (
    <div>
      <div className="table-responsive">
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>Attribute</th>
            <th> Value</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>Name</td>
            <td>
              <input
                type="text"
                value={props.nameValue}
                onChange={props.handleNameChange}
              />
            </td>
          </tr>
          <tr>
            <td>Network ID</td>
            <td>
              <input
                type="text"
                value={props.networkIdValue}
                onChange={props.handleNetworkIdChange}
              />
            </td>
          </tr>
          <tr>
            <td>Level</td>
            <td>
              <input
                type="text"
                value={props.levelValue}
                onChange={props.handleLevelChange}
              />
            </td>
          </tr>
          <tr>
            <td>Version</td>
            <td>
              <input
                type="text"
                value={props.versionValue}
                onChange={props.handleVersionChange}
              />
            </td>
          </tr>
          <tr>
            <td>Time step length in Seconds</td>
            <td>
              <input
                type="text"
                value={props.timeStepLengthValue}
                onChange={props.handleTimeStepLengthChange}
              />
            </td>
          </tr>
          <tr>
            <td>IDS enabled</td>
            <td>
              <select value={props.idsEnabled}
                      onChange={(e) => props.handleContainerIdsEnabledChange(e)}>
                <option value="true">True</option>
                <option value="false">False</option>

              </select>
            </td>
          </tr>
          <tr>
            <td>Description</td>
            <td>
                          <textarea
                            id="description"
                            value={props.description.textareaValue}
                            onChange={props.handleDescriptionChange}
                            rows="4"
                            style={{ width: '100%', boxSizing: 'border-box' }}
                          />
            </td>
          </tr>
          </tbody>
        </Table>
      </div>
    </div>
  )
}

AddEmulationGeneral.propTypes = {};
AddEmulationGeneral.defaultProps = {};
export default AddEmulationGeneral;
