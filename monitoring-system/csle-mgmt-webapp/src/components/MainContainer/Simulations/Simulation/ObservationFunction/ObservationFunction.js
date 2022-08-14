import React, {useState} from 'react';
import './ObservationFunction.css';
import ObservationFunctionHistogram from "../ObservationFunctionHistogram/ObservationFunctionHistogram";
import Select from 'react-select'

/**
 * Component containing a chart showing the observation function
 */
const ObservationFunction = (props) => {
    var initialA1 = 0
    var initialA2 = 0
    var initialS = 0
    if (props.A1Options.length > 0) {
        initialA1 = props.A1Options[0]
    }
    if (props.A2Options.length > 0) {
        initialA2 = props.A2Options[0]
    }
    if (props.sOptions.length > 0) {
        initialS = props.sOptions[0]
    }
    const [a1O, setA1O] = useState(initialA1);
    const [a2O, setA2O] = useState(initialA2);
    const [sO, setSO] = useState(initialS);

    const updateA1O = (a1) => {
        setA1O(a1)
    }
    const updateA2O = (a2) => {
        setA2O(a2)
    }
    const updateSO = (s) => {
        setSO(s)
    }

    if (props.simulation.plot_observation_function) {
        return (
            <div className="obsFunction">
                <h5 className="semiTitle">
                    Observation function
                </h5>
                <h5 className="semiTitle">
                    a1:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a1O}
                            defaultValue={a1O}
                            options={props.A1Options}
                            onChange={updateA1O}
                            placeholder="Select a1"
                        />
                    </div>
                    a2:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a2O}
                            defaultValue={a2O}
                            options={props.A2Options}
                            onChange={updateA2O}
                            placeholder="Select a2"
                        />
                    </div>
                    s:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={sO}
                            defaultValue={sO}
                            options={props.sOptions}
                            onChange={updateSO}
                            placeholder="Select s"
                        />
                    </div>
                </h5>
                <div className="row">
                    {Object.keys(props.simulation.observation_function_config.component_observation_tensors).map((componentObs, index) =>
                        <div className="col-sm-12 obsFunctionHistogram" key={componentObs + "-" + index}>
                            <h3 className="chartsTitle">{componentObs + " Z(o|a1,a2,s)"}</h3>
                            <ObservationFunctionHistogram
                                data={props.simulation.observation_function_config.component_observation_tensors[componentObs][a1O.value.id][a2O.value.id][sO.value.id]}
                                title={componentObs + " Z(o|a1,a2,s)"} componentObs={componentObs}
                            />
                        </div>
                    )}
                </div>
            </div>
        )
    } else {
        return (<div></div>)
    }
}

ObservationFunction.propTypes = {};
ObservationFunction.defaultProps = {};
export default ObservationFunction;
