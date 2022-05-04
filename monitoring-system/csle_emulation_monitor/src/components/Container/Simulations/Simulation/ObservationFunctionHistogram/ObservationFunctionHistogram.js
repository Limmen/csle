import React from 'react';
import './ObservationFunctionHistogram.css';
import {
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis
} from "recharts";

const ObservationFunctionHistogram = React.memo((props) => {
        const width = 500
        const height = 600
        const margin = {
            top: 10,
            right: 30,
            left: 60,
            bottom: 25
        }
        if (props.data !== undefined) {
            const data = props.data.map((prob, index) => {
                return {
                    "obs": index,
                    "prob": prob
                }
            })
            var domain = [0, 2]
            return (
                <ResponsiveContainer width='100%' height={height}>
                    <BarChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <text x={1200} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                            <tspan fontSize="22">{props.title}</tspan>
                        </text>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="obs" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                            <Label value={props.componentObs + " o"} offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number" tick={{transform: 'translate(-10,3)'}}>
                            <Label angle={270} value="Probability" offset={-40} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                className="largeFont"/>
                        <Bar dataKey="prob" fill="#8884d8" stroke="black" maxBarSize={15}
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
ObservationFunctionHistogram.propTypes = {};
ObservationFunctionHistogram.defaultProps = {};
export default ObservationFunctionHistogram;
