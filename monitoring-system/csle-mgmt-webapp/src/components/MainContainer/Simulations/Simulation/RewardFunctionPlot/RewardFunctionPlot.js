import React from 'react';
import './RewardFunctionPlot.css';
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

/**
 * Component containing a chart showing the reward function
 */
const RewardFunctionPlot = React.memo((props) => {
        const width = 500
        const height = 400
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }
        const num_samples = 100
        if (props.data !== undefined) {
            const p = num_samples/props.data.length
            var data = []
            for (let i = 0; i < props.data.length; i++) {
                if(Math.random() < p) {
                    data.push({
                        "state": i,
                        "rew": props.data[i]
                    })
                }
            }
            var domain = [props.minState, props.maxState]
            return (
                <ResponsiveContainer width='100%' height={height}>
                    <LineChart
                        width={width}
                        height={height}
                        data={data}
                        margin={margin}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="state" type="number" domain={domain} tick={{transform: 'translate(0,5)'}}>
                            <Label value="s" offset={-20} position="insideBottom" className="largeFont"/>
                        </XAxis>
                        <YAxis type="number" tick={{transform: 'translate(-10,3)'}}>
                            <Label angle={270} value="Reward" offset={0} position="insideLeft"
                                   className="largeFont"
                                   dy={50}/>
                        </YAxis>
                        <Tooltip/>
                        <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                className="largeFont"/>
                        <Line type="monotone" dataKey="rew"  stroke="#8884d8" addDot={false} activeDot={{r: 8}}/>
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
RewardFunctionPlot.propTypes = {};
RewardFunctionPlot.defaultProps = {};
export default RewardFunctionPlot;
