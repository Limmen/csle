
const getIpString = (ips) => {
    var ipsStr = ""
    for (let i = 0; i < ips.length; i++) {
        ipsStr = ipsStr + ips[i] + ","
    }
    return ipsStr
}

export default getIpString;