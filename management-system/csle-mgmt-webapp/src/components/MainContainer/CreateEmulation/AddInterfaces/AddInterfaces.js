import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddInterfaces.css';

const AddInterfaces = (props) => {
  return (
    <div>
      <div>
        Add a network interface to the
        container {props.container.name} &nbsp;&nbsp;
        <Button type="button"
                onClick={() => props.addInterfaceHandler(props.containerIndex)}
                variant="success" size="sm">
          <i className="fa fa-plus" aria-hidden="true" />
        </Button>
      </div>
      <div className="table-responsive">
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>Interface Attribute</th>
            <th>Value</th>
          </tr>
          </thead>
          <tbody>
          {props.container.interfaces.map((containerInterfaces, interfaceIndex) => (
            <React.Fragment
              key={'form-' + containerInterfaces.name + '-' + interfaceIndex + '-' + props.containerIndex}>
              <tr
                key={'interface-' + containerInterfaces.name + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td><Button type="button" onClick={() =>
                    props.deleteInterfaceHandler(props.containerIndex, interfaceIndex)}
                            variant="danger" size="sm"
                            style={{ marginRight: '5px' }}>
                  <i className="fa fa-trash startStopIcon"
                     aria-hidden="true" />
                </Button> Name</td>
                <td>
                  <FormControl
                      ref={props.inputNameRef}
                      value={containerInterfaces.name}
                      onChange={(event) => props.handleInterfaceNameChange(event, props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Name"
                  />
                </td>
              </tr>
              <tr key={'ip-' + containerInterfaces.ip + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> IP </td>
                <td>
                  <FormControl
                      ref={props.inputIPRef}
                      value={containerInterfaces.ip}
                      onChange={(event) => props.handleIPChange(event, props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="IP"
                  />
                </td>
              </tr>
              <tr
                key={'subnet-' + containerInterfaces.subnetMask + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Subnet mask</td>
                <td>
                  <FormControl
                      ref={props.inputSubnetMaskRef}
                      value={containerInterfaces.subnetMask}
                      onChange={(event) => props.handleSubnetMaskChange(event, props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Subnet mask"
                  />
                </td>
              </tr>
              <tr
                key={'eth-' + containerInterfaces.physicalInterface + '-' +
                  interfaceIndex + '-' + props.containerIndex}>
                <td>Physical interface</td>
                <td>
                  <select
                    value={containerInterfaces.physicalInterface}
                    onChange={(e) => props.handleNetworkPhysicalInterface(e, props.containerIndex, interfaceIndex)}>
                    <option value="eth0">eth0</option>
                    <option value="eth1">eth1</option>
                    <option value="eth2">eth2</option>
                    <option value="eth3">eth3</option>
                    <option value="eth4">eth4</option>
                    <option value="eth5">eth5</option>
                    <option value="eth6">eth6</option>
                    <option value="eth7">eth7</option>
                    <option value="eth8">eth8</option>
                    <option value="eth9">eth9</option>
                    <option value="eth10">eth10</option>

                  </select>
                </td>
              </tr>
              <tr
                key={'packet-limit-' + containerInterfaces.limitPacketsQueue + '-' +
                  interfaceIndex + '-' + props.containerIndex}>
                <td> Limit packets queue</td>
                <td>
                  <FormControl
                      ref={props.inputLimitPacketsQueueRef}
                      value={containerInterfaces.limitPacketsQueue}
                      onChange={(event) =>
                          props.handleLimitPacketsQueueChange(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Limits packets queue"
                  />
                </td>
              </tr>
              <tr
                key={'packet-delay-' + containerInterfaces.packetDelayMs + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay (ms)</td>
                <td>
                  <FormControl
                      ref={props.inputPacketDelayMsRef}
                      value={containerInterfaces.packetDelayMs}
                      onChange={(event) => props.handlePacketDelayMs(event, props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet delay (ms)"
                  />
                </td>
              </tr>
              <tr
                key={'packet-jitter-' + containerInterfaces.packetDelayJitterMs + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay jitter (ms)</td>
                <td>
                  <FormControl
                      ref={props.inputPacketDelayJitterMsRef}
                      value={containerInterfaces.packetDelayJitterMs}
                      onChange={(event) =>
                          props.handlePacketDelayJitterMs(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet delay jitter (ms)"
                  />
                </td>
              </tr>
              <tr
                key={'packet-correlation-' + containerInterfaces.packetDelayCorrelationPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay correlation percentage
                </td>
                <td>
                  <FormControl
                      ref={props.inputPacketDelayCorrelationPercentageRef}
                      value={containerInterfaces.packetDelayCorrelationPercentage}
                      onChange={(event) =>
                          props.handlePacketDelayCorrelationPercentage(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet delay correlation percentage"
                  />
                </td>
              </tr>
              <tr>
                <td> Packet delay distribution</td>
                <td>
                  <select
                    value={containerInterfaces.packetDelayDistribution}
                    onChange={(e) => props.handlePacketDelayDistribution(e, props.containerIndex,
                      interfaceIndex)}
                    ref={props.inputPacketDelayDistributionRef}>
                    <option value="0">Uniform</option>
                    <option value="1">Normal</option>
                    <option value="2">Pareto</option>
                    <option value="3">Pareto normal
                    </option>
                  </select>
                </td>
              </tr>
              <tr>
                <td> Packet loss type</td>
                <td>
                  <select
                    value={containerInterfaces.packetLossType}
                    onChange={(e) => props.handlePacketLossType(e, props.containerIndex,
                      interfaceIndex)}
                    ref={props.inputPacketLossTypeRef}>
                    <option value="0">Random</option>
                    <option value="1">State</option>
                    <option value="2">Gemodel</option>
                  </select>
                </td>
              </tr>
              <tr
                key={'loss-gemodelp-' + containerInterfaces.lossGemodelp + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel P</td>
                <td>
                  <FormControl
                      ref={props.inputLossGemodelpRef}
                      value={containerInterfaces.lossGemodelp}
                      onChange={(event) =>
                          props.handleLossGemodelp(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Loss GeModel P"
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelr-' + containerInterfaces.lossGemodelr + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel R</td>
                <td>
                  <FormControl
                      ref={props.inputLossGemodelrRef}
                      value={containerInterfaces.lossGemodelr}
                      onChange={(event) =>
                          props.handleLossGemodelr(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Loss GeModel R"
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelk-' + containerInterfaces.lossGemodelk + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel K</td>
                <td>
                  <FormControl
                      ref={props.inputLossGemodelkRef}
                      value={containerInterfaces.lossGemodelk}
                      onChange={(event) =>
                          props.handleLossGemodelk(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Loss GeModel K"
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelh-' + containerInterfaces.lossGemodelh + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel H</td>
                <td>
                  <FormControl
                      ref={props.inputLossGemodelhRef}
                      value={containerInterfaces.lossGemodelh}
                      onChange={(event) =>
                          props.handleLossGemodelh(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Loss GeModel H"
                  />
                </td>
              </tr>
              <tr
                key={'packet-corruption-' + containerInterfaces.packetCorruptPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet corruption percentage</td>
                <td>
                  <FormControl
                      ref={props.inputPacketCorruptPercentageRef}
                      value={containerInterfaces.packetCorruptPercentage}
                      onChange={(event) =>
                          props.handlePacketCorruptPercentage(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet corruption percentage"
                  />
                </td>
              </tr>
              <tr
                key={'packet-corruption-correlation' +
                  containerInterfaces.packetCorruptCorrelationPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet corruption correlation
                  percentage
                </td>
                <td>
                  <FormControl
                      ref={props.inputPacketCorruptCorrelationPercentageRef}
                      value={containerInterfaces.packetCorruptCorrelationPercentage}
                      onChange={(event) =>
                          props.handlePacketCorruptCorrelationPercentage(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet corruption correlation percentage"
                  />
                </td>
              </tr>
              <tr
                key={'pecket-duplicate-percentage-' +
                  containerInterfaces.packetDuplicatePercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet duplicate percentage</td>
                <td>
                  <FormControl
                      ref={props.inputPacketDuplicatePercentageRef}
                      value={containerInterfaces.packetDuplicatePercentage}
                      onChange={(event) =>
                          props.handlePacketDuplicatePercentage(event, props.containerIndex,
                              interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet duplicate percentage"
                  />
                </td>
              </tr>
              <tr
                key={'pecket-duplicate-correlation-percentage-' +
                  containerInterfaces.packetDuplicateCorrelationPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet duplicate correlation
                  percentage
                </td>
                <td>
                  <FormControl
                      ref={props.inputPacketDuplicateCorrelationPercentageRef}
                      value={containerInterfaces.packetDuplicateCorrelationPercentage}
                      onChange={(event) =>
                          props.handlePacketDuplicateCorrelationPercentage(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet duplicate correlation percentage"
                  />
                </td>
              </tr>
              <tr
                key={'pecket-reorder-percentage-' +
                  containerInterfaces.packetReorderPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet reorder percentage</td>
                <td>
                  <FormControl
                      ref={props.inputPacketReorderPercentageRef}
                      value={containerInterfaces.packetReorderPercentage}
                      onChange={(event) =>
                          props.handlePacketReorderPercentage(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet reorder percentage"
                  />
                </td>
              </tr>
              <tr
                key={'pecket-reorder-correlation-percentage-' +
                  containerInterfaces.packetReorderCorrelationPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet reorder correlation percentage
                </td>
                <td>
                  <FormControl
                      ref={props.inputPacketReorderCorrelationPercentageRef}
                      value={containerInterfaces.packetReorderCorrelationPercentage}
                      onChange={(event) =>
                          props.handlePacketReorderCorrelationPercentage(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet reorder correlation percentage"
                  />
                </td>
              </tr>
              <tr
                key={'pecket-reorder-gap-' +
                  containerInterfaces.packetReorderGap + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet reorder gap</td>
                <td>
                  <FormControl
                      ref={props.inputPacketReorderGapRef}
                      value={containerInterfaces.packetReorderGap}
                      onChange={(event) =>
                          props.handlePacketReorderGap(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet reorder gap"
                  />
                </td>
              </tr>
              <tr
                key={'rate-limit-' +
                  containerInterfaces.rateLimitMbitRef + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Rate limit M bit</td>
                <td>
                  <FormControl
                      ref={props.inputRateLimitMbitRef}
                      value={containerInterfaces.rateLimitMbit}
                      onChange={(event) =>
                          props.handleRateLimitMbit(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Rate limit M bit"
                  />
                </td>
              </tr>
              <tr
                key={'packet-overhead-bytes-' +
                  containerInterfaces.packetOverheadBytes + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet overhead bytes</td>
                <td>
                  <FormControl
                      ref={props.inputPacketOverheadBytesRef}
                      value={containerInterfaces.packetOverheadBytes}
                      onChange={(event) =>
                          props.handlePacketOverheadBytes(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Packet overhead bytes"
                  />
                </td>
              </tr>
              <tr
                key={'call-overhead-bytes-' +
                  containerInterfaces.cellOverheadBytes + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Cell overhead bytes</td>
                <td>
                  <FormControl
                      ref={props.inputCellOverheadBytesRef}
                      value={containerInterfaces.cellOverheadBytes}
                      onChange={(event) =>
                          props.handleCellOverheadBytes(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Cell overhead bytes"
                  />
                </td>
              </tr>
              <tr
                key={'default-gateway-' +
                  containerInterfaces.defaultGateway + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Default gateway</td>
                <td>
                  <FormControl
                      ref={props.inputDefaultGatewayRef}
                      value={containerInterfaces.defaultGateway}
                      onChange={(event) =>
                          props.handleDefaultGateway(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Default Gateway"
                  />
                </td>
              </tr>
              <tr>
                <td> Firewall rule: default input</td>
                <td>
                  <select
                    value={containerInterfaces.defaultInput}
                    onChange={(e) => props.handleDefaultInput(e, props.containerIndex,
                      interfaceIndex)}>
                    <option value="accept">Accept
                    </option>
                    <option value="drop">Drop</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td> Firewall rule: default output</td>
                <td>
                  <select
                    value={containerInterfaces.defaultOutput}
                    onChange={(e) => props.handleDefaultOutput(e, props.containerIndex,
                      interfaceIndex)}>
                    <option value="accept">Accept
                    </option>
                    <option value="drop">Drop</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td> Firewall rule: default forward</td>
                <td>
                  <select
                    value={containerInterfaces.defaultForward}
                    onChange={(e) => props.handleDefaultForward(e, props.containerIndex,
                      interfaceIndex)}>
                    <option value="accept">Accept
                    </option>
                    <option value="drop">Drop</option>
                  </select>
                </td>
              </tr>
              <tr
                key={'traffic-manager-port-' + containerInterfaces.trafficManagerPort + '-'
                  + interfaceIndex + "-" + props.containerIndex}>
                <td> Traffic manager port</td>
                <td>
                  <FormControl
                      ref={props.inputTrafficManagerPortRef}
                      value={containerInterfaces.trafficManagerPort}
                      onChange={(event) =>
                          props.handleTrafficManagerPort(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Traffic manager port"
                  />
                </td>
              </tr>
              <tr
                key={'traffic-manager-log-file-' + containerInterfaces.trafficManagerLogFile + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager log file</td>
                <td>
                  <FormControl
                      ref={props.inputTrafficManagerLogFileRef}
                      value={containerInterfaces.trafficManagerLogFile}
                      onChange={(event) =>
                          props.handleTrafficManagerLogFile(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Traffic manager log file"
                  />
                </td>
              </tr>
              <tr
                key={'traffic-manager-log-dir-' +
                  containerInterfaces.trafficManagerLogDir + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager log directory</td>
                <td>
                  <FormControl
                      ref={props.inputTrafficManagerLogDirRef}
                      value={containerInterfaces.trafficManagerLogDir}
                      onChange={(event) =>
                          props.handleTrafficManagerLogDir(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Traffic manager log directory"
                  />
                </td>
              </tr>
              <tr className="custom-td"
                  key={'traffic-manager-max-workers-' +
                    containerInterfaces.trafficManagerMaxWorkers + '-'
                    + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager maximum workers</td>
                <td>
                  <FormControl
                      ref={props.inputTrafficManagerMaxWorkersRef}
                      value={containerInterfaces.trafficManagerMaxWorkers}
                      onChange={(event) =>
                          props.handleTrafficManagerMaxWorkers(event,
                              props.containerIndex, interfaceIndex)}
                      size="sm"
                      className="createEmulationInput"
                      placeholder="Traffic manager maximum workers"
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

AddInterfaces.propTypes = {};
AddInterfaces.defaultProps = {};
export default AddInterfaces;
