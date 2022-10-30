
const getTopicsString = (topics) => {
    var topicsStr = ""
    for (let i = 0; i < topics.length; i++) {
        if (i != topics.length-1) {
            topicsStr = topicsStr + topics[i] + ", "
        } else {
            topicsStr = topicsStr + topics[i]
        }
    }
    return topicsStr
}

export default getTopicsString;