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

/**
 * Component containing a metric plot shown as part of an experiment
 */
const MetricPlot = React.memo((props) => {
        const width = 500
        const height = 400
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        if (props.data !== undefined && props.data !== null && props.data.length > 0 && !Array.isArray(props.data[0])) {
            const data = props.data.map((metric, index) => {
                var row = {}
                row["t"] = index
                row[props.metricName] = metric
                if (props.stds !== undefined && props.stds !== null) {
                    row["err"] = props.stds[index]
                } else {
                    row["err"] = 0
                }
                return row
            })
            var domain = [0, 1]
            return (
                <div>
                    <h3>{props.title}</h3>
                    <ResponsiveContainer width='100%' height={height}>
                        <LineChart
                            width={width}
                            height={height}
                            data={data}
                            margin={margin}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="t" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                                <Label value="Training iteration" offset={-20} position="insideBottom"
                                       className="largeFont"/>
                            </XAxis>
                            <YAxis type="number" tick={{transform: 'translate(-10,3)'}}>
                                <Label angle={270} value={props.metricName} offset={0} position="insideLeft"
                                       className="largeFont"
                                       dy={50}/>
                            </YAxis>
                            <Tooltip/>
                            <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                    className="largeFont"/>
                            <Line type="monotone" dataKey={props.metricName} stroke="#8884d8" addDot={false}
                                  activeDot={{r: 8}}>
                                <ErrorBar dataKey="err" width={4} strokeWidth={2} stroke="green" direction="y"/>
                            </Line>
                        </LineChart>
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
MetricPlot.propTypes = {};
MetricPlot.defaultProps = {};
export default MetricPlot;
