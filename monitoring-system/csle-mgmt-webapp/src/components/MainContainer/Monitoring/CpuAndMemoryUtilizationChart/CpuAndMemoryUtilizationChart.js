import React from 'react';
import './CpuAndMemoryUtilizationChart.css';
import {
    Area,
    AreaChart,
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";

/**
 * Component containing a plot showing the CPU and memory utilization
 */
const CpuAndMemoryUtilizationChart = React.memo((props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.stats !== undefined && props.stats.length > 0) {
            const data = props.stats.map((docker_stats, index) => {
                return {
                    "t": (index + 1),
                    "Avg CPU Utilization %": parseInt(docker_stats.cpu_percent),
                    "Avg Memory Utilization %": parseInt(docker_stats.mem_percent),
                }
            })
            var domain = [0, Math.max(1, data.length)]

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <AreaChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={domain}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="%" offset={0} position="insideLeft" className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                className="largeFont"/>
                        <Area isAnimationActive={props.animation} animation={props.animation} type="monotone"
                              stackId={"1"}
                              dataKey="Avg CPU Utilization %"
                              stroke="#8884d8" fill="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}/>
                        <Area animation={props.animation} type="monotone" dataKey="Avg Memory Utilization %"
                              stackId={"1"}
                              stroke="#82ca9d" fill="#82ca9d" animationEasing={'linear'}
                              animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                              isAnimationActive={props.animation}/>
                    </AreaChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }
)
CpuAndMemoryUtilizationChart.propTypes = {};

CpuAndMemoryUtilizationChart.defaultProps = {};

export default CpuAndMemoryUtilizationChart;
