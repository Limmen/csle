
const parseLogs = (lines) => {
    /**
     * Parses a list of log lines into a list of dicts
     *
     * @param lines the list of log lines to parse
     * @returns {*} the list of dicts
     */
    var data = lines.map((line, index) => {
        return {
            index: index,
            content: line
        }
    })
    return data
}

export default parseLogs;