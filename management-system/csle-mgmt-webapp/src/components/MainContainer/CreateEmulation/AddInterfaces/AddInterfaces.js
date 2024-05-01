import React from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import './AddInterfaces.css';
import AddServices from '../AddServices/AddServices'

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
                <td> Name</td>
                <td>
                  <input
                    ref={props.inputNameRef}
                    type="text"
                    value={containerInterfaces.name}
                    onChange={(event) => props.handleInterfaceNameChange(event, props.containerIndex, interfaceIndex)}
                  />
                  <Button type="button" onClick={() =>
                    props.deleteInterfaceHandler(props.containerIndex, interfaceIndex)}
                          variant="danger" size="sm"
                          style={{ marginLeft: '5px' }}>
                    <i className="fa fa-trash startStopIcon"
                       aria-hidden="true" />
                  </Button>
                </td>
              </tr>
              <tr key={'ip-' + containerInterfaces.ip + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> IP </td>
                <td>
                  <input
                    ref={props.inputIPRef}
                    type="text"
                    value={containerInterfaces.ip}
                    onChange={(event) => props.handleIPChange(event, props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'subnet-' + containerInterfaces.subnetMask + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Subnet mask</td>
                <td>
                  <input
                    ref={props.inputSubnetMaskRef}
                    type="text"
                    value={containerInterfaces.subnetMask}
                    onChange={(event) =>
                      props.handleSubnetMaskChange(event, props.containerIndex, interfaceIndex)}
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
                  <input
                    ref={props.inputLimitPacketsQueueRef}
                    type="text"
                    value={containerInterfaces.limitPacketsQueue}
                    onChange={(event) =>
                      props.handleLimitPacketsQueueChange(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'packet-delay-' + containerInterfaces.packetDelayMs + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay (ms)</td>
                <td>
                  <input
                    ref={props.inputPacketDelayMsRef}
                    type="text"
                    value={containerInterfaces.packetDelayMs}
                    onChange={(event) =>
                      props.handlePacketDelayMs(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'packet-jitter-' + containerInterfaces.packetDelayJitterMs + '-' + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay jitter (ms)</td>
                <td>
                  <input
                    ref={props.inputPacketDelayJitterMsRef}
                    type="text"
                    value={containerInterfaces.packetDelayJitterMs}
                    onChange={(event) =>
                      props.handlePacketDelayJitterMs(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'packet-correlation-' + containerInterfaces.packetDelayCorrelationPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet delay correlation percentage
                </td>
                <td>
                  <input
                    ref={props.inputPacketDelayCorrelationPercentageRef}
                    type="text"
                    value={containerInterfaces.packetDelayCorrelationPercentage}
                    onChange={(event) =>
                      props.handlePacketDelayCorrelationPercentage(event, props.containerIndex,
                        interfaceIndex)}
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
                  <input
                    ref={props.inputLossGemodelpRef}
                    type="text"
                    value={containerInterfaces.lossGemodelp}
                    onChange={(event) =>
                      props.handleLossGemodelp(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelr-' + containerInterfaces.lossGemodelr + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel R</td>
                <td>
                  <input
                    ref={props.inputLossGemodelrRef}
                    type="text"
                    value={containerInterfaces.lossGemodelr}
                    onChange={(event) =>
                      props.handleLossGemodelr(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelk-' + containerInterfaces.lossGemodelk + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel K</td>
                <td>
                  <input
                    ref={props.inputLossGemodelkRef}
                    type="text"
                    value={containerInterfaces.lossGemodelk}
                    onChange={(event) =>
                      props.handleLossGemodelk(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'loss-gemodelh-' + containerInterfaces.lossGemodelh + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Loss Gemodel H</td>
                <td>
                  <input
                    ref={props.inputLossGemodelhRef}
                    type="text"
                    value={containerInterfaces.lossGemodelh}
                    onChange={(event) =>
                      props.handleLossGemodelh(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'packet-corruption-' + containerInterfaces.packetCorruptPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet corruption percentage</td>
                <td>
                  <input
                    ref={props.inputPacketCorruptPercentageRef}
                    type="text"
                    value={containerInterfaces.packetCorruptPercentage}
                    onChange={(event) =>
                      props.handlePacketCorruptPercentage(event, props.containerIndex,
                        interfaceIndex)}
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
                  <input
                    ref={props.inputPacketCorruptCorrelationPercentageRef}
                    type="text"
                    value={containerInterfaces.packetCorruptCorrelationPercentage}
                    onChange={(event) =>
                      props.handlePacketCorruptCorrelationPercentage(event, props.containerIndex,
                        interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'pecket-duplicate-percentage-' +
                  containerInterfaces.packetDuplicatePercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet duplicate percentage</td>
                <td>
                  <input
                    ref={props.inputPacketDuplicatePercentageRef}
                    type="text"
                    value={containerInterfaces.packetDuplicatePercentage}
                    onChange={(event) =>
                      props.handlePacketDuplicatePercentage(event, props.containerIndex,
                        interfaceIndex)}
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
                  <input
                    ref={props.inputPacketDuplicateCorrelationPercentageRef}
                    type="text"
                    value={containerInterfaces.packetDuplicateCorrelationPercentage}
                    onChange={(event) =>
                      props.handlePacketDuplicateCorrelationPercentage(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'pecket-reorder-percentage-' +
                  containerInterfaces.packetReorderPercentage + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet reorder percentage</td>
                <td>
                  <input
                    ref={props.inputPacketReorderPercentageRef}
                    type="text"
                    value={containerInterfaces.packetReorderPercentage}
                    onChange={(event) =>
                      props.handlePacketReorderPercentage(event,
                        props.containerIndex, interfaceIndex)}
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
                  <input
                    ref={props.inputPacketReorderCorrelationPercentageRef}
                    type="text"
                    value={containerInterfaces.packetReorderCorrelationPercentage}
                    onChange={(event) =>
                      props.handlePacketReorderCorrelationPercentage(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'pecket-reorder-gap-' +
                  containerInterfaces.packetReorderGap + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet reorder gap</td>
                <td>
                  <input
                    ref={props.inputPacketReorderGapRef}
                    type="text"
                    value={containerInterfaces.packetReorderGap}
                    onChange={(event) =>
                      props.handlePacketReorderGap(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'rate-limit-' +
                  containerInterfaces.rateLimitMbitRef + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Rate limit M bit</td>
                <td>
                  <input
                    ref={props.inputRateLimitMbitRef}
                    type="text"
                    value={containerInterfaces.rateLimitMbit}
                    onChange={(event) =>
                      props.handleRateLimitMbit(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'packet-overhead-bytes-' +
                  containerInterfaces.packetOverheadBytes + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Packet overhead bytes</td>
                <td>
                  <input
                    ref={props.inputPacketOverheadBytesRef}
                    type="text"
                    value={containerInterfaces.packetOverheadBytes}
                    onChange={(event) =>
                      props.handlePacketOverheadBytes(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'call-overhead-bytes-' +
                  containerInterfaces.cellOverheadBytes + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Cell overhead bytes</td>
                <td>
                  <input
                    ref={props.inputCellOverheadBytesRef}
                    type="text"
                    value={containerInterfaces.cellOverheadBytes}
                    onChange={(event) =>
                      props.handleCellOverheadBytes(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'default-gateway-' +
                  containerInterfaces.defaultGateway + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Default gateway</td>
                <td>
                  <input
                    ref={props.inputDefaultGatewayRef}
                    type="text"
                    value={containerInterfaces.defaultGateway}
                    onChange={(event) =>
                      props.handleDefaultGateway(event,
                        props.containerIndex, interfaceIndex)}
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
                  <input
                    ref={props.inputTrafficManagerPortRef}
                    type="text"
                    value={containerInterfaces.trafficManagerPort}
                    onChange={(event) =>
                      props.handleTrafficManagerPort(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'traffic-manager-log-file-' + containerInterfaces.trafficManagerLogFile + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager log file</td>
                <td>
                  <input
                    ref={props.inputTrafficManagerLogFileRef}
                    type="text"
                    value={containerInterfaces.trafficManagerLogFile}
                    onChange={(event) =>
                      props.handleTrafficManagerLogFile(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr
                key={'traffic-manager-log-dir-' +
                  containerInterfaces.trafficManagerLogDir + '-'
                  + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager log directory</td>
                <td>
                  <input
                    ref={props.inputTrafficManagerLogDirRef}
                    type="text"
                    value={containerInterfaces.trafficManagerLogDir}
                    onChange={(event) =>
                      props.handleTrafficManagerLogDir(event,
                        props.containerIndex, interfaceIndex)}
                  />
                </td>
              </tr>
              <tr className="custom-td"
                  key={'traffic-manager-max-workers-' +
                    containerInterfaces.trafficManagerMaxWorkers + '-'
                    + interfaceIndex + '-' + props.containerIndex}>
                <td> Traffic manager maximum workers</td>
                <td>
                  <input
                    ref={props.inputTrafficManagerMaxWorkersRef}
                    type="text"
                    value={containerInterfaces.trafficManagerMaxWorkers}
                    onChange={(event) =>
                      props.handleTrafficManagerMaxWorkers(event,
                        props.containerIndex, interfaceIndex)}
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
