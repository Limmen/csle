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
            position: {x: gatewayBaseX + appServerHorizontalPadding*0.5, y: gatewayBaseY}
        },
        {
            id: 'ids',
            type: 'ids',
            className: "nodrag",
            data: {label: 'ids', text:'IDS'},
            position: {x: gatewayBaseX + appServerHorizontalPadding*1.8, y: gatewayBaseY - appServerVerticalPadding*0.25}
        },
        {
            id: 'n1',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N1', text:'N1'},
            position: {x: gatewayBaseX-4*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n2',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N2', text:'N2'},
            position: {x: appServerBaseX-3*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n3',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N3', text:'N3'},
            position: {x: appServerBaseX-2*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n4',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N4', text:'N4'},
            position: {x: appServerBaseX-1*appServerHorizontalPadding, y: appServerBaseY}
        },
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX, y: appServerBaseY}
        },
        //New
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
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
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX +appServerHorizontalPadding*3, y: appServerBaseY}
        },
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX +appServerHorizontalPadding*4, y: appServerBaseY}
        },
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX +appServerHorizontalPadding*5, y: appServerBaseY}
        },

        //NewEnd

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding}
        },

        {
            id: 'n6',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*1.7}
        },
        {
            id: 'n7',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N7', text:'N7'},
            position: {x: appServerBaseX-appServerHorizontalPadding*5.5, y: appServerBaseY+appServerVerticalPadding*2.7}
        },
        {
            id: 'n8',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N8', text:'N8'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*2.7}
        },
        {
            id: 'n9',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N9', text:'N9'},
            position: {x: appServerBaseX-appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*2.7}
        },
        {
            id: 'n10',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX-appServerHorizontalPadding*2.5, y: appServerBaseY+appServerVerticalPadding*2.7}
        },

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX-appServerHorizontalPadding*1, y: appServerBaseY+appServerVerticalPadding*1.15}
        },

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX+appServerHorizontalPadding*2, y: appServerBaseY+appServerVerticalPadding*1.15}
        },

        {
            id: 'n11',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.5, y: appServerBaseY+appServerVerticalPadding*1}
        },

        {
            id: 'n12',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.5, y: appServerBaseY+appServerVerticalPadding*2}
        },

        {
            id: 'n13',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*1}
        },

        {
            id: 'n13',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*1}
        },

        {
            id: 'n14',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*2}
        },

        {
            id: 'n15',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*2}
        },

        {
            id: 'n16',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*3}
        },

        {
            id: 'n16',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*3}
        },

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.45, y: appServerBaseY+appServerVerticalPadding*3.1}
        },

        {
            id: 'n17',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX-appServerHorizontalPadding*0, y: appServerBaseY+appServerVerticalPadding*3.95}
        },

        {
            id: 'n17',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*1, y: appServerBaseY+appServerVerticalPadding*3.95}
        },

        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*5}
        },

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*4.25}
        },

        {
            id: 'n71',
            type: 'switch',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3, y: appServerBaseY+appServerVerticalPadding*4.25}
        },

        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*1.5, y: appServerBaseY+appServerVerticalPadding*5}
        },
        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*2.5, y: appServerBaseY+appServerVerticalPadding*5}
        },
        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*5}
        },
        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*5}
        },

        {
            id: 'defender',
            type: 'defender',
            className: "nodrag",
            data: {label: 'defender', text:'Defender'},
            position: {x: gatewayBaseX, y: appServerBaseY+appServerVerticalPadding*6}
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
