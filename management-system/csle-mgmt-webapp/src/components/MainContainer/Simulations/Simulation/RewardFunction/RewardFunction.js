import React, {useState} from 'react';
import './RewardFunction.css';
import RewardFunctionPlot from "../RewardFunctionPlot/RewardFunctionPlot";
import Select from 'react-select'


/**
 * Component containing a chart showing the reward function
 */
const RewardFunction = (props) => {
    var initialA1 = 0
    var initialA2 = 0
    var initialL = 0
    if (props.A1Options.length > 0) {
        initialA1 = props.A1Options[0]
    }
    if (props.A2Options.length > 0) {
        initialA2 = props.A2Options[0]
    }
    if (props.lOptions.length > 0) {
        initialL = props.lOptions[0]
    }
    const [a1R, setA1R] = useState(initialA1);
    const [a2R, setA2R] = useState(initialA2);
    const [lR, setLR] = useState(initialL);

    const updateA1R = (a1) => {
        setA1R(a1)
    }
    const updateA2R = (a2) => {
        setA2R(a2)
    }
    const updateLR = (l) => {
        setLR(l)
    }

    if (props.simulation.plot_reward_function) {
        return (
            <div className="rewardFun">
                <h5 className="semiTitle">
                    Reward function r(a1,a2,s,l):
                </h5>
                <h5 className="semiTitle">
                    a1:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a1R}
                            defaultValue={a1R}
                            options={props.A1Options}
                            onChange={updateA1R}
                            placeholder="Select a1"
                        />
                    </div>
                    a2:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={a2R}
                            defaultValue={a2R}
                            options={props.A2Options}
                            onChange={updateA2R}
                            placeholder="Select a2"
                        />
                    </div>
                    l:
                    <div className="selectBlock inline-block" style={{width: "200px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={lR}
                            defaultValue={lR}
                            options={props.lOptions}
                            onChange={updateLR}
                            placeholder="Select l"
                        />
                    </div>
                </h5>
                <RewardFunctionPlot
                    data={props.simulation.reward_function_config.reward_tensor[lR.value.id][a1R.value.id][a2R.value.id]}
                    title={"r(a1,a2,s,l)"} minState={props.minState} maxState={props.maxState}
                />
            </div>
        )
    } else {
        return (<div></div>)
    }
}

RewardFunction.propTypes = {};
RewardFunction.defaultProps = {};
export default RewardFunction;
