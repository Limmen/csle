import React, { useState } from 'react';
import ReactFlow, {
    ReactFlowProvider
} from 'react-flow-renderer';
import getElements from './getElements';
import './AttackerNetwork.css';
import ApplicationServer from "./ApplicationServer/ApplicationServer";
import Gateway from "./Gateway/Gateway";
import Client from "./Client/Client";
import Attacker from "./Attacker/Attacker";
import Defender from "./Defender/Defender";


/**
 * Called when the graph loads
 *
 */
const onLoad = (reactFlowInstance) => {
    reactFlowInstance.fitView();
}

/**
 * The DefenderNetwork Component
 */
const AttackerNetwork = () => {
    const rawElements = getElements({ x: 0, y:0})
    const [elements, setElements] = useState(rawElements);
    const height = 550
    const nodeTypes = {
        applicationServer: ApplicationServer,
        gateway: Gateway,
        client: Client,
        attacker: Attacker,
        defender: Defender
    };

    return (
        <div className="Network">
            {/*<h4 className="attackerNetworkTitle"> IT Infrastructure Status </h4>*/}
            <div className="layoutflow">
                <ReactFlowProvider>
                    <ReactFlow
                        style={{ height: height}}
                        elements={elements}
                        onLoad={onLoad}
                        nodesDraggable={false}
                        nodesConnectable={false}
                        paneMoveable={false}
                        defaultZoom={1}
                        minZoom={1}
                        maxZoom={1}
                        nodeTypes={nodeTypes}
                    />
                </ReactFlowProvider>
            </div>
        </div>
    );
}

AttackerNetwork.propTypes = {};
AttackerNetwork.defaultProps = {};
export default AttackerNetwork;
