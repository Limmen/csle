import React from 'react';
import './ShellButton.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

/**
 * Component representing the button to create a new SSH shell to a container on the page /control-plane page
 */
const ShellButton = (props) => {
    console.log(props.ip)

    const renderShellTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Open SSH shell
        </Tooltip>)
    }

    return (
        <OverlayTrigger
            placement="right"
            delay={{show: 0, hide: 0}}
            overlay={renderShellTooltip}
        >
            <Button variant="secondary" className="startButton" size="sm"
                    onClick={() => props.getLogs(props.name)}>
                <i className="fa fa-terminal startStopIcon" aria-hidden="true"/>
            </Button>
        </OverlayTrigger>
    );
}

ShellButton.propTypes = {};
ShellButton.defaultProps = {};
export default ShellButton;
