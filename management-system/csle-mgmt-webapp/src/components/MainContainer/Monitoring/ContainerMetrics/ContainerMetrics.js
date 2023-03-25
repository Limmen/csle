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
import SnortAlertsChart from "../SnortAlertsChart/SnortAlertsChart";

/**
 * Component containing a plot showing a number of container-specific plots
 */
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
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg memory and CPU utilization</h3>
                        <CpuAndMemoryUtilizationChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg network load</h3>
                        <NetworkChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Filesystem I/O</h3>
                        <BlockIOChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of processes</h3>
                        <PidsChart
                            stats={props.dockerMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Login events</h3>
                        <LoginsChart
                            stats={props.hostMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Connections and user sessions</h3>
                        <ConnectionsChart
                            stats={props.hostMetrics}
                            animation={props.animation} animationDuration={props.animationDuration}
                            animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">OSSEC HIDS Alerts</h3>
                        <OssecAlertsChart stats={props.ossecAlerts}
                                          animation={props.animation} animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Snort IDS Alerts</h3>
                        <SnortAlertsChart stats={props.snortAlerts}
                                          animation={props.animation} animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
            </div>
        )
    }
})

ContainerMetrics.propTypes = {};
ContainerMetrics.defaultProps = {};
export default ContainerMetrics;
