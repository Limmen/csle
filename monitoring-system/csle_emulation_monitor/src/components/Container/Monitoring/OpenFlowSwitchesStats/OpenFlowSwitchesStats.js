import React from 'react';
import './OpenFlowSwitchesStats.css';
import Spinner from 'react-bootstrap/Spinner'
import ReceivedBytesChart from "../ReceivedBytesChart/ReceivedBytesChart";
import ReceivedPacketsChart from "../ReceivedPacketsChart/ReceivedPacketsChart";
import TransmittedBytesChart from "../TransmittedBytesChart/TransmittedBytesChart";
import TransmittedPacketsChart from "../TransmittedPacketsChart/TransmittedPacketsChart";
import NumCollisionsChart from "../NumCollisionsChart/NumCollisionsChart.js";
import ReceivedCRCErrorsChart from "../ReceivedCRCErrorsChart/ReceivedCRCErrorsChart.js";
import ReceivedErrorsChart from "../ReceivedErrorsChart/ReceivedErrorsChart.js";
import ReceivedDroppedChart from "../ReceivedDroppedChart/ReceivedDroppedChart.js";
import ReceivedFrameErrorsChart from "../ReceivedFrameErrorsChart/ReceivedFrameErrorsChart.js";
import ReceivedOverrunErrorsChart from "../ReceivedOverrunErrorsChart/ReceivedOverrunErrorsChart.js";
import TransmittedDroppedChart from "../TransmittedDroppedChart/TransmittedDroppedChart.js";
import TransmittedErrorsChart from "../TransmittedErrorsChart/TransmittedErrorsChart.js";
import FlowDurationChart from "../FlowDurationChart/FlowDurationChart";
import FlowPriorityChart from "../FlowPriorityChart/FlowPriorityChart";

const OpenFlowSwitchesStats = React.memo((props) => {
    if(!props.loading && (props.flowStats === null || props.portStats === null)) {
        return (<></>)
    }
    if (props.loading || props.flowStats === null || props.portStats === null) {
        return (
            <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
                <span className="visually-hidden"></span>
            </Spinner>)
    } else {
        return (
            <div className="aggregatedMetrics">
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ReceivedBytesChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <TransmittedBytesChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ReceivedPacketsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <TransmittedPacketsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ReceivedErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <TransmittedErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ReceivedDroppedChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <TransmittedDroppedChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <NumCollisionsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <ReceivedOverrunErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ReceivedCRCErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <ReceivedFrameErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <FlowDurationChart
                            stats={props.flowStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <FlowPriorityChart
                            stats={props.flowStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
            </div>
        )
    }
})

OpenFlowSwitchesStats.propTypes = {};
OpenFlowSwitchesStats.defaultProps = {};
export default OpenFlowSwitchesStats;
