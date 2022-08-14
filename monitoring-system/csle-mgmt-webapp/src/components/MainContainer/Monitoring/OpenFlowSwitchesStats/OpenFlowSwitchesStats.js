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
import NumFlowsChart from "../NumFlowsChart/NumFlowsChart";


/**
 * Component containing various plots related to openflow switch statistics
 */
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
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Received bytes</h3>
                        <ReceivedBytesChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Transmitted bytes</h3>
                        <TransmittedBytesChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Received packets</h3>
                        <ReceivedPacketsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Transmitted packets</h3>
                        <TransmittedPacketsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of Received errors</h3>
                        <ReceivedErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of Transmitted errors</h3>
                        <TransmittedErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of Received dropped frames</h3>
                        <ReceivedDroppedChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of Transmitted dropped frames</h3>
                        <TransmittedDroppedChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of frame collisions</h3>
                        <NumCollisionsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Received overrun errors</h3>
                        <ReceivedOverrunErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of Received CRC errors</h3>
                        <ReceivedCRCErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Received frame errors</h3>
                        <ReceivedFrameErrorsChart
                            stats={props.portStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>

                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg Flow Duration (s)</h3>
                        <FlowDurationChart
                            stats={props.flowStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg Flow Priority</h3>
                        <FlowPriorityChart
                            stats={props.flowStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Num flows</h3>
                        <NumFlowsChart
                            stats={props.aggFlowStats}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                    </div>
                </div>
            </div>
        )
    }
})

OpenFlowSwitchesStats.propTypes = {};
OpenFlowSwitchesStats.defaultProps = {};
export default OpenFlowSwitchesStats;
