
const getTransportProtocolStr = (transportProtocolType) => {
    /**
     * Converts a numeric transport protocol type into a string
     *
     * @param transportProtocolType the type of the transport protocol
     * @returns {string} the transport protocol string
     */
    if(transportProtocolType === 0) {
        return "TCP"
    }
    if(transportProtocolType === 1) {
        return "UDP"
    }
    else {
        return "Unknown"
    }
}

export default getTransportProtocolStr;