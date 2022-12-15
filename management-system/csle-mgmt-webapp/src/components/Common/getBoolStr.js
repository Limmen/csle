
const getBoolStr = (bool) => {
    /**
     * Converts a boolean into a string
     *
     * @param bool the boolean to convert
     * @returns {string} the resulting string
     */
    if(bool) {
        return "true"
    } else {
        return "false"
    }
}

export default getBoolStr;