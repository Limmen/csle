import React from 'react';
import './DockerContainerConfigurations.css';

const DockerContainerConfigurations = (props) => {

    const DockerContainersTableBody = (props) => {
        if (props.traces.length > 0) {
            return (
                <tbody>
                {props.traces[props.activeTrace].containers_config.containers.map((container, index) =>
                    <tr key={index}>
                        <td>{container.ip}</td>
                        <td>{container.level}</td>
                        <td>{container.minigame}</td>
                        <td>{container.name}</td>
                        <td>{container.network}</td>
                        <td>{container.version}</td>
                    </tr>
                )}
                </tbody>
            )
        } else {
            return <tbody></tbody>
        }
    }

    return (
        <div className="DockerContainerConfigurations">
            <div className="row">
                <div className="row">
                    <div className="row">
                        <div className="col-sm-12">
                            <h5> Docker Containers </h5>
                            <table className="table table-hover table-striped">
                                <thead>
                                <tr>
                                    <th>IP</th>
                                    <th>Level</th>
                                    <th>Minigame</th>
                                    <th>Image</th>
                                    <th>Network</th>
                                    <th>Version</th>
                                </tr>
                                </thead>
                                <DockerContainersTableBody traces={props.traces} activeTrace={props.activeTrace}/>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

DockerContainerConfigurations.propTypes = {};
DockerContainerConfigurations.defaultProps = {};
export default DockerContainerConfigurations;