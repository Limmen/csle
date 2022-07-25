
const getSystemModelTypeStr = (systemModelType) => {
    if(systemModelType === 0) {
        return "gaussian_mixture"
    }
    if(systemModelType === 1) {
        return "empirical"
    }
    if(systemModelType === 2) {
        return "gp"
    }
    else {
        return "Unknown"
    }
}

export default getSystemModelTypeStr;