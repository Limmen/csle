import React from 'react';
import './SpinnerOrButton.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import { confirmAlert } from 'react-confirm-alert';
import Spinner from 'react-bootstrap/Spinner'

/**
 * Subcomponent of the /control-plane page
 */
const SpinnerOrButton = (props) => {


    const startOrStopConfirm = (start, stop, entity, name, ip) => {
        confirmAlert({
            title: 'Confirm action',
            message: ('Are you sure you want to ' + (start ? "start": "stop") + 'the ' + entity + " with IP: " + ip + "?"),
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => props.startOrStop(start, stop, entity, name, ip)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({ onClose }) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm action</h1>
                                    Are you sure you want to  {start ? "start": "stop"} the {entity} with IP: {ip}?
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    props.startOrStop(start, stop, entity, name, ip)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, perform the action.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const renderStopTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop
        </Tooltip>)
    }

    const renderStartTooltip = (props) => {
        return (<Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start
        </Tooltip>)
    }
    if (props.loading) {
        return (<Spinner
            as="span"
            animation="grow"
            size="sm"
            role="status"
            aria-hidden="true"
        />)
    } else {
        if (props.running) {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStopTooltip}
                >
                    <Button variant="warning" className="startButton" size="sm"
                            onClick={() => startOrStopConfirm(false, true, props.entity, props.name, props.ip)}>
                        <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (
                <OverlayTrigger
                    placement="top"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip}
                >
                    <Button variant="success" className="startButton" size="sm"
                            onClick={() => startOrStopConfirm(true, false, props.entity, props.name, props.ip)}>
                        <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        }
    }
}

SpinnerOrButton.propTypes = {};
SpinnerOrButton.defaultProps = {};
export default SpinnerOrButton;
