import React from 'react';
import './LogsButton.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

/**
 * Subcomponent of the /control-plane page that the button to view logs
 */
const LogsButton = (props) => {

    const renderLogsTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            View logs
        </Tooltip>)
    }

    return (
        <OverlayTrigger
            placement="top"
            delay={{show: 0, hide: 0}}
            overlay={renderLogsTooltip}
        >
            <Button variant="info" className="startButton" size="sm"
                    onClick={() => props.getLogs(props.name, props.entity)}>
                <i className="fa fa-folder-open startStopIcon" aria-hidden="true"/>
            </Button>
        </OverlayTrigger>
    );
}

LogsButton.propTypes = {};
LogsButton.defaultProps = {};
export default LogsButton;
