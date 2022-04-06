import React from 'react';
import './ConditionalHistogramDistribution.css';
import {
    CartesianGrid,
    Label,
    Legend, Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis
} from "recharts";

const ConditionalHistogramDistribution = React.memo((props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.stats !== undefined) {

            const data = Object.values(props.stats).map((val, index) => {
                return {
                    "value": index,
                    "count": val
                }
            })
            var domain = [0, Math.max(1, data.length)]

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <BarChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <text x={650} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                            <tspan fontSize="22">{props.title}</tspan>
                        </text>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="value" type="number" domain={domain}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="# Proecsses" offset={0} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                className="largeFont"/>
                        <Bar dataKey="count" fill="#8884d8" stroke="black" animationEasing={'linear'}
                             animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                        />
                    </BarChart>
                </ResponsiveContainer>
            )

        } else {
            return (
                <div></div>
            )
        }
    }
)
ConditionalHistogramDistribution.propTypes = {};

ConditionalHistogramDistribution.defaultProps = {};

export default ConditionalHistogramDistribution;
