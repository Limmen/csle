import React from 'react';
import './ShellButton.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import {useNavigate} from "react-router-dom";
import {CONTAINER_TERMINAL_PAGE_RESOURCE} from "../../../../Common/constants";

/**
 * Component representing the button to create a new SSH shell to a container on the page /control-plane page
 */
const ShellButton = (props) => {
    const navigate = useNavigate();

    const renderShellTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Open SSH shell
        </Tooltip>)
    }

    const openShell = (ip, executionId, emulation) => {
        navigate(`/${CONTAINER_TERMINAL_PAGE_RESOURCE}`,
            {state: {ip: ip, executionId: executionId, emulation: emulation}});
    }

    return (
        <OverlayTrigger
            placement="top"
            delay={{show: 0, hide: 0}}
            overlay={renderShellTooltip}
        >
            <Button variant="secondary" className="startButton" size="sm"
                    onClick={() => openShell(props.ip, props.executionId, props.emulation)}>
                <i className="fa fa-terminal startStopIcon" aria-hidden="true"/>
            </Button>
        </OverlayTrigger>
    );
}

ShellButton.propTypes = {};
ShellButton.defaultProps = {};
export default ShellButton;
