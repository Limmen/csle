import React, { useState, useEffect } from 'react';
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
import Switch from "./Switch/Switch";
import IDS from "./IDS/IDS";


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
const AttackerNetwork = (props) => {
    var attacker_found_nodes = []
    var attacker_compromised_nodes = []
    if (props.traces.length > 0) {
        attacker_found_nodes = props.traces[props.activeTrace].attacker_found_nodes[props.t]
        attacker_compromised_nodes = props.traces[props.activeTrace].attacker_compromised_nodes[props.t]
    }
    attacker_found_nodes.push("attacker")
    attacker_found_nodes.push("client")
    attacker_found_nodes.push("ids")
    attacker_found_nodes.push("gateway")

    const rawElements = getElements({ x: 0, y:0})
    const [elements, setElements] = useState(rawElements);
    const [isHidden, setIsHidden] = useState(false);
    const [attackerFoundNodes, setAttackerFoundNodes] = useState(attacker_found_nodes);
    const height = 850
    const nodeTypes = {
        applicationServer: ApplicationServer,
        gateway: Gateway,
        client: Client,
        attacker: Attacker,
        defender: Defender,
        ids: IDS,
        switch: Switch
    };

    useEffect(() => {
        setElements((els) =>
            els.map((e, index) => {
                e.isHidden = (!attacker_found_nodes.includes(e.id) && !(attacker_found_nodes.includes(e.source) && attacker_found_nodes.includes(e.target)));
                return e;
            })
        );
    }, [props, attacker_found_nodes]);

    // useEffect(() => {
    //     setElements(elements);
    // }, [elements, setElements()]);

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
