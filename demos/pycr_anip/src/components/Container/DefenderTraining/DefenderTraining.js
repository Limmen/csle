import React, {useEffect, useState} from 'react';
import './DefenderTraining.css';
import {
    Area,
    AreaChart,
    CartesianGrid,
    Label,
    Legend, Line,
    LineChart,
    BarChart,
    Bar,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
    ReferenceLine
} from "recharts";
import Slider from "rc-slider";
import "rc-slider/assets/index.css";

const DefenderTraining = (props) => {

    const [animationDuration, setAnimationDuration] = useState(100);
    const [animation, setAnimation] = useState(false);
    const animiationDurationFactor = 50000
    const fullDomain = true
    const fullRange = true

    const onSliderChange = (value) => {
        setAnimationDuration(value)
        if (value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const RewardsLineChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].training_avg_defender_rewards_simulation
                .map((defender_reward, index) => {
                    return {
                        "t": (index + 1) * 10000,
                        "πΘ Emulation": props.traces[props.activeTrace].training_avg_defender_rewards_simulation[index],
                        "πΘ Simulation": props.traces[props.activeTrace].training_avg_defender_rewards_emulation[index],
                        "Baseline": props.traces[props.activeTrace].training_avg_defender_rewards_baseline[index],
                    }
                })
            var domain = [0, Math.max(1, data.length)]
            if (fullDomain) {
                domain = [1, props.traces[props.activeTrace].defender_observations.length]
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="# training episodes" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Reward" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative'}}/>
                        <ReferenceLine y={props.traces[props.activeTrace].training_reward_upper_bound}
                                       stroke="black" label={{
                            position: 'insideTopLeft',
                            value: 'Upper bound', fill: 'black',
                            fontSize: 14, marginTop: "10px"
                        }} strokeDasharray="3 3"/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="πΘ Emulation"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="πΘ Simulation"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Baseline"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }


    const EpisodeLengthsCharts = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].training_avg_defender_episode_lengths_simulation
                .map((defender_reward, index) => {
                    return {
                        "t": (index + 1) * 10000,
                        "πΘ Emulation": props.traces[props.activeTrace].training_avg_defender_episode_lengths_simulation[index],
                        "πΘ Simulation": props.traces[props.activeTrace].training_avg_defender_episode_lengths_emulation[index],
                        "Baseline": props.traces[props.activeTrace].training_avg_defender_episode_lengths_baseline[index],
                    }
                })
            var domain = [0, Math.max(1, data.length)]
            if (fullDomain) {
                domain = [1, props.traces[props.activeTrace].defender_observations.length]
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="# training episodes" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Time-steps" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative'}}/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="πΘ Emulation"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="πΘ Simulation"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Baseline"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }


    const IntrusionPreventedProbabilityChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].training_avg_defender_intrusion_prevented_prob_simulation
                .map((defender_reward, index) => {
                    return {
                        "t": (index + 1) * 10000,
                        "πΘ Emulation": props.traces[props.activeTrace].training_avg_defender_intrusion_prevented_prob_simulation[index],
                        "πΘ Simulation": props.traces[props.activeTrace].training_avg_defender_intrusion_prevented_prob_emulation[index],
                        "Baseline": props.traces[props.activeTrace].training_avg_defender_intrusion_prevented_prob_baseline[index],
                    }
                })
            var domain = [0, Math.max(1, data.length)]
            if (fullDomain) {
                domain = [1, props.traces[props.activeTrace].defender_observations.length]
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="# training episodes" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Probability" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative'}}/>
                        <ReferenceLine y={props.traces[props.activeTrace].intrusion_prevented_upper_bound}
                                       stroke="black" label={{
                            position: 'insideTopLeft',
                            value: 'Upper bound', fill: 'black',
                            fontSize: 14, marginTop: "10px"
                        }} strokeDasharray="3 3"/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="πΘ Emulation"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="πΘ Simulation"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Baseline"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }


    const EarlyStoppingProbabilityChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].training_avg_defender_early_stopping_prob_simulation
                .map((defender_reward, index) => {
                    return {
                        "t": (index + 1) * 10000,
                        "πΘ Emulation": props.traces[props.activeTrace].training_avg_defender_early_stopping_prob_simulation[index],
                        "πΘ Simulation": props.traces[props.activeTrace].training_avg_defender_early_stopping_prob_emulation[index],
                        "Baseline": props.traces[props.activeTrace].training_avg_defender_early_stopping_prob_baseline[index],
                    }
                })
            var domain = [0, Math.max(1, data.length)]
            if (fullDomain) {
                domain = [1, props.traces[props.activeTrace].defender_observations.length]
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="# training episodes" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Probability" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative'}}/>
                        <ReferenceLine y={props.traces[props.activeTrace].early_stopping_upper_bound}
                                       stroke="black" label={{
                            position: 'insideTopLeft',
                            value: 'Lower bound', fill: 'black',
                            fontSize: 14, marginTop: "10px"
                        }} strokeDasharray="3 3"/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="πΘ Emulation"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="πΘ Simulation"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Baseline"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }


    const IntrusionDurationChart = (props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.traces.length > 0) {
            const data = props.traces[props.activeTrace].training_avg_intrusion_duration_simulation
                .map((defender_reward, index) => {
                    return {
                        "t": (index + 1) * 10000,
                        "πΘ Emulation": props.traces[props.activeTrace].training_avg_intrusion_duration_simulation[index],
                        "πΘ Simulation": props.traces[props.activeTrace].training_avg_intrusion_duration_emulation[index],
                        "Baseline": props.traces[props.activeTrace].training_avg_intrusion_duration_baseline[index],
                    }
                })
            var domain = [0, Math.max(1, data.length)]
            if (fullDomain) {
                domain = [1, props.traces[props.activeTrace].defender_observations.length]
            }

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number">
                            <Label value="# training episodes" offset={-20} position="insideBottom"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="Time-steps" offset={0} position="insideLeft"/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative'}}/>
                        <ReferenceLine y={props.traces[props.activeTrace].intrusion_duration_upper_bound}
                                       stroke="black" label={{
                            position: 'insideTopLeft',
                            value: 'Lower bound', fill: 'black',
                            fontSize: 14, marginTop: "10px"
                        }} strokeDasharray="3 3"/>
                        <Line isAnimationActive={animation} animation={animation} type="monotone"
                              dataKey="πΘ Emulation"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}/>
                        <Line animation={animation} type="monotone" dataKey="πΘ Simulation"
                              stroke="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                        <Line animation={animation} type="monotone" dataKey="Baseline"
                              stroke="#742911" animationEasing={'linear'}
                              animationDuration={((1 - (animationDuration / 100)) * animiationDurationFactor)}
                              isAnimationActive={animation}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }

    return (
        <div className="DefenderTraining">
            <div className="row">
                <div className="row">
                    <div className="col-sm-12">
                        <h4> Defender Learning Curves </h4>
                    </div>
                </div>
                <div className="row">
                    <div className="col-sm-6">
                        <div className="row">
                            <div className="RewardsPlot row justify-content-center card">
                                <div className="card-header cardHeader"><h4>Reward per episode</h4></div>
                                <div className="card-body">
                                    <RewardsLineChart traces={props.traces} activeTrace={props.activeTrace}
                                                      t={props.t}/>
                                </div>
                                <div className="row evolutionRow">
                                    <div className="col-sm-4">
                                        <p className="defenderPolicyPlotSliderLabel">Evolution speed:</p>
                                    </div>
                                    <div className="col-sm-4">
                                        <Slider
                                            className="defenderPolicyPlotSlider"
                                            min={0}
                                            max={100}
                                            value={animationDuration}
                                            onChange={onSliderChange}
                                        />
                                    </div>
                                    <div className="col-sm-8">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="col-sm-6">
                        <div className="row">
                            <div className="EpisodeLengthsPlot row justify-content-center card">
                                <div className="card-header cardHeader"><h4>Episode Lengths</h4></div>
                                <div className="card-body">
                                    <EpisodeLengthsCharts traces={props.traces} activeTrace={props.activeTrace}
                                                          t={props.t}/>
                                </div>
                                <div className="row evolutionRow">
                                    <div className="col-sm-4">
                                        <p className="defenderPolicyPlotSliderLabel">Evolution speed:</p>
                                    </div>
                                    <div className="col-sm-4">
                                        <Slider
                                            className="defenderPolicyPlotSlider"
                                            min={0}
                                            max={100}
                                            value={animationDuration}
                                            onChange={onSliderChange}
                                        />
                                    </div>
                                    <div className="col-sm-8">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-sm-6">
                        <div className="row">
                            <div className="EpisodeLengthsPlot row justify-content-center card">
                                <div className="card-header cardHeader"><h4>P(Intrusion Prevented)</h4></div>
                                <div className="card-body">
                                    <IntrusionPreventedProbabilityChart traces={props.traces}
                                                                        activeTrace={props.activeTrace}
                                                                        t={props.t}/>
                                </div>
                                <div className="row evolutionRow">
                                    <div className="col-sm-4">
                                        <p className="defenderPolicyPlotSliderLabel">Evolution speed:</p>
                                    </div>
                                    <div className="col-sm-4">
                                        <Slider
                                            className="defenderPolicyPlotSlider"
                                            min={0}
                                            max={100}
                                            value={animationDuration}
                                            onChange={onSliderChange}
                                        />
                                    </div>
                                    <div className="col-sm-8">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-6">
                        <div className="row">
                            <div className="EpisodeLengthsPlot row justify-content-center card">
                                <div className="card-header cardHeader"><h4>P(Early Stopping)</h4></div>
                                <div className="card-body">
                                    <EarlyStoppingProbabilityChart traces={props.traces} activeTrace={props.activeTrace}
                                                                   t={props.t}/>
                                </div>
                                <div className="row evolutionRow">
                                    <div className="col-sm-4">
                                        <p className="defenderPolicyPlotSliderLabel">Evolution speed:</p>
                                    </div>
                                    <div className="col-sm-4">
                                        <Slider
                                            className="defenderPolicyPlotSlider"
                                            min={0}
                                            max={100}
                                            value={animationDuration}
                                            onChange={onSliderChange}
                                        />
                                    </div>
                                    <div className="col-sm-8">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-sm-6">
                        <div className="row">
                            <div className="EpisodeLengthsPlot row justify-content-center card">
                                <div className="card-header cardHeader"><h4>Duration of intrusion</h4></div>
                                <div className="card-body">
                                    <IntrusionDurationChart traces={props.traces} activeTrace={props.activeTrace}
                                                                   t={props.t}/>
                                </div>
                                <div className="row evolutionRow">
                                    <div className="col-sm-4">
                                        <p className="defenderPolicyPlotSliderLabel">Evolution speed:</p>
                                    </div>
                                    <div className="col-sm-4">
                                        <Slider
                                            className="defenderPolicyPlotSlider"
                                            min={0}
                                            max={100}
                                            value={animationDuration}
                                            onChange={onSliderChange}
                                        />
                                    </div>
                                    <div className="col-sm-8">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

DefenderTraining.propTypes = {};
DefenderTraining.defaultProps = {};
export default DefenderTraining;