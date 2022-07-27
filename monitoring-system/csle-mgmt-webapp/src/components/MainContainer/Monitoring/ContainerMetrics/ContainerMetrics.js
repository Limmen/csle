import React from 'react';
import './ContainerMetrics.css';
import Spinner from 'react-bootstrap/Spinner'
import CpuAndMemoryUtilizationChart from "../CpuAndMemoryUtilizationChart/CpuAndMemoryUtilizationChart";
import NetworkChart from "../NetworkChart/NetworkChart";
import BlockIOChart from "../BlockIOChart/BlockIOChart";
import PidsChart from "../PidsChart/PidsChart";
import LoginsChart from "../LoginsChart/LoginsChart";
import ConnectionsChart from "../ConnectionsChart/ConnectionsChart";
import OssecAlertsChart from "../OssecAlertsChart/OssecAlertsChart";

const ContainerMetrics = React.memo((props) => {
    if(!props.loading && (props.dockerMetrics === null || props.hostMetrics === null)) {
        return (<></>)
    }
    if (props.loading || props.dockerMetrics === null || props.hostMetrics === null) {
        return (
            <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
                <span className="visually-hidden"></span>
            </Spinner>)
    } else {
        return (
            <div className="aggregatedMetrics">
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <CpuAndMemoryUtilizationChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <NetworkChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <BlockIOChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <PidsChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <LoginsChart
                            stats={props.hostMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <ConnectionsChart
                            stats={props.hostMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <OssecAlertsChart stats={props.ossecAlerts}
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

ContainerMetrics.propTypes = {};
ContainerMetrics.defaultProps = {};
export default ContainerMetrics;
