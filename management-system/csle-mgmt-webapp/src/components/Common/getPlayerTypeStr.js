
const getPlayerTypeStr = (playerType) => {
    /**
     * Converts a numeric player type into a string
     *
     * @param playerType the numeric player type to convert
     * @returns {string} the player type string
     */
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