import React, {useState, useCallback} from 'react';
import {useAlert} from "react-alert";
import './Login.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import ChangeUserDataForm from "./ChangeUserDataForm/ChangeUserDataForm";
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    HTTP_PREFIX,
    HTTP_REST_POST,
    LOGIN_RESOURCE
} from "../../Common/constants";

/**
 * The component representing the /login-page
 */
const Login = (props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showEditModal, setShowEditModal] = useState(false);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const setSessionData = props.setSessionData

    const loginUser = useCallback((credentials) => {
        fetch(
           `${HTTP_PREFIX}${ip}:${port}/${LOGIN_RESOURCE}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify(credentials)
            }
        )
            .then(res => {
                if (!res.ok) {
                    alert.show("Login failed. Wrong username and password combination.")
                    return null
                } else {
                    return res.json()
                }
            })
            .then(response => {
                if (response !== null) {
                    setSessionData(response)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, ip, port, setSessionData]);

    const loginFormSubmit = async (event) => {
        event.preventDefault()
        const credentials = {
            "username": username,
            "password": password
        }
        if (username === "" || password === "") {
            alert.show("Username or password cannot be empty")
        } else {
            loginUser(credentials)
        }
    }

    const logout = () => {
        setSessionData(null)
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    const handlePwChange = (event) => {
        setPassword(event.target.value)
    }

    const renderEditTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Change user account details
        </Tooltip>
    );

    const renderLogoutTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Logout
        </Tooltip>
    );

    const edit = () => {
        setShowEditModal(true)
    }

    const EditModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Update user account
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="row">
                        <ChangeUserDataForm sessionData={props.sessionData} setSessionData={props.setSessionData} />
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    if (!props.sessionData) {
        return (<div className="Login Auth-form-container">
            <form className="Auth-form" onSubmit={loginFormSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Sign In</h3>
                    <div className="form-group mt-3">
                        <label>Username</label>
                        <input
                            type="username"
                            className="form-control mt-1"
                            placeholder="Enter username"
                            value={username}
                            onChange={handleUsernameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control mt-1"
                            placeholder="Enter password"
                            value={password}
                            onChange={handlePwChange}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Submit
                        </button>
                    </div>
                </div>
            </form>
        </div>)
    } else {
        return (
            <div>
                <h3 className="loggedInTitle"> Logged in.
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderLogoutTooltip}
                    >
                        <Button variant="danger" onClick={logout} size="sm" className="logoutButton">
                            Logout
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderEditTooltip}
                    >
                        <Button variant="button" onClick={edit}>
                            <i className="fa fa-edit editButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <EditModal show={showEditModal} onHide={() => setShowEditModal(false)}
                               sessionData={props.sessionData} setSessionData={props.setSessionData}
                    />
                </h3>
            </div>
        )
    }
}

Login.propTypes = {};
Login.defaultProps = {};
export default Login;
