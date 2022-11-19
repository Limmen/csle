import React from 'react';
import './About.css';
import Arch from './arch.png'
import YoutubeEmbed from "../YoutubeEmbed/YoutubeEmbed";

/**
 * Component representing the /about-page
 */
const About = () => {

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
                        <br></br>
                        The framework consists of libraries, a command-line interface, a rest-api, storage systems, and a management system.
                        The user interface you are viewing right now is the management system. This interface allows the user to
                        start/stop digital twins (see the <a href="/emulations-page">emulations page</a>),
                        to start/stop simulations (see the <a href="/simulations-page">simulations page</a>),
                        to start/stop reinforcement learning algorithms (see the <a href="/jobs-page">jobs page</a>),
                        to start/stop system identification jobs (see the <a href="/jobs-page">jobs page</a>),
                        to start/stop data collection jobs (see the <a href="/jobs-page">jobs page</a>),
                        to inspect learned security policies (see the <a href="/policy-examination-page">policy examination page</a> and the <a href="/policies-page">policies page</a>),
                        to manage experiments (see the <a href="/experiments-page">experiments page</a>),
                        to manage system models (see the <a href="/system-models-page">models page</a> and the <a href="/emulation-statistics-page">statistics page</a>),
                        to inspect execution traces (see the <a href="/traces-page">traces page</a>),
                        to manage SDN controllers of runnign emulations (see the <a href="/sdn-controllers-page">SDN controllers page</a>),
                        to monitor executions (see the <a href="/monitor">monitoring page</a>),
                        to control executions of emulations (see the <a href="/control-plane-page">control plane page</a>)
                        and to download public datasets (see the <a href="/downloads-page">downloads page</a>).
                    </p>
                </div>
                <div className="col-sm-2"></div>
            </div>

            <h3 className="publicationsTitle"> Architecture </h3>
            <div className="row">
                <div className="col-sm-2"></div>
                <div className="col-sm-8">
                    <p className="aboutText">
                        <span className="boldSpan aboutText">Digital twin (Emulation). </span>
                        The digital twin collects traces and evaluates
                        learned policies. It emulates the target system and is periodically updated when changes to the
                        target system are detected.
                        To evaluate a defender policy π π, it runs attack scenarios and executes defender responses
                        prescribed by π If a policy π
                        is deemed effective, the digital twin sends it to the target
                        system for implementation. From each such evaluation, a trace h of defender actions, system
                        observations, and rewards is obtained.
                        The traces are then sent to the system identification process.
                    </p>
                    <p className="aboutText">
                        <span className="boldSpan aboutText">System identification process. </span>
                        The system identification
                        process periodically receives traces ht from the digital twin
                        and runs a system identification algorithm ϕ, which learns a
                        system model M based on ht. After obtaining M, the system
                        identification process sends M to the policy learning process.
                    </p>

                    <p className="aboutText">
                        <span className="boldSpan aboutText">Policy learning process. </span>
                        The policy learning process periodically receives a system model M from the
                        system identification process, learns an effective policy π through simulating M and
                        running the reinforcement learning algorithm φ, and then sends π to the digital twin for
                        evaluation.
                    </p>
                </div>
                <div className="col-sm-2"></div>
            </div>
            <img src={Arch} alt="CSLE Architecture" className="img-fluid archImg"/>

            <h3 className="publicationsTitle"> Code and API Documentation</h3>
            <div className="row">
                <div className="col-sm-2"></div>
                <div className="col-sm-8">
                    <p className="aboutText">
                        The framework is written in a combination of Python, Scala, Erlang, and JavaScript.
                        The emulation system is based on Docker and the telemetry system is based on gRPC and Kafka.
                        The code and the API documentation will be freely available under the CC BY-SA 4.0 license when the framework is released.
                    </p>
                </div>
                <div className="col-sm-2"></div>
            </div>

            <h3 className="publicationsTitle"> Video demonstration </h3>
            <div className="row">
                <div className="col-sm-2"></div>
                <div className="col-sm-8">
                    <YoutubeEmbed embedId="18P7MjPKNDg"/>
                </div>
                <div className="col-sm-2"></div>
            </div>

            <h3 className="publicationsTitle"> Publications </h3>
            <div className="row">
                <div className="col-sm-2"></div>
                <div className="col-sm-8">
                    <p className="aboutText">
                        <a href="https://limmen.dev/assets/papers/CNSM22_preprint_8_sep_Hammar_Stadler.pdf">
                            <span className="boldSpan aboutText">
                                An Online Framework for Adapting Security Policies in Dynamic IT Environments, (Hammar & Stadler 2022). </span>
                                International Conference on Network and Service Management (CNSM 2022).
                        </a>
                    </p>
                    <p className="aboutText">
                        <a href="https://ieeexplore.ieee.org/document/9779345">
                            <span className="boldSpan aboutText">Intrusion Prevention through Optimal Stopping, (Hammar & Stadler 2022). </span>
                            IEEE Transactions on Network and Service Management (TNSM).
                        </a>
                    </p>
                    <p className="aboutText">
                        <a href="https://limmen.dev/assets/papers/icml_ml4cyber_Hammar_Stadler_final_24_june_2022.pdf">
                            <span className="boldSpan aboutText">Learning Security Strategies through Game Play and Optimal Stopping, (Hammar & Stadler 2022). </span>
                            ICML Ml4Cyber Workshop 2022: International Conference on Machine Learning.
                        </a>
                    </p>
                    <p className="aboutText">
                        <a href="https://ieeexplore.ieee.org/document/9789707">
                            <span className="boldSpan aboutText">A System for Interactive Examination of Learned Security Policies, (Hammar & Stadler 2022). </span>
                            IEEE/IFIP Network Operations and Management Symposium (NOMS 2022). (Best demonstration paper award)
                        </a>
                    </p>
                    <p className="aboutText">
                        <a href="https://ieeexplore.ieee.org/document/9615542">
                            <span className="boldSpan aboutText">Learning Intrusion Prevention Policies through Optimal Stopping, (Hammar & Stadler 2021). </span>
                            International Conference on Network and Service Management (CNSM 2021).
                        </a>
                    </p>
                    <p className="aboutText">
                        <a href="https://ieeexplore.ieee.org/document/9269092">
                            <span className="boldSpan aboutText">Finding Effective Security Strategies through Reinforcement Learning and Self-Play, (Hammar & Stadler 2020). </span>
                            International Conference on Network and Service Management (CNSM 2020).
                        </a>
                    </p>
                    <div className="col-sm-2"></div>
                </div>
            </div>
        </div>
    );
}

About.propTypes = {};
About.defaultProps = {};
export default About;
