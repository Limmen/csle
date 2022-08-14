import React, {useState} from 'react';
import './TransitionProbabilities.css';
import StateTransitionHistogram from "../StateTransitionHistogram/StateTransitionHistogram";
import Select from 'react-select'

/**
 * Component containing a chart showing the transition probabilities
 */
const TransitionProbabilities = (props) => {
    var initialA1 = 0
    var initialA2 = 0
    var initialS = 0
    var initialL = 0
    if (props.A1Options.length > 0) {
        initialA1 = props.A1Options[0]
    }
    if (props.A2Options.length > 0) {
        initialA2 = props.A2Options[0]
    }
    if (props.sOptions.length > 0) {
        initialS = props.sOptions[0]
    }
    if (props.lOptions.length > 0) {
        initialL = props.lOptions[0]
    }

    const [a1, setA1] = useState(initialA1);
    const [a2, setA2] = useState(initialA2);
    const [s, setS] = useState(initialS);
    const [l, setL] = useState(initialL);

    const updateA1 = (a1) => {
        setA1(a1)
    }
    const updateA2 = (a2) => {
        setA2(a2)
    }
    const updateS = (s) => {
        setS(s)
    }
    const updateL = (l) => {
        setL(l)
    }

    if (props.simulation.plot_transition_probabilities) {
        return (
            <div>
                <h5 className="semiTitle">
                    Transition probabilities P(s'|a1,a2,s,l)
                </h5>
                <h5 className="semiTitle">
                    a1:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a1}
                            defaultValue={a1}
                            options={props.A1Options}
                            onChange={updateA1}
                            placeholder="Select a1"
                        />
                    </div>
                    a2:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a2}
                            defaultValue={a2}
                            options={props.A2Options}
                            onChange={updateA2}
                            placeholder="Select a2"
                        />
                    </div>
                    s:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={s}
                            defaultValue={s}
                            options={props.sOptions}
                            onChange={updateS}
                            placeholder="Select s"
                        />
                    </div>
                    l:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={l}
                            defaultValue={l}
                            options={props.lOptions}
                            onChange={updateL}
                            placeholder="Select l"
                        />
                    </div>
                </h5>
                <StateTransitionHistogram
                    data={props.simulation.transition_operator_config.transition_tensor[l.value.id][a1.value.id][a2.value.id][s.value.id]}
                    title={"P(s'|a1,a2,s,l)"}
                    minState={props.minState} maxState={props.maxState}
                />
            </div>
        )
    } else {
        return (<div></div>)
    }
}

TransitionProbabilities.propTypes = {};
TransitionProbabilities.defaultProps = {};
export default TransitionProbabilities;
