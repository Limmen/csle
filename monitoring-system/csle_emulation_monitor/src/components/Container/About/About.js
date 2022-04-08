import React from 'react';
import './About.css';
import Arch from './arch.png'

const About = () => {

    return (
        <div className="About">
            <h3> About the Cyber Security Learning Environment (CSLE) </h3>
            <p className="aboutText">
                CSLE is a framework and environment for building self-learning systems for security use cases.
                The framework includes two systems. First, we develop an
                emulation system where key functional components of the
                target infrastructure are replicated. In this system, we run
                attack scenarios and defender responses. These runs produce
                system metrics and logs that we use to estimate empirical
                distributions of infrastructure metrics, which are needed to
                simulate episodes of Markov decision processes or games. Second, we develop a simulation
                system where episodes are executed and policies are
                incrementally learned. Finally, the policies are extracted and
                evaluated in the emulation system and possibly implemented
                in the target infrastructure. In short, the emulation
                system is used to provide the statistics needed to simulate
                the the Markov decision process or game and to evaluate policies, whereas the simulation
                system is used to learn policies.
            </p>
            <img src={Arch} alt="CSLE Architecture"/>
        </div>
    );
}

About.propTypes = {};
About.defaultProps = {};
export default About;
