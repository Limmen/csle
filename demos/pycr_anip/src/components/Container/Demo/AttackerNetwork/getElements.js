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
            position: {x: attackerBaseX, y: attackerBaseY},
            isHidden : false
        },
        {
            id: 'client',
            type: 'client',
            className: "nodrag",
            data: {label: 'client1', text:'Client population'},
            position: {x: clientBaseX, y: clientBaseY},
            isHidden : false
        },
        {
            id: 'gateway',
            type: 'gateway',
            className: "nodrag",
            data: {label: 'gateway_n1', text:'Gateway'},
            position: {x: gatewayBaseX + appServerHorizontalPadding*0.5, y: gatewayBaseY},
            isHidden : false
        },
        {
            id: 'ids',
            type: 'ids',
            className: "nodrag",
            data: {label: 'ids', text:'IDS'},
            position: {x: gatewayBaseX + appServerHorizontalPadding*1.8, y: gatewayBaseY - appServerVerticalPadding*0.06},
            isHidden : false
        },
        {
            id: 'n2',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N2', text:'N2'},
            position: {x: gatewayBaseX-4*appServerHorizontalPadding, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n3',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N3', text:'N3'},
            position: {x: appServerBaseX-3*appServerHorizontalPadding, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n4',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N4', text:'N4'},
            position: {x: appServerBaseX-2*appServerHorizontalPadding, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n5',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N5', text:'N5'},
            position: {x: appServerBaseX-1*appServerHorizontalPadding, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n6',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N6', text:'N6'},
            position: {x: appServerBaseX, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n7',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N7', text:'N7'},
            position: {x: appServerBaseX +appServerHorizontalPadding*1, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n8',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N8', text:'N8'},
            position: {x: appServerBaseX +appServerHorizontalPadding*2, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n9',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N9', text:'N9'},
            position: {x: appServerBaseX +appServerHorizontalPadding*3, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n9_compromised',
            type: 'applicationServerCompromised',
            className: "nodrag",
            data: {label: 'N9', text:'N9'},
            position: {x: appServerBaseX +appServerHorizontalPadding*3, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n10',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N10', text:'N10'},
            position: {x: appServerBaseX +appServerHorizontalPadding*4, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'n11',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N11', text:'N11'},
            position: {x: appServerBaseX +appServerHorizontalPadding*5, y: appServerBaseY},
            isHidden : false
        },
        {
            id: 'switch1',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch1', text:'switch1'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding},
            isHidden : false
        },
        {
            id: 'n12',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N12', text:'N12'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*1.7},
            isHidden : false
        },
        {
            id: 'n13',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N13', text:'N13'},
            position: {x: appServerBaseX-appServerHorizontalPadding*5.5, y: appServerBaseY+appServerVerticalPadding*2.7},
            isHidden : false
        },
        {
            id: 'n14',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N14', text:'N14'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*2.7},
            isHidden : false
        },
        {
            id: 'n15',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N15', text:'N15'},
            position: {x: appServerBaseX-appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*2.7},
            isHidden : false
        },
        {
            id: 'n16',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N16', text:'N16'},
            position: {x: appServerBaseX-appServerHorizontalPadding*2.5, y: appServerBaseY+appServerVerticalPadding*2.7},
            isHidden : false
        },
        {
            id: 'switch2',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch2', text:'switch2'},
            position: {x: appServerBaseX-appServerHorizontalPadding*1, y: appServerBaseY+appServerVerticalPadding*1.15},
            isHidden : false
        },

        {
            id: 'switch3',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch3', text:'switch3'},
            position: {x: appServerBaseX+appServerHorizontalPadding*2, y: appServerBaseY+appServerVerticalPadding*1.15},
            isHidden : false
        },
        {
            id: 'n17',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N17', text:'N17'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.5, y: appServerBaseY+appServerVerticalPadding*1},
            isHidden : false
        },

        {
            id: 'n18',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N18', text:'N18'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.5, y: appServerBaseY+appServerVerticalPadding*2},
            isHidden : false
        },


        {
            id: 'n19',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N19', text:'N19'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*1},
            isHidden : false
        },
        {
            id: 'n20',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N20', text:'N20'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*1},
            isHidden : false
        },

        {
            id: 'n21',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N21', text:'N21'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*2},
            isHidden : false
        },
        {
            id: 'n22',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N22', text:'N22'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*2},
            isHidden : false
        },

        {
            id: 'n23',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N23', text:'N23'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*3},
            isHidden : false
        },

        {
            id: 'n24',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N24', text:'N24'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*3},
            isHidden : false
        },
        {
            id: 'switch4',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch4', text:'switch4'},
            position: {x: appServerBaseX+appServerHorizontalPadding*0.45, y: appServerBaseY+appServerVerticalPadding*3.1},
            isHidden : false
        },

        {
            id: 'n25',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N25', text:'N25'},
            position: {x: appServerBaseX-appServerHorizontalPadding*0, y: appServerBaseY+appServerVerticalPadding*3.95},
            isHidden : false
        },
        {
            id: 'n26',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N26', text:'N26'},
            position: {x: appServerBaseX+appServerHorizontalPadding*1, y: appServerBaseY+appServerVerticalPadding*3.95},
            isHidden : false
        },
        {
            id: 'n27',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N27', text:'N27'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*5},
            isHidden : false
        },

        {
            id: 'switch5',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch5', text:'switch5'},
            position: {x: appServerBaseX-appServerHorizontalPadding*4, y: appServerBaseY+appServerVerticalPadding*4.25},
            isHidden : false
        },

        {
            id: 'switch6',
            type: 'switch',
            className: "nodrag",
            data: {label: 'switch6', text:'switch6'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3, y: appServerBaseY+appServerVerticalPadding*4.25},
            isHidden : false
        },

        {
            id: 'n28',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N28', text:'N28'},
            position: {x: appServerBaseX+appServerHorizontalPadding*1.5, y: appServerBaseY+appServerVerticalPadding*5},
            isHidden : false
        },
        {
            id: 'n29',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N29', text:'N29'},
            position: {x: appServerBaseX+appServerHorizontalPadding*2.5, y: appServerBaseY+appServerVerticalPadding*5},
            isHidden : false
        },
        {
            id: 'n30',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N30', text:'N30'},
            position: {x: appServerBaseX+appServerHorizontalPadding*3.5, y: appServerBaseY+appServerVerticalPadding*5},
            isHidden : false
        },
        {
            id: 'n31',
            type: 'applicationServer',
            className: "nodrag",
            data: {label: 'N31', text:'N31'},
            position: {x: appServerBaseX+appServerHorizontalPadding*4.5, y: appServerBaseY+appServerVerticalPadding*5},
            isHidden : false
        },
        {
            id: 'defender',
            type: 'defender',
            className: "nodrag",
            data: {label: 'defender', text:'Defender'},
            position: {x: gatewayBaseX, y: appServerBaseY+appServerVerticalPadding*6},
            isHidden : false
        },
    ]
};

