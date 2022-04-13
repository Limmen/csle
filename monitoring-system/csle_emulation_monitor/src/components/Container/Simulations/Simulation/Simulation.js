import React from 'react';
import './Simulation.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Accordion from 'react-bootstrap/Accordion';
import TransitionProbabilities from "./TransitionProbabilities/TransitionProbabilities";
import ObservationFunction from "./ObservationFunction/ObservationFunction";
import RewardFunction from "./RewardFunction/RewardFunction";


const Simulation = (props) => {
    var A1Options = []
    for (let i = 0; i < props.simulation.joint_action_space_config.action_spaces[0].actions.length; i++) {
        A1Options.push({
            value: props.simulation.joint_action_space_config.action_spaces[0].actions[i],
            label: i.toString()
        })
    }
    var A2Options = []
    if (props.simulation.joint_action_space_config.action_spaces.length > 1) {
        for (let i = 0; i < props.simulation.joint_action_space_config.action_spaces[1].actions.length; i++) {
            A2Options.push({
                value: props.simulation.joint_action_space_config.action_spaces[1].actions[i],
                label: i.toString()
            })
        }
    }
    var sOptions = []
    for (let i = 0; i < props.simulation.state_space_config.states.length; i++) {
        sOptions.push({
            value: props.simulation.state_space_config.states[i],
            label: i.toString()
        })
    }
    var lOptions = []
    for (let i = 0; i < props.simulation.env_parameters_config.parameters.length; i++) {
        lOptions.push({
            value: props.simulation.env_parameters_config.parameters[i],
            label: i.toString()
        })
    }

    const minState = 0
    const maxState = props.simulation.state_space_config.states.length - 1

    const getTimeStr = (time_id) => {
        if (time_id === 0) {
            return "Discrete"
        } else {
            return "Continuous"
        }
    }

    const player_ids = props.simulation.players_config.player_configs.map((player, index) => (player.id))
    const filtered_action_spaces = props.simulation.joint_action_space_config.action_spaces.filter(action_space => (player_ids.includes(action_space.player_id)))

    return (<Card key={props.simulation.name} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.simulation.name} className="mgHeader">
                <span className="subnetTitle">ID: {props.simulation.id}, name: {props.simulation.name}</span>
                # players: {player_ids.length}
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.simulation.name}>
            <Card.Body>
                <h5 className="semiTitle">
                    General Information about the simulation:
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Attribute</th>
                        <th> Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>Description</td>
                        <td>{props.simulation.descr}</td>
                    </tr>
                    <tr>
                        <td>Number of players</td>
                        <td>{props.simulation.players_config.player_configs.length}</td>
                    </tr>
                    <tr>
                        <td>OpenAI gym environment name</td>
                        <td>{props.simulation.gym_env_name}</td>
                    </tr>
                    <tr>
                        <td>Time</td>
                        <td>{getTimeStr(props.simulation.time_step_type)}</td>
                    </tr>
                    <tr>
                        <td>Version</td>
                        <td>{props.simulation.version}</td>
                    </tr>
                    <tr>
                        <td>Configuration</td>
                        <td>
                            <Button variant="link"
                                    onClick={() => fileDownload(JSON.stringify(props.simulation), "config.json")}>
                                config.json
                            </Button>
                        </td>
                    </tr>
                    </tbody>
                </Table>

                <img src={`data:image/jpeg;base64,${props.simulation.image}`} className="simulationImg"
                     alt="Image of the simulation"/>

                <h5 className="semiTitle">
                    Players
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Player ID</th>
                        <th>Player name</th>
                        <th>Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.simulation.players_config.player_configs.map((player, index) =>
                        <tr key={player.id + "-" + index}>
                            <td>{player.id}</td>
                            <td>{player.name}</td>
                            <td>{player.descr}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>

                <h5 className="semiTitle">
                    State space
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>State ID</th>
                        <th>State name</th>
                        <th>Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.simulation.state_space_config.states.map((state, index) =>
                        <tr key={state.id + "-" + index}>
                            <td>{state.id}</td>
                            <td>{state.name}</td>
                            <td>{state.descr}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>
                {filtered_action_spaces.map((action_space, index1) =>
                    <div key={action_space.player_id + "-" + index1}>
                        <h5 className="semiTitle">
                            Action space for player {action_space.player_id}
                        </h5>
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Action ID</th>
                                <th>Description</th>
                            </tr>
                            </thead>
                            <tbody>
                            {action_space.actions.map((action, index2) =>
                                <tr key={action.id + "-" + index2}>
                                    <td>{action.id}</td>
                                    <td>{action.descr}</td>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                )}
                <h5 className="semiTitle">
                    Initial state distribution
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>State ID</th>
                        <th>Probability</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.simulation.initial_state_distribution_config.initial_state_distribution.map((prob, index) =>
                        <tr key={prob + "-" + index}>
                            <td>{index}</td>
                            <td>{prob}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>

                <h5 className="semiTitle">
                    Other environment parameters
                </h5>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.simulation.env_parameters_config.parameters.map((param, index) =>
                        <tr key={param.id + "-" + index}>
                            <td>{param.id}</td>
                            <td>{param.name}</td>
                            <td>{param.descr}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>

                {props.simulation.joint_observation_space_config.observation_spaces.map((observation_space, index1) =>
                    <div key={observation_space.player_id + "-" + index1}>
                        <h5 className="semiTitle">
                            Observation space for player {observation_space.player_id}
                        </h5>
                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Attribute</th>
                                <th>Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Num observations</td>
                                <td>{observation_space.observations.length}</td>
                            </tr>
                            <tr>
                                <td>Description</td>
                                <td>{observation_space.descr}</td>
                            </tr>
                            </tbody>
                        </Table>

                        <Table striped bordered hover>
                            <thead>
                            <tr>
                                <th>Observation ID</th>
                                <th>Name</th>
                            </tr>
                            </thead>
                            <tbody>
                            {Object.keys(observation_space.observation_component_name_to_index).map((obs_name, index) =>
                                <tr key={obs_name + "-" + index}>
                                    <td>{observation_space.observation_component_name_to_index[obs_name]}</td>
                                    <td>{obs_name}</td>
                                </tr>
                            )}
                            </tbody>
                        </Table>
                    </div>
                )}

                <TransitionProbabilities simulation={props.simulation} A1Options={A1Options} lOptions={lOptions}
                                         A2Options={A2Options} sOptions={sOptions} minState={minState}/>
                <ObservationFunction simulation={props.simulation} A1Options={A1Options}
                                     A2Options={A2Options} sOptions={sOptions} minState={minState}/>
                <RewardFunction simulation={props.simulation}
                                A1Options={A1Options} A2Options={A2Options} lOptions={lOptions} minState={minState}
                                maxState={maxState} />
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Simulation.propTypes = {};
Simulation.defaultProps = {};
export default Simulation;
