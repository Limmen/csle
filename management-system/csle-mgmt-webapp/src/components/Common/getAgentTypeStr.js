
const getAgentTypeStr = (agentType) => {
    if(agentType === 0) {
        return "T-SPSA"
    }
    if(agentType === 1) {
        return "PPO"
    }
    if(agentType === 2) {
        return "T-FP"
    }
    if(agentType === 3) {
        return "DQN"
    }
    if(agentType === 4) {
        return "REINFORCE"
    }
    if(agentType === 5) {
        return "NFSP"
    }
    if(agentType === 6) {
        return "RANDOM"
    }
    if(agentType === 7) {
        return "NONE"
    }
    if(agentType === 8) {
        return "VALUE ITERATION"
    }
    if(agentType === 9) {
        return "HSVI"
    }
    if(agentType === 10) {
        return "SONDIK's VALUE ITERATION"
    }
    if(agentType === 11) {
        return "RANDOM SEARCH"
    }
    if(agentType === 12) {
        return "DIFFERENTIAL EVOLUTION"
    }
    if(agentType === 13) {
        return "CROSS ENTROPY METHOD"
    }
    if(agentType === 14) {
        return "KIEFER WOLFOWITZ"
    }
    if(agentType === 15) {
        return "Q_LEARNING"
    }
    if(agentType === 16) {
        return "SARSA"
    }
    if(agentType === 17) {
        return "POLICY ITERATION"
    }
    if(agentType === 18) {
        return "SHAPLEY ITERATION"
    }
    if(agentType === 19) {
        return "HSVI for OS-POSGs"
    }
    if(agentType === 20) {
        return "FICTITIOUS PLAY"
    }
    if(agentType === 21) {
        return "LINEAR PROGRAMMING FOR NORMAL-FORM GAMES"
    }
    if(agentType === 22) {
        return "DynaSec"
    }
    if(agentType === 23) {
        return "BAYESIAN OPTIMIZATION"
    }
    else {
        return "Unknown"
    }
}

export default getAgentTypeStr;