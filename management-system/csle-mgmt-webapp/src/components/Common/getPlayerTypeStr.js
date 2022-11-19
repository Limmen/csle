
const getPlayerTypeStr = (playerType) => {
    if(playerType === 1) {
        return "Defender"
    }
    if(playerType === 2) {
        return "Attacker"
    }
    if(playerType === 3) {
        return "Self Play"
    }
    else {
        return "Unknown"
    }
}

export default getPlayerTypeStr;