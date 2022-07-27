import React from 'react';
import './ClientsChart.css';
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

const ClientsChart = React.memo((props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.stats !== undefined && props.stats.length > 0) {
            const data = props.stats.map((client_metrics, index) => {
                return {
                    "t": (index + 1),
                    "Number of clients": parseInt(client_metrics.num_clients)
                }
            })
            var domain = [0, Math.max(1, data.length)]

            return (
                <ResponsiveContainer width='100%' height={300}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <text x={500} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                            <tspan fontSize="15">Number of clients</tspan>
                        </text>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="t" type="number" domain={domain}>
                            <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number">
                            <Label angle={270} value="# Proecsses" offset={0} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                className="largeFont"/>
                        <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                              dataKey="Number of clients"
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

ClientsChart.propTypes = {};

ClientsChart.defaultProps = {};

export default ClientsChart;
