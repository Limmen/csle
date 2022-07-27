import React, {useState, useCallback} from 'react';
import { useAlert } from "react-alert";
import './Login.css';

const Login = (props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const ip = "localhost"
    const alert = useAlert();

    const loginUser = useCallback((credentials) => {
        fetch(
            `http://` + ip + ':7777/login',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify(credentials)
            }
        )
            .then(res => res.json())
            .then(response => {
                if(!response.ok) {
                    alert.show("Oh look, an alert!")
                } else {
                    console.log("Received token")
                    console.log(response)
                    // props.setToken(token)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const formSubmit = async (event) => {
        event.preventDefault()
        const credentials = {
            "username": username,
            "password": password
        }
        loginUser(credentials)
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    const handlePwChange = (event) => {
        setPassword(event.target.value)
    }

    return (
        <div className="Login Auth-form-container">
            <form className="Auth-form" onSubmit={formSubmit}>
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
        </div>
    );
}

Login.propTypes = {};
Login.defaultProps = {};
export default Login;
