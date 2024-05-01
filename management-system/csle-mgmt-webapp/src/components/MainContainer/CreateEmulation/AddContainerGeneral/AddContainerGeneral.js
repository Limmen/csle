import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddContainerGeneral.css';

/**
 * Component representing the AddServices part of the create emulation page
 */
const AddContainerGeneral = (props) => {

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
              {/*<SpinnerOrTable images={filteredImages} loading={loading} index={index} />*/}
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
              <input
                type="text"
                value={props.container.cpu}
                onChange={(event) => props.handleCpuChange(event, props.containerIndex)}
              />
            </td>
          </tr>
          <tr>
            <td>Available memory in GB</td>
            <td>
              <input
                type="text"
                value={props.container.mem}
                onChange={(event) => props.handleMemoryChange(event, props.containerIndex)}
              />
            </td>
          </tr>
          <tr>
            <td>Flag ID</td>
            <td>
              <input
                type="text"
                value={props.container.flagId}
                onChange={(event) => props.handleFlagIdChange(event, props.containerIndex)}
              />
            </td>
          </tr>
          <tr>
            <td>Flag score</td>
            <td>
              <input
                type="text"
                value={props.container.flagScore}
                onChange={(event) => props.handleFlagScoreChange(event, props.containerIndex)}
              />
            </td>
          </tr>
          <tr>
            <td>Flag requires root permission</td>
            <td>
              <select value={props.container.flagPermission}
                      onChange={(e) => props.handleFlagPermissionChange(e, props.containerIndex)}>
                <option value="true">True</option>
                <option value="false">False</option>

              </select>
            </td>
          </tr>
          <tr>
            <td>Reachable by agent</td>
            <td>
              <select
                value={props.container.reachableByAgent}
                onChange={(e) => props.handleReachableByAgentChange(e, props.containerIndex)}>
                <option value="true">True</option>
                <option value="false">False</option>

              </select>
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
