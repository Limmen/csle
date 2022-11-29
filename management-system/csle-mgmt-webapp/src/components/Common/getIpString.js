
const getIpString = (ips) => {
    var ipsStr = ""
    for (let i = 0; i < ips.length; i++) {
        ipsStr = ipsStr + ips[i]
        if (i !== ips.length-1) {
            ipsStr = ipsStr + ", "
        }
    }
    return ipsStr
}

export default getIpString;