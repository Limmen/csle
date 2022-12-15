
const convertListToCommaSeparatedString = (listToConvert) => {
    /**
     * Converts a list of strings into a single comma separated string
     *
     * @param listToConvert the list to convert
     * @returns {string} the comma separated string
     */
    var str = ""
    for (let i = 0; i < listToConvert.length; i++) {
        if (i !== listToConvert.length-1) {
            str = str + listToConvert[i] + ", "
        } else {
            str = str + listToConvert[i]
        }
    }
    return str
}

export default convertListToCommaSeparatedString;