import React from 'react';
import './OpenFlowSwitchesStats.css';
import Spinner from 'react-bootstrap/Spinner'
import ReceivedBytesChart from "../ReceivedBytesChart/ReceivedBytesChart";

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
                    </div>
                </div>
            </div>
        )
    }
})

OpenFlowSwitchesStats.propTypes = {};
OpenFlowSwitchesStats.defaultProps = {};
export default OpenFlowSwitchesStats;
