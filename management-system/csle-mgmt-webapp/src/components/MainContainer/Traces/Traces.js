import React, {useState} from 'react';
import Select from 'react-select'
import './Traces.css';
import 'react-confirm-alert/src/react-confirm-alert.css';
import EmulationTraces from "./EmulationTraces/EmulationTraces";
import SimulationTraces from "./SimulationTraces/SimulationTraces";

/**
 * Component representing the /traces-page
 */
const Traces = (props) => {
    const traceTypes = [
        {
            value: 0,
            label: "Emulation traces"
        },
        {
            value: 1,
            label: "Simulation traces"
        }
    ]
    const [selectedTraceType, setSelectedTraceType] = useState(traceTypes[0]);

    const updatedSelectedTraceType = (selectedTraceType) => {
        setSelectedTraceType(selectedTraceType)
    }

    const SelectedTraceTypeComponent = (props) => {
        if (props.selectedTraceType.value === 0) {
            return (
                <EmulationTraces sessionData={props.sessionData} setSessionData={props.setSessionData}/>
            )
        }
        if (props.selectedTraceType.value === 1) {
            return (
                <SimulationTraces sessionData={props.sessionData} setSessionData={props.setSessionData}/>
            )
        }
    }

    return (
        <div className="Traces">
            <h3 className="managementTitle"> Management of Traces </h3>
            <div className="traceTypeSelection inline-block">
                <div className="conditionalDist inline-block conditionalLabel">
                    Trace type:
                </div>
                <div className="conditionalDist inline-block" style={{width: "300px"}}>
                    <Select
                        style={{display: 'inline-block'}}
                        value={selectedTraceType}
                        defaultValue={selectedTraceType}
                        options={traceTypes}
                        onChange={updatedSelectedTraceType}
                        placeholder="Select trace type"
                    />
                </div>
            </div>
            <SelectedTraceTypeComponent selectedTraceType={selectedTraceType} sessionData={props.sessionData}
                                     setSessionData={props.setSessionData}/>
        </div>
    );
}

Traces.propTypes = {};
Traces.defaultProps = {};
export default Traces;
