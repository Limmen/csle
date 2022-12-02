
const convertListToCommaSeparatedString = (listToConvert) => {
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