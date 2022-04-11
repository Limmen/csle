import React from 'react';
import './MetricPlot.css';
import {
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    Line, ErrorBar,
    LineChart,
    XAxis,
    YAxis
} from "recharts";

const MetricPlot = React.memo((props) => {
        const width = 500
        const height = 600
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.data !== undefined) {
            const data = props.data.map((metric, index) => {
                var row = {}
                row["t"] = index
                row[props.metricName] = metric
                row["err"] =props.stds[index]
                return row
            })
            var domain = [0, 1]
            return (
                <ResponsiveContainer width='100%' height={height}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <text x={1300} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                            <tspan fontSize="22">{props.title}</tspan>
                        </text>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                            <Label value="Training iteration" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number" tick={{transform: 'translate(-10,3)'}}>
                            <Label angle={270} value={props.metricName} offset={0} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                className="largeFont"/>
                        <Line type="monotone" dataKey={props.metricName}  stroke="#8884d8" addDot={false} activeDot={{r: 8}}>
                            <ErrorBar dataKey="err" width={4} strokeWidth={2} stroke="green" direction="y" />
                        </Line>
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
MetricPlot.propTypes = {};
MetricPlot.defaultProps = {};
export default MetricPlot;
