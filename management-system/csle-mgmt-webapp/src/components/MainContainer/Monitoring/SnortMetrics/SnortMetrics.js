import React from 'react';
import './SnortMetrics.css';
import SnortAlertsChart from "../SnortAlertsChart/SnortAlertsChart";
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of Snort metrics
 */
const SnortMetrics = React.memo((props) => {
    if(!props.loading && (props.snortIdsMetrics === null)) {
        return (<></>)
    }
    if (props.loading || props.snortIdsMetrics === null) {
            return (
                <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        }
    else {
        return (
            <div className="aggregatedMetrics">
                <div className="row chartsRow">
                    <div className="col-sm-12 chartsCol">

                        <h3 className="chartsTitle">Snort IDS Alerts</h3>
                        <SnortAlertsChart stats={props.snortIdsMetrics}
                                          animation={props.animation} animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor}/>
                    </div>
                </div>
            </div>
            )
        }
    }
)

SnortMetrics.propTypes = {};
SnortMetrics.defaultProps = {};
export default SnortMetrics;
