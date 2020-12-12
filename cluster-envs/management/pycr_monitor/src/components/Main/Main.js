import React, { useState , useEffect }  from 'react';
import PropTypes from 'prop-types';
import './Main.css';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'

const Main = () => {
    // Declare a new state variable, which we'll call "count"
    const [count, setCount] = useState(0);
    const [envs, setEnvs] = useState([]);


    useEffect(() => {
        fetch(
            `http://localhost:7777/environments`,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                console.log("response" + response)
                setEnvs(response.test);
            })
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="Main">
            <Accordion defaultActiveKey="0">
                <Card>
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="0">
                            Click me!
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="0">
                        <Card.Body>Hello! I'm the body</Card.Body>
                    </Accordion.Collapse>
                </Card>
                <Card>
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="1">
                            Click me!
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="1">
                        <Card.Body>
                            Hello! I'm another body
                            <p onClick={() => setCount(count + 1)}>
                                Click me
                            </p>
                            <p>You clicked {count} times</p>
                            <p>
                                Test: {envs}
                            </p>
                        </Card.Body>
                    </Accordion.Collapse>
                </Card>
            </Accordion>
        </div>
    );
}

Main.propTypes = {};

Main.defaultProps = {};

export default Main;
