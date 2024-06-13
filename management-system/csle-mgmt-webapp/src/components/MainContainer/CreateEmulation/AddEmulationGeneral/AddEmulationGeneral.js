import React, {useState} from 'react';
import FormControl from 'react-bootstrap/FormControl';
import Table from 'react-bootstrap/Table'
import Select from 'react-select'
import './AddEmulationGeneral.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddEmulationGeneral = (props) => {
  const idsEnabledOptions = [
    {
      value: true,
      label: "True"
    },
    {
      value: false,
      label: "False"
    }
  ]
  const [selectedIdsEnabled, setSelectedIdsEnabled] = useState(idsEnabledOptions[0]);

  const updatedIdsEnabled = (idsEnabledOption) => {
    setSelectedIdsEnabled(idsEnabledOption)
    props.handleContainerIdsEnabledChange(idsEnabledOption.value)
  }

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
              <FormControl
                  value={props.nameValue}
                  onChange={props.handleNameChange}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Name"
              />
            </td>
          </tr>
          <tr>
            <td>Network ID</td>
            <td>
              <FormControl
                  value={props.networkIdValue}
                  onChange={props.handleNetworkIdChange}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Network ID"
              />
            </td>
          </tr>
          <tr>
            <td>Level</td>
            <td>
              <FormControl
                  value={props.levelValue}
                  onChange={props.handleLevelChange}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Level"
              />
            </td>
          </tr>
          <tr>
            <td>Version</td>
            <td>
              <FormControl
                  value={props.versionValue}
                  onChange={props.handleVersionChange}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Version"
              />
            </td>
          </tr>
          <tr>
            <td>Time step length in Seconds</td>
            <td>
              <FormControl
                  value={props.timeStepLengthValue}
                  onChange={props.handleTimeStepLengthChange}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Time step length"
              />
            </td>
          </tr>
          <tr>
            <td>IDS enabled</td>
            <td>
              <Select
                  style={{display: 'inline-block'}}
                  value={selectedIdsEnabled}
                  defaultValue={selectedIdsEnabled}
                  options={idsEnabledOptions}
                  onChange={updatedIdsEnabled}
                  placeholder="IDS enabled"
              />
            </td>
          </tr>
          <tr>
            <td>Description</td>
            <td>
              <FormControl
                  value={props.description.textareaValue}
                  onChange={props.handleDescriptionChange}
                  as="textarea"
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Description"
                  rows={3}
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