/**
 * Gets the list of edges
 */
const getEdges = (edgeType = 'smoothstep') => {
    return [

        //Defender and Attacker to Gateway
        {id: 'e_attacker_gateway', source: 'attacker', className: "nodrag", target: 'gateway', type: edgeType, animated: true, isHidden: false},
        {id: 'e_client_gateway', source: 'client', className: "nodrag", target: 'gateway', type: edgeType, animated: true, isHidden: false},

        //Gateway to first layer
        {id: 'e_gateway_n2', source: 'gateway', className: "nodrag", target: 'n2', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n3', source: 'gateway', className: "nodrag", target: 'n3', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n4', source: 'gateway', className: "nodrag", target: 'n4', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n5', source: 'gateway', className: "nodrag", target: 'n5', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n6', source: 'gateway', className: "nodrag", target: 'n6', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n7', source: 'gateway', className: "nodrag", target: 'n7', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n8', source: 'gateway', className: "nodrag", target: 'n8', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n9', source: 'gateway', className: "nodrag", target: 'n9', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n10', source: 'gateway', className: "nodrag", target: 'n10', type: edgeType, animated: true, isHidden: false},
        {id: 'e_gateway_n11', source: 'gateway', className: "nodrag", target: 'n11', type: edgeType, animated: true, isHidden: false},

        //Gateway to IDS
        {id: 'e_gateway_ids', source: 'gateway', className: "nodrag", target: 'ids', type: edgeType, animated: true, isHidden: false},

        //N1 to switch
        {id: 'e_n1_switch1', source: 'n2', className: "nodrag", target: 'switch1', type: edgeType, animated: true, isHidden: false},

        //switch1 to N12
        {id: 'e_switch1_n12', source: 'switch1', className: "nodrag", target: 'n12', type: edgeType, animated: true, isHidden: false},

        //N12 to N13-16
        {id: 'e_n12_n13', source: 'n12', className: "nodrag", target: 'n13', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n12_n14', source: 'n12', className: "nodrag", target: 'n14', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n12_n15', source: 'n12', className: "nodrag", target: 'n15', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n12_n16', source: 'n12', className: "nodrag", target: 'n16', type: edgeType, animated: true, isHidden: false},

        //N4 to switch2
        {id: 'e_n14_switch2', source: 'n4', className: "nodrag", target: 'switch2', type: edgeType, animated: true, isHidden: false},

        //switch2 to n17
        {id: 'e_switch2_n17', source: 'switch2', className: "nodrag", target: 'n17', type: edgeType, animated: true, isHidden: false},

        //n17 to n18
        {id: 'e_n17_n18', source: 'n17', className: "nodrag", target: 'n18', type: edgeType, animated: true, isHidden: false},

        //n17 to switch3
        {id: 'e_n17_switch3', source: 'n17', className: "nodrag", target: 'switch3', type: edgeType, animated: true, isHidden: false},

        //switch3 to n19-24
        {id: 'e_switch3_n19', source: 'switch3', className: "nodrag", target: 'n19', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch3_n20', source: 'switch3', className: "nodrag", target: 'n20', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch3_n21', source: 'switch3', className: "nodrag", target: 'n21', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch3_n22', source: 'switch3', className: "nodrag", target: 'n22', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch3_n23', source: 'switch3', className: "nodrag", target: 'n23', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch3_n24', source: 'switch3', className: "nodrag", target: 'n24', type: edgeType, animated: true, isHidden: false},

        //n18 to switch4
        {id: 'e_n18_switch4', source: 'n18', className: "nodrag", target: 'switch4', type: edgeType, animated: true, isHidden: false},

        //switch4 to n25-26
        {id: 'e_switch4_n25', source: 'switch4', className: "nodrag", target: 'n25', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch4_n26', source: 'switch4', className: "nodrag", target: 'n26', type: edgeType, animated: true, isHidden: false},

        //n26 to switch6
        {id: 'e_n26_switch6', source: 'n26', className: "nodrag", target: 'switch6', type: edgeType, animated: true, isHidden: false},

        //n25 to switch5
        {id: 'e_n25_switch5', source: 'n25', className: "nodrag", target: 'switch5', type: edgeType, animated: true, isHidden: false},

        //switch5 to n27
        {id: 'e_switch5_n27', source: 'switch5', className: "nodrag", target: 'n27', type: edgeType, animated: true, isHidden: false},

        //switch6 to n28-31
        {id: 'e_switch6_n28', source: 'switch6', className: "nodrag", target: 'n28', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch6_n29', source: 'switch6', className: "nodrag", target: 'n29', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch6_n30', source: 'switch6', className: "nodrag", target: 'n30', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch6_n31', source: 'switch6', className: "nodrag", target: 'n31', type: edgeType, animated: true, isHidden: false},

        //n28-31, n7, switch5, n25, n26 to defender
        {id: 'e_n31_defender', source: 'n31', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n30_defender', source: 'n30', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n29_defender', source: 'n29', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n28_defender', source: 'n28', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n27_defender', source: 'n27', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n26_defender', source: 'n26', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_n25_defender', source: 'n25', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},
        {id: 'e_switch5_defender', source: 'switch5', className: "nodrag", target: 'defender', type: edgeType, animated: true, isHidden: false},


    ]
};

/**
 * Gets the list of elements (nodes and edges)
 */
const getElements = (xy, traces, activeTrace, t) => {
    const nodes = getNodes(xy)
    const edges = getEdges()
    const elements = nodes.concat(edges)
    return elements
};

export default getElements;
