import React, { useState , useEffect, createRef }  from 'react';
import './Main.css';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'


const Main = () => {
    const [envs, setEnvs] = useState([]);
    const [stopped_envs, setStoppedEnvs] = useState([]);
    const ip = "localhost"
    // const ip = "172.31.212.92"


    useEffect(() => {
        fetch(
            `http://` + ip + ':7777/envs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setEnvs(response);
            })
            .catch(error => console.log("error:"+ error));
    }, []);


    useEffect(() => {
        fetch(
            `http://` + ip + ':7777/stopped_envs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setStoppedEnvs(response);
            })
            .catch(error => console.log("error:"+ error));
    }, []);


    const getSubnetMasks = (env) => {
        let networks = env.containers_config.networks
        const subnets = []
        for (let i = 0; i < networks.length; i++) {
            subnets.push(networks[i].subnet_mask)
        }
        return subnets.join(", ")
    }

    const getNetworkNames = (env) => {
        let networks = env.containers_config.networks
        const network_names = []
        for (let i = 0; i < networks.length; i++) {
            network_names.push(networks[i].name)
        }
        return network_names.join(", ")
    }

    const getContainers = (env) => {
        const containers = []
        let cs = env.containers_config.containers
        for (let i = 0; i < cs.length; i++) {
            const ips = []
            for (let j = 0; j < cs[i].ips_and_networks.length; j++) {
                ips.push(cs[i].ips_and_networks[j]["py/tuple"][0])
            }
            containers.push({
                name: cs[i].name + "-level" + cs[i].level + cs[i].suffix,
                ips: ips.join(", ")
            })
        }
        return containers
    }

    const wrapper = createRef();

    return (
        <div className="Main">
            <h1>
                Active emulation environments
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg" version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg>
            </h1>
            <Accordion defaultActiveKey="0">
                {envs.map((env, index) =>
                    <Card key={env.name} ref={wrapper}>
                        <Card.Header>
                            <Accordion.Toggle as={Button} variant="link" eventKey={env.name} className="mgHeader">
                                <span className="subnetTitle">Name: {env.name}</span>, Minigame: {env.minigame}, # Containers: {env.num_containers}
                            </Accordion.Toggle>
                        </Card.Header>
                        <Accordion.Collapse eventKey={env.name}>
                            <Card.Body>
                                <h5 className="semiTitle">
                                    General Information about the Environment:
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
                                        <td>Emulation name</td>
                                        <td>{env.name}</td>
                                    </tr>
                                    <tr>
                                        <td>Subnets</td>
                                        <td>{getSubnetMasks(env.config)}</td>
                                    </tr>
                                    <tr>
                                        <td>Minigame</td>
                                        <td>{env.minigame}</td>
                                    </tr>
                                    <tr>
                                        <td>Network names</td>
                                        <td>{getNetworkNames(env.config)}</td>
                                    </tr>
                                    <tr>
                                        <td># Containers</td>
                                        <td>{env.num_containers}</td>
                                    </tr>
                                    <tr>
                                        <td>Emulation config</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.config), "config.json")}>
                                                config.json
                                            </Button>
                                        </td>
                                    </tr>

                                    </tbody>
                                </Table>

                                <h5 className="semiTitle">
                                    Containers:
                                </h5>
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Container name</th>
                                        <th>Ip</th>
                                        <th>Docker image name</th>
                                        <th>Id</th>
                                        <th>Hostname</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {env.containers.map((container, index) =>
                                    <tr key={container.id}>
                                        <td>{container.name}</td>
                                        <td>{container.ip}</td>
                                        <td>{container.image_name}</td>
                                        <td>{container.id}</td>
                                        <td>{container.name2}</td>
                                    </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>)
                }
            </Accordion>
            <h1 className="nonActiveTitle">
                Non-active emulation environments
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg" version="1.1">
                    <circle r="15" cx="15" cy="15" fill="red"></circle>
                </svg>
            </h1>
            <Accordion defaultActiveKey="0">
                {stopped_envs.map((env, index) =>
                    <Card key={env.name} ref={wrapper}>
                        <Card.Header>
                            <Accordion.Toggle as={Button} variant="link" eventKey={env.name} className="mgHeader">
                                <span className="subnetTitle">Name: {env.name}</span>
                                , Minigame: {env.containers_config.containers[0].minigame}, # Containers: {env.containers_config.containers.length}
                            </Accordion.Toggle>
                        </Card.Header>
                        <Accordion.Collapse eventKey={env.name}>
                            <Card.Body>
                                <h5 className="semiTitle">
                                    General Information about the Environment:
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
                                        <td>Emulation name</td>
                                        <td>{env.name}</td>
                                    </tr>
                                    <tr>
                                        <td>Subnets</td>
                                        <td>{getSubnetMasks(env)}</td>
                                    </tr>
                                    <tr>
                                        <td>Minigame</td>
                                        <td>{env.containers_config.containers[0].minigame}</td>
                                    </tr>
                                    <tr>
                                        <td>Network names</td>
                                        <td>{getNetworkNames(env)}</td>
                                    </tr>
                                    <tr>
                                        <td># Containers</td>
                                        <td>{env.containers_config.containers.length}</td>
                                    </tr>
                                    <tr>
                                        <td>Emulation config</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env), "config.json")}>
                                                config.json
                                            </Button>
                                        </td>
                                    </tr>
                                    </tbody>
                                </Table>
                                <h5 className="semiTitle">
                                    Containers:
                                </h5>
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Container name</th>
                                        <th>Ips</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {getContainers(env).map((container, index) =>
                                        <tr key={"csle-" + env.containers_config.containers[0].minigame + "-" + container.name}>
                                            <td>{"csle-" + env.containers_config.containers[0].minigame + "-" + container.name}</td>
                                            <td>{container.ips}</td>
                                        </tr>
                                    )}
                                    </tbody>
                                </Table>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>)
                }
            </Accordion>
        </div>
    );
}

Main.propTypes = {};

Main.defaultProps = {};

export default Main;
