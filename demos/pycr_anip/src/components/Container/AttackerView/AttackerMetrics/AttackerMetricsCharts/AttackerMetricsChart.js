import React, {useState} from 'react';
import './AttackerMetricsChart.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';
import Slider from 'rc-slider';


const AttackerMetricsChart = (props) => {
    const [animationDuration, setAnimationDuration] = useState(0);
    const [animation, setAnimation] = useState(false);

    const animiationDurationFactor = 50000

    const onSliderChange = (value) => {
        setAnimationDuration(value)
        if(value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const AttackerMetricsLineChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const filteredFoundNodes = props.traces[props.activeTrace].attacker_number_of_found_nodes
                .filter((prob, index) => index <= props.t)
            const filteredCompromisedNodes = props.traces[props.activeTrace].attacker_number_of_compromised_nodes
                .filter((prob, index) => index <= props.t)
            var data = []
            for (let i = 0; i < filteredCompromisedNodes.length; i++) {
                var accumulatedFoundNodes = filteredFoundNodes[i]
                var accumulatedCompromisedNodes = filteredCompromisedNodes[i]
                data.push(
                    {
                        t: i + 1,
                        "Found nodes ΣΔx": accumulatedFoundNodes,
                        "Compromised nodes ΣΔy": accumulatedCompromisedNodes,
                    }
                )
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="t" type="number" domain={[1, data.length]}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip />
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Found nodes ΣΔx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Compromised nodes ΣΔy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={[]}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="t" type="number">
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip />
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Found nodes ΣΔx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Compromised nodes ΣΔy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )
        }
    }



    const DeltaAlertsLineChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const filteredFoundNodes = props.traces[props.activeTrace].attacker_number_of_found_nodes
                .filter((prob, index) => index <= props.t)
            const filteredCompromisedNodes = props.traces[props.activeTrace].attacker_number_of_compromised_nodes
                .filter((prob, index) => index <= props.t)
            var data = []
            for (let i = 0; i < filteredCompromisedNodes.length; i++) {
                var deltaFoundNodes = filteredFoundNodes[i]
                var deltaCompromisedNodes = filteredCompromisedNodes[i]
                if (i > 0) {
                    deltaFoundNodes = filteredFoundNodes[i] - filteredFoundNodes[i-1]
                    deltaCompromisedNodes = filteredCompromisedNodes[i] - filteredCompromisedNodes[i-1]
                }
                data.push(
                    {
                            t: i + 1,
                            "Found nodes Δx": deltaFoundNodes,
                            "Compromised nodes Δy": deltaCompromisedNodes,
                        }
                )
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="t" type="number" domain={[1, data.length]}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip />
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Found nodes Δx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Compromised nodes Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={[]}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="t" type="number">
                            <Label value="Time-step t" offset={-20} position="insideBottom" />
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Value" offset={0} position="insideLeft" />
                        </YAxis>
                        <Tooltip />
                        <Legend verticalAlign="top" height={36}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Found nodes Δx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Compromised nodes Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )
        }
    }

    return (
        <div className="SevereAlertsChart">
            <h5 className="line-chart-title">
                 Δ Metrics
            </h5>
            <DeltaAlertsLineChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>

            <h5 className="line-chart-title alertsChart">
                Accumulated Metrics ΣΔ
            </h5>
            <AttackerMetricsLineChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
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

AttackerMetricsChart.propTypes = {};
AttackerMetricsChart.defaultProps = {};
export default AttackerMetricsChart;
