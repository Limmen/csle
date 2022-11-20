import React, {useState, useEffect, useCallback} from 'react';
import './LogsAdmin.css';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import Tooltip from 'react-bootstrap/Tooltip';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";

/**
 * Component representing the /logs-admin-page
 */
const LogsAdmin = (props) => {
    const [loading, setLoading] = useState(true);
    const ip = serverIp;
    const port = serverPort;
    const alert = useAlert();
    const navigate = useNavigate();

    const refresh = () => {
        setLoading(true)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload logs from the backend
        </Tooltip>
    );


    useEffect(() => {
        setLoading(true);
    }, []);

    return (
        <div className="Admin">
            TODO
        </div>
    );
}

LogsAdmin.propTypes = {};
LogsAdmin.defaultProps = {};
export default LogsAdmin;
