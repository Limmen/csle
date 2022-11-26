import React, {useState, useCallback} from 'react';
import { useAlert } from "react-alert";
import { useNavigate } from "react-router-dom";
import './Register.css';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    HTTP_PREFIX,
    LOGIN_PAGE_RESOURCE,
    USERS_RESOURCE,
    CREATE_SUBRESOURCE,
    HTTP_REST_POST
} from "../../Common/constants";

/**
 * The component representing the /register-page
 */
const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [organization, setOrganization] = useState("");
    const [email, setEmail] = useState("");
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();

    const createUser = useCallback((userConfiguration) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${USERS_RESOURCE}/${CREATE_SUBRESOURCE}`,
            {
                method: HTTP_REST_POST,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify(userConfiguration)
            }
        )
            .then(res => {
                if(res.status === 400 || res.status === 409) {
                    if(res.status === 400) {
                        alert.show("Registration failed. Username or password cannot be empty")
                    } else {
                        alert.show("A user with that username already exists")
                    }
                    return null
                } else {
                    return res.json()
                }
            })
            .then(response => {
                if(response !== null) {
                    alert.show("Registration successful")
                    setUsername("")
                    setPassword("")
                    setUsername("")
                    setEmail("")
                    setFirstName("")
                    setLastName("")
                    setOrganization("")
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                }
            })
            .catch(error => console.log("error:" + error))
    }, [alert, navigate, ip, port]);

    const formSubmit = async (event) => {
        event.preventDefault()
        const userConfiguration = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": firstName,
            "last_name": lastName,
            "organization": organization
        }
        if (username === "" || password === "") {
            alert.show("Username or password cannot be empty")
        } else {
            createUser(userConfiguration)
        }
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    const handlePwChange = (event) => {
        setPassword(event.target.value)
    }

    const handleEmailChange = (event) => {
        setEmail(event.target.value)
    }

    const handleFirstNameChange = (event) => {
        setFirstName(event.target.value)
    }

    const handleLastNameChange = (event) => {
        setLastName(event.target.value)
    }

    const handleOrganizationChange = (event) => {
        setOrganization(event.target.value)
    }

    return (
        <div className="Login Auth-form-container">
            <form className="Auth-form" onSubmit={formSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Register</h3>
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
                    <div className="form-group mt-3">
                        <label>First name</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter first name"
                            value={firstName}
                            onChange={handleFirstNameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Last name</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter last name"
                            value={lastName}
                            onChange={handleLastNameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Organization</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter organization"
                            value={organization}
                            onChange={handleOrganizationChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>E-mail</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter e-mail"
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Register
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}

Register.propTypes = {};
Register.defaultProps = {};
export default Register;
