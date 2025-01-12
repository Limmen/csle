import React from 'react';
import './DeltaAlertsLineChart.css';
import {
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
    Bar,
    BarChart,
    ReferenceLine
} from "recharts";

/**
 * Component representing the delta alerts chart in the policy examination page
 */
const DeltaAlertsLineChart = React.memo((props) => {
        const width = 5000
        const height = 310
        const margin = {
            top: 10,
            right: 30,
            left: 15,
            bottom: 25
        }

        if (props.activeTrace !== null && props.activeTrace !== undefined) {
            // const filteredData = props.activeTrace.defender_observations
            //     .filter((prob, index) => index <= props.t)
            var data = []
            const filteredData = props.activeTrace.value.defender_observations
            var ticks = []
            for (let i = 0; i < filteredData.length; i++) {
                var deltaX = filteredData[i][0]
                var deltaY = filteredData[i][1]
                var deltaZ = filteredData[i][2]
                data.push(
                    {
                        t: i + 1,
                        "Severe Alerts Δx": deltaX,
                        "Warning Alerts Δy": deltaY,
                        "Login Attempts Δz": deltaZ
                    }
                )
                ticks.push(i + 1)
            }
            var domain = [0, Math.max(1, data.length)]
            if (props.fullDomain) {
                domain = [1, props.activeTrace.value.defender_observations.length]
            }
            return (
                <div className="DefenderPolicy row justify-content-center card demoCard">
                    <div className="card-header cardHeader">
                        <h4>
                            Measured infrastructure metrics (Δx, Δy, Δz)
                        </h4>
                    </div>
                    <ResponsiveContainer width='100%' height={height}>
                        <BarChart
                            width={width}
                            height={height}
                            data={data.slice(0, props.t)}
                            margin={margin}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="t" type="number" domain={domain}
                                   ticks={ticks.slice(0, props.t)}
                            >
                                <Label value="Time-step t" offset={-20} position="insideBottom"
                                       className="largeFont"/>
                            </XAxis>
                            <YAxis type="number">
                                <Label angle={270} value="Value" offset={0} position="insideLeft"
                                       className="largeFont"/>
                            </YAxis>
                            <Tooltip/>
                            <Legend verticalAlign="top" wrapperStyle={{position: 'relative', fontSize: '15px'}}
                                    className="largeFont"/>
                            <ReferenceLine x={props.activeTrace.value.intrusion_start_index}
                                           stroke="black" label={{
                                position: 'insideTopRight',
                                value: 'Intrusion starts', fill: 'black',
                                fontSize: 15, marginTop: "10px"
                            }} strokeDasharray="3 3"
                            />
                            <Bar dataKey="Severe Alerts Δx" fill="#8884d8" stroke="black" animationEasing={'linear'}
                                 animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                            />
                            <Bar dataKey="Warning Alerts Δy" fill="#82ca9d" stroke="black"
                                 animationEasing={'linear'}
                                 animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                            />
                            <Bar dataKey="Login Attempts Δz" fill="#742911" stroke="black"
                                 animationEasing={'linear'}
                                 animationDuration={((1 - (props.animationDuration / 100)) * props.animiationDurationFactor)}
                            />
                        </BarChart>
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
DeltaAlertsLineChart.propTypes = {};
DeltaAlertsLineChart.defaultProps = {};
export default DeltaAlertsLineChart;
