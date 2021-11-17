import React, {useState} from 'react';
import './DefenderPolicyChart.css';
import {AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Label} from 'recharts';
import {Dropdown} from "react-bootstrap"
import DefenderPolicyDropdownElement from "./DefenderPolicyDropdownElement/DefenderPolicyDropdownElement"
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';

const DefenderPolicyChart = (props) => {

    const [animationDuration, setAnimationDuration] = useState(0);
    const [animation, setAnimation] = useState(false);

    const onSliderChange = (value) => {
        setAnimationDuration(value)
        if(value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const PolicyAreaChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].defender_stop_probabilities
                .filter((prob, index) => index <= props.t).map((prob, index) => {
                return {
                    t: index + 1,
                    StoppingProbability: prob
                }
            })

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <AreaChart
                        width={width}
                        height={height}
                        data={data}
                        syncId="anyId"
                        margin={margin}
                    >
                        <defs>
                            <linearGradient id="colorProb" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={[1, data.length]}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number" domain={[0, 1]}>
                            <Label angle={270} value="Probability" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip/>
                        <Area type="monotone" dataKey="StoppingProbability" stroke="#8884d8" fill="#82ca9d"
                              isAnimationActive={animation} fillOpacity={1} fill="url(#colorProb)"
                              animationEasing={'linear'} animationDuration={(1000-(animationDuration/100)*10000)}/>
                    </AreaChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <AreaChart
                        width={width}
                        height={height}
                        data={[]}
                        syncId="anyId"
                        margin={margin}
                    >
                        <defs>
                            <linearGradient id="colorProb" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number" domain={[0, 1]}>
                            <Label angle={270} value="Probability" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip/>
                        <Area type="monotone" dataKey="StoppingProbability" stroke="#8884d8" fill="#82ca9d"
                              isAnimationActive={animation} fillOpacity={1} fill="url(#colorProb)"
                              animationEasing={'linear'} animationDuration={(1000-(animationDuration/100)*10000)}/>
                    </AreaChart>
                </ResponsiveContainer>
            )
        }
    }

    return (
        <div style={{width: '100%'}} className="BeliefAndStoppingChart">
            <div className="row">
                <div className="col-sm-2">
                    <Dropdown className="policyDropdown">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic" size="sm">
                            Policy: {props.activeDefenderPolicy}
                        </Dropdown.Toggle>

                        <Dropdown.Menu variant="dark">
                            {props.defenderPolicies.map((policy, index) =>
                                <DefenderPolicyDropdownElement
                                    policy={policy} index={index} key={index}
                                    setActiveDefenderPolicy={props.setActiveDefenderPolicy}/>
                            )}
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
                <div className="col-sm-10">
                    <h5 className="line-chart-title">
                        Stopping probability πΘ(stop|h)
                    </h5>
                </div>
            </div>
            <PolicyAreaChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
            <div className="row">
                <div className="col-sm-2">
                    <span className="defenderPolicyPlotSliderLabel">Animation:</span>
                </div>
                <div className="col-sm-2">
                    <Slider
                        className="defenderPolicyPlotSlider"
                        min={0}
                        max={100}
                        // step={1}
                        value={animationDuration}
                        onChange={onSliderChange}
                        // railStyle={{
                        //     height: 7,
                        //     width:200
                        // }}
                        // handleStyle={{
                        //     height: 20,
                        //     width: 20,
                        //     marginLeft: -14,
                        //     marginTop: -7,
                        //     // backgroundColor: "red",
                        //     border: 0
                        // }}
                        trackStyle={{
                            background: "none"
                        }}
                    />
                </div>
                <div className="col-sm-8">

                </div>
            </div>
        </div>
    );
}

DefenderPolicyChart.propTypes = {};
DefenderPolicyChart.defaultProps = {};
export default DefenderPolicyChart;


// <AreaChart
//     width={500}
//     height={200}
//     data={data}
//     syncId="anyId"
//     margin={{
//         top: 10,
//         right: 30,
//         left: 0,
//         bottom: 0,
//     }}
// >
//     <CartesianGrid strokeDasharray="3 3" />
//     <XAxis dataKey="name" />
//     <YAxis />
//     <Tooltip />
//     <Area type="monotone" dataKey="pv" stroke="#82ca9d" fill="#82ca9d" />
// </AreaChart>