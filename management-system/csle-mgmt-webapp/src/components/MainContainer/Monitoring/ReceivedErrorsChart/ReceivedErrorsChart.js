import React from 'react';
import './ReceivedErrorsChart.css';
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
 * Component containing a plot showing the average number of recieved errors over time
 */
const ReceivedErrorsChart = React.memo((props) => {
        const width = 500
        const height = 200
        const margin = {
            top: 10,
            right: 30,
            left: 60,
            bottom: 25
        }

        if (props.stats !== undefined && props.stats.length > 0) {
            var minReceivedErrors = 1000000000000
            var maxReceivedErrors = 0
            const data = props.stats.map((port_stats, index) => {
                if (parseInt(port_stats.total_num_received_errors) < minReceivedErrors){
                    minReceivedErrors = parseInt(port_stats.total_num_received_errors)
                }
                if (parseInt(port_stats.total_num_received_errors) > maxReceivedErrors){
                    maxReceivedErrors = parseInt(port_stats.total_num_received_errors)
                }
                return {
                    "t": (index + 1),
                    "Received errors": parseInt(port_stats.total_num_received_errors)
                }
            })
            var domain = [0, Math.max(1, data.length)]
            var yDomain = [minReceivedErrors, maxReceivedErrors]

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
                            <Label angle={270} value="# Received errors" offset={-50} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                className="largeFont"/>
                        <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                              dataKey="Received errors"
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
ReceivedErrorsChart.propTypes = {};
ReceivedErrorsChart.defaultProps = {};
export default ReceivedErrorsChart;
