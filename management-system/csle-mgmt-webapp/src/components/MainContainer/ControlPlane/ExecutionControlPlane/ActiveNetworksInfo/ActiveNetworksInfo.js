import React from 'react';
import './ActiveNetworksInfo.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from "../SpinnerOrButton/SpinnerOrButton";
import LogsButton from "../LogsButton/LogsButton";

/**
 * Subcomponent of the /control-plane page that contains information about active networks
 */
const ActiveNetworksInfo = (props) => {
    return (
        <Card className="subCard">
            <Card.Header>
                <Button
                    onClick={() => props.setActiveNetworksOpen(!props.activeNetworksOpen)}
                    aria-controls="activeNetworksBody"
                    aria-expanded={props.activeNetworksOpen}
                    variant="link"
                >
                    <h5 className="semiTitle"> Active networks </h5>
                </Button>
            </Card.Header>
            <Collapse in={props.activeNetworksOpen}>
                <div id="activeNetworksBody" className="cardBodyHidden">
                    <div className="table-responsive">
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Network name</th>
                                <th>Subnet mask</th>
                                <th>Bitmask</th>
                                <th>Status</th>
                            </tr>
                            </thead>
                            <tbody>
                            {props.activeNetworks.map((network, index) =>
                                <tr key={network.name + "-" + index}>
                                    <td>{network.name}</td>
                                    <td>{network.subnet_mask}</td>
                                    <td>{network.bitmask}</td>
                                    <td className="containerRunningStatus">Active</td>
                                </tr>
                            )}
                            {props.inactiveNetworks.map((network, index) =>
                                <tr key={network.name + "-" + index}>
                                    <td>{network.name}</td>
                                    <td>{network.subnet_mask}</td>
                                    <td>{network.bitmask}</td>
                                    <td className="containerStoppedStatus">Inactive</td>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </Collapse>
        </Card>
    );
}

ActiveNetworksInfo.propTypes = {};
ActiveNetworksInfo.defaultProps = {};
export default ActiveNetworksInfo;
