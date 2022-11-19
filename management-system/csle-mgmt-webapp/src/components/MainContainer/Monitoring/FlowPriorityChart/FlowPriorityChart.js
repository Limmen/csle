import React from 'react';
import './FlowPriorityChart.css';
import {
    CartesianGrid,
    Label,
    Legend, Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";


/**
 * Component containing a plot showing the average flow priority over time
 */
const FlowPriorityChart = React.memo((props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 60,
            bottom: 25
        }

        if (props.stats !== undefined && props.stats.length > 0) {
            var minPriority = 1000000000000
            var maxPriority = 0
            const data = props.stats.map((flow_stats, index) => {
                if (parseInt(flow_stats.avg_priority) < minPriority){
                    minPriority = parseInt(flow_stats.avg_priority)
                }
                if (parseInt(flow_stats.avg_priority) > maxPriority){
                    maxPriority = parseInt(flow_stats.avg_priority)
                }
                return {
                    "t": (index + 1),
                    "Avg Flow Priority": parseInt(flow_stats.avg_priority)
                }
            })
            var domain = [0, Math.max(1, data.length)]
            var yDomain = [minPriority, maxPriority]

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={domain}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number" domain={yDomain}>
                            <Label angle={270} value="Avg Flow Priority" offset={-50} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                className="largeFont"/>
                        <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                              dataKey="Avg Flow Priority"
                              stroke="#8884d8" addDot={false} activeDot={{r: 8}}
                              animationEasing={'linear'}
                              animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}/>
                    </LineChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }
)
FlowPriorityChart.propTypes = {};

FlowPriorityChart.defaultProps = {};

export default FlowPriorityChart;
