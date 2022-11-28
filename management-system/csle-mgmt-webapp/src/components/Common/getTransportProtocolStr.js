
const getTransportProtocolStr = (transportProtocolType) => {
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