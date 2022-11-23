import React from 'react';
import './PolicyAndBeliefChart.css';
import {
    Area,
    AreaChart,
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
    ReferenceLine
} from "recharts";

/**
 * Component representing the policy belief chart in the policy examination page
 */
const PolicyAndBeliefChart = React.memo((props) => {
        const width = 2000
        const height = 310
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.activeTrace !== null && props.activeTrace !== undefined) {
            const data = []
            const ticks = []
            var yMax = 1
            for (let i = 0; i <= props.activeTrace.value.defender_stop_probabilities.length; i++) {
                data.push({
                    t: i + 1,
                    "Probability of next defensive action": props.activeTrace.value.defender_stop_probabilities[i],
                    "Belief": props.activeTrace.value.defender_beliefs[i]
                })
                ticks.push(i + 1)
                yMax = Math.min(yMax, Math.max(props.activeTrace.value.defender_stop_probabilities[i],
                    props.activeTrace.value.defender_beliefs[i]))
            }
            var domain = [0, Math.max(1, data.length)]
            if (props.fullDomain) {
                domain = [1, props.activeTrace.value.defender_stop_probabilities.length]
            }
            var range = [0, 1]
            if (!props.fullRange) {
                range = [0, yMax]
            }
            return (
                <div className="DefenderPolicy row justify-content-center card demoCard">
                    <div className="card-header cardHeader">
                        <h4>
                            Probability of defensive action πΘ(a|h) and belief about intrusion b(1)
                        </h4>
                    </div>
                    <ResponsiveContainer width='100%' height={height}>
                        <AreaChart
                            width={width}
                            height={height}
                            data={data.slice(0,props.t)}
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
                            <XAxis dataKey="t" type="number" domain={domain} ticks={ticks.slice(0,props.t)}>
                                <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont"/>
                            </XAxis>
                            <YAxis type="number" domain={range}>
                                <Label angle={270} value="Probability" offset={0} position="insideLeft"
                                       className="largeFont"/>
                            </YAxis>
                            <Tooltip/>
                            <ReferenceLine x={props.activeTrace.value.intrusion_start_index}
                                           stroke="black" label={{
                                position: 'insideTopRight',
                                value: 'Intrusion starts', fill: 'black',
                                fontSize: 15, marginTop: "10px"
                            }} strokeDasharray="3 3"/>
                            <ReferenceLine y={0.5}
                                           stroke="black" strokeDasharray="5 5 "/>
                            <Area type="monotone" dataKey="Probability of next defensive action" stroke="#8884d8"
                                  isAnimationActive={props.animation} fillOpacity={1} fill="url(#colorProb)"
                                  animationEasing={'linear'}
                                  animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}/>

                            <Area type="monotone" dataKey="Belief" stroke="#82ca9d"
                                  isAnimationActive={props.animation} fillOpacity={1} fill="url(#colorPv)"
                                  animationEasing={'linear'}
                                  animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}/>
                            <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                    className="largeFont"/>
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            )

        } else {
            return (
                <div></div>
            )
        }
    }
)
PolicyAndBeliefChart.propTypes =
    {}
;
PolicyAndBeliefChart.defaultProps =
    {}
;
export default PolicyAndBeliefChart;
