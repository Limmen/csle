import React, {useState} from 'react';
import './AggregateMetrics.css';
import AlertsChart from "../AlertsChart/AlertsChart";
import Spinner from 'react-bootstrap/Spinner'
import CpuAndMemoryUtilizationChart from "../CpuAndMemoryUtilizationChart/CpuAndMemoryUtilizationChart";
import NetworkChart from "../NetworkChart/NetworkChart";
import BlockIOChart from "../BlockIOChart/BlockIOChart";
import ClientsChart from "../ClientsChart/ClientsChart";
import LoginsChart from "../LoginsChart/LoginsChart";
import ConnectionsChart from "../ConnectionsChart/ConnectionsChart";
import PidsChart from "../PidsChart/PidsChart";

const AggregateMetrics = React.memo((props) => {
    if (props.loading || props.idsMetrics === null || props.aggregatedDockerStats === null ||
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
                    <div className="col-sm-6">
                        <AlertsChart stats={props.idsMetrics}
                                     animation={props.animation} animationDuration={props.animationDuration}
                                     animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <CpuAndMemoryUtilizationChart stats={props.aggregatedDockerStats}
                                                      animation={props.animation}
                                                      animationDuration={props.animationDuration}
                                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <NetworkChart stats={props.aggregatedDockerStats}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <BlockIOChart stats={props.aggregatedDockerStats}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <PidsChart stats={props.aggregatedDockerStats}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <LoginsChart stats={props.aggregatedHostMetrics}
                                     animation={props.animation} animationDuration={props.animationDuration}
                                     animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
                <div className="row chartsRow">
                    <div className="col-sm-6">
                        <ConnectionsChart stats={props.aggregatedHostMetrics}
                                          animation={props.animation}
                                          animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                    <div className="col-sm-6">
                        <ClientsChart stats={props.clientMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor}/>
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
