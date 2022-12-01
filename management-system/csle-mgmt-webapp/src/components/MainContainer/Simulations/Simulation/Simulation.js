import React, {useState} from 'react';
import './Simulation.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Accordion from 'react-bootstrap/Accordion';
import TransitionProbabilities from "./TransitionProbabilities/TransitionProbabilities";
import ObservationFunction from "./ObservationFunction/ObservationFunction";
import RewardFunction from "./RewardFunction/RewardFunction";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'

/**
 * Component representing the /simulations/<id> resource
 */
const Simulation = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [playersOpen, setPlayersOpen] = useState(false);
    const [stateSpaceOpen, setStateSpaceOpen] = useState(false);
    const [actionSpacesOpen, setActionSpacesOpen] = useState(false);
    const [initialStateDistributionOpen, setInitialStateDistributionOpen] = useState(false);
    const [otherEnvParametersOpen, setOtherEnvParametersOpen] = useState(false);
    const [observationSpacesOpen, setObservationSpacesOpen] = useState(false);
    const [transitionProbabilitiesOpen, setTransitionProbabilitiesOpen] = useState(false);
    const [observationFunctionOpen, setObservationFunctionOpen] = useState(false);
    const [rewardFunctionOpen, setRewardFunctionOpen] = useState(false);

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

    const renderRemoveSimulationTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove simulation
        </Tooltip>
    );

    const SimulationImageOrEmpty = (props) => {
        if (props.simulation.image === null || props.simulation.image === undefined) {
            return (<></>)
        } else {
            return (
                <img src={`data:image/jpeg;base64,${props.simulation.image}`}
                     className="simulationImg img-fluid"
                     alt="Simulation"/>
            )
        }
    }

    const ActionsOrEmpty = (props) => {
        if(props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <h5 className="semiTitle">
                    Actions:
                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveSimulationTooltip}
                    >
                        <Button variant="danger" className="removeButton" size="sm"
                                onClick={() => props.removeSimulation(props.simulation)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>
            )
        } else {
            return (<></>)
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
                <ActionsOrEmpty removeSimulation={props.removeSimulation} sessionData={props.sessionData}/>
                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> General information about the simulation
                                <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
                            <div className="table-responsive">
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
                                            <Button variant="link" className="linkDownload"
                                                    onClick={() => fileDownload(JSON.stringify(props.simulation), "config.json")}>
                                                config.json
                                            </Button>
                                        </td>
                                    </tr>
                                    </tbody>
                                </Table>
                            </div>
                            <SimulationImageOrEmpty simulation={props.simulation}/>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setPlayersOpen(!playersOpen)}
                            aria-controls="playersBody"
                            aria-expanded={playersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Players
                                <i className="fa fa-users headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={playersOpen}>
                        <div id="playersBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setStateSpaceOpen(!stateSpaceOpen)}
                            aria-controls="stateSpaceBody"
                            aria-expanded={stateSpaceOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> State space
                                <i className="fa fa-table headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={stateSpaceOpen}>
                        <div id="stateSpaceBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setActionSpacesOpen(!actionSpacesOpen)}
                            aria-controls="actionSpacesBody"
                            aria-expanded={actionSpacesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Action spaces
                                <i className="fa fa-cogs headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={actionSpacesOpen}>
                        <div id="actionSpacesBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setInitialStateDistributionOpen(!initialStateDistributionOpen)}
                            aria-controls="initialStateDistributionBody"
                            aria-expanded={initialStateDistributionOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Initial state distribution
                                <i className="fa fa-area-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={initialStateDistributionOpen}>
                        <div id="initialStateDistributionBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setOtherEnvParametersOpen(!otherEnvParametersOpen)}
                            aria-controls="otherEnvParametersBody"
                            aria-expanded={otherEnvParametersOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Other environment parameters
                                <i className="fa fa-list headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={otherEnvParametersOpen}>
                        <div id="otherEnvParametersBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setObservationSpacesOpen(!observationSpacesOpen)}
                            aria-controls="observationSpacesBody"
                            aria-expanded={observationSpacesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Observation spaces
                                <i className="fa fa-list-ul headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={observationSpacesOpen}>
                        <div id="observationSpacesBody" className="cardBodyHidden">
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
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setTransitionProbabilitiesOpen(!transitionProbabilitiesOpen)}
                            aria-controls="transitionProbabilitiesBody"
                            aria-expanded={transitionProbabilitiesOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Transition probabilities
                                <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={transitionProbabilitiesOpen}>
                        <div id="transitionProbabilitiesBody" className="cardBodyHidden">
                            <TransitionProbabilities simulation={props.simulation} A1Options={A1Options}
                                                     lOptions={lOptions}
                                                     A2Options={A2Options} sOptions={sOptions} minState={minState}/>
                        </div>
                    </Collapse>
                </Card>


                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setObservationFunctionOpen(!observationFunctionOpen)}
                            aria-controls="observationFunctionBody"
                            aria-expanded={observationFunctionOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Observation function
                                <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={observationFunctionOpen}>
                        <div id="observationFunctionBody" className="cardBodyHidden">
                            <ObservationFunction simulation={props.simulation} A1Options={A1Options}
                                                 A2Options={A2Options} sOptions={sOptions} minState={minState}/>
                        </div>
                    </Collapse>
                </Card>

                <Card className="subCard">
                    <Card.Header>
                        <Button
                            onClick={() => setRewardFunctionOpen(!rewardFunctionOpen)}
                            aria-controls="rewardFunctionBody"
                            aria-expanded={rewardFunctionOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Reward function

                                <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                            </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={rewardFunctionOpen}>
                        <div id="rewardFunctionBody" className="cardBodyHidden">
                            <RewardFunction simulation={props.simulation}
                                            A1Options={A1Options} A2Options={A2Options} lOptions={lOptions}
                                            minState={minState}
                                            maxState={maxState}/>
                        </div>
                    </Collapse>
                </Card>
            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

Simulation.propTypes = {};
Simulation.defaultProps = {};
export default Simulation;
