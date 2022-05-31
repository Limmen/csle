import React from 'react';
import './ConditionalHistogramDistribution.css';
import {
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    Line,
    LineChart,
    XAxis,
    YAxis
} from "recharts";

const getConditionals  = (systemModel, selectedConditionals, selectedMetric) => {
    var conds = []
    for (let i = 0; i < systemModel.conditional_metric_distributions.length; i++) {
        for (let j = 0; j < systemModel.conditional_metric_distributions[i].length; j++) {
            if(systemModel.conditional_metric_distributions[i][j]){
                var conditionalMatch = false
                var metricMatch = false
                for (let k = 0; k < selectedConditionals.length; k++) {
                    if(selectedConditionals[k].value.conditional_name === systemModel.conditional_metric_distributions[i][j].conditional_name) {
                        conditionalMatch = true
                    }
                    if(selectedConditionals[k].value.metric_name === systemModel.conditional_metric_distributions[i][j].metric_name) {
                        metricMatch = true
                    }
                }
                if(conditionalMatch && metricMatch) {
                    conds.push(systemModel.conditional_metric_distributions[i][j])
                }
            }
        }
    }
    return conds
}

const ConditionalHistogramDistribution = React.memo((props) => {
        const width = 500
        const colors = ["#8884d8", "#82ca9d"]
        const shapes = ["triangle", "circle"]
        const height = 600
        const margin = {
            top: 10,
            right: 30,
            left: 60,
            bottom: 25
        }
        const num_samples = 100
        const conds = getConditionals(props.data, props.selectedConditionals, props.selectedMetric.value)
        if (props.data !== undefined && conds !== undefined && conds !== null && conds.length > 0) {
            var data = []
            const p = num_samples/conds[0].sample_space.length
            for (let k = 0; k < conds[0].sample_space.length; k++) {
                if(Math.random() < p) {
                    var data_row = {
                        "val": conds[0].sample_space[k]
                    }
                    for (let i = 0; i < conds.length; i++) {
                        var prob = 0
                        for (let j = 0; j < conds[i].weighted_mixture_distributions.length; j++) {
                            prob = prob + conds[i].weighted_mixture_distributions[j][k]
                        }
                        data_row[conds[i].conditional_name] = prob
                    }
                    data.push(data_row)
                }
            }
            var domain = conds[0].sample_space

            return (
                <div className="row">
                    <div className="col-sm-12">
                        <ResponsiveContainer width='100%' height={height}>
                            <LineChart
                                width={width}
                                height={height}
                                data={data}
                                margin={margin}
                            >
                                <text x={1150} y={20} fill="black" textAnchor="middle" dominantBaseline="central">
                                    <tspan fontSize="22">Metric: {conds[0].metric_name} (Downsampled to {num_samples} samples)</tspan>
                                </text>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="val" type="number" domain={domain}>
                                    <Label value="value" offset={-20} position="insideBottom" className="largeFont"/>
                                </XAxis>
                                <YAxis type="number">
                                    <Label angle={270} value="Probability" offset={-30} position="insideLeft"
                                           className="largeFont"
                                           dy={50}/>
                                </YAxis>
                                <Tooltip/>
                                {conds.map((cond, index) => {
                                    return (
                                        <Line key={cond.conditional_name + "-" + index}
                                              isAnimationActive={false} animation={props.animation} type="monotone"
                                              dataKey={cond.conditional_name}
                                              stroke={colors[index]} addDot={false} activeDot={{r: 8}}/>
                                    )
                                })}
                                <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '22px'}}
                                        className="largeFont"/>

                            </LineChart>
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
