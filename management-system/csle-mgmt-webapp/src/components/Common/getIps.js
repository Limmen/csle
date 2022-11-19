
const getIps = (ips_and_networks) => {
    const ips = []
    for (let i = 0; i < ips_and_networks.length; i++) {
        ips.push(ips_and_networks[i][0])
    }
    return ips
}

export default getIps;