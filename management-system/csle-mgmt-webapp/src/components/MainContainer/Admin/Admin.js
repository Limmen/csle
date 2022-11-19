import React, {useState, useEffect, useCallback} from 'react';
import './Admin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory from 'react-bootstrap-table2-editor';
import { Type } from 'react-bootstrap-table2-editor';
import serverIp from "../../Common/serverIp";

/**
 * Component representing the /admin-page
 */
const Admin = (props) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const ip = serverIp;
    const alert = useAlert();
    const navigate = useNavigate();

    const columns = [
        {
        dataField: 'id',
        text: 'ID'
        },
        {
            dataField: 'username',
            text: 'Username'
        },
        {
            dataField: 'first_name',
            text: 'First name'
        },
        {
            dataField: 'last_name',
            text: 'Last name'
        },
        {
            dataField: 'email',
            text: 'E-mail'
        },
        {
            dataField: 'organization',
            text: 'Organization'
        },
        {
            dataField: 'admin',
            text: 'Admin',
            editor: {
                type: Type.SELECT,
                options: [{
                    value: 'true',
                    label: 'true'
                }, {
                    value: 'false',
                    label: 'false'
                }
                ]
            }
        },
        {
            dataField: 'password',
            text: 'Password'
        }
    ];

    const fetchUsers = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/users' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                setUsers(response)
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const updateUser = useCallback((user) => {
        fetch(
            `http://` + ip + ':7777/users/' + user.id + "?token=" + props.sessionData.token,
            {
                method: "PUT",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({user: user})
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                if(res.status === 400) {
                    alert.show("Invalid request, could not update users")
                    return null
                }
                return res.json()
            })
            .then(response => {
                refresh()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const refresh = () => {
        setLoading(true)
        fetchUsers()
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulations from the backend
        </Tooltip>
    );

    const UsersTableOrSpinner = (props) => {
        if (!props.loading && props.users.length === 0) {
            return (
                <div>
                    <span className="emptyText">No users are available</span>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching users... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="usersTable">
                    <BootstrapTable
                        keyField="id"
                        data={ props.users }
                        columns={ columns }
                        cellEdit={ cellEditFactory({ mode: 'click' }) }
                    />
                </div>
            )
        }
    }

    const save = () => {
        for (let i = 0; i < users.length; i++) {
            updateUser(users[i])
        }
    }

    useEffect(() => {
        setLoading(true);
        fetchUsers()
    }, [fetchUsers]);

    return (
        <div className="About">
            <h3> User administration (click in a cell to edit)
                <button type="submit" className="btn btn-primary btn-sm saveUsersBtn" onClick={save}>
                    Save
                </button>
            </h3>
            <div className="row">
                <div className="col-sm-1"></div>
                <div className="col-sm-10">
                    <UsersTableOrSpinner users={users} loading={loading} />
                </div>
                <div className="col-sm-1"></div>
            </div>
        </div>
    );
}

Admin.propTypes = {};
Admin.defaultProps = {};
export default Admin;
