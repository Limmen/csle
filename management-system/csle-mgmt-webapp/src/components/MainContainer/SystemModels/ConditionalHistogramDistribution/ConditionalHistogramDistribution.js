import React from 'react';
import './ConditionalHistogramDistribution.css';
import getSystemModelTypeStr from '../../../Common/getSystemModelTypeStr'
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
import {
    MCMC_SYSTEM_MODEL_TYPE_INT, EMPIRICAL_SYSTEM_MODEL_TYPE, GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE, MCMC_SYSTEM_MODEL_TYPE
} from "../../../Common/constants";

const getConditionals = (systemModel, selectedConditionals, selectedMetric) => {
    if(systemModel.model_type === MCMC_SYSTEM_MODEL_TYPE_INT) {
        var posteriors = []
        for (let i = 0; i < systemModel.posteriors.length; i++) {
            for (let k = 0; k < selectedConditionals.length; k++) {
                if (selectedConditionals[k].value.posterior_name === systemModel.posteriors[i].posterior_name) {
                    posteriors.push(systemModel.posteriors[i])
                }
            }
        }
        return posteriors
    }
    var conds = []
    for (let i = 0; i < systemModel.conditional_metric_distributions.length; i++) {
        for (let j = 0; j < systemModel.conditional_metric_distributions[i].length; j++) {
            if (systemModel.conditional_metric_distributions[i][j]) {
                var conditionalMatch = false
                var metricMatch = false
                for (let k = 0; k < selectedConditionals.length; k++) {
                    if (selectedConditionals[k].value.conditional_name === systemModel.conditional_metric_distributions[i][j].conditional_name) {
                        conditionalMatch = true
                    }
                    if (selectedConditionals[k].value.metric_name === systemModel.conditional_metric_distributions[i][j].metric_name) {
                        metricMatch = true
                    }
                }
                if (conditionalMatch && metricMatch) {
                    conds.push(systemModel.conditional_metric_distributions[i][j])
                }
            }
        }
    }
    return conds
}

/**
 * Component containing a conditional distribution for a system model
 */
const ConditionalHistogramDistribution = React.memo((props) => {
        const width = 500
        const colors = ["#8884d8", "#82ca9d"]
        const height = 400
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
            var sample_space = conds[0].sample_space
            var p = num_samples / sample_space.length;
            for (let k = 0; k < sample_space.length; k++) {
                var maxY = 0
                if (Math.random() < p) {
                    var data_row = {
                        "val": sample_space[k]
                    }
                    for (let i = 0; i < conds.length; i++) {
                        var prob = 0
                        var name = conds[i].conditional_name
                        if (getSystemModelTypeStr(props.data.model_type) === GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE) {
                            for (let j = 0; j < conds[i].weighted_mixture_distributions.length; j++) {
                                prob = prob + conds[i].weighted_mixture_distributions[j][k]
                            }
                        }
                        if (getSystemModelTypeStr(props.data.model_type) === EMPIRICAL_SYSTEM_MODEL_TYPE) {
                            prob = conds[i].probabilities[k]
                        }
                        if (getSystemModelTypeStr(props.data.model_type) === MCMC_SYSTEM_MODEL_TYPE) {
                            prob = conds[i].densities[k]
                            name = conds[i].posterior_name
                        }
                        prob = Math.round(prob * 100000) / 100000
                        if (prob > maxY) {
                            maxY = prob
                        }
                        data_row[name] = prob
                    }
                    data.push(data_row)
                }
            }
            var domain = sample_space
            var yDomain = [0, maxY]

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
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="val" type="number" domain={domain}>
                                    <Label value="value" offset={-20} position="insideBottom" className="largeFont"/>
                                </XAxis>
                                <YAxis type="number" domain={yDomain}>
                                    <Label angle={270} value="Probability" offset={-30} position="insideLeft"
                                           className="largeFont"
                                           dy={50}/>
                                </YAxis>
                                <Tooltip/>
                                {conds.map((cond, index) => {
                                    var name = ""
                                    if(cond.conditional_name !== null && cond.conditional_name !== undefined){
                                        name = cond.conditional_name
                                    } else {
                                        name = cond.posterior_name
                                    }
                                    return (
                                        <Line key={name + "-" + index}
                                              isAnimationActive={false} animation={props.animation} type="monotone"
                                              dataKey={name}
                                              stroke={colors[index]} addDot={false} activeDot={{r: 8}}/>
                                    )
                                })}
                                <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
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
