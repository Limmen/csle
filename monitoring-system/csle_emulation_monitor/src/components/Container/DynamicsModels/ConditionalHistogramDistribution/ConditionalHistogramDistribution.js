import React from 'react';
import './ConditionalHistogramDistribution.css';
import {
    CartesianGrid,
    Label,
    Legend,
    Scatter, ScatterChart,
    ResponsiveContainer,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis
} from "recharts";

const ConditionalHistogramDistribution = React.memo((props) => {
        const width = 500
        const colors  = ["#8884d8", "#82ca9d"]
        const shapes  = ["triangle", "circle"]
        const height = 600
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.data !== undefined) {
            var max_val = -99999
            var min_val = 999999

            var keys = []
            for (let i = 0; i < props.selectedConditionals.length; i++) {
                var tempKeys = Object.keys(props.data[props.selectedConditionals[i].value][props.selectedMetric.value])
                for (let j = 0; j < tempKeys.length; j++) {
                    keys.push(tempKeys[j])
                }
            }
            keys = [...new Set(keys)];
            var data2 = []
            var data3 = []
            var data4 = []
            for (let i = 0; i < keys.length; i++) {
                var scatterDataRow1 = {}
                var scatterDataRow2 = {}
                var dataRow = {}
                dataRow["value"] = parseInt(keys[i])
                if (dataRow["value"] > max_val) {
                    max_val = dataRow["value"]
                }
                if (dataRow["value"] < min_val) {
                    min_val = dataRow["value"]
                }
                scatterDataRow1["value"] = dataRow["value"]
                scatterDataRow2["value"] = dataRow["value"]
                for (let j = 0; j < props.selectedConditionals.length; j++) {
                    if (props.data[props.selectedConditionals[j].value][props.selectedMetric.value].hasOwnProperty(keys[i])) {
                        dataRow[props.selectedConditionals[j].label] = props.data[props.selectedConditionals[j].value][props.selectedMetric.value][keys[i]]
                        if(j === 0) {
                            scatterDataRow1["count"] = props.data[props.selectedConditionals[j].value][props.selectedMetric.value][keys[i]]
                        } else {
                            scatterDataRow2["count"] = props.data[props.selectedConditionals[j].value][props.selectedMetric.value][keys[i]]
                        }
                    } else {
                        dataRow[props.selectedConditionals[j].label] = 0
                        if(j === 0) {
                            scatterDataRow1["count"] = 0
                        } else {
                            scatterDataRow2["count"] = 0
                        }
                    }
                }
                data2.push(dataRow)
                data3.push(scatterDataRow1)
                data4.push(scatterDataRow2)
            }
            var domain = [min_val, max_val]
            return (
                <div className="row">
                    <div className="col-sm-6">
                        <ResponsiveContainer width='100%' height={height}>
                            <ScatterChart
                                width={width}
                                height={height}
                                data={data3}
                                margin={margin}
                            >
                                <text x={1300 / 2} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                                    <tspan fontSize="22">{props.title2}</tspan>
                                </text>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="value" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                                    <Label value="Value" offset={-20} position="insideBottom" className="largeFont"/>
                                </XAxis>
                                <YAxis type="number" tick={{transform: 'translate(-10,3)'}} dataKey="count">
                                    <Label angle={270} value="# Count" offset={0} position="insideLeft"
                                           className="largeFont"
                                           dy={50}/>
                                </YAxis>
                                <Tooltip/>
                                <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                        className="largeFont"/>
                                {props.selectedConditionals.map((conditional, index) => {
                                    if (index === 0) {
                                        return (<Scatter key={conditional.label + "-" + index}
                                                         name={conditional.label}
                                                         data={data3} fill={colors[0]} stroke="black" animationEasing={'linear'}
                                                 animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                                                 shape={shapes[0]}/>)
                                    } else {
                                        return (<Scatter key={conditional.label + "-" + index}
                                            name={conditional.label}
                                                         data={data4} fill={colors[1]} stroke="black" animationEasing={'linear'}
                                                 animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                                                 shapes={shapes[1]}/>)
                                    }
                                })}
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="col-sm-6">
                        <ResponsiveContainer width='100%' height={height}>
                            <BarChart
                                width={width}
                                height={height}
                                data={data2}
                                margin={margin}
                            >
                                <text x={1300 / 2} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                                    <tspan fontSize="22">{props.title1}</tspan>
                                </text>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="value" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                                    <Label value="Value" offset={-20} position="insideBottom" className="largeFont"/>
                                </XAxis>
                                <YAxis type="number" tick={{transform: 'translate(-10,3)'}}>
                                    <Label angle={270} value="# Count" offset={0} position="insideLeft"
                                           className="largeFont"
                                           dy={50}/>
                                </YAxis>
                                <Tooltip/>
                                <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                        className="largeFont"/>
                                {props.selectedConditionals.map((conditional, index) => {
                                    return (
                                        <Bar key={conditional.label + "-" + index}
                                             dataKey={conditional.label}
                                             fill={colors[index]} stroke="black" animationEasing={'linear'}
                                             animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                                             maxBarSize={15}
                                        />
                                    )
                                })}
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
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
