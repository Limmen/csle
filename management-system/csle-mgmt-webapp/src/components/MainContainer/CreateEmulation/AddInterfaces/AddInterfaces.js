import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import FormControl from 'react-bootstrap/FormControl';
import Select from 'react-select'
import './AddInterfaces.css';

const AddInterfaces = (props) => {

  const physicalInterfaceOptions = [
    {
      value: "eth0",
      label: "eth0"
    },
    {
      value: "eth1",
      label: "eth1"
    },
    {
      value: "eth2",
      label: "eth2"
    },
    {
      value: "eth3",
      label: "eth3"
    },
    {
      value: "eth4",
      label: "eth4"
    },
    {
      value: "eth5",
      label: "eth5"
    },
    {
      value: "eth6",
      label: "eth6"
    },
    {
      value: "eth7",
      label: "eth7"
    },
    {
      value: "eth8",
      label: "eth8"
    },
    {
      value: "eth9",
      label: "eth9"
    },
    {
      value: "eth10",
      label: "eth10"
    }
  ]

  const packetDelayDistributionOptions = [
    {
      value: "Uniform",
      label: "Uniform"
    },
    {
      value: "Normal",
      label: "Normal"
    },
    {
      value: "Pareto",
      label: "Pareto"
    },
    {
      value: "Pareto Normal",
      label: "Pareto Normal"
    }
  ]

  const packetLossTypeOptions = [
    {
      value: "Random",
      label: "Random"
    },
    {
      value: "State",
      label: "State"
    },
    {
      value: "Gemodel",
      label: "Gemodel"
    }
  ]

  const firewallDefaultInputOptions = [
    {
      value: "Accept",
      label: "Accept"
    },
    {
      value: "Drop",
      label: "Drop"
    }
  ]

  const firewallDefaultOutputOptions = [
    {
      value: "Accept",
      label: "Accept"
    },
    {
      value: "Drop",
      label: "Drop"
    }
  ]

  const firewallDefaultForwardOptions = [
    {
      value: "Accept",
      label: "Accept"
    },
    {
      value: "Drop",
      label: "Drop"
    }
  ]

  const [selectedPhysicalInterface, setSelectedPhysicalInterface] = useState(physicalInterfaceOptions[0]);
  const [selectedPacketDelayDistribution, setSelectedPacketDelayDistribution] = useState(packetDelayDistributionOptions[0]);
  const [selectedPacketLossType, setSelectedPacketLossType] = useState(packetLossTypeOptions[0]);
  const [selectedFirewallDefaultInput, setSelectedFirewallDefaultInput] = useState(firewallDefaultInputOptions[0]);
  const [selectedFirewallDefaultOutput, setSelectedFirewallDefaultOutput] = useState(firewallDefaultOutputOptions[0]);
  const [selectedFirewallDefaultForward, setSelectedFirewallDefaultForward] = useState(firewallDefaultForwardOptions[0]);

  const updatedPhysicalInterface = (physicalInterfaceOption) => {
    setSelectedPhysicalInterface(physicalInterfaceOption)
    props.handleNetworkPhysicalInterface(physicalInterfaceOption.value, props.containerIndex)
  }

  const updatedPacketDelayDistribution = (packetDelayDistributionOption) => {
    setSelectedPacketDelayDistribution(packetDelayDistributionOption)
    props.handlePacketDelayDistribution(packetDelayDistributionOption.value, props.containerIndex)
  }

  const updatedPacketLossType = (packetLossTypeOption) => {
    setSelectedPacketLossType(packetLossTypeOption)
    props.handlePacketLossType(packetLossTypeOption.value, props.containerIndex)
  }

  const updatedFirewallInput = (firewallInputOption) => {
    setSelectedFirewallDefaultInput(firewallInputOption)
    props.handleDefaultInput(firewallInputOption.value, props.containerIndex)
  }

  const updatedFirewallOutput = (firewallOutputOption) => {
    setSelectedFirewallDefaultOutput(firewallOutputOption)
    props.handleDefaultOutput(firewallOutputOption.value, props.containerIndex)
  }

  const updatedFirewallForward = (firewallForwardOption) => {
    setSelectedFirewallDefaultForward(firewallForwardOption)
    props.handleDefaultForward(firewallForwardOption.value, props.containerIndex)
  }


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
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedPhysicalInterface}
                      defaultValue={selectedPhysicalInterface}
                      options={physicalInterfaceOptions}
                      onChange={updatedPhysicalInterface}
                      placeholder="Physical network interface"
                      className="createEmulationInput"
                      size="sm"
                  />
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
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedPacketDelayDistribution}
                      defaultValue={selectedPacketDelayDistribution}
                      options={packetDelayDistributionOptions}
                      onChange={updatedPacketDelayDistribution}
                      placeholder="Packet Delay Distribution"
                      className="createEmulationInput"
                      size="sm"
                  />
                </td>
              </tr>
              <tr>
                <td> Packet loss type</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedPacketLossType}
                      defaultValue={selectedPacketLossType}
                      options={packetLossTypeOptions}
                      onChange={updatedPacketLossType}
                      placeholder="Packet Loss Type"
                      className="createEmulationInput"
                      size="sm"
                  />
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
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedFirewallDefaultInput}
                      defaultValue={selectedFirewallDefaultInput}
                      options={firewallDefaultInputOptions}
                      onChange={updatedFirewallInput}
                      placeholder="Firewall default input rule"
                      className="createEmulationInput"
                      size="sm"
                  />
                </td>
              </tr>
              <tr>
                <td> Firewall rule: default output</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedFirewallDefaultOutput}
                      defaultValue={selectedFirewallDefaultOutput}
                      options={firewallDefaultOutputOptions}
                      onChange={updatedFirewallOutput}
                      placeholder="Firewall default output rule"
                      className="createEmulationInput"
                      size="sm"
                  />
                </td>
              </tr>
              <tr>
                <td> Firewall rule: default forward</td>
                <td>
                  <Select
                      style={{display: 'inline-block'}}
                      value={selectedFirewallDefaultForward}
                      defaultValue={selectedFirewallDefaultForward}
                      options={firewallDefaultForwardOptions}
                      onChange={updatedFirewallForward}
                      placeholder="Firewall default forward rule"
                      className="createEmulationInput"
                      size="sm"
                  />
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
