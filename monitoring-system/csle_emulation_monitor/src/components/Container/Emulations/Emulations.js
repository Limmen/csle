import React, {useState, useEffect, createRef, useCallback} from 'react';
import './Emulations.css';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import Emulation from "./Emulation/Emulation";
import Button from 'react-bootstrap/Button'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

const Emulations = () => {
    const [envs, setEnvs] = useState([]);
    const [loading, setLoading] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchEmulations = useCallback(() => {
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
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchEmulations();
    }, []);

    const refresh = () => {
        setLoading(true)
        fetchEmulations()
    }

    const EmulationAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.envs.map((env, index) =>
                        <Emulation env={env} wrapper={wrapper} key={env.name + "-" + index}/>
                    )}
                </Accordion>
            )
        }
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulations from the backend
        </Tooltip>
    );

    const wrapper = createRef();

    return (
        <div className="Emulations">
            <h3 className="text-center inline-block emulationsHeader"> Emulations

                <OverlayTrigger
                    placement="right"
                    delay={{show: 250, hide: 400}}
                    overlay={renderRefreshTooltip()}
                >
                    <Button variant="button" onClick={refresh}>
                        <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>

            </h3>
            <EmulationAccordions loading={loading} envs={envs}/>
        </div>
    );
}

Emulations.propTypes = {};
Emulations.defaultProps = {};
export default Emulations;
