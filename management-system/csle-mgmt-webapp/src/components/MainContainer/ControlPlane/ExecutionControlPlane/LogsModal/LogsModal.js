import React from 'react';
import './LogsModal.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Table from 'react-bootstrap/Table'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Subcomponent of the /control-plane page that represents a modal with logs
 */
const LogsModal = (props) => {

    const SpinnerOrLogs = (props) => {
        if (props.loadingLogs || props.logs === null || props.logs === undefined) {
            return (
                <div>
                    <span className="logsLabel">Fetching logs...</span>
                    <Spinner
                        as="span"
                        animation="grow"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                    />
                </div>
            )
        } else {
            return (
                <div className="table-responsive">
                    <Table striped bordered hover>
                        <thead>
                        <tr>
                            <th>Line number</th>
                            <th>Log</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.logs.map((logLine, index) => {
                            return <tr key={logLine.index + "-" + index}>
                                <td>{logLine.index}</td>
                                <td>{logLine.content}</td>
                            </tr>
                        })}
                        </tbody>
                    </Table>
                </div>
            )
        }
    }

    return (
        <Modal
            {...props}
            size="xl"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                    {props.entity} logs for: {props.name}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="logsModalBody">
                    <div className="table-responsive">
                        <SpinnerOrLogs loadingLogs={props.loading} logs={props.logs}/>
                    </div>
                </div>
            </Modal.Body>
            <Modal.Footer className="modalFooter">
                <Button onClick={props.onHide} size="sm">Close</Button>
            </Modal.Footer>
        </Modal>
    );
}

LogsModal.propTypes = {};
LogsModal.defaultProps = {};
export default LogsModal;
