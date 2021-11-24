import React from 'react';
import './UsersConfig.css';

const UsersConfig = (props) => {

    const UsersConfigTableBody = (props) => {
        if (props.traces.length > 0) {
            var users = []
            for (let i = 0; i < props.traces[props.activeTrace].users_config.users.length; i++) {
                const ip = props.traces[props.activeTrace].users_config.users[i].ip
                for (let j = 0; j < props.traces[props.activeTrace].users_config.users[i].users.length; j++) {
                    const username = props.traces[props.activeTrace].users_config.users[i].users[j]["py/tuple"][0]
                    const password = props.traces[props.activeTrace].users_config.users[i].users[j]["py/tuple"][1]
                    const rootBool = props.traces[props.activeTrace].users_config.users[i].users[j]["py/tuple"][2]
                    var rootAccess = "No"
                    if (rootBool) {
                        rootAccess = "Yes"
                    }
                    users.push({
                        "ip": ip,
                        "username": username,
                        "password": password,
                        "root": rootAccess
                    })
                }
            }
            return (
                <tbody>
                {users.map((user, index) => {
                        return (
                            <tr key={index}>
                                <td>{user.ip}</td>
                                <td>{user.username}</td>
                                <td>{user.password}</td>
                                <td>{user.root}</td>
                            </tr>
                        )
                    }
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    return (
        <div className="UsersConfig">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> User accounts </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>Container IP</th>
                                    <th>Username</th>
                                    <th>Password</th>
                                    <th>Root access</th>
                                </tr>
                                </thead>
                                <UsersConfigTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

UsersConfig.propTypes = {};
UsersConfig.defaultProps = {};
export default UsersConfig;