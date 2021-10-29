import React, { useState, useCallback } from 'react';
import ReactFlow, {
    ReactFlowProvider,
    addEdge,
    removeElements,
    isNode,
} from 'react-flow-renderer';
import dagre from 'dagre';
import initialElements from './initial-elements';
import './Main.css';

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 172;
const nodeHeight = 36;

const getLayoutedElements = (elements, direction = 'TB') => {
    const isHorizontal = direction === 'LR';
    dagreGraph.setGraph({ rankdir: direction });

    elements.forEach((el) => {
        if (isNode(el)) {
            dagreGraph.setNode(el.id, { width: nodeWidth, height: nodeHeight });
        } else {
            dagreGraph.setEdge(el.source, el.target);
        }
    });

    dagre.layout(dagreGraph);

    return elements.map((el) => {
        if (isNode(el)) {
            const nodeWithPosition = dagreGraph.node(el.id);
            el.targetPosition = isHorizontal ? 'left' : 'top';
            el.sourcePosition = isHorizontal ? 'right' : 'bottom';

            // unfortunately we need this little hack to pass a slightly different position
            // to notify react flow about the change. Moreover we are shifting the dagre node position
            // (anchor=center center) to the top left so it matches the react flow node anchor point (top left).
            el.position = {
                x: nodeWithPosition.x - nodeWidth / 2 + Math.random() / 1000,
                y: nodeWithPosition.y - nodeHeight / 2,
            };
        }

        return el;
    });
};

const layoutedElements = getLayoutedElements(initialElements);


const Main = () => {
    // Declare a new state variable, which we'll call "count"
    const [count, setCount] = useState(0);
    const [envs, setEnvs] = useState([]);

    const [elements, setElements] = useState(layoutedElements);
    const onConnect = (params) =>
        setElements((els) =>
            addEdge({ ...params, type: 'smoothstep', animated: true }, els)
        );
    const onElementsRemove = (elementsToRemove) =>
        setElements((els) => removeElements(elementsToRemove, els));

    const onLayout = useCallback(
        (direction) => {
            const layoutedElements = getLayoutedElements(elements, direction);
            setElements(layoutedElements);
        },
        [elements]
    );

    return (
        <div className="Main">
            <h1>
                TODO
            </h1>
            <div className="layoutflow">
                <ReactFlowProvider>
                    <ReactFlow
                        style={{ height: 500 }}
                        elements={elements}
                        onConnect={onConnect}
                        onElementsRemove={onElementsRemove}
                        connectionLineType="smoothstep"
                    />
                    <div className="controls">
                        <button onClick={() => onLayout('TB')}>vertical layout</button>
                        <button onClick={() => onLayout('LR')}>horizontal layout</button>
                    </div>
                </ReactFlowProvider>
            </div>
        </div>
    );
}

Main.propTypes = {};

Main.defaultProps = {};

export default Main;
