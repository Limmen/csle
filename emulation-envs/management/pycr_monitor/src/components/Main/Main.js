import React, { useState , useEffect, createRef }  from 'react';
import './Main.css';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import localIpUrl from 'local-ip-url'

const Main = () => {
    // Declare a new state variable, which we'll call "count"
    const [count, setCount] = useState(0);
    const [envs, setEnvs] = useState([]);
    const ip = localIpUrl('public', 'ipv4')


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
            .catch(error => console.log(error));
    }, []);

    const wrapper = createRef();

    return (
        <div className="Main">
            <h1>
                Active Environments
                <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg" version="1.1">
                    <circle r="15" cx="15" cy="15" fill="green"></circle>
                </svg>
            </h1>
            <Accordion defaultActiveKey="0">
                {envs.map((env, index) =>
                    <Card key={env.id} ref={wrapper}>
                        <Card.Header>
                            <Accordion.Toggle as={Button} variant="link" eventKey={env.id} className="mgHeader">
                                <span className="subnetTitle">Subnet: {env.subnet_mask}</span>, Minigame: {env.minigame}, # Containers: {env.num_containers}
                            </Accordion.Toggle>
                        </Card.Header>
                        <Accordion.Collapse eventKey={env.id}>
                            <Card.Body>
                                <p className="semiTitle">
                                    General Information about the Environment:
                                </p>
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Attribute</th>
                                        <th> Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td>Subnet mask</td>
                                        <td>{env.subnet_mask}</td>
                                    </tr>
                                    <tr>
                                        <td>Minigame</td>
                                        <td>{env.minigame}</td>
                                    </tr>
                                    <tr>
                                        <td>Network name</td>
                                        <td>{env.name}</td>
                                    </tr>
                                    <tr>
                                        <td>id</td>
                                        <td>{env.id}</td>
                                    </tr>
                                    <tr>
                                        <td># Containers</td>
                                        <td>{env.num_containers}</td>
                                    </tr>

                                    <tr>
                                        <td>Containers configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.containers_config), "containers.json")}>
                                                containers.json
                                            </Button>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>Users configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.users_config), "users.json")}>
                                                users.json
                                            </Button>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>Flags configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.flags_config), "flags.json")}>
                                                flags.json
                                            </Button>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>Vulnerabilities configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.vulnerabilities_config), "vulnerabilities.json")}>
                                                vulnerabilities.json
                                            </Button>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>Topology configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.topology_config), "topology.json")}>
                                                topology.json
                                            </Button>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td> Traffic configuration file</td>
                                        <td>
                                            <Button variant="link" onClick={() => fileDownload(JSON.stringify(env.traffic_config), "traffic.json")}>
                                                traffic.json
                                            </Button>
                                        </td>
                                    </tr>

                                    </tbody>
                                </Table>

                                <p className="semiTitle">
                                    Containers:
                                </p>
                                <Table striped bordered hover className="table2">
                                    <thead>
                                    <tr>
                                        <th>Container</th>
                                        <th>Ip</th>
                                        <th>Image name</th>
                                        <th>Id</th>
                                        <th>Internal name</th>
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
        </div>
    );
}

Main.propTypes = {};

Main.defaultProps = {};

export default Main;
