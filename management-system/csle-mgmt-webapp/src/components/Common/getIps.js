
const getIps = (ips_and_networks) => {
    /**
     * Converts a list of ips and networks into a list of ips
     *
     * @param ips_and_networks the list of ips and networksn
     * @returns {*[]} a list of ips
     */
    const ips = []
    for (let i = 0; i < ips_and_networks.length; i++) {
        ips.push(ips_and_networks[i][0])
    }
    return ips
}

export default getIps;