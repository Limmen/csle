import React, {useState} from 'react';
import './SevereAlertsChart.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';
import Slider from 'rc-slider';


const SevereAlertsChart = (props) => {
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

    const AlertsLineChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].defender_observations
                .filter((prob, index) => index <= props.t).map((defenderObs, index) => {
                    return {
                        t: index + 1,
                        "Severe Alerts ΣΔx": defenderObs[0],
                        "Warning Alerts ΣΔy": defenderObs[1],
                        "Login Attempts ΣΔz": defenderObs[2]
                    }
                })

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
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Severe Alerts ΣΔx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts ΣΔy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts ΣΔz"
                              stroke="#742911" animationEasing={'linear'}
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
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Severe Alerts Δx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts Δz"
                              stroke="#742911" animationEasing={'linear'}
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
            const filteredData = props.traces[props.activeTrace].defender_observations
                .filter((prob, index) => index <= props.t)
            var data = []
            for (let i = 0; i < filteredData.length; i++) {
                var deltaX = filteredData[i][0]
                var deltaY = filteredData[i][1]
                var deltaZ = filteredData[i][2]
                if (i > 0) {
                    deltaX = filteredData[i][0] - filteredData[i-1][0]
                    deltaY = filteredData[i][1] - filteredData[i-1][1]
                    deltaZ = filteredData[i][2] - filteredData[i-1][2]
                }
                data.push(
                    {
                            t: i + 1,
                            "Severe Alerts Δx": deltaX,
                            "Warning Alerts Δy": deltaY,
                            "Login Attempts Δz": deltaZ
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
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Severe Alerts Δx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={((1-(animationDuration/100))*animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts Δz"
                              stroke="#742911" animationEasing={'linear'}
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
                        <Line isAnimationActive={animation} animation={animation} type="monotone" dataKey="Severe Alerts Δx"
                              stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                              animationEasing={'linear'} animationDuration={(1000-(animationDuration/100)*10000)}/>
                        <Line animation={animation} type="monotone" dataKey="Warning Alerts Δy"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Login Attempts Δz"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1-(animationDuration/100))*animiationDurationFactor)} isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )
        }
    }

    return (
        <div className="SevereAlertsChart">
            <h5 className="line-chart-title">
                Observations o = (Δx, Δy, Δz)
            </h5>
            <DeltaAlertsLineChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>

            <h5 className="line-chart-title alertsChart">
                Accumulated Observations Σ o = (Σ Δx, Σ Δy, Σ Δz)
            </h5>
            <AlertsLineChart traces={props.traces} activeTrace={props.activeTrace} t={props.t}/>
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

SevereAlertsChart.propTypes = {};
SevereAlertsChart.defaultProps = {};
export default SevereAlertsChart;
