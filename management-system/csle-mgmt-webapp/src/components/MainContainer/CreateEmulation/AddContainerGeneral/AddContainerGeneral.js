import React, {useState} from 'react';
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddContainerGeneral.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddContainerGeneral = (props) => {

  const flagRequiresRootOptions = [
    {
      value: true,
      label: "True"
    },
    {
      value: false,
      label: "False"
    }
  ]
  const reachableByAgentOptions = [
    {
      value: true,
      label: "True"
    },
    {
      value: false,
      label: "False"
    }
  ]
  const [flagRequiresRootSelected, setFlagRequiresRootSelected] = useState(flagRequiresRootOptions[0]);
  const [reachableByAgentOptionsSelected, setReachableByAgentOptionsSelected] = useState(reachableByAgentOptions[0]);

  const updatedFlagRequiresRoot = (flagRequiresRootOption) => {
    setFlagRequiresRootSelected(flagRequiresRootOption)
    props.handleFlagPermissionChange(flagRequiresRootOption.value, props.containerIndex)
  }

  const updatedReachableByAgent = (reachableByAgentOption) => {
    setReachableByAgentOptionsSelected(reachableByAgentOption)
    props.handleReachableByAgentChange(reachableByAgentOption.value, props.containerIndex)
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
              {props.container.name}
            </td>
          </tr>
          <tr>
            <td>OS</td>
            <td>
              {props.container.os}
            </td>
          </tr>
          <tr>
            <td>Number of allocated CPU cores</td>
            <td>
              <FormControl
                  value={props.container.cpu}
                  onChange={(event) => props.handleCpuChange(event, props.containerIndex)}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="# CPUs"
              />
            </td>
          </tr>
          <tr>
            <td>Available memory in GB</td>
            <td>
              <FormControl
                  value={props.container.mem}
                  onChange={(event) => props.handleMemoryChange(event, props.containerIndex)}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Memory (GB)"
              />
            </td>
          </tr>
          <tr>
            <td>Flag ID</td>
            <td>
              <FormControl
                  value={props.container.flagId}
                  onChange={(event) => props.handleFlagIdChange(event, props.containerIndex)}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Flag ID"
              />
            </td>
          </tr>
          <tr>
            <td>Flag score</td>
            <td>
              <FormControl
                  value={props.container.flagScore}
                  onChange={(event) => props.handleFlagScoreChange(event, props.containerIndex)}
                  size="sm"
                  className="createEmulationInput"
                  placeholder="Flag Score"
              />
            </td>
          </tr>
          <tr>
            <td>Flag requires root permission</td>
            <td>
              <Select
                  style={{display: 'inline-block'}}
                  value={flagRequiresRootSelected}
                  defaultValue={flagRequiresRootSelected}
                  options={flagRequiresRootOptions}
                  onChange={updatedFlagRequiresRoot}
                  placeholder="Flag requires root"
                  className="createEmulationInput"
                  size="sm"
              />
            </td>
          </tr>
          <tr>
            <td>Reachable by agent</td>
            <td>
              <Select
                  style={{display: 'inline-block'}}
                  value={reachableByAgentOptionsSelected}
                  defaultValue={reachableByAgentOptionsSelected}
                  options={reachableByAgentOptions}
                  onChange={updatedReachableByAgent}
                  placeholder="Reachable by agent"
                  className="createEmulationInput selectMarginBottom"
                  size="sm"
              />
            </td>
          </tr>
          </tbody>
        </Table>
      </div>
    </div>
  )
}

AddContainerGeneral.propTypes = {};
AddContainerGeneral.defaultProps = {};
export default AddContainerGeneral;
