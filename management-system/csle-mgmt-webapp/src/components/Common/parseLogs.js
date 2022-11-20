
const parseLogs = (lines) => {
    var data = lines.map((line, index) => {
        return {
            index: index,
            content: line
        }
    })
    return data
}

export default parseLogs;