
const getSystemModelTypeStr = (systemModelType) => {
    /**
     * Converts a numeric system type into a string
     *
     * @param systemModelType the numeric system type to convert
     * @returns {string} the converted string
     */
    if(systemModelType === 0) {
        return "gaussian_mixture"
    }
    if(systemModelType === 1) {
        return "empirical"
    }
    if(systemModelType === 2) {
        return "gp"
    }
    if(systemModelType === 3) {
        return "mcmc"
    }
    else {
        return "Unknown"
    }
}

export default getSystemModelTypeStr;