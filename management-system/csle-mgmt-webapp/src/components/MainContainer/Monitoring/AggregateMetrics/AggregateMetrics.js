import React from 'react';
import './AggregateMetrics.css';
import SnortAlertsChart from "../SnortAlertsChart/SnortAlertsChart";
import OssecAlertsChart from "../OssecAlertsChart/OssecAlertsChart";
import Spinner from 'react-bootstrap/Spinner'
import CpuAndMemoryUtilizationChart from "../CpuAndMemoryUtilizationChart/CpuAndMemoryUtilizationChart";
import NetworkChart from "../NetworkChart/NetworkChart";
import BlockIOChart from "../BlockIOChart/BlockIOChart";
import ClientsChart from "../ClientsChart/ClientsChart";
import ClientsArrivalRateChart from "../ClientsArrivalRateChart/ClientsArrivalRateChart";
import ClientsServiceTimeChart from "../ClientsServiceTimeChart/ClientsServiceTimeChart";
import LoginsChart from "../LoginsChart/LoginsChart";
import ConnectionsChart from "../ConnectionsChart/ConnectionsChart";
import PidsChart from "../PidsChart/PidsChart";

/**
 * Component containing plots of aggregate metrics
 */
const AggregateMetrics = React.memo((props) => {
    if(!props.loading && (props.snortIdsMetrics === null || props.aggregatedHostMetrics === null
        || props.aggregatedDockerStats === null || props.clientMetrics === null)) {
        return (<></>)
    }
    if (props.loading || props.snortIdsMetrics === null || props.aggregatedDockerStats === null ||
            props.aggregatedHostMetrics === null || props.clientMetrics === null) {
            return (
                <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
    else {
        return (
            <div className="aggregatedMetrics">
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">

                        <h3 className="chartsTitle">Snort IDS Alerts</h3>
                        <SnortAlertsChart stats={props.snortIdsMetrics}
                                          animation={props.animation} animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg memory and CPU utilization</h3>
                        <CpuAndMemoryUtilizationChart stats={props.aggregatedDockerStats}
                                                      animation={props.animation}
                                                      animationDuration={props.animationDuration}
                                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Avg network load</h3>
                        <NetworkChart stats={props.aggregatedDockerStats}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Filesystem I/O</h3>
                        <BlockIOChart stats={props.aggregatedDockerStats}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of processes</h3>
                        <PidsChart stats={props.aggregatedDockerStats}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Login events</h3>
                        <LoginsChart stats={props.aggregatedHostMetrics}
                                     animation={props.animation} animationDuration={props.animationDuration}
                                     animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Connections and user sessions</h3>
                        <ConnectionsChart stats={props.aggregatedHostMetrics}
                                          animation={props.animation}
                                          animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Number of clients</h3>
                        <ClientsChart stats={props.clientMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Clients arrival rate</h3>
                        <ClientsArrivalRateChart stats={props.clientMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">OSSEC HIDS Alerts</h3>
                        <OssecAlertsChart stats={props.aggregatedOSSECMetrics}
                                     animation={props.animation} animationDuration={props.animationDuration}
                                     animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6 chartsCol">
                        <h3 className="chartsTitle">Clients average service time</h3>
                        <ClientsServiceTimeChart stats={props.clientMetrics}
                                                 animation={props.animation} animationDuration={props.animationDuration}
                                                 animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6 chartsCol">
                    </div>
                </div>
            </div>
            )
        }
    }
)

AggregateMetrics.propTypes = {};
AggregateMetrics.defaultProps = {};
export default AggregateMetrics;
