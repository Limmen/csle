/**
 * Get the elements to render.
 * An element is either a node or an edge.
 */

import getWindowDimensions from "./getDimensions";

/**
 * Gets the list of nodes
 */
const getNodes = (base_position = {x: 0, y: 0}) => {
    const dimensions = getWindowDimensions()
    const attackerBaseY=dimensions.height
    const attackerBaseX=0
    const gatewayBaseY = attackerBaseY + 100
    const gatewayBaseX = attackerBaseX + 175
    const clientBaseY = attackerBaseY + 10
    const clientBaseX = gatewayBaseX + 100

    const appServerHorizontalPadding = 50
    const appServerVerticalPadding = 100
    const appServerBaseY=gatewayBaseY+ 80
    const appServerBaseX=gatewayBaseX
    return [
        {
            id: 'attacker',
            type: 'attacker',
            className: "nodrag",
            data: {label: 'attacker', text:'Attacker'},
            position: {x: attackerBaseX, y: attackerBaseY}
        },
        {
            id: 'client',
            type: 'client',
            className: "nodrag",
            data: {label: 'client1', text:'Client population'},
            position: {x: clientBaseX, y: clientBaseY}
        },
        {
            id: 'gateway',
            type: 'gateway',
            className: "nodrag",
            data: {label: 'gateway', text:'Gateway'},
            position: {x: gatewayBaseX, y: gatewayBaseY}
        },
        {
            id: 'n1',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N1', text:'N1'},
            position: {x: gatewayBaseX-2*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n2',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N2', text:'N2'},
            position: {x: appServerBaseX-1*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n3',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N3', text:'N3'},
            position: {x: appServerBaseX, y: appServerBaseY}
        },
        {
            id: 'n4',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N4', text:'N4'},
            position: {x: appServerBaseX +appServerHorizontalPadding*1, y: appServerBaseY}
        },
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX +appServerHorizontalPadding*2, y: appServerBaseY}
        },
        {
            id: 'n6',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX-appServerHorizontalPadding*2, y: appServerBaseY+appServerVerticalPadding}
        },
        {
            id: 'n7',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N7', text:'N7'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*2}
        },
        {
            id: 'n8',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N8', text:'N8'},
            position: {x: appServerBaseX-appServerHorizontalPadding*3, y: appServerBaseY+appServerVerticalPadding*2}
        },
        {
            id: 'n9',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N9', text:'N9'},
            position: {x: appServerBaseX-appServerHorizontalPadding*2, y: appServerBaseY+appServerVerticalPadding*2}
        },
        {
            id: 'n10',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX-appServerHorizontalPadding*1, y: appServerBaseY+appServerVerticalPadding*2}
        },
        {
            id: 'defender',
            type: 'defender',
            className: "nodrag",
            data: {label: 'defender', text:'Defender'},
            position: {x: gatewayBaseX, y: appServerBaseY+appServerVerticalPadding*3}
        },
    ]
};

/**
 * Gets the list of edges
 */
const getEdges = (edgeType = 'smoothstep') => {
    return [
        {id: 'e13', source: 'attacker', className: "nodrag", target: 'gateway', type: edgeType, animated: true},
        {id: 'e23', source: 'client', className: "nodrag", target: 'gateway', type: edgeType, animated: true},
        {id: 'e34', source: 'gateway', className: "nodrag", target: 'n1', type: edgeType, animated: true},
        {id: 'e35', source: 'gateway', className: "nodrag", target: 'n2', type: edgeType, animated: true},
        {id: 'e36', source: 'gateway', className: "nodrag", target: 'n3', type: edgeType, animated: true},
        {id: 'e37', source: 'gateway', className: "nodrag", target: 'n4', type: edgeType, animated: true},
        {id: 'e38', source: 'gateway', className: "nodrag", target: 'n5', type: edgeType, animated: true},
        {id: 'e39', source: 'n1', className: "nodrag", target: 'n6', type: edgeType, animated: true},
        {id: 'e310', source: 'n6', className: "nodrag", target: 'n7', type: edgeType, animated: true},
        {id: 'e311', source: 'n6', className: "nodrag", target: 'n8', type: edgeType, animated: true},
        {id: 'e312', source: 'n6', className: "nodrag", target: 'n9', type: edgeType, animated: true},
        {id: 'e313', source: 'n6', className: "nodrag", target: 'n10', type: edgeType, animated: true},
        {id: 'e10defender', source: 'n7', className: "nodrag", target: 'defender', type: edgeType, animated: true},
        {id: 'e11defender', source: 'n8', className: "nodrag", target: 'defender', type: edgeType, animated: true},
        {id: 'e12defender', source: 'n9', className: "nodrag", target: 'defender', type: edgeType, animated: true},
        {id: 'e13defender', source: 'n10', className: "nodrag", target: 'defender', type: edgeType, animated: true},
    ]
};
/**
 * Gets the list of elements (nodes and edges)
 */
const getElements = (xy) => {
    const nodes = getNodes(xy)
    const edges = getEdges()
    const elements = nodes.concat(edges)
    return elements
};

export default getElements;
