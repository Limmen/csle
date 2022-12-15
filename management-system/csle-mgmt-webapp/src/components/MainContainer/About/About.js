import React from 'react';
import './About.css';
import Arch from './arch.png'

const About = () => {
    /**
     * Component representing the /about-page
     *
     * @returns {JSX.Element}
     * @constructor
     */
    return (
        <div className="About">
            <h3> About</h3>
            <div className="row">
                <div className="col-sm-2"></div>
                <div className="col-sm-8">
                    <p className="aboutText">
                        The Cyber Security Learning Environment (CSLE) is a framework for learning, testing, and
                        deploying policies for autonomous security management. It includes three components:
                        a digital twin (emulation) of the target system,
                        which continuously collects data and evaluates learned policies; a
                        system identification process, which periodically estimates system
                        models based on the collected data; and a policy learning
                        process that is based on reinforcement learning.
                        <br></br>
                    </p>
                    <img src={Arch} alt="CSLE Architecture" className="img-fluid archImg"/>
                    <br></br>
                    <br></br>
                    <p className="aboutText">
                        The framework is written in a combination of Python and JavaScript.
                        The emulation system is based on Docker and the telemetry system is based on gRPC,
                        the Elastic stack and Kafka.
                        The code and the documentation is freely available under the CC BY-SA 4.0 license.
                        The code is available <a href="https://github.com/Limmen/csle">here</a> and the documentation
                        is available <a href="https://limmen.dev/csle/">here</a>.
                    </p>
                </div>
                <div className="col-sm-2"></div>
            </div>
        </div>
    );
}

About.propTypes = {};
About.defaultProps = {};
export default About;
